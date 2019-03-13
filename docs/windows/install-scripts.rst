For example, on a new system without python or git installed, they can be installed from a powershell terminal
open as administrator: ::

    Set-ExecutionPolicy Unrestricted -Force
    [System.Net.ServicePointManager]::SecurityProtocol = 3072 -bor 768 -bor 192 -bor 48

    iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-python-36-x64.ps1'))
    iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-git.ps1'))


Read `here <https://technet.microsoft.com/en-us/library/ee176961.aspx>`_ to learn about the
powershell execution policy.

Details for each ``install-*.ps1`` scripts are reported below.


``install-cmake.ps1``
^^^^^^^^^^^^^^^^^^^^^

Install selected CMake version in ``C:\cmake-X.Y.Z``.

From a powershell terminal open as administrator: ::

    Set-ExecutionPolicy Unrestricted -Force
    [System.Net.ServicePointManager]::SecurityProtocol = 3072 -bor 768 -bor 192 -bor 48

    $cmakeVersion="3.8.1"
    iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-cmake.ps1'))

.. note::

    - CMake is **NOT** added to the ``PATH``
    - setting ``$cmakeVersion`` to "X.Y.Z" before executing the script allows to select a specific CMake version.
    - on AppVeyor, the download and install can be skipped by adding directory ``C:\cmake-X.Y.Z`` to the ``cache``. For more details, see https://www.appveyor.com/docs/build-cache/#configuring-cache-items

.. note::

    - to understand why ``SecurityProtocol`` is set, see :ref:`addressing_underlying_connection_closed`

``install-flang.ps1``
^^^^^^^^^^^^^^^^^^^^^

Install latest ``flang`` in a new conda environment named `flang-env`.

From a powershell terminal open as administrator: ::

    Set-ExecutionPolicy Unrestricted -Force
    [System.Net.ServicePointManager]::SecurityProtocol = 3072 -bor 768 -bor 192 -bor 48

    iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-flang.ps1'))

Flang is a Fortran compiler targeting LLVM, it was `announced <https://www.llnl.gov/news/nnsa-national-labs-team-nvidia-develop-open-source-fortran-compiler-technology>`_
in 2015.

Source code is hosted on GitHub at https://github.com/flang-compiler/flang, the windows fork is hosted as https://github.com/isuruf/flang

.. note::

    - to understand why ``SecurityProtocol`` is set, see :ref:`addressing_underlying_connection_closed`

``install-git.ps1``
^^^^^^^^^^^^^^^^^^^

Install Git 2.11.0 (including Git Bash) on the system.

From a powershell terminal open as administrator: ::

    Set-ExecutionPolicy Unrestricted -Force
    [System.Net.ServicePointManager]::SecurityProtocol = 3072 -bor 768 -bor 192 -bor 48

    iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-git.ps1'))


.. note::

    - Git executables are added to the ``PATH``

.. note::

    - to understand why ``SecurityProtocol`` is set, see :ref:`addressing_underlying_connection_closed`

``install-miniconda3.ps1``
^^^^^^^^^^^^^^^^^^^^^^^^^^

Install latest miniconda3 environment into ``C:\Miniconda3``.

From a powershell terminal open as administrator: ::

    Set-ExecutionPolicy Unrestricted -Force
    [System.Net.ServicePointManager]::SecurityProtocol = 3072 -bor 768 -bor 192 -bor 48

    iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-miniconda3.ps1'))


.. note::

    - miniconda environment is **NOT** added to the ``PATH`` and registry.

.. note::

    - to understand why ``SecurityProtocol`` is set, see :ref:`addressing_underlying_connection_closed`

``install-ninja.ps1``
^^^^^^^^^^^^^^^^^^^^^

Install ninja executable v1.7.2 into ``C:\ninja-1.7.2``.

From a powershell terminal open as administrator: ::

    Set-ExecutionPolicy Unrestricted -Force
    [System.Net.ServicePointManager]::SecurityProtocol = 3072 -bor 768 -bor 192 -bor 48

    iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-ninja.ps1'))


.. note::

    - ninja executable is **NOT** added to the ``PATH``

.. note::

    - to understand why ``SecurityProtocol`` is set, see :ref:`addressing_underlying_connection_closed`

