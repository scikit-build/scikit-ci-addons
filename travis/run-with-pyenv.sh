#!/usr/bin/env bash

set -e

echo "+ eval \"\$( pyenv init - )\""
eval "$( pyenv init - )"

echo "+ pyenv local \$PYTHON_VERSION"
pyenv local $PYTHON_VERSION

echo "+ eval \"\$@\""
eval "$@"
