=======
Add-ons
=======

Each category is named after a CI worker (e.g AppVeyor) or operating system (e.g Windows)
and references add-ons designed to be used on the associated continuous integration service
or system.

An add-on is a file that could either directly be executed or used as a
parameter for an other tool.

Anyci
-----

This a special category containing scripts that could be executed on a broad
range of CI services.

.. include:: anyci/ctest_junit_formatter.rst
.. include:: anyci/docker_py.rst
.. include:: anyci/noop_py.rst
.. include:: anyci/publish_github_release_py.rst
.. include:: anyci/run_sh.rst

Appveyor
--------

.. warning::

  These scripts were designed to work on worker from http://appveyor.com/

  They have been retired and are available only in scikit-ci-addons <= 0.25.0

  See https://scikit-ci-addons.readthedocs.io/en/0.25.0/addons.html#appveyor


``enable-worker-remote-access.ps1``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``install_cmake.py``
^^^^^^^^^^^^^^^^^^^^

``run-with-visual-studio.cmd``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``patch_vs2008.py``
^^^^^^^^^^^^^^^^^^^

``rolling-build.ps1``
^^^^^^^^^^^^^^^^^^^^^

``tweak_environment.py``
^^^^^^^^^^^^^^^^^^^^^^^^

Circle
------

These scripts are designed to work on worker from http://circleci.com/

.. include:: circle/install_cmake_py.rst

Travis
------

These scripts are designed to work on worker from http://travis-ci.org/

.. include:: travis/install_cmake_py.rst
.. include:: travis/pyenv.rst
.. include:: travis/enable-worker-remote-access_sh.rst

Windows
-------

These scripts are designed to work on any windows workstation running Windows 7 and above and can
be directly used from a powershell terminal (or command line terminal) using a simple one-liner.

Content of the scripts can easily be inspected in the `associated source repository <https://github.com/scikit-build/scikit-ci-addons/tree/master/windows>`_.

.. include:: windows/install-scripts.rst
