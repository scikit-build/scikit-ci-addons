===============================
scikit-ci-addons
===============================

.. image:: https://ci.appveyor.com/api/projects/status/gr60jc9hkjlqoo4a?svg=true
    :target: https://ci.appveyor.com/project/scikit-build/scikit-ci-addons/branch/master

.. image:: https://circleci.com/gh/scikit-build/scikit-ci-addons/tree/master.svg?style=svg
    :target: https://circleci.com/gh/scikit-build/scikit-ci-addons/tree/master

.. image:: https://img.shields.io/travis/scikit-build/scikit-ci-addons.svg?maxAge=2592000
    :target: https://travis-ci.org/scikit-build/scikit-ci-addons

scikit-ci-addons is a set of scripts useful to install prerequisites for building
Python extension on CI services.

* Free software: Apache Software license
* Source code: https://github.com/scikit-build/scikit-addons
* Mailing list: https://groups.google.com/forum/#!forum/scikit-build


Each directory contains scripts designed to be executed on the CI worker named
after the directory.


Appveyor
--------

These scripts are designed to work on worker from http://appveyor.com/


``install_cmake.py``
^^^^^^^^^^^^^^^^^^^^

Download and install in the PATH the specified version of CMake binaries.

Usage:

  python appveyor/install_cmake.py X.Y.Z

Example:

  python appveyor/install_cmake.py 3.6.2

Notes:

- CMake archive is downloaded and extracted into ``C:\\cmake-X.Y.Z``. That
  same directory can then be added to the cache. See `Build Cache <https://www.appveyor.com/docs/build-cache/>`_
  documentation for more details.

- ``C:\\cmake-X.Y.Z`` is prepended to the ``PATH``.
  TODO: Is the env global on AppVeyor ? Or does this work only with scikit-ci ?



``install_visual_studio_wrapper.py``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Usage:

  python appveyor/install_visual_studio_wrapper.py

Notes:

- Download ``run-with-visual-studio.cmd`` from `gh:ogrisel/python-appveyor-demo <https://github.com/ogrisel/python-appveyor-demo/tree/master/appveyor>`_


``run-with-visual-studio.cmd``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is a wrapper script setting the Visual Studio environment
matching the selected version of Python. This is particularly
important when building Python C Extensions.


Usage:

  run-with-visual-studio.cmd \\path\\to\\command [arg1 [...]]


Example:

  SET PYTHON_DIR="C:\\Python35"
  SET PYTHON_VERSION="3.5.x"
  SET PATH=%PYTHON_DIR%;%PYTHON_DIR%\\Scripts;%PATH%
  run-with-visual-studio.cmd python setup.by bdist_wheel


Notes:

- Python version selection is done by setting the ``PYTHON_VERSION`` and
  ``PYTHON_ARCH`` environment variables.

- Possible values for  ``PYTHON_VERSION`` are:

  - ``"2.7.x"``

  - ``"3.4.x"``

  - ``"3.5.x"``

- Possible values for ``PYTHON_ARCH`` are:

  - ``"32"``

  - ``"64"``

Author:

-  Olivier Grisel

License:

- `CC0 1.0 Universal <http://creativecommons.org/publicdomain/zero/1.0/>`_



``patch_vs2008.py``
^^^^^^^^^^^^^^^^^^^

This script patches the installation of `Visual C++ 2008 Express <https://www.appveyor.com/docs/installed-software/#visual-studio-2008>`_
so that it can be used to build 64-bit projects.

Usage:

  python appveyor/patch_vs2008.py

Notes:

- Download `vs2008_patch.zip <https://github.com/menpo/condaci/raw/master/vs2008_patch.zip>`_
  and execute ``setup_x64.bat``.

Credits:

- Xia Wei, sunmast#gmail.com

Links:

- http://www.cppblog.com/xcpp/archive/2009/09/09/vc2008express_64bit_win7sdk.html


``tweak_environment.py``
^^^^^^^^^^^^^^^^^^^^^^^^

- Update ``notepad++`` settings:

  - ``TabSetting.replaceBySpace`` set to ``yes``


Circle
------

These scripts are designed to work on worker from http://circleci.com/

``install_cmake.py``
^^^^^^^^^^^^^^^^^^^^

Download and install in the PATH the specified version of CMake binaries.

Usage:

  python appveyor/install_cmake.py X.Y.Z

Example:

  python appveyor/install_cmake.py 3.6.2

Notes:

- The script will skip the download if current version matches the selected
  one.


Travis
------

These scripts are designed to work on worker from http://travis-ci.org/

``install_cmake.py``
^^^^^^^^^^^^^^^^^^^^

Download and install in the PATH the specified version of CMake binaries.

Usage:

  python appveyor/install_cmake.py X.Y.Z

Example:

  python appveyor/install_cmake.py 3.6.2


Notes:

- The script automatically detects the operating system (``linux`` or ``osx``)
  and install CMake in a valid location.

- The archives are downloaded in ``/home/travis/downloads`` to allow
  caching. See `Caching Dependencies and Directories <https://docs.travis-ci.com/user/caching/>`_
  The script the download if the correct CMake archive is found in ``/home/travis/downloads``.

- Linux:

  - To support worker with and without ``sudo`` enabled, CMake is installed
    in ``HOME`` (i.e /home/travis). Since ``~/bin`` is already in the ``PATH``,
    CMake executables will be available in the PATH after running this script.

- MacOSX:

  - Consider using this script only if the available version does **NOT**
    work for you. See the `Compilers-and-Build-toolchain <https://docs.travis-ci.com/user/osx-ci-environment/#Compilers-and-Build-toolchain>`_
    in Travis documentation.

  - What does this script do ? First, it removes the older version of CMake
    executable installed in ``/usr/local/bin``. Then, it installs the selected
    version of CMake using ``sudo cmake-gui --install``.



``install_pyenv.py``
^^^^^^^^^^^^^^^^^^^^


``run-with-pyenv.sh``
^^^^^^^^^^^^^^^^^^^^^
