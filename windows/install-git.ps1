trap { Write-Error $_; Exit 1 }

$downloadDir = "C:/Downloads"
New-Item -ItemType Directory -Force -Path $downloadDir

if (![System.IO.File]::Exists("$downloadDir\install-utils.ps1")) {
  Write-Host "Download install-utils.ps1"
  $url = "https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-utils.ps1"
  (new-object net.webclient).DownloadFile($url, "$downloadDir\install-utils.ps1")
}
Import-Module "$downloadDir\install-utils.ps1" -Force

$version = "2.11.0"
$archiveName = "Git-$version-64-bit.exe"

Download-URL "https://github.com/git-for-windows/git/releases/download/v$version.windows.1/$archiveName" $downloadDir

$installer = Join-Path $downloadDir $archiveName
Write-Host "Installing $installer"

Start-Process $installer -ArgumentList "/SP- /NORESTART /SUPPRESSMSGBOXES /SILENT /SAVEINF=`"$downloadDir\git-settings.txt`" /LOG=`"$downloadDir\git-installer.log`"" -NoNewWindow -PassThru -Wait
