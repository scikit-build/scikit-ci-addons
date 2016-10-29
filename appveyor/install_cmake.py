
"""
Usage::

    import install_cmake
    install_cmake.install()

"""

import os
import shutil
import sys
import zipfile

from subprocess import CalledProcessError, check_output

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

DEFAULT_CMAKE_VERSION = "3.5.2"


def _log(*args):
    script_name = os.path.basename(__file__)
    print("[appveyor:%s] " % script_name + " ".join(args))
    sys.stdout.flush()


def _env_prepend(key, *values):
    os.environ[key] = os.pathsep.join(
        list(values) + os.environ.get(key, "").split(os.pathsep))


def install(cmake_version=DEFAULT_CMAKE_VERSION):
    """Download and install CMake into ``C:\\cmake``.

    The function also make sure to prepend ``C:\\cmake\\bin``
    to the ``PATH``."""

    cmake_version_major = cmake_version.split(".")[0]
    cmake_version_minor = cmake_version.split(".")[1]
    cmake_directory = "C:\\cmake-{}".format(cmake_version)
    cmake_package = "cmake-{}-win32-x86.zip".format(cmake_version)

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

    _log("Downloading", cmake_package)
    if not os.path.exists(cmake_directory):
        remote_file = urlopen(
            "https://cmake.org/files/v{}.{}/{}".format(
                cmake_version_major, cmake_version_minor, cmake_package))

        with open("C:\\%s" % cmake_package, "wb") as local_file:
            shutil.copyfileobj(remote_file, local_file)
        _log("  ->", "done")

        _log("Making directory", cmake_directory)
        try:
            os.mkdir(cmake_directory)
        except OSError:
            pass
        _log("  ->", "done")

        _log("Unpacking", cmake_package)
        with zipfile.ZipFile("C:\\%s" % cmake_package) as local_zip:
            local_zip.extractall(cmake_directory)
        _log("  ->", "done")

    else:
        _log("  ->", "skipping download: directory %s exists" % cmake_package)

    _log("Updating PATH with", cmake_directory)
    _env_prepend("PATH", "%s\bin" % cmake_directory)
    _log("  ->", "done")


if __name__ == '__main__':
    install(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CMAKE_VERSION)
