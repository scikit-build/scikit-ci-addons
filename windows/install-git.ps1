trap { Write-Error $_; Exit 1 }

if (![System.IO.File]::Exists(".\install-utils.ps1")) {
  Write-Host "Download install-utils.ps1"
  $url = "https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-utils.ps1"
  $cwd = (Get-Item -Path ".\" -Verbose).FullName
  (new-object net.webclient).DownloadFile($url, "$cwd\install-utils.ps1")
}
Import-Module .\install-utils.ps1 -Force

$downloadDir = "C:/Downloads"

$version = "2.11.0"
$archiveName = "Git-$version-64-bit.exe"

Download-URL "https://github.com/git-for-windows/git/releases/download/v$version.windows.1/$archiveName" $downloadDir

$installer = Join-Path $downloadDir $archiveName
Write-Host "Installing $installer"

Start-Process $installer -ArgumentList "/SP- /NORESTART /SUPPRESSMSGBOXES /SILENT /SAVEINF=`"$downloadDir\git-settings.txt`" /LOG=`"$downloadDir\git-installer.log`"" -NoNewWindow -PassThru -Wait
