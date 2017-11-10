#!/usr/bin/env python

"""Test the ``publish_github_release`` add-on.

Given a repository and a token, this script will go through few
different scenarios while checking the state of the repository.
"""

import argparse
import datetime as dt
import fnmatch
import operator
import os
import shlex
import shutil
import subprocess
import sys
import textwrap

from functools import reduce

from github_release import get_releases, gh_release_create, gh_asset_upload

MODULE = "publish_github_release"
PYTHON_VERSIONS = ["cp27-cp27m", "cp34-cp34m", "cp35-cp35m", "cp36-cp36m"]
PACKAGE_DIR = "dist"
PRERELEASE_TAG = "nightly"

INTERACTIVE = False
TEST_CASE = None
PROJECT_NAME = "sandbox"
REPO_NAME = None

PLATFORMS = {
    'manylinux1': ['manylinux1_x86_64'],
    'macosx': ['macosx_10_11_x86_64'],
    'win': ['win_amd64', 'win32']
}


#
# Git
#

def generate_author_date():
    start_date = dt.datetime.strptime(
        "2017-01-01 12:00:00", "%Y-%m-%d %H:%M:%S")
    days = int(run("git rev-list --count HEAD", limit=1))
    return start_date + dt.timedelta(days=days)


def get_author_date(ref="HEAD"):
    return dt.datetime.strptime(
        run(
            "git log -1 --format=\"%%ad\" --date=local %s" % str(ref), limit=1),
        "%a %b %d %H:%M:%S %Y").strftime("%Y%m%d")


def get_tag(ref="HEAD"):
    return run(
        "git describe --tags --exact-match %s" % str(ref),
        limit=1, ignore_errors=True)


def do_commit(version=None, release_tag=None, push=False):
    # Compose commit message
    author_date = generate_author_date()
    if version is None:
        version = read_version_file()
    msg = "Update to %s.dev%s" % (version, author_date.strftime("%Y%m%d"))
    if release_tag is not None:
        msg = "%s %s" % (PROJECT_NAME, release_tag)
        version = release_tag
    commit_msg = "ENH: %s" % msg
    # Update README and VERSION files
    with open("README.md", "a") as content:
        content.write("* %s\n" % msg)
    with open("VERSION", "w") as content:
        content.write(version)
    # Commit changes
    run("git add README.md")
    run("git add VERSION")
    run("git commit -m \"%s\" --date=%s" % (commit_msg,
                                            author_date.isoformat()))
    # Push
    if push:
        run("git push origin master")
    # Create tag
    if release_tag is not None:
        run("git tag -a -m \"ENH: %s %s\" %s" % (
            PROJECT_NAME, release_tag, release_tag))
        if push:
            run("git push origin %s" % release_tag)
    print("")


#
# Version
#

def read_version_file():
    with open("VERSION") as content:
        return content.readline().strip()


def get_full_version():
    version = get_tag()
    dev_str = ""
    if version is None or version == PRERELEASE_TAG:
        version = read_version_file()
        dev_str = ".dev%s" % get_author_date()
    return version + dev_str


#
# Package
#

def package_name(project_name, full_version, py_ver, platform):
    return "{project_name}-{full_version}-{py_ver}-{platform}.whl".format(
        **locals())


def package_names(full_version, systems=None):
    if systems is None:
        systems = []
    if not isinstance(systems, list):
        systems = [systems]
    systems = systems if systems else list(PLATFORMS.keys())

    # List of platform matching selected systems
    platforms = []
    for system in PLATFORMS:
        if system not in systems:
            continue
        platforms.extend(PLATFORMS[system])

    return [
        package_name(PROJECT_NAME, full_version, py_ver, platform)
        for py_ver in PYTHON_VERSIONS
        for platform in platforms
        ]


def generate_packages(full_version, systems=None, clear=True):
    if systems is None:
        systems = []
    systems = systems if systems else list(PLATFORMS.keys())
    print("generating %s packages" % systems)
    if clear:
        clear_package_directory()
    if not os.path.exists(PACKAGE_DIR):
        os.mkdir(PACKAGE_DIR)
    paths = []
    for package in package_names(full_version, systems):
        filepath = os.path.join(PACKAGE_DIR, package)
        print("  " + filepath)
        with open(filepath, "w") as content:
            content.write(filepath)
        paths.append(filepath)
    print("")
    return paths


