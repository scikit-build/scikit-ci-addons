
import datetime as dt
import os
import shlex
import subprocess
import sys

import pytest

import ci_addons

from . import (push_dir)


def _run(cmd):
    print("Executing: %s" % cmd)
    subprocess.check_call(shlex.split(cmd))


def _expected_commit_yyyymmdd():
    commit_date = dt.datetime.now()
    return commit_date.strftime("%Y%m%d")


def _do_commit(release_tag=None):
    expected_commit_yyyymmdd = _expected_commit_yyyymmdd()
    msg = "Update %s" % expected_commit_yyyymmdd
    with open("README.md", "a") as content:
        content.write("* %s\n" % msg)
    # Commit changes
    _run("git add README.md")
    _run("git commit -m \"ENH: %s\"" % msg)
    # Create tag(s)
    if isinstance(release_tag, str):
        release_tag = [release_tag]
    if isinstance(release_tag, (list, tuple)):
        for tag in release_tag:
            _run("git tag %s -a -m \"ENH: %s\"" % (tag, tag))
    expected_sha = subprocess.check_output(
        ["git", "rev-parse", "--short", "HEAD"]).strip()
    if sys.version_info[0] >= 3:
        expected_sha = expected_sha.decode()
    return expected_sha, expected_commit_yyyymmdd


@pytest.fixture(scope="function")
def src_dir(tmpdir_factory):
    # Import addon to facilitate testing
    sys.path.insert(0, os.path.join(ci_addons.home(), 'anyci'))

    tmp_dir = tmpdir_factory.mktemp("source")
    with push_dir(tmp_dir):
        tmp_dir.ensure("dist", dir=1).join('dummy.txt').write("# dummy package")
        _run("git init")
        # Arbitrary user name and email
        _run("git config user.email "
             "scikit-ci-addons-bot@users.noreply.github.com")
        _run("git config user.name "
             "scikit-ci-addons-bot")
        return tmp_dir


@pytest.mark.parametrize("tags,extra_args", [
    ([], []),
    (["latest"], []),
    (["nightly"], ["--prerelease-tag", "nightly"]),
])
def test_create_prerelease(src_dir, mocker, tags, extra_args):

    pgr = __import__('publish_github_release')

    upload_prerelease = mocker.patch(
        'publish_github_release._upload_prerelease')
    upload_release = mocker.patch(
        'publish_github_release._upload_release')

    with push_dir(src_dir):
        _do_commit(release_tag=tags)
        pgr.main([
            "ci_addons", "anyci/publish_github_release",
            "--token", "123456",
            "--prerelease-packages", "dist/*",
            "--release-packages", "dist/*",
        ] + extra_args)
        assert upload_prerelease.call_count == 1
        assert upload_release.call_count == 0


@pytest.mark.parametrize("tags,extra_args", [
    (["1.0.0"], []),
    (["1.0.0", "latest"], []),
    (["latest"], ["--prerelease-tag", "nightly"]),
])
def test_create_release(src_dir, mocker, tags, extra_args):
    pgr = __import__('publish_github_release')

    upload_prerelease = mocker.patch(
        'publish_github_release._upload_prerelease')
    upload_release = mocker.patch(
        'publish_github_release._upload_release')

    with push_dir(src_dir):
        _do_commit(release_tag=tags)
        pgr.main([
            "ci_addons", "anyci/publish_github_release",
            "--token", "123456",
            "--prerelease-packages", "dist/*",
            "--release-packages", "dist/*",
        ] + extra_args)
        assert upload_prerelease.call_count == 0
        assert upload_release.call_count == 1
        if upload_release.call_count:
            release_tag = upload_release.call_args[0][0]
            # The first tag is expected to be the one
            assert release_tag == tags[0]


@pytest.mark.parametrize("tags,expected_prerelease,expected_release", [
    ([], 1, 0),
    (["1.0.0"], 0, 1),
])
def test_packages_selection_minilanguage(
        src_dir, mocker, tags, expected_prerelease, expected_release):
    pgr = __import__('publish_github_release')

    upload_prerelease = mocker.patch(
        'publish_github_release._upload_prerelease')
    upload_release = mocker.patch(
        'publish_github_release._upload_release')

    package_suffix = "<COMMIT_DATE>-<COMMIT_SHORT_SHA>*.txt"

    argv = [
        "ci_addons", "anyci/publish_github_release",
        "--token", "123456",
        "--prerelease-packages", "dist/prerelease*" + package_suffix,
        "--prerelease-packages-clear-pattern", "dist/clear*" + package_suffix,
        "--prerelease-packages-keep-pattern", "dist/keep*" + package_suffix,
        "--release-packages", "dist/release*" + package_suffix,
    ]

    with push_dir(src_dir):
        expected_sha, expected_commit_yyyymmdd = _do_commit(release_tag=tags)
        pgr.main(argv)
        assert upload_prerelease.call_count == expected_prerelease
        assert upload_release.call_count == expected_release

        expected_str = (expected_commit_yyyymmdd, expected_sha)

        if expected_prerelease:
            args = upload_prerelease.call_args[0][0]
            assert args.prerelease_packages == [
                "dist/prerelease*%s-%s*.txt" % expected_str]
            assert args.prerelease_packages_clear_pattern == \
                "dist/clear*%s-%s*.txt" % expected_str
            assert args.prerelease_packages_keep_pattern == \
                "dist/keep*%s-%s*.txt" % expected_str

        if expected_release == 1:
            release_tag = upload_release.call_args[0][0]
            assert release_tag == "1.0.0"
            args = upload_release.call_args[0][1]
            assert args.release_packages == [
                "dist/release*%s-%s*.txt" % expected_str]


def test_missing_token(src_dir, mocker, capsys, monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN")

    pgr = __import__('publish_github_release')

    upload_prerelease = mocker.patch(
        'publish_github_release._upload_prerelease')
    upload_release = mocker.patch(
        'publish_github_release._upload_release')

    with push_dir(src_dir):
        _do_commit()
        with pytest.raises(SystemExit) as excinfo:
            pgr.main([
                "ci_addons", "anyci/publish_github_release",
                "--prerelease-packages", "dist/*"
            ])
            assert upload_prerelease.call_count == 0
            assert upload_release.call_count == 0
            assert excinfo.value.code == 1

        out, _ = capsys.readouterr()
        assert "error: A token is expected." in out

        with pytest.raises(SystemExit) as excinfo:
            pgr.main([
                "ci_addons", "anyci/publish_github_release",
                "--exit-success-if-missing-token",
                "--prerelease-packages", "dist/*"
            ])
            assert upload_prerelease.call_count == 0
            assert upload_release.call_count == 0
            assert excinfo.value.code == 0

        out, _ = capsys.readouterr()
        assert "skipping: A token is expected." in out
