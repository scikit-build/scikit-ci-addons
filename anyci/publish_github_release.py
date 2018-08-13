"""
This add-on allows to automatically create GitHub releases or prereleases
and upload associated packages. It respectively provides a "release" and
a "prerelease" sub-command.
"""
from __future__ import print_function

import argparse
import datetime as dt
import errno
import glob
import os
import platform
import re
import sys
import subprocess
import textwrap


from functools import wraps

from github_release import (
    gh_asset_delete,
    gh_asset_upload,
    gh_commit_get,
    get_refs,
    get_release_info,
    gh_release_create,
    gh_release_edit
)


#
# Git
#

GITS = ["git"]
if sys.platform == "win32":
    GITS = ["git.cmd", "git.exe"]


# Copied from https://github.com/warner/python-versioneer/blob/master/src/subprocess_helper.py  # noqa: E501
def run_command(commands, args, cwd=None, verbose=False, hide_stderr=False,
                env=None):
    """Call the given command(s)."""
    assert isinstance(commands, list)
    for c in commands:
        dispcmd = str([c] + args)
        try:
            # remember shell=False, so use git.cmd on windows, not just git
            p = subprocess.Popen([c] + args, cwd=cwd, env=env,
                                 stdout=subprocess.PIPE,
                                 stderr=(subprocess.PIPE if hide_stderr
                                         else None))
            break
        except EnvironmentError:
            e = sys.exc_info()[1]
            if e.errno == errno.ENOENT:
                continue
            if verbose:
                print("unable to run %s" % dispcmd)
                print(e)
            return None, None
    else:
        if verbose:
            print("unable to find command, tried %s" % (commands,))
        return None, None
    stdout = p.communicate()[0].strip()
    if sys.version_info[0] >= 3:
        stdout = stdout.decode()
    if p.returncode != 0:
        if verbose:
            print("unable to run %s (error)" % dispcmd)
            print("stdout was %s" % stdout)
        return None, p.returncode
    return stdout, p.returncode


def git_repo_required(func):
    """This decorator raises :class:`RuntimeError` if the current
    directory does not belong to a git working tree.
    """
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        output, _ = run_command(
            GITS, ["rev-parse", "--is-inside-work-tree"],
            hide_stderr=True)

        if output != "true":
            raise RuntimeError(
                "Current directory is expected to be inside a git working tree: %s" % os.getcwd())
        return func(*args, **kwargs)
    return func_wrapper


@git_repo_required
def get_tags(ref="HEAD"):
    """If any, return all tags associated with `ref`.

    Note that since git (<=2.5.0) does *NOT* provide a direct way to get
    these, we first get the sha of the HEAD tag (if any), then group the
    the tag by SHA and return the corresponding list.
    """
    output, _ = run_command(
        GITS, ["describe", "--tags", "--exact-match", str(ref)],
        hide_stderr=True)
    if output is None:
        return []
    # Get tag's commit
    tag_sha, _ = run_command(GITS, ["rev-list", "-n",  "1", output])
    # List all tags and associated SHAs
    tags, _ = run_command(GITS, ["tag", "--list"])
    # map of sha -> tags
    all_tags = {}
    for tag in tags.splitlines():
        sha, _ = run_command(
            GITS, ["rev-list", "-n",  "1", "refs/tags/%s" % tag])
        if sha not in all_tags:
            all_tags[sha] = [tag]
        else:
            all_tags[sha].append(tag)
    return all_tags[tag_sha]


def get_current_date():
    now = dt.datetime.utcnow()
    return now.strftime("%Y-%m-%d %H:%m UTC")


@git_repo_required
def get_commit_date(ref="HEAD"):
    # 2017-06-14 22:53:31 -0400
    output, _ = run_command(
        GITS, ["log", "-1", "--format=%ci", str(ref)])
    # 2017-06-14 22:53:31
    output = " ".join(output.split(" ")[:2])
    # 20170614
    return dt.datetime.strptime(
        output, "%Y-%m-%d %H:%M:%S").strftime("%Y%m%d")


@git_repo_required
def get_commit_short_sha(ref="HEAD"):
    output, _ = run_command(
        GITS, ["rev-parse", "--short=7", str(ref)])
    return output