def clear_package_directory():
    shutil.rmtree(os.path.join(PACKAGE_DIR), ignore_errors=True)


#
# User interaction
#

def pause(text):
    for line in ["", "*" * 80, "*",
                 "* %s: %s" % (TEST_CASE.upper(), text),
                 "*", "*" * 80, ""]:
        print(line)
    if INTERACTIVE:
        if sys.version_info[0] == 3 and sys.version_info[1] >= 3:
            input("Press Enter to continue...")
        else:
            raw_input("Press Enter to continue...")  # noqa: F821
    print("")


def ask_user_check():
    pause("All set. You can now check that the pre-release is updated.")


#
# Subprocess
#

def run(*popenargs, **kwargs):
    """Run command with arguments and returns a list of captured lines.

    Process output is read line-by-line and captured until execution is over.
    Specifying the ``limit`` argument allow to limit the number of line captured
    and exit earlier.

    By default, captured lines are displayed as they are captured. Setting
    ``verbose`` to False disable this. Unless, verbose has been explicitly
    enabled, setting ``limit`` also disable output.

    Otherwise, the arguments are the same as for the Popen constructor.

    If ``ignore_errors`` is set, errors are ignored; otherwise, if the exit code
    was non-zero it raises a CalledProcessError.  The CalledProcessError object
    will have the return code in the returncode attribute and output in the
    output attribute.

    The stdout argument is not allowed as it is used internally.
    To capture standard error in the result, use stderr=STDOUT.
    """
    limit = kwargs.pop("limit", None)
    verbose = kwargs.pop("verbose", limit is None)
    ignore_errors = kwargs.pop("ignore_errors", False)
    line_count = 0
    captured_lines = []
    null_output = None
    if 'stdout' in kwargs:
        raise ValueError('stdout argument not allowed, it will be overridden.')
    if ignore_errors and 'stderr' not in kwargs:
        null_output = open(os.devnull, 'w')
        kwargs['stderr'] = null_output
    popenargs = list(popenargs)
    if isinstance(popenargs[0], str) and not kwargs.get("shell", False):
        popenargs[0] = shlex.split(popenargs[0])
    process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
    # Adapted from http://blog.endpoint.com/2015/01/getting-realtime-output-using-python.html  # noqa: E501
    while True:
        output = process.stdout.readline()
        if sys.version_info[0] >= 3:
            output = output.decode()
        if output == '' and process.poll() is not None:
            break
        if output:
            captured_lines.append(output.strip())
            if verbose:
                print(output.rstrip())
            line_count += 1
        if limit is not None and line_count == limit:
            process.kill()
            break
    ret_code = process.poll()
    if null_output is not None:
        null_output.close()
    error_occurred = ret_code is not None and ret_code > 0
    if error_occurred and not ignore_errors:
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = popenargs[0]
        raise subprocess.CalledProcessError(
            ret_code, cmd, output="\n".join(captured_lines))
    if error_occurred and ignore_errors:
        return None
    return (captured_lines[0]
            if limit == 1 and len(captured_lines) == 1
            else captured_lines)


#
# GitHub
#

def reset():
    pause("We will now reset '%s'" % REPO_NAME)

    clear_package_directory()

    # Reset to first commit
    first_sha = run("git log --reverse --pretty=\"%H\"", limit=1)
    run("git reset --hard %s" % first_sha)
    run("git push origin master --force")

    # Remove release and tags from GitHub
    run("githubrelease release %s delete *" % REPO_NAME)
    run("githubrelease ref %s delete --tags *" % REPO_NAME)

    # Remove local tags
    for tag in run("git tag"):
        run("git tag -d %s" % tag)

    assert len(get_releases(repo_name=REPO_NAME)) == 0


def do_release(release_tag):
    expected_packages = package_names(release_tag)

    pause("We will now add release %s with %s assets" % (
        release_tag, len(expected_packages)))

    # Create release
    do_commit(release_tag=release_tag, push=True)
    gh_release_create(REPO_NAME, release_tag, publish=True)
    # Generate packages
    generate_packages(release_tag)
    # Upload packages
    gh_asset_upload(REPO_NAME, release_tag, PACKAGE_DIR + "/*")


