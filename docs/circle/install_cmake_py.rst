``install_cmake.py``
^^^^^^^^^^^^^^^^^^^^

Download and install in the PATH the specified version of CMake binaries.

Usage::

    ci_addons circle/install_cmake.py X.Y.Z

Example::

    $ ci_addons circle/install_cmake.py 3.6.2

.. note::

    - The script will skip the download if current version matches the selected
      one.