@git_repo_required
def get_commit_distance(tag):
    """Return the distance to the given ``tag``. If ``tag`` is not found, it returns
    the number of commits.
    """
    # Code adapted from python-versioneer/src/git/from_vcs.py
    output, _ = run_command(
        GITS, ["describe", "--tags", "--dirty", "--always", "--long", "--match", str(tag)])

    # parse output. It will be like TAG-NUM-gHEX[-dirty] or HEX[-dirty]
    # TAG might have hyphens.
    git_describe = output

    # look for -dirty suffix and remove it
    if git_describe.endswith("-dirty"):
        git_describe = git_describe[:git_describe.rindex("-dirty")]

    # now we have TAG-NUM-gHEX or HEX
    if "-" in git_describe:
        # TAG-NUM-gHEX
        mo = re.search(r'^.+-(\d+)-g[0-9a-f]+$', git_describe)

        # distance: number of commits since tag
        distance = int(mo.group(1))

    else:
        # HEX: no tags
        output, _ = run_command(
            GITS, ["rev-list", "HEAD", "--count"])
        distance = int(output)  # total number of commits

    return str(distance)


#
# Python
#

def python_wheel_platform():
    this_platform = platform.system().lower()
    return {
        "linux": "manylinux1", "darwin": "macosx", "windows": "win"
    }.get(this_platform, this_platform)


#
# Mini-language for package selection
#

def _substitute_package_selection_strings(package, what, script_args):
    """Return an updated package name where mini-language tokens
    have been updated.
    """
    tokens = {
        '<PYTHON_WHEEL_PLATFORM>': (python_wheel_platform, [], {}),
        '<COMMIT_DATE>': (get_commit_date, [], {}),
        '<COMMIT_SHORT_SHA>': (get_commit_short_sha, [], {}),
        '<COMMIT_DISTANCE>': (get_commit_distance, [script_args.prerelease_release_tag_pattern], {})
    }
    if any([token in package for token in tokens]):
        print("Updating %s [%s]" % (what, package))
    for token, (replace_func, func_args, func_kwargs) in tokens.items():
        if token in package:
            updated_value = replace_func(*func_args, **func_kwargs)
            print("  %s -> %s" % (token, updated_value))
            package = package.replace(token, updated_value)
    return package


def _update_package_list(input_packages, what, script_args):
    """Return an updated list of packages where mini-language
    tokens have been replaced using :py:func:`_substitute_package_selection_strings`.
    """
    if input_packages is None:
        return input_packages
    packages = []
    if isinstance(input_packages, str):
        return _substitute_package_selection_strings(input_packages, what, script_args)
    for package in input_packages:
        packages.append(
            _substitute_package_selection_strings(package, what, script_args))
    return packages


#
# Entry point
#

def configure_parser(parser):
    parser.add_argument(
        "repo_name", type=str, metavar="ORG/PROJECT",
        help="Name of the repository"
    )
    # "release" arguments
    release_group = parser.add_argument_group('release')
    release_group.add_argument(
        "--release-packages", metavar="PATTERN", type=str, nargs="*",
        help="Path(s) and/or wildcard expression(s)"
    )
    # "prerelease" arguments
    prerelease_group = parser.add_argument_group('prerelease')
    prerelease_group.add_argument(
        "--prerelease-packages", metavar="PATTERN", type=str, nargs="*",
        help="Path(s) and/or globbing pattern(s)"
    )
    prerelease_group.add_argument(
        "--prerelease-packages-clear-pattern",
        type=str, metavar="PATTERN",
        help="Globbing pattern selecting the set of packages to remove"
    )
    prerelease_group.add_argument(
        "--prerelease-packages-keep-pattern",
        type=str, metavar="PATTERN",
        help="Globbing pattern identifying the subset of packages to keep"
    )
    prerelease_group.add_argument(
        "--prerelease-tag", type=str,
        help="Name of the tag to associate with the pre-release. "
             "If needed, tag is created or updated (default: latest)"
    )
    prerelease_group.add_argument(
        "--prerelease-name", type=str,
        help="Name of the pre-release "
             "(default: 'TagName (updated on YYYY-MM-DD HH:MM UTC)'. "
             "Example: 'Latest (updated on 2017-02-12 14:42 UTC)')"
    )
    prerelease_group.add_argument(
        "--prerelease-sha", type=str,
        help="Commit or branch name to associate with the pre-release "
             "(default: master)"
    )
    prerelease_group.add_argument(
        "--prerelease-release-tag-pattern", type=str,
        help="Release tag used to compute <COMMIT_DISTANCE>"
             "(default: *.*.*)"
    )
    # Common arguments
    parser.add_argument(
        "--token", type=str, metavar="GITHUB_TOKEN",
        help="If not specified, expects GITHUB_TOKEN env. variable"
    )
    parser.add_argument(
        "--exit-success-if-missing-token", action="store_true",
        help="Gracefully exit if no GITHUB_TOKEN env. variable is found"
    )
    parser.add_argument(
        "--re-upload", action="store_true",
        help="If packages with same exist, delete and re-upload them"
    )
    parser.add_argument(
        "--display-python-wheel-platform", action="store_true",
        help="Display current python platform (manylinux1, macosx, or win)"
             " used for Python wheels."
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="don't create release, upload or erase packages "
             "but act like it was done"
    )
    parser.set_defaults(
        token=os.environ.get("GITHUB_TOKEN", None),
        prerelease_packages_clear_pattern=None,
        prerelease_packages_keep_pattern=None,
        prerelease_name=None,
        prerelease_sha="master",
        prerelease_tag="latest",
        prerelease_release_tag_pattern="*.*.*"
    )


