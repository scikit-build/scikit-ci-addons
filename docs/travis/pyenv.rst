
``install_pyenv.py``
^^^^^^^^^^^^^^^^^^^^

Usage::

  export PYTHON_VERSION=X.Y.Z
  ci_addons travis/install_pyenv.py

.. note::

    - Update the version of ``pyenv`` using ``brew``.

    - Install the version of python selected setting ``PYTHON_VERSION``
      environment variable.


``run-with-pyenv.sh``
^^^^^^^^^^^^^^^^^^^^^

This is a wrapper script setting the environment corresponding to the
version selected setting ``PYTHON_VERSION`` environment variable.

Usage::

    export PYTHON_VERSION=X.Y.Z
    ci_addons --install ../
    ../travis/run-with-pyenv.sh python --version
