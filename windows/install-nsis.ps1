Import-Module .\install-utils.ps1

$downloadDir = "C:/Downloads"

$version = "3.01"
$archiveName = "nsis-$version-setup.exe"

Download-URL "http://downloads.sourceforge.net/project/nsis/NSIS%203/$version/$archiveName" $downloadDir

$installer = Join-Path $downloadDir $archiveName
Start-Process $installer -ArgumentList "/S" -NoNewWindow -Wait

