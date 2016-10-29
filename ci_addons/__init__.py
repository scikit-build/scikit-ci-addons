# -*- coding: utf-8 -*-

"""
scikit-ci-addons is a command line tool and a set of scripts useful to install
prerequisites for building Python extension on CI services.
"""

import os
import shutil
import sys

from subprocess import check_call

__author__ = 'The scikit-build team'
__email__ = 'scikit-build@googlegroups.com'
__version__ = '0.5.0'


def addons():
    """Return all available add-ons."""

    addons = []

    for dirname, dirnames, filenames in os.walk(home()):

        for v in list(dirnames):
            dirnames.remove(v)
        dirnames += ['anyci', 'appveyor', 'circle', 'travis']

        if dirname == home():
            continue

        for filename in filenames:
            if filename in ['__init__.py']:
                continue
            addon_path = os.path.join(dirname, filename)
            addons.append(os.path.relpath(addon_path, home()))

    return addons


def home():
    """Return directory where all add-ons can be found."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def path(addon_name):
    """Return path of ``addon_name``.

    This is particularly useful when the selected add-on is not a python
    script and is expected to be used an input to an other tool."""

    addon_path = tmp_addon_path = os.path.join(home(), addon_name)
    if not os.path.exists(tmp_addon_path):
        tmp_addon_path += '.py'
    if not os.path.exists(tmp_addon_path):
        raise RuntimeError("Could not find addon: %s" % addon_path)
    return tmp_addon_path


def install(dst_path, force=False):
    """Copy add-ons into ``dst_path``.

    By default, existing add-ons are *NOT* overwritten. Specifying ``force``
    allow to overwrite them.
    """
    dst_path = os.path.normpath(os.path.abspath(dst_path))
    if dst_path == os.path.normpath(home()):
        raise RuntimeError(
            "skipping install: target directory already contains addons")
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
    check_call(cmd)
