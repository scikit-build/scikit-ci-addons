=====
Usage
=====

The scikit-ci-addons command line executable allows to discover, execute and
get the path of any of the distributed :doc:`add-ons </addons>`.

For example:

.. code-block:: bash

    ci_addons appveyor/patch_vs2008


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
