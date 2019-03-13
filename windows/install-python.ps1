trap { Write-Error $_; Exit 1 }

#
# By default, all version of python are installed.
#
# Setting $pythonVersion to "2.7", "3.4", "3.5", "3.6", "3.7" or "3.8" allows to install a specific version
#
# Setting $pythonArch to either "64", "86" or "32" allows to install python for specific architecture.
# Values "86" and "32" correspond to the same architecture.
#
# Setting $pythonPrependPath to 1 will:
# - add install and Scripts directories to the PATH
# - and .PY to PATHEXT.
# The variable should be set only if $pythonVersion and $pythonArch are set.
# By default, the value is 0.
#

$downloadDir = "C:/Downloads"

New-Item -ItemType Directory -Force -Path $downloadDir;

if (![System.IO.File]::Exists("$downloadDir\install-utils.ps1")) {
  Write-Host "Download install-utils.ps1"
  $url = "https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-utils.ps1"
  (new-object net.webclient).DownloadFile($url, "$downloadDir\install-utils.ps1")
}
Import-Module "$downloadDir\install-utils.ps1" -Force

function Get-Python-InstallPath {
param (
  [string]$pythonVersion,  # Version specified as "X.Y"
  [string]$pythonArch      # Arch specified as "86" or "64"
  )
  $suffix = '-32'
  if ($pythonArch.CompareTo('64') -eq 0) {
    $suffix = ''
  }
  $roots = @("HKCU", "HKLM")
  foreach ($root in $roots) {
    $path = "$($root):\Software\Python\PythonCore\$pythonVersion$suffix\InstallPath"
    if (Test-Path -Path $path -PathType Container) {
      $properties = Get-ItemProperty -Path $path
      if ($properties -And (Get-Member -InputObject $properties -Name '(Default)')) {
        $installPath = (Get-ItemProperty -Path $path -Name '(Default)').'(Default)'
        return (Resolve-Path(Join-Path $installPath "\\")).Path
      }
    }
  }
  return ""
}

# Only for Python >= 3.6
function Get-Python-Version {
param (
  [string]$pythonVersion,  # Version specified as "X.Y"
  [string]$pythonArch      # Arch specified as "86", "32" or "64"
  )
  $suffix = '-32'
  if ($pythonArch.CompareTo('64') -eq 0) {
    $suffix = ''
  }
  $roots = @("HKCU", "HKLM")
  foreach ($root in $roots) {
    $path = "$($root):\Software\Python\PythonCore\$pythonVersion$suffix"
    if (Test-Path -Path $path -PathType Container) {
      $properties = Get-ItemProperty -Path $path
      if ($properties -And (Get-Member -InputObject $properties -Name 'Version')) {
        $version = (Get-ItemProperty -Path $path -Name 'Version').'Version'
        return $version
      }
    }
  }
  return ""
}

function Get-Python-Executable-Version{
param (
  [string]$pythonInstallPath  # Path to python install directory
  )
  $interpreter = Join-Path $pythonInstallPath "python.exe"

  # See https://stackoverflow.com/a/8762068/1539918 and https://stackoverflow.com/a/11549817/1539918
  $pinfo = New-Object System.Diagnostics.ProcessStartInfo
  $pinfo.FileName = "$interpreter"
  $pinfo.Arguments = "-c `"import sys;sys.stdout.write('%s.%s.%s' % sys.version_info[0:3])`""
  $pinfo.UseShellExecute = $false
  $pinfo.CreateNoWindow = $true
  $pinfo.RedirectStandardError = $true
  $pinfo.RedirectStandardOutput = $true
  $process = New-Object System.Diagnostics.Process
  $process.StartInfo = $pinfo
  $process.Start() | Out-Null
  $process.WaitForExit()
  $pythonVersion = $process.StandardOutput.ReadToEnd()

  return $pythonVersion
}

function Install-Python {
param (
  [string]$installerPath,
  [string]$targetDir
  )

  Write-Host "Installing $installerPath into $targetDir"
  $interpreter = Join-Path $targetDir "python.exe"
  if ([System.IO.Directory]::Exists($interpreter)) {
    Write-Host "-> skipping: found $interpreter"
    return
  }
  if (![System.IO.Directory]::Exists($targetDir)) {
    [System.IO.Directory]::CreateDirectory($targetDir)
  }
  #
  # See https://docs.python.org/3.6/using/windows.html#installing-without-ui
  #
  Start-Process $installerPath -ArgumentList "TargetDir=$targetDir DefaultAllUsersTargetDir=$targetDir InstallAllUsers=1 Include_launcher=0 PrependPath=$pythonPrependPath Shortcuts=0 /passive" -NoNewWindow -Wait
}

function Install-Python-27-34 {
param (
  [string]$targetDir,
  [string]$installerName,
  [string]$downloadURL
  )
  Download-URL $downloadURL $downloadDir
  Always-Install-MSI $installerName $downloadDir $targetDir
  Install-Pip $targetDir $downloadDir
  Pip-Install $targetDir 'virtualenv'
  if ($pythonPrependPath -eq 1) {
    Write-Host "Pre-pending '$targetDir;$targetDir\Scripts\' to PATH"
    [Environment]::SetEnvironmentVariable("Path", "$targetDir;$targetDir\Scripts\;$env:Path", "Machine")
  }
}

# See https://pip.pypa.io/en/stable/installing/
function Install-Pip {
param (
  [string]$pythonDir,
  [string]$downloadDir
  )
  # Workaround https://github.com/scikit-build/scikit-ci-addons/issues/54
  # Download-URL 'https://bootstrap.pypa.io/get-pip.py' $downloadDir
  $url = 'https://gist.githubusercontent.com/jcfr/db7347e8708b9f32d45ab36125fad6d3/raw/8478d43e8f774c9602c78f9e81902792f923dd5c/get-pip.py'
  Download-URL $url $downloadDir
  
  $get_pip_script = Join-Path $downloadDir "get-pip.py"

  $interpreter = Join-Path $pythonDir "python.exe"
  Write-Host "Installing pip using $interpreter"

  Start-Process $interpreter -ArgumentList "`"$get_pip_script`"" -NoNewWindow -Wait
}

