For example, on a new system without python or git installed, the following can be done to
install them:

* from a windows command terminal open as administrator ::

    @powershell -ExecutionPolicy Unrestricted "iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-python-36-x64.ps1'))"
    @powershell -ExecutionPolicy Unrestricted "iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-git.ps1'))"


* or from a powershell terminal open as administrator: ::

    Set-ExecutionPolicy Unrestricted
    iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-python-36-x64.ps1'))
    iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-git.ps1'))


Read `here <https://technet.microsoft.com/en-us/library/ee176961.aspx>`_ to learn about the
powershell execution policy.

Details for each ``install-*.ps1`` scripts are reported below.


``install-cmake.ps1``
^^^^^^^^^^^^^^^^^^^^^

Install selected CMake version in ``C:\cmake-X.Y.Z``.

* from a windows command terminal open as administrator ::

    @powershell -ExecutionPolicy Unrestricted "$cmakeVersion='3.8.1'; iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-cmake.ps1'))"


* from a powershell terminal open as administrator: ::

    Set-ExecutionPolicy Unrestricted
    $cmakeVersion="3.8.1"
    iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-cmake.ps1'))

.. note::

    - CMake is **NOT** added to the ``PATH``
    - setting ``$cmakeVersion`` to "X.Y.Z" before executing the script allows to select a specific CMake version.
    - By default, install CMake 3.7.1 in directory ``C:\cmake-3.7.1``


``install-git.ps1``
^^^^^^^^^^^^^^^^^^^

Install Git 2.11.0 (including Git Bash) on the system.

* from a windows command terminal open as administrator ::

    @powershell -ExecutionPolicy Unrestricted "iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-git.ps1'))"


* from a powershell terminal open as administrator: ::

    Set-ExecutionPolicy Unrestricted
    iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-git.ps1'))


.. note::

    - Git executables are added to the ``PATH``


``install-ninja.ps1``
^^^^^^^^^^^^^^^^^^^^^

Install ninja executable v1.7.2 into ``C:\ninja-1.7.2``.

* from a windows command terminal open as administrator ::

    @powershell -ExecutionPolicy Unrestricted "iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-ninja.ps1'))"


* from a powershell terminal open as administrator: ::

    Set-ExecutionPolicy Unrestricted
    iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-ninja.ps1'))


.. note::

    - ninja executable is **NOT** added to the ``PATH``


``install-nsis.ps1``
^^^^^^^^^^^^^^^^^^^^

Install NSIS 3.01 on the system.

* from a windows command terminal open as administrator ::

    @powershell -ExecutionPolicy Unrestricted "iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-nsis.ps1'))"


* from a powershell terminal open as administrator: ::

    Set-ExecutionPolicy Unrestricted
    iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-nsis.ps1'))


.. note::

    - nsis executable is added to the ``PATH``


``install-python.ps1``
^^^^^^^^^^^^^^^^^^^^^^

Install Python 2.7.12, 3.3.5, 3.4.4, 3.5.3 and 3.6.1 (32 and 64-bit) along with pip and virtualenv
in the following directories: ::

    C:\Python27-x64
    C:\Python27-x86

    C:\Python33-x64
    C:\Python33-x86

    C:\Python34-x64
    C:\Python34-x86

    C:\Python35-x64
    C:\Python35-x86

    C:\Python36-x64
    C:\Python36-x86


.. note::
    - python interpreter is **NOT** added to the ``PATH``
    - setting ``$pythonVersion`` to either "2.7", "3.3", "3.4", "3.5" or "3.6" before executing the script allows
      to install a specific version. By default, all are installed.
    - setting ``$pythonArch`` to either "86" or "64" before executing the script allows
      to install python for specific architecture. By default, both are installed.
    - setting ``$pythonPrependPath`` to 1 will add install and Scripts directories the PATH and .PY to PATHEXT. This
      variable should be set only if ``$pythonVersion`` and ``$pythonArch`` are set. By default, the value is 0.

.. warning::
    - The downloaded versions of python ``3.3`` and ``3.4`` are **NOT** the latest version including security patches.
      If running in a production environment (e.g webserver), these versions should be built from source.

``install-python-27-x64.ps1``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Install Python 2.7 64-bit and update the PATH.

* from a windows command terminal open as administrator ::

    @powershell -ExecutionPolicy Unrestricted "iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-python-27-x64.ps1'))"


* from a powershell terminal open as administrator: ::

    Set-ExecutionPolicy Unrestricted
    iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-python-27-x64.ps1'))


This is equivalent to: ::

    Set-ExecutionPolicy Unrestricted
    $pythonVersion = "2.7"
    $pythonArch = "64"
    $pythonPrependPath = "1"
    iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-python.ps1'))

.. note::

    - ``C:\Python27-x64`` and ``C:\Python27-x64\Scripts`` are prepended to the ``PATH``


``install-python-36-x64.ps1``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Install Python 3.6 64-bit and update the PATH.

* from a windows command terminal open as administrator ::

    @powershell -ExecutionPolicy Unrestricted "iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-python-36-x64.ps1'))"


* from a powershell terminal open as administrator: ::

    Set-ExecutionPolicy Unrestricted
    iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-python-36-x64.ps1'))


This is equivalent to: ::

    Set-ExecutionPolicy Unrestricted
    $pythonVersion = "3.6"
    $pythonArch = "64"
    $pythonPrependPath = "1"
    iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-python.ps1'))

.. note::

    - ``C:\Python36-x64`` and ``C:\Python36-x64\Scripts`` are prepended to the ``PATH``


``install-svn.ps1``
^^^^^^^^^^^^^^^^^^^^

Install `Slik SVN <https://sliksvn.com/download/>`_ 1.9.5 in the following directory: ::

    C:\SlikSvn


* from a windows command terminal open as administrator ::

    @powershell -ExecutionPolicy Unrestricted "iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-svn.ps1'))"


* from a powershell terminal open as administrator: ::

    Set-ExecutionPolicy Unrestricted
    iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-svn.ps1'))


.. note::

    - svn executable is added to the ``PATH``


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