trap { Write-Error $_; Exit 1 }

if (![System.IO.File]::Exists(".\install-utils.ps1")) {
  Write-Host "Download install-utils.ps1"
  $url = "https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-utils.ps1"
  $cwd = (Get-Item -Path ".\" -Verbose).FullName
  (new-object net.webclient).DownloadFile($url, "$cwd\install-utils.ps1")
}
Import-Module .\install-utils.ps1 -Force

$downloadDir = "C:/Downloads"

$archiveName = "Miniconda3-latest-Windows-x86_64.exe"

Download-URL "https://repo.continuum.io/miniconda/$archiveName" $downloadDir

$installer = Join-Path $downloadDir $archiveName
Start-Process $installer -ArgumentList "/InstallationType=JustMe /AddToPath=0 /NoRegistry=1 /RegisterPython=0 /S /D=C:\Miniconda3" -NoNewWindow -Wait
