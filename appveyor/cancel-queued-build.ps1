param([string]$tag_pattern="^latest(-tmp)?$")

trap { Write-Error $_; Exit 1 }

#
# Cancel queued builds with tag matching selected tags.
#

#
# Usage:
#
#  cancel-queued-build.ps1 [-tag_pattern "^latest(-tmp)?$"]
#

#
# Description:
#
# If there any queued build whose name matches the provided pattern, they
# will be cancelled.
#
# By default, build with tag matching `^latest(-tmp)?$` are cancelled.
#
# The following environment variables are expected to be defined:
#
#  * APPVEYOR_ACCOUNT_NAME
#  * APPVEYOR_PROJECT_SLUG
#  * APPVEYOR_API_TOKEN
#
# This script was initially created to workaround issue
# See https://github.com/scikit-build/scikit-ci-addons/issues/45
#

$msg = "Cancelling 'queued' AppVeyor build(s) associated with tag matching [$tag_pattern]"
Write-Host ""
Write-Host "$msg"


if ( !$env:APPVEYOR_ACCOUNT_NAME ) {
  throw "'APPVEYOR_ACCOUNT_NAME' environment variable is NOT set"
}

if ( !$env:APPVEYOR_PROJECT_SLUG ) {
  throw "'APPVEYOR_PROJECT_SLUG' environment variable is NOT set"
}

if ( !$env:APPVEYOR_API_TOKEN ) {
  throw "'APPVEYOR_API_TOKEN' environment variable is NOT set"
}

( Invoke-RestMethod https://ci.appveyor.com/api/projects/$env:APPVEYOR_ACCOUNT_NAME/$env:APPVEYOR_PROJECT_SLUG/history?recordsNumber=20 ).builds                                                                             `
  | Where-Object {$_.status -eq "queued" -and ( $_.tag -match $tag_pattern ) }  |
  %{ $_.version }                                                             |
  %{
    $msg = "Found build version $_"
    Write-Host "  $msg"
    $url = "https://ci.appveyor.com/api/builds/$env:APPVEYOR_ACCOUNT_NAME/$env:APPVEYOR_PROJECT_SLUG/$_"
    Invoke-RestMethod $url   `
      -Method Delete         `
      -Headers @{"Authorization" = "Bearer $env:APPVEYOR_API_TOKEN"};
    Write-Host "  $msg - cancelled"
  }

Write-Host "done"
