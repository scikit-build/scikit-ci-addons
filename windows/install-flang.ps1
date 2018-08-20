trap { Write-Error $_; Exit 1 }

$CONDA_ROOT="C:\Miniconda3"

if(!(Test-Path -Path $CONDA_ROOT )){
  throw "Creating 'flang-env' environment and installing 'flang' requires $CONDA_ROOT"
}
$env:path = "$CONDA_ROOT;$CONDA_ROOT\Scripts;$env:path"
conda config --set show_channel_urls yes
conda config --prepend channels conda-forge
conda create -q -y -n flang-env flang