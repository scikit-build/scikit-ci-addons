trap { Write-Error $_; Exit 1 }

$downloadDir = "C:/Downloads"
New-Item -ItemType Directory -Force -Path $downloadDir

if (![System.IO.File]::Exists("$downloadDir\install-utils.ps1")) {
  Write-Host "Download install-utils.ps1"
  $url = "https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-utils.ps1"
  (new-object net.webclient).DownloadFile($url, "$downloadDir\install-utils.ps1")
}
Import-Module "$downloadDir\install-utils.ps1" -Force

$archiveName = "Miniconda3-latest-Windows-x86_64.exe"

Download-URL "https://repo.continuum.io/miniconda/$archiveName" $downloadDir

$installer = Join-Path $downloadDir $archiveName
Start-Process $installer -ArgumentList "/InstallationType=JustMe /AddToPath=0 /NoRegistry=1 /RegisterPython=0 /S /D=C:\Miniconda3" -NoNewWindow -Wait
