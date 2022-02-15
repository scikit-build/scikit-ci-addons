=====
Usage
=====

The scikit-ci-addons command line executable allows to discover, execute and
get the path of any of the distributed :doc:`add-ons </addons>`.

Executing an add-on
-------------------

::

    ci_addons ADDON_NAME

where ``ADDON_NAME`` can be any of the names displayed using ``ci_addons --list``.

For example:

.. code-block:: bash

    $ ci_addons circle/install_cmake


Listing available add-ons
-------------------------

::

    ci_addons --list


For example:

.. code-block:: bash

    $ ci_addons --list

    anyci/ctest_junit_formatter.py
    anyci/publish_github_release.py
    anyci/run.sh
    anyci/ctest_junit_formatter.xsl
    anyci/noop.py
    anyci/docker.py

    circle/install_cmake.py

    windows/install-miniconda3.ps1
    windows/install-utils.ps1
    windows/install-cmake.ps1
    windows/install-python-27-x64.ps1
    windows/install-nsis.ps1
    windows/install-svn.ps1
    windows/install-ninja.ps1
    windows/install-python.ps1
    windows/install-python-36-x64.ps1
    windows/install-git.ps1
    windows/install-flang.ps1

.. note::

    To learn more about each add-on, consider reading the
    :doc:`add-ons </addons>` section.


Getting directory containing all add-ons
----------------------------------------

::

    ci_addons --home

For example:

.. code-block:: bash

    $ ci_addons --home
    /home/jcfr/.virtualenvs/test/local/lib/python2.7/site-packages


Installing add-ons into selected directory
------------------------------------------

::

    ci_addons --install DIR

where ``DIR`` is a valid path to an existing directory.

For example:

.. code-block:: bash

    $ ci_addons --install /tmp
    /tmp/anyci/ctest_junit_formatter.py
    /tmp/anyci/publish_github_release.py
    /tmp/anyci/run.sh
    /tmp/anyci/ctest_junit_formatter.xsl
    /tmp/anyci/noop.py
    /tmp/anyci/docker.py
    /tmp/circle/install_cmake.py
    /tmp/windows/install-miniconda3.ps1
    /tmp/windows/install-utils.ps1
    /tmp/windows/install-cmake.ps1
    /tmp/windows/install-python-27-x64.ps1
    /tmp/windows/install-nsis.ps1
    /tmp/windows/install-svn.ps1
    /tmp/windows/install-ninja.ps1
    /tmp/windows/install-python.ps1
    /tmp/windows/install-python-36-x64.ps1
    /tmp/windows/install-git.ps1
    /tmp/windows/install-flang.ps1


Getting full path of an add-on
------------------------------

::

    ci_addons --path PATH

where ``PATH`` can be any of these:

- relative path with or without extension (e.g ``circle/install_cmake.py``
  or ``circle/install_cmake.py``)

- full path (e.g ``/path/to/circle/install_cmake.py``)

- script name with or without extension (e.g ``install_cmake.py``
  or ``patch_vs2008``). If there are multiple add-ons with the same bame,
  ``ci_addons`` reports an error message listing the add-ons to choose from.

For example:

.. code-block:: bash

    $ ci_addons --path circle/install_cmake.py
    /home/jcfr/.virtualenvs/test/local/lib/python2.7/site-packages/circle/install_cmake.py

.. note::

    This function is particularly useful when the selected add-on is not a
    python script and is expected to be used as an input to an other tool.


Calling scikit-ci-addons through ``python -m ci_addons``
--------------------------------------------------------

You can invoke scikit-ci-addons through the Python interpreter from the command
line::

    python -m ci_addons [...]

This is equivalent to invoking the command line script ``ci_addons [...]``
directly.


Getting help on version, option names
-------------------------------------

::

    ci_addons --version   # shows where ci_addons was imported from
    ci_addons -h | --help # show help on command line