def _github_asset_name(asset_name):
    """Asset uploaded on GitHub always have "plus" sign found
    in their name replaced by a "dot".
    """
    return os.path.basename(asset_name.replace("+", "."))


def _get_matching_packages(repo_name, tag, packages):
    """Filter the list of ``packages`` removing the ones
    already uploaded as assets for ``repo_name`` and ``tag``.

    Packages can be a list of file paths or globbing expressions.
    """
    matching_packages = []
    release = get_release_info(repo_name, tag)
    asset_names = [asset['name'] for asset in release['assets']]
    for package in packages:
        for path in glob.glob(package):
            if _github_asset_name(path) in asset_names:
                matching_packages.append(path)
    return matching_packages


def _delete_matching_packages(repo_name, tag, packages):
    """Delete all assets associated with ``repo_name`` and ``tag`` having
    file names matching the one associated with given ``packages``.

    Packages can be a list of file paths or globbing expressions.
    """
    for local_asset_name in _get_matching_packages(repo_name, tag, packages):
        gh_asset_delete(repo_name, tag, _github_asset_name(local_asset_name))


def _collect_packages(packages):
    """Given a list of file paths or globbing expressions, returns all package
    file paths found on the local filesystem.
    """
    file_paths = []
    for package in packages:
        file_paths.extend(glob.glob(package))
    return file_paths


def _upload_release(release_tag, args):
    """This function creates a release named ``release_tag`` and uploads
    associated packages.

    If ``args.re_upload`` is True, existing packages with matching names
    are deleted first.

    The ``args`` parameter is a dictionary where the following
    keys are expected to be set:

      * ``repo_name``: Specified as a string with the following format "<org_name>/<repo_name>".

      * ``release_packages``: List of packages specified as relative or absolute paths.

      * ``re_upload``: True or False. If True, existing packages with matching names are
        deleted first using :py:func:`_delete_matching_packages`.

      * ``dry_run``: True or False
    """
    assert release_tag is not None
    # Create release
    gh_release_create(
        args.repo_name,
        release_tag,
        publish=True, prerelease=False
    )
    # Remove existing assets matching selected ones
    if args.re_upload:
        _delete_matching_packages(
            args.repo_name, release_tag, args.release_packages)
    # Upload packages
    gh_asset_upload(
        args.repo_name, release_tag, args.release_packages, args.dry_run)
    return True


def _cancel_additional_appveyor_builds(prerelease_tag):
    """
    This function is a workaround for
    https://github.com/scikit-build/scikit-ci-addons/issues/45
    """
    appveyor = os.environ.get("APPVEYOR", "").lower()
    if appveyor != "true":
        return
    print("")
    script_name = "cancel-queued-build.ps1"
    script = os.path.join(os.path.dirname(__file__), "../appveyor", script_name)
    if not os.path.exists(script):
        print("skipping AppVeyor job cancellation: "
              "script %s not found" % script)
        return

    tag_pattern = "^%s(-tmp)?$" % prerelease_tag

    subprocess.check_call([
        "powershell", "-ExecutionPolicy", "Unrestricted",
        "-file", script, "-tag_pattern", tag_pattern
    ])