``install-nsis.ps1``
^^^^^^^^^^^^^^^^^^^^

Install NSIS 3.01 on the system.

From a powershell terminal open as administrator: ::

    Set-ExecutionPolicy Unrestricted -Force
    [System.Net.ServicePointManager]::SecurityProtocol = 3072 -bor 768 -bor 192 -bor 48

    iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-nsis.ps1'))


.. note::

    - nsis executable is added to the ``PATH``

.. note::

    - to understand why ``SecurityProtocol`` is set, see :ref:`addressing_underlying_connection_closed`

``install-python.ps1``
^^^^^^^^^^^^^^^^^^^^^^

Install Python 2.7.15, 3.4.4, 3.5.4, 3.6.8, 3.7.2 and 3.8.0a2 (32 and 64-bit) along with pip and virtualenv
in the following directories: ::

    C:\Python27-x64
    C:\Python27-x86

    C:\Python34-x64
    C:\Python34-x86

    C:\Python35-x64
    C:\Python35-x86

    C:\Python36-x64
    C:\Python36-x86

    C:\Python37-x64
    C:\Python37-x86

    C:\Python38-x64
    C:\Python38-x86

.. note::
    - python interpreter is **NOT** added to the ``PATH``
    - setting ``$pythonVersion`` to either "2.7", "3.4", "3.5", "3.6", "3.7" or "3.8" before executing the script allows
      to install a specific version. By default, all are installed.
    - setting ``$pythonArch`` to either "86", "32" or "64" before executing the script allows
      to install python for specific architecture. By default, both are installed.
      Values "86" and "32" correspond to the same architecture.
    - setting ``$pythonPrependPath`` to 1 will add install and Scripts directories the PATH and .PY to PATHEXT. This
      variable should be set only if ``$pythonVersion`` and ``$pythonArch`` are set. By default, the value is 0.

.. note::

    - to understand why ``SecurityProtocol`` is set, see :ref:`addressing_underlying_connection_closed`

.. warning::
    - The downloaded versions of python may **NOT** be the latest version including security patches.
      If running in a production environment (e.g webserver), these versions should be built from source.


``install-python-27-x64.ps1``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Install Python 2.7 64-bit and update the PATH.

From a powershell terminal open as administrator: ::

    Set-ExecutionPolicy Unrestricted -Force
    [System.Net.ServicePointManager]::SecurityProtocol = 3072 -bor 768 -bor 192 -bor 48

    iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-python-27-x64.ps1'))


This is equivalent to: ::

    Set-ExecutionPolicy Unrestricted -Force
    [System.Net.ServicePointManager]::SecurityProtocol = 3072 -bor 768 -bor 192 -bor 48

    $pythonVersion = "2.7"
    $pythonArch = "64"
    $pythonPrependPath = "1"
    iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-python.ps1'))

.. note::

    - ``C:\Python27-x64`` and ``C:\Python27-x64\Scripts`` are prepended to the ``PATH``

.. note::

    - to understand why ``SecurityProtocol`` is set, see :ref:`addressing_underlying_connection_closed`


``install-python-36-x64.ps1``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Install Python 3.6 64-bit and update the PATH.

From a powershell terminal open as administrator: ::

    Set-ExecutionPolicy Unrestricted -Force
    [System.Net.ServicePointManager]::SecurityProtocol = 3072 -bor 768 -bor 192 -bor 48

    iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-python-36-x64.ps1'))


This is equivalent to: ::

    Set-ExecutionPolicy Unrestricted -Force
    [System.Net.ServicePointManager]::SecurityProtocol = 3072 -bor 768 -bor 192 -bor 48

    $pythonVersion = "3.6"
    $pythonArch = "64"
    $pythonPrependPath = "1"
    iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-python.ps1'))

.. note::

    - ``C:\Python36-x64`` and ``C:\Python36-x64\Scripts`` are prepended to the ``PATH``

.. note::

    - to understand why ``SecurityProtocol`` is set, see :ref:`addressing_underlying_connection_closed`


``install-svn.ps1``
^^^^^^^^^^^^^^^^^^^^

Install `Slik SVN <https://sliksvn.com/download/>`_ 1.9.5 in the following directory: ::

    C:\SlikSvn


