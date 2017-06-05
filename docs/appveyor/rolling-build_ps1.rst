``rolling-build.ps1``
^^^^^^^^^^^^^^^^^^^^^

Cancel on-going build if there is a newer build queued for the same PR

Usage:

.. code-block:: yaml

  - ps: rolling-build.ps1

.. note::

    - If there is a newer build queued for the same PR, cancel this one.
      The AppVeyor 'rollout builds' option is supposed to serve the same
      purpose but it is problematic because it tends to cancel builds pushed
      directly to master instead of just PR builds (or the converse).
      credits: JuliaLang developers.