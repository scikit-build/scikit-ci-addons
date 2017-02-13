# -*- coding: utf-8 -*-

"""
scikit-ci-addons is a command line tool and a set of scripts useful to install
prerequisites for building Python extension on CI services.
"""

import os
import shutil
import sys

from subprocess import CalledProcessError, check_call

from ._version import get_versions

__author__ = 'The scikit-build team'
__email__ = 'scikit-build@googlegroups.com'
__version__ = get_versions()['version']
del get_versions

DIR_NAMES = ['anyci', 'appveyor', 'circle', 'travis']


class SKAddonsError(RuntimeError):
    """Exception raised when a user error occurs.
    """
    pass


def addons():
    """Return all available add-ons."""

    addons = []

    for dirname, dirnames, filenames in os.walk(home()):

        for v in list(dirnames):
            dirnames.remove(v)
        dirnames += DIR_NAMES

        if dirname == home():
            continue

        for filename in filenames:
            if filename in ['__init__.py'] or filename.endswith(".pyc"):
                continue
            addon_path = os.path.join(dirname, filename)
            addons.append(os.path.relpath(addon_path, home()))

    return addons


def home():
    """Return directory where all add-ons can be found."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def path(addon_name):
    """Return path of ``addon_name``.

    Supported values for ``addon_name`` are listed below:
    - relative path with or without extension (e.g ``appveyor/patch_vs2008.py``
      or ``appveyor/patch_vs2008.py``)
    - full path (e.g ``/path/to/appveyor/patch_vs2008.py``
    - script name with or without extension (e.g ``patch_vs2008.py``
      or ``patch_vs2008``). If there are multiple matching scripts, a
      ``SKAddonsError`` exception is raised.
    """
    def _path(_addon_name):
        _addon_path = os.path.join(dir_name, home(), _addon_name)
        if (not os.path.exists(_addon_path)
                and not _addon_path.endswith(".py")):
            _addon_path += '.py'
        return _addon_path if os.path.exists(_addon_path) else ""

    candidates = []
    for dir_name in DIR_NAMES + [""]:
        addon_path = _path(os.path.join(dir_name, addon_name))
        if addon_path and addon_path not in candidates:
            candidates.append(addon_path)
    if len(candidates) > 1:
        raise SKAddonsError(
            "Failed to return a single path because it found %d matching "
            "paths. You must select one of these:\n  %s" % (
                len(candidates), "\n  ".join(candidates)))
    elif len(candidates) == 1:
        return candidates[0]
    else:
        raise SKAddonsError("Could not find addon: %s" % addon_name)


def install(dst_path, force=False):
    """Copy add-ons into ``dst_path``.

    By default, existing add-ons are *NOT* overwritten. Specifying ``force``
    allow to overwrite them.
    """
    dst_path = os.path.normpath(os.path.abspath(dst_path))
    if dst_path == os.path.normpath(home()):
        raise SKAddonsError(
            "skipping install: target directory already contains add-ons")
    for addon in addons():
        dst_addon_path = os.path.join(dst_path, addon)
        dst_addon_dir = os.path.split(dst_addon_path)[0]
        if not os.path.exists(dst_addon_dir):
            os.makedirs(dst_addon_dir)
        src_addon_path = os.path.join(home(), addon)
        extra = ""
        do_copy = True
        if os.path.exists(dst_addon_path):
            extra = " (skipped)"
            do_copy = False
            if force:
                extra = " (overwritten)"
                do_copy = True
        if do_copy:
            shutil.copy(src_addon_path, dst_addon_path)
        print(dst_addon_path + extra)


def execute(addon_name, arguments=[]):
    """Execute ``addon_name`` with ``arguments``.

    Executable add-ons are python script.
    """
    cmd = [sys.executable, path(addon_name)] + arguments
    try:
        check_call(cmd)
    except CalledProcessError as error:
        sys.exit(error.returncode)