def publish_github_release(mode, system=None, re_upload=False, prerelease_sha=None):
    if system is None:
        system = list(PLATFORMS.keys())

    if isinstance(system, list):
        for _system in system:
            publish_github_release(mode, _system, re_upload, prerelease_sha)
        return

    assert system in PLATFORMS.keys()

    if not isinstance(mode, list):
        mode = [mode]

    pause("We will generate packages like it would on [%s] system(s)" % system)
    generate_packages(get_full_version(), system)

    tag_name = PRERELEASE_TAG if "prerelease" in mode else get_tag()
    author_date = get_author_date()

    # Summary
    print(textwrap.dedent(
        r"""
        * We will now run [{module}.py] in [{mode}] mode(s)
        * like it would run on [{system}] system(s)
        *
        * If it applies, the following will happen:
        *   (1) creation of [{tag_name}] release
        *   (2) upload of associated packages
        *
        * Re-upload of packages if name matches: {re_upload}
        *
        """.format(
            module=MODULE,
            mode=",".join(mode), system=system, tag_name=tag_name,
            re_upload=re_upload)
    ))

    # Common arguments
    common_args = [MODULE + ".py", REPO_NAME]
    single_args = []
    if re_upload:
        single_args.append("--re-upload")
    args = []
    # Release arguments
    if "release" in mode:
        for arg in [

            "--release-packages", PACKAGE_DIR + "/*%s*.whl" % system,
        ]:
            args.append(arg)
    # Prerelease arguments
    if "prerelease" in mode:
        for arg in [
            "--prerelease-tag", tag_name,
            "--prerelease-packages",
                PACKAGE_DIR + "/*.dev%s*%s*.whl" % (author_date, system),
            "--prerelease-packages-clear-pattern",
                "*%s*.whl" % system,
            "--prerelease-packages-keep-pattern",
                "*.dev%s*.whl" % author_date
        ]:
            args.append(arg)
        if prerelease_sha is not None:
            args.extend(["--prerelease-sha", prerelease_sha])

    # Format command arguments to display them nicely across multiple lines
    args_as_str = ""
    for index in range(len(single_args)):
        line_continuation = "\\" if index < len(single_args) - 1 else ""
        args_as_str += "  %s %s\n" % (single_args[index], line_continuation)
    for index in range(0, len(args), 2):
        line_continuation = "\\" if index < len(args) - 2 else ""
        args_as_str += "  %s %s %s\n" % (
            args[index], args[index+1], line_continuation)

    pause(textwrap.dedent(
        r"""
        *
        * The following command will be executed:

        """) + "%s \\\n%s" % (" ".join(common_args), args_as_str))

    # Publish release
    __import__(MODULE).main(common_args + single_args + args)

    # Fetch changes
    remote = "origin"
    msg = "fetching changes from remote '%s'" % remote
    print(msg)
    run("git fetch --tags %s" % remote)
    print("%s - done\n" % msg)


#
# Test
#

def get_release_packages(release):
    return [asset["name"] for asset in release["assets"]]


def display_package_names(expected, release):
    print("Package names:")
    if "packages" in expected:
        print("  expected:\n    %s" % "\n    ".join(expected["packages"]))
    print("  current:\n    %s" % "\n    ".join(get_release_packages(release)))


def display_release(what, release):
    print("%s [%s] release:" % (what, release["tag_name"]))
    for attribute in ["name", "draft", "prerelease"]:
        if attribute in release:
            print("  %s: %s" % (attribute, release[attribute]))


