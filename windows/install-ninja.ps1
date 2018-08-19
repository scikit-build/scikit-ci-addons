trap { Write-Error $_; Exit 1 }


$downloadDir = "C:/Downloads"
New-Item -ItemType Directory -Force -Path $downloadDir

if (![System.IO.File]::Exists("$downloadDir\install-utils.ps1")) {
  Write-Host "Download install-utils.ps1"
  $url = "https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-utils.ps1"
  (new-object net.webclient).DownloadFile($url, "$downloadDir\install-utils.ps1")
}
Import-Module .\install-utils.ps1 -Force

$version = "1.7.2"
$archiveName = "ninja-win"
$targetDir = "C:\\ninja-$version"

if ([System.IO.Directory]::Exists($targetDir)) {
  Write-Host "Installing $archiveName.zip into $targetDir"
  Write-Host "-> skipping: existing target directory"
  return
}

Download-File "https://github.com/ninja-build/ninja/releases/download/v$version/$archiveName.zip" "$downloadDir/ninja-$version.zip"

Always-Extract-Zip (Join-Path $downloadDir "ninja-$version.zip") "$targetDir"
