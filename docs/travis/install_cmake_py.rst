``install_cmake.py``
^^^^^^^^^^^^^^^^^^^^

Download and install in the PATH the specified version of CMake binaries.

Usage::

    ci_addons appveyor/install_cmake.py X.Y.Z

Example::

    $ ci_addons appveyor/install_cmake.py 3.6.2


.. note::

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