function Pip-Install {
param (
  [string]$pythonDir,
  [string]$package
  )

  $interpreter = Join-Path $pythonDir "python.exe"
  Write-Host "Installing $package using pip with $interpreter"

  Start-Process $interpreter -ArgumentList "-m pip install `"$package`"" -NoNewWindow -Wait
}

if ($pythonVersion) {
  $pythonVersion = [string]::Join("", $pythonVersion.Split("."), 0, 2)
  Write-Host "Installing Python version $pythonVersion"
}

if ($pythonArch) {
  if(!($pythonArch -match "^(64|86|32)$")){
    throw "'pythonArch' variable incorrectly set to [$pythonArch]. Hint: '64', '86' or '32' value is expected."
  }
  Write-Host "Installing Python for architecture x$pythonArch"
}

if (!$pythonVersion -Or !$pythonArch) {
  if ($pythonPrependPath) {
    throw "'pythonPrependPath' variable should explicitly be set when both 'pythonVersion' and 'pythonArch' are set"
  }
}
if (!$pythonPrependPath) {
  $pythonPrependPath = 0
  Write-Host "Defaulting 'pythonPrependPath' variable to 0."
}

if(!($pythonPrependPath -match "^(0|1)$")){
  throw "'$pythonPrependPath' variable incorrectly set to [$pythonPrependPath]. Hint: '0' or '1' value is expected."
}

#
# Python 2.7 and 3.4
#
# * 3.4.4 is last 3.4.x version released in binary form
#
$exeVersions = @("2.7.15", "3.4.4")
foreach ($version in $exeVersions) {

  $split = $version.Split(".")
  $majorMinor = [string]::Join("", $split, 0, 2)
  $majorMinorDot = [string]::Join(".", $split, 0, 2)

  if($pythonVersion -And ! $pythonVersion.CompareTo($majorMinor) -eq 0) {
    Write-Host "Skipping $majorMinor"
    continue
  }

  #
  # 64-bit
  #
  if (!$pythonArch -Or $pythonArch.CompareTo("64") -eq 0) {
    $targetDir = "C:\Python$($majorMinor)-x64"
    $installerName = "python-$($version).amd64.msi"
    $downloadURL = "https://www.python.org/ftp/python/$($version)/$($installerName)"
    Install-Python-27-34 $targetDir $installerName $downloadURL
  }

  #
  # 32-bit
  #
  if (!$pythonArch -Or $pythonArch.CompareTo("86") -eq 0 -Or $pythonArch.CompareTo("32") -eq 0) {
    $targetDir = "C:\Python$($majorMinor)-x86"
    $installerName = "python-$($version).msi"
    $downloadURL = "https://www.python.org/ftp/python/$($version)/$($installerName)"
    Install-Python-27-34 $targetDir $installerName $downloadURL
  }
}

#
# Python 3.5, 3.6, 3.7 and 3.8
#
# * 3.5.4 is last 3.5.x version released in binary form
#
$exeVersions = @("3.5.4", "3.6.8", "3.7.2", "3.8.0a2")
foreach ($version in $exeVersions) {

  $split = $version.Split(".")
  $majorMinor = [string]::Join("", $split, 0, 2)
  $majorMinorDot = [string]::Join(".", $split, 0, 2)
  $xyzVersion = [regex]::Replace($version, "(\d+\.\d+\.\d+).+", '$1')

  if($pythonVersion -And ! $pythonVersion.CompareTo($majorMinor) -eq 0) {
    Write-Host "Skipping $majorMinor"
    continue
  }

  #
  # 64-bit
  #
  if (!$pythonArch -Or $pythonArch.CompareTo("64") -eq 0) {

    Download-URL "https://www.python.org/ftp/python/$($xyzVersion)/python-$($version)-amd64.exe" $downloadDir

    $pythonInstallPath = Get-Python-InstallPath $majorMinorDot "64"
    $targetInstallPath = "C:\Python$($majorMinor)-x64\"
    $installerPath = Join-Path $downloadDir "python-$($version)-amd64.exe"
    $unInstallerPath = $installerPath

    if (!$pythonInstallPath.CompareTo($targetInstallPath) -eq 0) {
      if ($pythonInstallPath) {
        $installedPythonVersion = Get-Python-Version $majorMinorDot "64"
        if ($installedPythonVersion) {
          Download-URL "https://www.python.org/ftp/python/$installedPythonVersion/python-$installedPythonVersion-amd64.exe" $downloadDir
          $unInstallerPath = Join-Path $downloadDir "python-$installedPythonVersion-amd64.exe"
        }

        Write-Host "Found a python installation in a different directory [$pythonInstallPath] - Uninstalling"
        Start-Process $unInstallerPath -ArgumentList "/uninstall /passive" -NoNewWindow -Wait

      }
    } elseif ($pythonInstallPath) {
      $installedPythonVersion = Get-Python-Executable-Version $pythonInstallPath
      if (!$installedPythonVersion.CompareTo($version) -eq 0) {
        Download-URL "https://www.python.org/ftp/python/$installedPythonVersion/python-$installedPythonVersion-amd64.exe" $downloadDir
        $unInstallerPath = Join-Path $downloadDir "python-$installedPythonVersion-amd64.exe"

        Write-Host "Updating existing installation [$pythonInstallPath] from $installedPythonVersion to $($version)"
        Start-Process $unInstallerPath -ArgumentList "/uninstall /passive" -NoNewWindow -Wait
        }
    }

    Install-Python $installerPath $targetInstallPath
    Install-Pip $targetInstallPath $downloadDir
    Pip-Install $targetInstallPath 'virtualenv'
  }

  #
  # 32-bit
  #
  if (!$pythonArch -Or $pythonArch.CompareTo("86") -eq 0 -Or $pythonArch.CompareTo("32") -eq 0) {
    Download-URL "https://www.python.org/ftp/python/$($xyzVersion)/python-$($version).exe" $downloadDir

    $pythonInstallPath = Get-Python-InstallPath $majorMinorDot "86"
    $targetInstallPath = "C:\Python$($majorMinor)-x86\"
    $installerPath = Join-Path $downloadDir "python-$($version).exe"
    $unInstallerPath = $installerPath

    if (!$pythonInstallPath.CompareTo($targetInstallPath) -eq 0) {
      if ($pythonInstallPath) {

        $installedPythonVersion = Get-Python-Version $majorMinorDot "86"
        if ($installedPythonVersion) {
          Download-URL "https://www.python.org/ftp/python/$installedPythonVersion/python-$installedPythonVersion.exe" $downloadDir
          $unInstallerPath = Join-Path $downloadDir "python-$installedPythonVersion.exe"
        }

        Write-Host "Found a python installation in a different directory [$pythonInstallPath] - Uninstalling"
        Start-Process $unInstallerPath -ArgumentList "/uninstall /passive" -NoNewWindow -Wait
      }
    } elseif ($pythonInstallPath) {
      $installedPythonVersion = Get-Python-Executable-Version $pythonInstallPath
      if (!$installedPythonVersion.CompareTo($version) -eq 0) {
        Download-URL "https://www.python.org/ftp/python/$installedPythonVersion/python-$installedPythonVersion.exe" $downloadDir
        $unInstallerPath = Join-Path $downloadDir "python-$installedPythonVersion.exe"

        Write-Host "Updating existing installation [$pythonInstallPath] from $installedPythonVersion to $($version)"
        Start-Process $unInstallerPath -ArgumentList "/uninstall /passive" -NoNewWindow -Wait
      }
    }

    Install-Python  $installerPath $targetInstallPath
    Install-Pip $targetInstallPath $downloadDir
    Pip-Install $targetInstallPath 'virtualenv'
  }

}
