trap { Write-Error $_; Exit 1 }

if (![System.IO.File]::Exists(".\install-utils.ps1")) {
  Write-Host "Download install-utils.ps1"
  $url = "https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-utils.ps1"
  $cwd = (Get-Item -Path ".\" -Verbose).FullName
  (new-object net.webclient).DownloadFile($url, "$cwd\install-utils.ps1")
}
Import-Module .\install-utils.ps1 -Force

$downloadDir = "C:/Downloads"

$version = "3.01"
$archiveName = "nsis-$version-setup.exe"

Download-URL "http://downloads.sourceforge.net/project/nsis/NSIS%203/$version/$archiveName" $downloadDir

$installer = Join-Path $downloadDir $archiveName
Start-Process $installer -ArgumentList "/S" -NoNewWindow -Wait

