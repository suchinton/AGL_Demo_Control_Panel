# Docker container for AGL Demo Control Panel

## Building

In this directory run:

```bash
$ docker build \
 --pull -t agl-demo-control-panel .
```
Or, if you have an apt cacher like squid-deb-proxy:

```bash
$ docker build \
 --build-arg httpproxy="http://<proxy IP>:<proxy port>/" \
 --build-arg httpsproxy="https://<proxy IP>:<proxy port>/" \
 --pull -t agl-demo-control-panel .
```

## Running the container

```bash
$ docker run -ti --rm --network host agl-demo-control-panel
```

If you plan to use this frequently do consider adding it as an alias into your ~/.bashrc!

Edit ~/.bashrc and add this line:

```bash
alias docker_agl-demo-control-panel='docker run -ti --rm --network host agl-demo-control-panel'
```

Then source ~/.bashrc or log out and in and simply run:

```bash
$ docker_agl-demo-control-panel
```
