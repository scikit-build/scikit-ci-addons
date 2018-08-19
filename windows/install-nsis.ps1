trap { Write-Error $_; Exit 1 }

$downloadDir = "C:/Downloads"
New-Item -ItemType Directory -Force -Path $downloadDir

if (![System.IO.File]::Exists("$downloadDir\install-utils.ps1")) {
  Write-Host "Download install-utils.ps1"
  $url = "https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-utils.ps1"
  (new-object net.webclient).DownloadFile($url, "$downloadDir\install-utils.ps1")
}
Import-Module "$downloadDir\install-utils.ps1" -Force

$version = "3.01"
$archiveName = "nsis-$version-setup.exe"

Download-URL "http://downloads.sourceforge.net/project/nsis/NSIS%203/$version/$archiveName" $downloadDir

$installer = Join-Path $downloadDir $archiveName
Start-Process $installer -ArgumentList "/S" -NoNewWindow -Wait

