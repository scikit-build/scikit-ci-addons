``install_cmake.py``
^^^^^^^^^^^^^^^^^^^^

Download and install in the PATH the specified version of CMake binaries.

Usage::

    ci_addons appveyor/install_cmake.py X.Y.Z

Example::

    $ ci_addons appveyor/install_cmake.py 3.6.2

.. note::

    - CMake archive is downloaded and extracted into ``C:\\cmake-X.Y.Z``. That
      same directory can then be added to the cache. See `Build Cache <https://www.appveyor.com/docs/build-cache/>`_
      documentation for more details.

    - ``C:\\cmake-X.Y.Z`` is prepended to the ``PATH``.
      TODO: Is the env global on AppVeyor ? Or does this work only with scikit-ci ?