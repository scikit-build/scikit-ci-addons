``run-with-visual-studio.cmd``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is a wrapper script setting the Visual Studio environment
matching the selected version of Python. This is particularly
important when building Python C Extensions.


Usage::

    ci_addons --install ../
    ../appveyor/run-with-visual-studio.cmd \\path\\to\\command [arg1 [...]]

Example::

    SET PYTHON_DIR="C:\\Python35"
    SET PYTHON_VERSION="3.5.x"
    SET PYTHON_ARCH="64"
    SET PATH=%PYTHON_DIR%;%PYTHON_DIR%\\Scripts;%PATH%
    ci_addons --install ../
    ../appveyor/run-with-visual-studio.cmd python setup.by bdist_wheel

Author:

-  Olivier Grisel

License:

- `CC0 1.0 Universal <http://creativecommons.org/publicdomain/zero/1.0/>`_

.. note::

    - Python version selection is done by setting the ``PYTHON_VERSION`` and
      ``PYTHON_ARCH`` environment variables.

    - Possible values for  ``PYTHON_VERSION`` are:

      - ``"2.7.x"``

      - ``"3.4.x"``

      - ``"3.5.x"``

    - Possible values for ``PYTHON_ARCH`` are:

      - ``"32"``

      - ``"64"``