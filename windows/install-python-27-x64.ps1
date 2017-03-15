trap { Write-Error $_; Exit 1 }

$scriptName = "install-python.ps1"
if (![System.IO.File]::Exists(".\$scriptName")) {
  Write-Host "Download $scriptName"
  $url = "https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/$scriptName"
  $cwd = (Get-Item -Path ".\" -Verbose).FullName
  (new-object net.webclient).DownloadFile($url, "$cwd\$scriptName")
}

$pythonPrependPath = "1"
$pythonVersion = "2.7"
$pythonArch = "64"
Invoke-Expression ".\$scriptName"