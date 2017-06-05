``enable-worker-remote-access.ps1``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Enable access to the build worker via Remote Desktop.

Usage::

    - ci_addons --install ../
    - ps: ../appveyor/enable-worker-remote-access.ps1 [-block|-check_for_block]

Example::

    - ci_addons --install ../
    - ps: ../appveyor/enable-worker-remote-access.ps1 -block


.. note::

    - Calling this script will enable and display the Remote Desktop
      connection details. By default, the connection will be available
      for the length of the build.

    - Specifying ``-block`` option will ensure the connection remains
      open for at least 60 mins.

    - Specifying ``-check_for_block`` option will keep the connection
      open only if the environment variable ``BLOCK`` has been set to ``1``.