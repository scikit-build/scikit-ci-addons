``install_cmake.py``
^^^^^^^^^^^^^^^^^^^^

Download and install in the PATH the specified version of CMake binaries.

Usage::

    ci_addons circle/install_cmake.py X.Y.Z

Example::

    $ ci_addons circle/install_cmake.py 3.6.2

.. note::

    - The script will skip the download in two cases:

      - if current version matches the selected one.

      - if archive already exist in ``$HOME/downloads`` directory.

    - Adding directory ``$HOME/downloads`` to the CircleCI cache can speed up
      the build. For more details, see `Caching Dependencies <https://circleci.com/docs/2.0/caching/>`_.