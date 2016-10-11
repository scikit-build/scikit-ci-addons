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

Each directory contains scripts designed to be executed on the CI worker named
after the directory.


Appveyor
--------

These scripts are designed to work on worker from http://appveyor.com/

- ``install_cmake.py``
- ``install_visual_studio_wrapper.py``
- ``run-with-visual-studio.cmd``
- ``patch_vs2008.py``
- ``tweak_environment.py``


Circle
------

These scripts are designed to work on worker from http://circleci.com/

- ``install_cmake.py``


Travis
------

These scripts are designed to work on worker from http://travis-ci.org/

- ``install_cmake.py``
- ``install_pyenv.py``
- ``run-with-pyenv.sh``


Resources
=========

* Free software: Apache Software license
* Source code: https://github.com/scikit-build/scikit-addons
* Mailing list: https://groups.google.com/forum/#!forum/scikit-build