def _upload_prerelease(args):
    # Set default prerelease name
    prerelease_name = args.prerelease_name
    if prerelease_name is None:
        prerelease_name = "%s (updated on %s)" % (
            args.prerelease_tag.title(), get_current_date()
        )
    # Create release
    gh_release_create(
        args.repo_name,
        args.prerelease_tag,
        name=prerelease_name,
        publish=True, prerelease=True
    )

    # Retrieve list of packages by evaluating globbing expressions if any.
    packages = _collect_packages(args.prerelease_packages)

    # Remove existing assets matching selected ones
    if args.re_upload:
        _delete_matching_packages(
            args.repo_name, args.prerelease_tag, packages)
    else:
        # or skip upload of existing packages
        matching_packages = _get_matching_packages(
            args.repo_name, args.prerelease_tag, packages)
        for matching_package in matching_packages:
            if matching_package in packages:
                print("skipping %s package "
                      "(already uploaded)" % matching_package)
                packages.remove(matching_package)
        if matching_packages:
            print("")

    # Upload packages
    gh_asset_upload(
        args.repo_name, args.prerelease_tag, packages, args.dry_run
    )
    # Remove obsolete assets
    if args.prerelease_packages_clear_pattern is not None:
        gh_asset_delete(
            args.repo_name,
            args.prerelease_tag,
            args.prerelease_packages_clear_pattern,
            keep_pattern=args.prerelease_packages_keep_pattern,
            dry_run=args.dry_run
        )
    # If needed, update target commit
    sha = args.prerelease_sha
    if sha is not None:
        # If a branch name is specified, get associated commit
        refs = get_refs(args.repo_name, pattern="refs/heads/%s" % sha)
        if refs:
            assert len(refs) == 1
            branch = sha
            sha = refs[0]["object"]["sha"]
            print("resolved '%s' to '%s'" % (branch, sha))
        # Check that sha exists
        if gh_commit_get(args.repo_name, sha) is None:
            raise ValueError("Failed to get commit associated with --prerelease-sha: %s" % sha)

        gh_release_edit(
            args.repo_name,
            args.prerelease_tag,
            target_commitish=sha
        )

    # Set a draft first, and switch to prerelease afterward so that
    # the release date is current.
    gh_release_edit(
        args.repo_name,
        args.prerelease_tag,
        draft=True,
    )
    # Update draft, prerelease and name properties.
    gh_release_edit(
        args.repo_name,
        args.prerelease_tag,
        name=prerelease_name,
        draft=False,
        prerelease=True
    )

    _cancel_additional_appveyor_builds(args.prerelease_tag)

    return True


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    configure_parser(parser)
    args = parser.parse_args(argv[1:] if argv else None)

    if args.display_python_wheel_platform:
        print(python_wheel_platform())
        exit(0)

    # Check required parameters
    upload_release = (len(args.release_packages) > 0
                      if args.release_packages else False)
    upload_prerelease = (len(args.prerelease_packages) > 0
                         if args.prerelease_packages else False)
    if not upload_release and not upload_prerelease:
        parser.print_usage()
        print("error: at least --release-packages or --prerelease-packages "
              "argument is required")
        sys.exit(1)
    dual = upload_release and upload_prerelease

    if not args.token:
        print("-" * 80)
        print(textwrap.dedent(
            r"""
            %s: A token is expected.

            Specify the --token parameter or set GITHUB_TOKEN environment variable.
            See https://help.github.com/articles/creating-an-access-token-for-command-line-use/
            """ % ("skipping" if args.exit_success_if_missing_token else "error")  # noqa: E501
        ).lstrip())
        print("-" * 80)
        parser.print_usage()
        exit(0 if args.exit_success_if_missing_token else 1)
    os.environ["GITHUB_TOKEN"] = args.token

    # Update package arguments by substituting mini-language tokens with
    # their corresponding values.
    args.release_packages = _update_package_list(
        args.release_packages, "release package", args)
    args.prerelease_packages = _update_package_list(
        args.prerelease_packages, "prerelease package", args)
    args.prerelease_packages_clear_pattern = _update_package_list(
        args.prerelease_packages_clear_pattern,
        "prerelease package clear pattern", args)
    args.prerelease_packages_keep_pattern = _update_package_list(
        args.prerelease_packages_keep_pattern,
        "prerelease package keep pattern", args)

    msg = "Checking if HEAD is a release tag"
    print(msg)

    # Filter prerelease_tag from the list of existing releases.
    head_tags = get_tags()
    head_tags = list(filter(lambda tag: tag != args.prerelease_tag, head_tags))

    is_release = False
    release_tag = None

    if len(head_tags) > 0:
        is_release = True
        # If there are more than one tag (different from args.prerelease_tag)
        # associated with the HEAD, we use the first one.
        release_tag = head_tags[0]

    uploaded = False

    # If relevant, upload release
    if upload_release:
        if is_release:
            print("%s - yes "
                  "(found %s: creating release)\n" % (msg, release_tag))
            uploaded = _upload_release(release_tag, args)
        elif not dual:
            print("%s - no (skipping release upload)\n" % msg)

    # If relevant, upload prerelease
    if not uploaded and upload_prerelease:
        if not is_release:
            print("%s - no (creating prerelease)\n" % msg)
            _upload_prerelease(args)
        elif not dual:
            print("%s - yes (found %s: "
                  "skipping prerelease upload)\n" % (msg, release_tag))


if __name__ == "__main__":
    main()
