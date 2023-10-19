FROM debian:bookworm-slim as base

ENV DEBIAN_FRONTEND=noninteractive

# If you have a running instance of squid-deb-proxy or apt-cacher-ng this will
# allow you to use it an avoid wasting bandwith every time you create an image.
ARG httpproxy
ARG httpsproxy
ENV http_proxy=$httpproxy
ENV https_proxy=$httpproxy

COPY install_packages.sh /tmp
RUN /tmp/install_packages.sh
COPY set_up_agl-demo-control-panel.sh /tmp
RUN /tmp/set_up_agl-demo-control-panel.sh

COPY entrypoint.sh /opt

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Clean proxy variables.
ENV http_proxy=
ENV https_proxy=

# Set the locale
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8

ENTRYPOINT /opt/entrypoint.sh