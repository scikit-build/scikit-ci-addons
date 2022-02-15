
"""
Usage::

    import install_cmake
    install_cmake.install()

"""

import os
import platform
import subprocess
import sys

from subprocess import CalledProcessError, check_output

DEFAULT_CMAKE_VERSION = "3.22.2"


def _log(*args):
    script_name = os.path.basename(__file__)
    print("[travis:%s] " % script_name + " ".join(args))
    sys.stdout.flush()


def install(cmake_version=DEFAULT_CMAKE_VERSION, is_darwin=False):
    """Download and install CMake into ``/usr/local``."""

    cmake_version_major = cmake_version.split(".")[0]
    cmake_version_minor = cmake_version.split(".")[1]
    cmake_version_patch = cmake_version.split(".")[2]

    cmake_os = "Darwin" if is_darwin else "Linux"
    cmake_arch = "x86_64"
    if is_darwin and cmake_version_major >= 3 and cmake_version_minor >= 19 and cmake_version_patch >= 2:
        cmake_os = "macos"
        cmake_arch = "universal"
    if not is_darwin and cmake_version_major >= 3 and cmake_version_minor >= 20:
        cmake_os = "linux"

    cmake_name = "cmake-{}-{}-{}".format(cmake_version, cmake_os, cmake_arch)
    cmake_package = ".".join((cmake_name, "tar", "gz"))

    _log("Looking for cmake", cmake_version, "in PATH")
    try:
        output = check_output(
            "cmake --version", shell=True).decode("utf-8")
        current_cmake_version = output.splitlines()[0]
        if cmake_version in current_cmake_version:
            _log("  ->", "found %s:" % current_cmake_version,
                 "skipping download: version matches expected one")
            return
        else:
            _log("  ->", "found %s:" % current_cmake_version,
                 "not the expected version")
    except (OSError, CalledProcessError):
        _log("  ->", "not found")
        pass

    download_dir = os.environ["HOME"] + "/downloads"
    downloaded_package = os.path.join(download_dir, cmake_package)

    if not os.path.exists(downloaded_package):

        _log("Making directory: ", download_dir)
        try:
            os.mkdir(download_dir)
        except OSError:
            pass
        _log("  ->", "done")

        _log("Downloading", cmake_package)
        try:
            check_output([
                "wget", "--no-check-certificate", "--progress=dot",
                "https://cmake.org/files/v{}.{}/{}".format(
                    cmake_version_major, cmake_version_minor, cmake_package),
                "-P", download_dir
            ], stderr=subprocess.STDOUT)
        except (OSError, CalledProcessError):
            check_output([
                "curl", "--progress-bar", "-L",
                "https://cmake.org/files/v{}.{}/{}".format(
                    cmake_version_major, cmake_version_minor, cmake_package),
                "-o", downloaded_package
            ], stderr=subprocess.STDOUT)
        _log("  ->", "done")

    else:
        _log("Downloading", cmake_package)
        _log("  ->", "skipping download: Found ", downloaded_package)

    _log("Extracting", downloaded_package, "into", download_dir)
    check_output(["tar", "xzf", downloaded_package, '-C', download_dir])
    _log("  ->", "done")

    if is_darwin:
        prefix = "/usr/local/bin"
        _log("Removing CMake executables from", prefix)
        check_output(
            ["sudo", "rm", "-f"] + [
                "/".join((prefix, subdir)) for subdir in
                ("cmake", "cpack", "cmake-gui", "ccmake", "ctest")
                ]
        )
        _log("  ->", "done")

        _log("Installing CMake in", prefix)
        check_output([
            "sudo",
            download_dir + "/" + cmake_name
            + "/CMake.app/Contents/bin/cmake-gui",
            "--install"
        ])
        _log("  ->", "done")

    else:
        home = os.environ["HOME"]
        assert os.path.exists(home)
        _log("Copying", download_dir + "/" + cmake_name, "to", home)
        check_output([
            "rsync", "-avz",
            download_dir + "/" + cmake_name + "/", home])
        _log("  ->", "done")


if __name__ == '__main__':
    install(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CMAKE_VERSION,
            is_darwin=platform.system().lower() == "darwin")
