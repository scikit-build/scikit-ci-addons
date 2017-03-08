Import-Module .\install-utils.ps1

$downloadDir = "C:/Downloads"
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
