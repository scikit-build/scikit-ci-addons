#!/usr/bin/env bash

set -e

echo "+ eval \"\$( pyenv init - )\""
eval "$( pyenv init - )"

echo "+ pyenv local \$PYTHONVERSION"
pyenv local $PYTHONVERSION

echo "+ eval \"\$@\""
eval "$@"
