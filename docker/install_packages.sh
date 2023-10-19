#!/bin/bash

# Exit as soon as something fails.
set -e

# The idea behind doing all this in a script is to reduce the final size of the
# docker image, as all this will only generate one layer.

echo "http_proxy is $http_proxy"
echo "https_proxy is $https_proxy"

# Keep the dependency list as short as reasonable
apt-get update
apt-get install --yes \
 bash \
 git \
 locales

# Install AGL Demo Control Panel dependencies
apt-get install --yes \
 python3-pip \
 python3-pyqt5 \
 python3-qtpy \
 pyqt5-dev-tools

# Set bash as default shell
echo "dash dash/sh boolean false" | debconf-set-selections - && dpkg-reconfigure dash

# Set the locale
sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen

apt-get --yes clean
apt-get --yes autoremove
