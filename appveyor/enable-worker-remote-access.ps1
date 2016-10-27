#
# Enable access to the build worker via Remote Desktop
#

#
# Usage:
#
#  enable-worker-remote-access.ps1 [-block|-check_for_block]
#
#
# Calling this script will enable and display the Remote Desktop
# connection details. By default, the connection will be available
# for the length of the build.
#
# Specifying ``-block`` option will ensure the connection remains
# open for at least 60 mins.
#
# Specifying ```-check_for_block`` option will keep the connection
# open only if the environment variable ``BLOCK`` has been set to ``1``.
#

param (
  [switch]$block = $false,
  [switch]$check_for_block = $false
)

$blockRdp = $block;

if ($check_for_block) {
  Write-Host "appveyor: checking BLOCK environment variable" -ForegroundColor Gray
  if ($Env:BLOCK -ceq "1") {
    $blockRdp = $true ;
  }
}

Write-Host "appveyor: blocking enabled: $blockRdp" -ForegroundColor Gray

# Copied from https://www.appveyor.com/docs/how-to/rdp-to-build-worker/
if (!$check_for_block -or ($check_for_block -and $blockRdp)) {
  iex (
    (New-Object Net.Webclient).DownloadString(
      'https://raw.githubusercontent.com/appveyor/ci/master/scripts/enable-rdp.ps1'
    )
  )
}