From a powershell terminal open as administrator: ::

    Set-ExecutionPolicy Unrestricted -Force
    [System.Net.ServicePointManager]::SecurityProtocol = 3072 -bor 768 -bor 192 -bor 48

    iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-svn.ps1'))


.. note::

    - svn executable is added to the ``PATH``

.. note::

    - to understand why ``SecurityProtocol`` is set, see :ref:`addressing_underlying_connection_closed`


``install-utils.ps1``
^^^^^^^^^^^^^^^^^^^^^

This script is automatically included (and downloaded if needed) by the other addons, it
provides convenience functions useful to download and install programs:


  ``Always-Download-File($url, $file)``:

    Systematically download `$url` into `$file`.


  ``Download-File($url, $file)``:

    If file is not found, download `$url` into `$file`.


  ``Download-URL($url, $downloadDir)``:

    Download `$url` into `$downloadDir`. The filename is extracted from `$url`.


  ``Install-MSI($fileName, $downloadDir, $targetDir)``:

    Programatically install MSI installers `$downloadDir\$fileName`
    into `$targetDir`. The package is installed for all users.


  ``Which($progName)``

    Search for `$progName` in the ``PATH`` and return its full path.


  ``Download-7zip($downloadDir)``:

    If not found, download 7zip executable ``7za.exe`` into `$downloadDir`. The function
    returns the full path to the executable.


  ``Always-Extract-Zip($filePath, $destDir)``:

    Systematically extract zip file `$filePath` into `$destDir` using
    7zip. If 7zip executable ``7za.exe`` is not found in `$downloadDir`, it is downloaded
    using function ``Download-7zip``.


  ``Extract-Zip($filePath, $destDir)``:

    Extract zip file into `$destDir` only if `$destDir` does not exist.


Frequently Asked Questions
^^^^^^^^^^^^^^^^^^^^^^^^^^

Installing add-on from a Windows command line terminal
""""""""""""""""""""""""""""""""""""""""""""""""""""""

This can be using the following syntax::

    @powershell -ExecutionPolicy Unrestricted "iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-ninja.ps1'))"


.. _addressing_underlying_connection_closed:

Addressing "The underlying connection was closed" error
"""""""""""""""""""""""""""""""""""""""""""""""""""""""

::

    PS C:\Users\dashboard> iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-python.ps1'))

    Error: 0
    Description: The underlying connection was closed: An unexpected error occurred on a receive.


As explained the `chololatey documentation <https://github.com/chocolatey/choco/wiki/Installation#installing-with-restricted-tls>`_,
this most likely happens because the build script is attempting to download from a server that needs to use TLS 1.1 or
TLS 1.2 and has restricted the use of TLS 1.0 and SSL v3.

The first things to try is to use the following snippet replacing ``https://file/to/download`` with
the appropriate value::

    $securityProtocolSettingsOriginal = [System.Net.ServicePointManager]::SecurityProtocol

    try {
        # Set TLS 1.2 (3072), then TLS 1.1 (768), then TLS 1.0 (192), finally SSL 3.0 (48)
        # Use integers because the enumeration values for TLS 1.2 and TLS 1.1 won't
        # exist in .NET 4.0, even though they are addressable if .NET 4.5+ is
        # installed (.NET 4.5 is an in-place upgrade).
        [System.Net.ServicePointManager]::SecurityProtocol = 3072 -bor 768 -bor 192 -bor 48
    } catch {
        Write-Warning 'Unable to set PowerShell to use TLS 1.2 and TLS 1.1 due to old .NET Framework installed. If you see underlying connection closed or trust errors, you may need to upgrade to .NET Framework 4.5 and PowerShell v3'
    }

    iex ((new-object net.webclient).DownloadString('https://file/to/download'))

    [System.Net.ServicePointManager]::SecurityProtocol = $securityProtocolSettingsOriginal


If that does not address the problem, you should update the version of `.NET` installed and install
a newer version of PowerShell:

* https://en.wikipedia.org/wiki/.NET_Framework_version_history#Overview
* https://social.technet.microsoft.com/wiki/contents/articles/21016.how-to-install-windows-powershell-4-0.aspx
