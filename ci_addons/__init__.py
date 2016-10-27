# -*- coding: utf-8 -*-

"""
scikit-ci-addons is a command line tool and a set of scripts useful to install
prerequisites for building Python extension on CI services.
"""

import os
import sys

from subprocess import check_call

__author__ = 'The scikit-build team'
__email__ = 'scikit-build@googlegroups.com'
__version__ = '0.2.0'


def addons():
    """Return all available addons."""

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
    """Return directory where all addons can be found."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def path(addon_name):
    """Return path of ``addon_name``.

    This is particularly useful when the selected addon is not a python
    script and is expected to be used an input to an other tool."""

    addon_path = tmp_addon_path = os.path.join(home(), addon_name)
    if not os.path.exists(tmp_addon_path):
        tmp_addon_path += '.py'
    if not os.path.exists(tmp_addon_path):
        raise RuntimeError("Could not find addon: %s" % addon_path)
    return tmp_addon_path


def execute(addon_name, arguments=[]):
    """Execute ``addon_name`` with ``arguments``.

    Executable addons are python script.
    """
    cmd = [sys.executable, path(addon_name)] + arguments
    check_call(cmd)
