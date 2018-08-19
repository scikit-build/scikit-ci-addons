trap { Write-Error $_; Exit 1 }

$downloadDir = "C:/Downloads"
New-Item -ItemType Directory -Force -Path $downloadDir

if (![System.IO.File]::Exists("$downloadDir\install-utils.ps1")) {
  Write-Host "Download install-utils.ps1"
  $url = "https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/windows/install-utils.ps1"
  (new-object net.webclient).DownloadFile($url, "$downloadDir\install-utils.ps1")
}
Import-Module "$downloadDir\install-utils.ps1" -Force

if (!$cmakeVersion) {
  $cmakeVersion = "3.7.1"
}

$version = $cmakeVersion

$major = [int]$version.Split(".")[0]
$minor = [int]$version.Split(".")[1]

$arch = "win64-x64"

# win64-x64 archives were introduced with CMake 3.6
if ($major -le 3 -And $minor -lt 6) {
  $arch = "win32-x86"
}

$installDir = "C:/cmake-$version"
$major_minor = "$major.$minor"

$archiveName = "cmake-$version-$arch"

if (![System.IO.Directory]::Exists($installDir)) {

  Download-URL "https://cmake.org/files/v$major_minor/$archiveName.zip" $downloadDir

  Extract-Zip (Join-Path $downloadDir "$archiveName.zip") "$installDir-tmp"

  $from = Join-Path "$installDir-tmp" $archiveName
  Write-Host "Moving $from to $installDir"
  Move-Item $from $installDir

  Write-Host "Removing $installDir-tmp"
  Remove-Item "$installDir-tmp"
} else {
  Write-Host "Skipping installation: Directory [$installDir] already exists"
}
