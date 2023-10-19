#!/bin/bash

set -x

cd /opt/agl-demo-control-panel
QT_QPA_PLATFORM="vnc:size=1920x1080" python3 -u main.py