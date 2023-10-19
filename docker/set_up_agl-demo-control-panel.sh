#!/bin/bash

# Disable the package proxy.
export http_proxy=""
export https_proxy=""

# Clone AGL Demo Control Panel
cd /opt
http_proxy="" https_proxy="" git clone "https://gerrit.automotivelinux.org/gerrit/src/agl-demo-control-panel"
cd agl-demo-control-panel

# We do not need to install all the requirements.
cp requirements.txt requirements_small.txt
sed -i 's/pyqt5/#pyqt5/g' requirements_small.txt
cat requirements_small.txt
pip3 install --break-system-packages -r requirements_small.txt
pyrcc5 assets/res.qrc -o res_rc.py