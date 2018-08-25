
"""
Usage::

    import install_cmake
    install_cmake.install()

"""

import os
import subprocess
import sys
import textwrap

from subprocess import CalledProcessError, check_output

DEFAULT_CMAKE_VERSION = "3.5.0"


def _log(*args):
    script_name = os.path.basename(__file__)
    print("[circle:%s] " % script_name + " ".join(args))
    sys.stdout.flush()


def _check_executables_availability(executables):
    """Try to run each executable with the `--version` argument. If at least
    one could not be executed, it raises :exception:`RuntimeError` suggesting
    approaches to mitigate the problem.
    """
    missing_executables = []
    for executable_name in executables:
        try:
            subprocess.check_output([executable_name, "--version"])
        except (OSError, CalledProcessError):
            missing_executables.append(executable_name)

    if missing_executables:
        raise RuntimeError(textwrap.dedent(
            """
            The following executables are required to install CMake:

              {missing_executables}

            Few options to address this:

            (1) install the missing executables using the system package manager. For example:

                sudo apt-get install {missing_executables}

            (2) install CMake wheel using pip. For example:

                pip install cmake
            """.format(
                missing_executables=" ".join(missing_executables),
            )
        ))


def install(cmake_version=DEFAULT_CMAKE_VERSION):
    """Download and install CMake into ``/usr/local``."""

    _check_executables_availability(["rsync", "tar", "wget"])

    cmake_directory = "/usr/local"

    cmake_exe = os.path.join(cmake_directory, 'bin/cmake')

    if os.path.exists(cmake_exe):
        output = check_output([cmake_exe, '--version']).decode("utf-8")
        if output.strip() == cmake_version:
            _log("Skipping download: Found %s (v%s)" % (
                cmake_exe, cmake_version))
            return

    _log("Looking for cmake", cmake_version, "in PATH")
    try:
        output = check_output(
            ["cmake", "--version"]).decode("utf-8")
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

    cmake_arch = "x86_64"

    name = "cmake-{}-Linux-{}".format(cmake_version, cmake_arch)
    cmake_package = "{}.tar.gz".format(name)

    _log("Downloading", cmake_package)

    download_dir = os.environ["HOME"] + "/downloads"
    downloaded_package = os.path.join(download_dir, cmake_package)

    if not os.path.exists(downloaded_package):

        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        cmake_version_major = cmake_version.split(".")[0]
        cmake_version_minor = cmake_version.split(".")[1]

        try:
            check_output([
                "wget", "--no-check-certificate", "--progress=dot",
                "https://cmake.org/files/v{}.{}/{}".format(cmake_version_major, cmake_version_minor, cmake_package),
                "-O", downloaded_package
            ], stderr=subprocess.STDOUT)
        except (OSError, CalledProcessError):
            _check_executables_availability(['curl'])
            check_output([
                "curl", "--progress-bar", "-L",
                "https://cmake.org/files/v{}.{}/{}".format(cmake_version_major, cmake_version_minor, cmake_package),
                "-o", downloaded_package
            ], stderr=subprocess.STDOUT)
        _log("  ->", "done")
    else:
        _log("  ->", "skipping download: found", downloaded_package)

    _log("Extracting", downloaded_package)
    check_output(["tar", "xzf", downloaded_package])
    _log("  ->", "done")

    _log("Installing", name, "into", cmake_directory)
    check_output([
        "sudo", "rsync", "-avz", name + "/", cmake_directory
    ])
    _log("  ->", "done")


if __name__ == '__main__':
    install(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CMAKE_VERSION)