def check_releases(expected, releases=None):  # noqa: C901
    """Return False if expected release data are missing or incorrect.

    Expected data can be either a dictionary or a list of dictionaries.

    Supported attributes are tag_name, name, draft, prerelease, package_count,
    package_pattern, packages and tag_date.

    * tag_name and name are string
    * draft and prerelease are boolean
    * package_count is an integer
    * packages is a list of strings
    * package_pattern is either one tuple or a list of tuples of the
      form (expected_count, pattern).
    """

    def display_error():
        print("-" * 80 + "\nERROR:\n")

    if releases is None:
        releases = get_releases(REPO_NAME)
    if isinstance(expected, list):
        # Check overall count
        if len(releases) != len(expected):
            display_error()
            print("Numbers of releases is incorrect")
            print("  expected: %s" % len(expected))
            print("   current: %s" % len(releases))
            print("")
            return False
        # Check each release
        statuses = []
        for _expected in expected:
            statuses.append(check_releases(_expected, releases))
        return reduce(operator.and_, statuses) if statuses else True

    # Lookup release
    current_release = None
    for release in releases:
        if release["tag_name"] == expected["tag_name"]:
            current_release = release
            break
    if current_release is None:
        display_error()
        print("release [%s] not found" % expected["tag_name"])
        print("")
        return False
    # Check simple attributes
    for attribute in ["name", "draft", "prerelease"]:
        if attribute not in expected:
            continue
        if attribute not in release:
            display_error()
            print("Release [%s] is missing [%s] "
                  "attributes" % (expected["tag_name"], attribute))
            display_release("Expected", expected)
            display_release("Current", release)
            print("")
            return False
        if expected[attribute] != release[attribute]:
            display_error()
            print("Release [%s]: attribute [%s] is "
                  "different" % (expected["tag_name"], attribute))
            display_release("Expected", expected)
            display_release("Current", release)
            print("")
            return False
    if "package_count" in expected:
        current_count = len(release["assets"])
        expected_count = expected["package_count"]
        if current_count != expected_count:
            display_error()
            print("Release [%s]: "
                  "Number of packages does not match" % expected["tag_name"])
            print("  expected: %s" % expected["package_count"])
            print("  current: %s" % current_count)
            print("")
            display_package_names(expected, release)
            return False
    if "package_pattern" in expected:
        if "packages" in expected:
            display_error()
            print("Release [%s]: attributes 'package_pattern' and 'packages' "
                  "are exclusive. Use only one." % expected["tag_name"])
            print("")
            return False
        if "package_count" in expected:
            display_error()
            print("Release [%s]: attributes 'package_pattern' and "
                  "'package_count' are exclusive. "
                  "Use only one." % expected["tag_name"])
            print("")
            return False
        patterns = expected["package_pattern"]
        if not isinstance(patterns, list):
            patterns = [patterns]
        for expected_package_count, pattern in patterns:
            current_package_count = 0
            for package in get_release_packages(release):
                if fnmatch.fnmatch(package, pattern):
                    current_package_count += 1
                    continue
            if expected_package_count != current_package_count:
                display_error()
                print("Release [%s]: "
                      "Number of packages associated with pattern [%s] "
                      "does not match" % (expected["tag_name"], pattern))
                print("  expected: %s" % expected_package_count)
                print("  current: %s" % current_package_count)
                print("")
                display_package_names(expected, release)
                print("")
                return False
    if "packages" in expected:
        diff = set(expected["packages"]) & set(get_release_packages(release))
        if diff:
            display_error()
            print("Release [%s]: "
                  "List of packages names are different" % expected["tag_name"])
            display_package_names(expected, release)
            print("")
            return False
    if "tag_date" in expected:
        expected_tag_date = expected["tag_date"]
        release_tag_date = get_author_date(release["tag_name"])
        if expected_tag_date != release_tag_date:
            display_error()
            print("Release [%s]: tag dates do not match" % expected["tag_name"])
            print("  expected tag_date: %s" % expected_tag_date)
            print("  current tag_date: %s" % release_tag_date)
            print("")
            return False
    # Check that expected attributes are correct (e.g without typo)
    for attribute in [
            "tag_name", "name", "draft", "prerelease",
            "package_count", "package_pattern", "packages",
            "tag_date"]:
        expected.pop(attribute, None)
    if len(expected) > 0:
        display_error()
        print("Unknown expected attributes: %s\n" % ", ".join(expected))
        return False
    return True


#
# Entry point
#


def lookup_module_path():
    script_dir = os.path.dirname(__file__)
    module_path = os.path.join(script_dir, "..")
    return module_path


