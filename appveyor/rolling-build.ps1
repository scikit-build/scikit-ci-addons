#
# Cancel on-going build if there is a newer build queued for the same PR
#

#
# Usage:
#
#  rolling-build.ps1
#
#
# If there is a newer build queued for the same PR, cancel this one.
# The AppVeyor 'rollout builds' option is supposed to serve the same
# purpose but it is problematic because it tends to cancel builds pushed
# directly to master instead of just PR builds (or the converse).
# credits: JuliaLang developers.

if (
  $env:APPVEYOR_PULL_REQUEST_NUMBER -and
  $env:APPVEYOR_BUILD_NUMBER -ne (
    (
      Invoke-RestMethod https://ci.appveyor.com/api/projects/$env:APPVEYOR_ACCOUNT_NAME/$env:APPVEYOR_PROJECT_SLUG/history?recordsNumber=50
    ).builds | Where-Object pullRequestId -eq $env:APPVEYOR_PULL_REQUEST_NUMBER
  )[0].buildNumber
) { throw "There are newer queued builds for this pull request, failing early." }