trap { Write-Error $_; Exit 1 }

$downloadDir = "C:/Downloads"
New-Item -ItemType Directory -Force -Path $downloadDir

$scriptName = "install-python.ps1"
if (![System.IO.File]::Exists("$downloadDir\$scriptName")) {
  Write-Host "Download $scriptName"
  $url = "https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/$scriptName"
  (new-object net.webclient).DownloadFile($url, "$downloadDir\$scriptName")
}

$pythonPrependPath = "1"
$pythonVersion = "2.7"
$pythonArch = "64"
Invoke-Expression ".\$scriptName"