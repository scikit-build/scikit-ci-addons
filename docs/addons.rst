=======
Add-ons
=======

Each category is named after a CI worker (e.g appveyor) and references add-ons
designed to be used on the associated continuous integration service.

An add-on is a file that could either directly be executed or used as a
parameter for an other tool.


Anyci
-----

This a special category containing scripts that could be executed on a broad
range of CI services.


``docker.py``
^^^^^^^^^^^^^

Add-on facilitating docker use on CI services.

It allows to load an image from local cache, pull and save back using
a convenience one-liner.

Usage::

  docker.py load-pull-save [-h] [--cache-dir CACHE_DIR] [--verbose]
                                NAME[:TAG|@DIGEST]

Example::

  $ python anyci/docker.py load-pull-save hello-world:latest
  [anyci:docker.py] Loading cached image from /home/jcfr/docker/hello-world-latest.tar
  [anyci:docker.py]   -> cached image not found
  [anyci:docker.py] Pulling image: hello-world:latest
  [anyci:docker.py]   -> done
  [anyci:docker.py] Reading image ID from current image
  [anyci:docker.py]   -> image ID: sha256:c54a2cc56cbb2f04003c1cd4507e118af7c0d340fe7e2720f70976c4b75237dc
  [anyci:docker.py] Caching image
  [anyci:docker.py]   -> image cached: /home/jcfr/docker/hello-world-latest.tar
  [anyci:docker.py] Saving image ID into /home/jcfr/docker/hello-world-latest.image_id
  [anyci:docker.py]   -> done

Notes:

- Image is saved into the cache only if needed. In addition to the image
  archive (e.g `image-name.tar`), a file containing the image ID is also
  saved into the cache directory (e.g `image-name.image_id`). This allows
  to quickly read back the image ID of the cached image and determine if
  the current image should be saved into the cache.

``noop.py``
^^^^^^^^^^^

Display name of script and associated argument (basically the value of
``sys.argv``).


``run.sh``
^^^^^^^^^^

Wrapper script executing command and arguments passed as parameters.


Appveyor
--------

These scripts are designed to work on worker from http://appveyor.com/


``enable-worker-remote-access.ps1``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Enable access to the build worker via Remote Desktop.

Usage::

  - ps: enable-worker-remote-access.ps1 [-force|-check_for_block]

Example::

  - ps: ../addons/appveyor/enable-worker-remote-access.ps1 -block

Notes::

- Calling this script will enable and display the Remote Desktop
  connection details. By default, the connection will be available
  for the length of the build.

- Specifying ``-block`` option will ensure the connection remains
  open for at least 60 mins.

- Specifying ```-check_for_block`` option will keep the connection
  open only if the environment variable ``BLOCK`` has been set to ``1``.



``install_cmake.py``
^^^^^^^^^^^^^^^^^^^^

Download and install in the PATH the specified version of CMake binaries.

Usage::

  python appveyor/install_cmake.py X.Y.Z

Example::

  python appveyor/install_cmake.py 3.6.2

Notes:

- CMake archive is downloaded and extracted into ``C:\\cmake-X.Y.Z``. That
  same directory can then be added to the cache. See `Build Cache <https://www.appveyor.com/docs/build-cache/>`_
  documentation for more details.

- ``C:\\cmake-X.Y.Z`` is prepended to the ``PATH``.
  TODO: Is the env global on AppVeyor ? Or does this work only with scikit-ci ?



``run-with-visual-studio.cmd``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is a wrapper script setting the Visual Studio environment
matching the selected version of Python. This is particularly
important when building Python C Extensions.


Usage::

  run-with-visual-studio.cmd \\path\\to\\command [arg1 [...]]

Example::

  SET PYTHON_DIR="C:\\Python35"
  SET PYTHON_VERSION="3.5.x"
  SET PYTHON_ARCH="64"
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

Usage::

  python appveyor/patch_vs2008.py

Notes:

- Download `vs2008_patch.zip <https://github.com/menpo/condaci/raw/master/vs2008_patch.zip>`_
  and execute ``setup_x64.bat``.

Credits:

- Xia Wei, sunmast#gmail.com

Links:

- http://www.cppblog.com/xcpp/archive/2009/09/09/vc2008express_64bit_win7sdk.html


``rolling-build.ps1``
^^^^^^^^^^^^^^^^^^^^^

Cancel on-going build if there is a newer build queued for the same PR

Usage::

  - ps: rolling-build.ps1

Notes::

- If there is a newer build queued for the same PR, cancel this one.
  The AppVeyor 'rollout builds' option is supposed to serve the same
  purpose but it is problematic because it tends to cancel builds pushed
  directly to master instead of just PR builds (or the converse).
  credits: JuliaLang developers.


``tweak_environment.py``
^^^^^^^^^^^^^^^^^^^^^^^^

Usage::

  python tweak_environment.py

Notes:

- Update ``notepad++`` settings:

  - ``TabSetting.replaceBySpace`` set to ``yes``


Circle
------

These scripts are designed to work on worker from http://circleci.com/

``install_cmake.py``
^^^^^^^^^^^^^^^^^^^^

Download and install in the PATH the specified version of CMake binaries.

Usage::

  python appveyor/install_cmake.py X.Y.Z

Example::

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

Usage::

  python appveyor/install_cmake.py X.Y.Z

Example::

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

Usage::

  export PYTHONVERSION=X.Y.Z
  python install_pyenv.py

Notes:

- Update the version of ``pyenv`` using ``brew``.

- Install the version of python selected setting ``PYTHONVERSION``
  environment variable.


``run-with-pyenv.sh``
^^^^^^^^^^^^^^^^^^^^^

This is a wrapper script setting the environment corresponding to the
version selected setting ``PYTHONVERSION`` environment variable.

Usage::

  export PYTHONVERSION=X.Y.Z
  run-with-pyenv.sh python --version
