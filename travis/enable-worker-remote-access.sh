#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

case $TRAVIS_OS_NAME in
  linux)
    curl -L https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip -o $SCRIPT_DIR/ngrok.zip
  ;;
  osx)
    curl -f -L -C - -o $SCRIPT_DIR/ngrok.zip https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-darwin-amd64.zip
  ;;
  *)
    echo "TRAVIS_OS_NAME env. variable is not set !"
    exit 1
  ;;
esac

unzip "$SCRIPT_DIR/ngrok.zip"
{
    mkfifo pipe
    echo "Executing nc"
    nc -l -v 8888 <pipe | bash >pipe
    killall -SIGINT ngrok && echo "ngrok terminated"
} &
{
    echo "Executing ngrok"
    ./ngrok authtoken $NGROK_TOKEN
    ./ngrok tcp 8888 --log=stdout --log-level=debug
}
