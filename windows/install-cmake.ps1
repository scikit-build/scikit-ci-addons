Import-Module .\install-utils.ps1

$downloadDir = "C:/Downloads"

#$version = "3.5.2"
#$arch = "win32-x86"
$version = "3.7.1"
$arch = "win64-x64"

$installDir = "C:/cmake-$version"
$major_minor = $version.Split(".")[0..1] -join "."

$archiveName = "cmake-$version-$arch"

if (![System.IO.Directory]::Exists($installDir)) {

  Download-URL "https://cmake.org/files/v$major_minor/$archiveName.zip" $downloadDir

  Extract-Zip (Join-Path $downloadDir "$archiveName.zip") "$installDir-tmp"

  $from = Join-Path "$installDir-tmp" $archiveName
  Write-Host "Moving $from to $installDir"
  Move-Item $from $installDir

  Write-Host "Removing $installDir-tmp"
  Remove-Item "$installDir-tmp"
}