def main():
    global INTERACTIVE
    global REPO_NAME

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "repo_name", type=str, metavar="ORG/PROJECT",
        help="Name of the repository"
    )
    parser.add_argument(
        "--token", type=str, metavar="GITHUB_TOKEN",
        help="If not specified, expects GITHUB_TOKEN env. variable"
    )
    parser.add_argument(
        "--module-path", type=str,
        help="Directory containing %s module. "
             "(default: %s)" % (MODULE, lookup_module_path())
    )
    parser.add_argument(
        "--no-interactive", action="store_true",
        help="Do not expect the user to press a key to proceed to the next step"
    )
    parser.add_argument(
        "--generate-dummy-packages", action="store_true",
        help="Generate dummy release and development packages in dist directory"
    )
    parser.set_defaults(
        token=os.environ.get("GITHUB_TOKEN", None),
        module_path=lookup_module_path()
    )
    args = parser.parse_args()

    if args.generate_dummy_packages:
        generate_packages("1.0.0", clear=False)
        generate_packages("1.0.0.dev20170212", clear=False)
        generate_packages("1.0.0.dev20170213", clear=False)
        exit(0)

    if not args.token:
        print("-" * 80)
        print(textwrap.dedent(
            r"""
            error: A token is expected.

            Specify the --token parameter or set GITHUB_TOKEN environment variable.
            See https://help.github.com/articles/creating-an-access-token-for-command-line-use/
            """  # noqa: E501
        ).lstrip())
        print("-" * 80)
        parser.print_usage()
        exit(1)
    os.environ["GITHUB_TOKEN"] = args.token

    if not os.path.exists(args.module_path):
        print("error: module path '%s' doesn't exist" % args.module_path)
        parser.print_usage()
        exit(1)

    # Update global variables
    INTERACTIVE = not args.no_interactive
    REPO_NAME = args.repo_name

    # Check that the project found in the current directory matches
    # the selected project.
    if not os.path.exists(".git"):
        print("error: current directory is NOT a git project")
        exit(1)
    remote_url = run("git config --get remote.origin.url", limit=1)
    if not remote_url:
        print("error: failed to read 'remote.origin.url' git option")
        exit(1)
    remote_url = remote_url.replace(".git", "")
    if not remote_url.endswith(REPO_NAME):
        print("error: selected ORG/PROJECT is not associated with "
              "git option 'remote.origin.url' read from current directory:")
        print("  org/project      : %s" % REPO_NAME)
        print("  remote.origin.url: %s" % remote_url)
        exit(1)

    # Update sys.path
    sys.path.insert(0, args.module_path)

    def test_prerelease_mode():
        """In ``prerelease`` mode, the script is expected to create a
        prerelease only if HEAD is not associated with a tag different
        from the prerelease tag"""

        global TEST_CASE
        TEST_CASE = "test_prerelease_mode"

        mode = "prerelease"
        reset()  # 2017-01-01
        do_commit()  # 2017-01-02
        do_release("1.0.0")  # 2017-01-03
        do_commit(version="2.0.0", push=True)  # 2017-01-04
        publish_github_release(mode)

        assert(check_releases([
            # Release 1.0.0
            {"tag_name": "1.0.0", "tag_date": "20170103",
             "draft": False, "prerelease": False,
             "package_pattern": (16, "*1.0.0-*.whl")},

            # Prerelease
            {"tag_name": PRERELEASE_TAG, "tag_date": "20170104",
             "draft": False, "prerelease": True,
             "package_pattern": (16, "*2.0.0.dev*.whl")}
        ]))

        # Get 'published_at' value
        initial_published_at = [
            release["published_at"]
            for release in get_releases(REPO_NAME)
            if release["tag_name"] == PRERELEASE_TAG
            ][0]

        do_commit(push=True)  # 2017-01-05

        #
        # Check that the correct assets are removed after
        # publishing packages associated with each system.
        #

        publish_github_release(mode, system="manylinux1")
        publish_github_release(mode, system="manylinux1", re_upload=True)
        assert (check_releases([
            # Release 1.0.0
            {"tag_name": "1.0.0", "tag_date": "20170103",
             "draft": False, "prerelease": False,
             "package_pattern": (16, "*1.0.0-*.whl")},

            # Prerelease
            {"tag_name": PRERELEASE_TAG, "tag_date": "20170105",
             "draft": False, "prerelease": True,
             "package_pattern": [
                 (12, "*2.0.0.dev20170104*.whl"),
                 (4, "*2.0.0.dev20170105*.whl")
             ]}
        ]))

        final_published_at = [
            release["published_at"]
            for release in get_releases(REPO_NAME)
            if release["tag_name"] == PRERELEASE_TAG
            ][0]

        print("")
        print("Check that 'published_at' was updated:")
        print("  initial_published_at: %s" % initial_published_at)
        print("    final_published_at: %s" % final_published_at)
        assert initial_published_at != final_published_at

        publish_github_release(mode, system="macosx")
        assert (check_releases([
            # Release 1.0.0
            {"tag_name": "1.0.0", "tag_date": "20170103",
             "draft": False, "prerelease": False,
             "package_pattern": (16, "*1.0.0-*.whl")},

            # Prerelease
            {"tag_name": PRERELEASE_TAG, "tag_date": "20170105",
             "draft": False, "prerelease": True,
             "package_pattern": [
                 (8, "*2.0.0.dev20170104*.whl"),
                 (8, "*2.0.0.dev20170105*.whl")
             ]}
        ]))

        publish_github_release(mode, system="win")
        assert (check_releases([
            # Release 1.0.0
            {"tag_name": "1.0.0", "tag_date": "20170103",
             "draft": False, "prerelease": False,
             "package_pattern": (16, "*1.0.0-*.whl")},

            # Prerelease
            {"tag_name": PRERELEASE_TAG, "tag_date": "20170105",
             "draft": False, "prerelease": True,
             "package_pattern": [
                 (0, "*2.0.0.dev20170104*.whl"),
                 (16, "*2.0.0.dev20170105*.whl")
             ]}
        ]))

        do_commit()  # 2017-01-06

        do_commit(release_tag="2.0.0", push=True)  # 2017-01-07

        #
        # Check that no prerelease is created if HEAD is associated
        # to a tag different from PRERELEASE_TAG
        #

        publish_github_release(mode, system="manylinux1")
        assert (check_releases([
            # Release 1.0.0
            {"tag_name": "1.0.0", "tag_date": "20170103",
             "draft": False, "prerelease": False,
             "package_pattern": (16, "*1.0.0-*.whl")},

            # Prerelease
            {"tag_name": PRERELEASE_TAG, "tag_date": "20170105",
             "draft": False, "prerelease": True,
             "package_pattern": (16, "*2.0.0.dev20170105*.whl")}
        ]))

        #
        # Check that re-uploading the same packages does not raise an exception
        #

        publish_github_release(mode, system="manylinux1")
        assert (check_releases([
            # Release 1.0.0
            {"tag_name": "1.0.0", "tag_date": "20170103",
             "draft": False, "prerelease": False,
             "package_pattern": (16, "*1.0.0-*.whl")},

            # Prerelease
            {"tag_name": PRERELEASE_TAG, "tag_date": "20170105",
             "draft": False, "prerelease": True,
             "package_pattern": (16, "*2.0.0.dev20170105*.whl")}
        ]))

    def test_invalid_prerelease_sha_raise_exception():
        """Check that an exception is raised if using an invalid ``--prerelease-sha``"""
        global TEST_CASE
        TEST_CASE = "test_invalid_prerelease_sha_raise_exception"
        mode = "prerelease"
        reset()
        expected_msg = "Failed to get commit associated with --prerelease-sha: %s" % "invalid"
        try:
            msg = ""
            publish_github_release(mode, system="manylinux1", prerelease_sha="invalid")
        except ValueError as exc:
            msg = exc.args[0]
            print("Caught exception: %s" % exc)
        if msg != expected_msg:
            print("         msg [%s]\n"
                  "expected_msg [%s]" % (msg, expected_msg))
        assert msg == expected_msg

    def test_release_mode():
        """In ``release`` mode, the script is expected to upload a release
        only if HEAD is directly associated with to a tag.
        """
        global TEST_CASE
        TEST_CASE = "test_release_mode"

        mode = "release"
        reset()  # 2017-01-01
        do_commit(push=True)  # 2017-01-02

        #
        # Check that no release is created
        #
        publish_github_release(mode, system="manylinux1")
        assert (check_releases([]))

        do_commit(release_tag="1.0.0", push=True)  # 2017-01-03

        #
        # Check that a release is created
        #
        publish_github_release(mode)
        assert (check_releases([
            # Release 1.0.0
            {"tag_name": "1.0.0", "tag_date": "20170103",
             "draft": False, "prerelease": False,
             "package_pattern": (16, "*1.0.0-*.whl")},
        ]))

        #
        # Check that calling the function twice causes no harm
        #
        publish_github_release(mode)
        assert (check_releases([
            # Release 1.0.0
            {"tag_name": "1.0.0", "tag_date": "20170103",
             "draft": False, "prerelease": False,
             "package_pattern": (16, "*1.0.0-*.whl")},
        ]))

        do_commit()  # 2017-01-04
        do_commit(release_tag="2.0.0", push=True)  # 2017-01-05

        #
        # Check that an other release can be created
        #
        publish_github_release(mode, system="manylinux1")
        publish_github_release(mode, system="manylinux1", re_upload=True)
        assert (check_releases([
            # Release 1.0.0
            {"tag_name": "1.0.0", "tag_date": "20170103",
             "draft": False, "prerelease": False,
             "package_pattern": (16, "*1.0.0-*.whl")},

            # Release 2.0.0
            {"tag_name": "2.0.0", "tag_date": "20170105",
             "draft": False, "prerelease": False,
             "package_pattern": (4, "*2.0.0-*manylinux1*.whl")},
        ]))
        publish_github_release(mode, system=["macosx", "win"])
        assert (check_releases([
            # Release 1.0.0
            {"tag_name": "1.0.0", "tag_date": "20170103",
             "draft": False, "prerelease": False,
             "package_pattern": (16, "*1.0.0-*.whl")},

            # Release 2.0.0
            {"tag_name": "2.0.0", "tag_date": "20170105",
             "draft": False, "prerelease": False,
             "package_pattern": (16, "*2.0.0-*.whl")},
        ]))

    def test_dual_mode():
        """This test that the script works as expected when both
        release and prerelease arguments are given."""
        global TEST_CASE
        TEST_CASE = "test_dual_mode"

        mode = ["release", "prerelease"]
        reset()  # 2017-01-01
        do_commit(push=True)  # 2017-01-02

        #
        # Check that a prerelease is created
        #
        publish_github_release(mode, system="manylinux1")
        assert (check_releases([
            # Prerelease
            {"tag_name": PRERELEASE_TAG, "tag_date": "20170102",
             "draft": False, "prerelease": True,
             "package_pattern": (4, "*0.0.0.dev20170102*.whl")}
        ]))

        do_commit()  # 2017-01-03
        do_commit(release_tag="1.0.0", push=True)  # 2017-01-04

        #
        # Check that a release is created
        #
        publish_github_release(mode)
        assert (check_releases([
            # Prerelease
            {"tag_name": PRERELEASE_TAG, "tag_date": "20170102",
             "draft": False, "prerelease": True,
             "package_pattern": (4, "*0.0.0.dev20170102*.whl")},

            # Release 1.0.0
            {"tag_name": "1.0.0", "tag_date": "20170104",
             "draft": False, "prerelease": False,
             "package_pattern": (16, "*1.0.0-*.whl")},
        ]))

        do_commit(version="1.0.1", push=True)  # 2017-01-05

        #
        # Check that the prerelease is updated
        #
        publish_github_release(mode, system=["macosx", "win"])
        assert (check_releases([
            # Release 1.0.0
            {"tag_name": "1.0.0", "tag_date": "20170104",
             "draft": False, "prerelease": False,
             "package_pattern": (16, "*1.0.0-*.whl")},

            # Prerelease
            {"tag_name": PRERELEASE_TAG, "tag_date": "20170105",
             "draft": False, "prerelease": True,
             "package_pattern": [
                 (4, "*0.0.0.dev20170102*.whl"),
                 (12, "*1.0.1.dev20170105*.whl")
             ]},
        ]))

    test_prerelease_mode()
    test_invalid_prerelease_sha_raise_exception()
    test_release_mode()
    test_dual_mode()


if __name__ == "__main__":
    main()
