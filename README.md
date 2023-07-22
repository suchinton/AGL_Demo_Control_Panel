# AGL_Demo_Control_Panel

A PyQt5 application to simulate CAN Bus signals using Kuksa.val for the AGL Demo platform. This application is to be used in parallel to the relevant AGL Images or any application that subscribes to VSS signals using [Kuksa.val-server](https://github.com/eclipse/kuksa.val/tree/master/kuksa-val-server) or [Kuksa-databroker](https://github.com/eclipse/kuksa.val/tree/master/kuksa_databroker).

## # Installation

Clone the repository
```bash
git clone https://github.com/suchinton/AGL_Demo_Control_Panel.git && cd ./AGL_Demo_Control_Panel
```
Install the Python dependencies by running
```
pip install -r requirements.txt
```


## # Usage

First, we run the kuksa-val-server on the machine, you can also run the [docker image](https://github.com/eclipse/kuksa.val/tree/master/kuksa-val-server#quick-start) for the same. 

### 1. Running the Docker Image for Kuksa-val-server:

By default, the server runs on localhost, so the settings mentioned below can be used,

```
#--- Settings for AGL Demo Control Panel ---#

IP Address: localhost
Insecure Mode: False (Unchecked)
```

### 2. AGL Image

If you are using an AGL image (using QEMU/KVM or VirtualBox) to test the application, you need to set up a bridged network to communicate with the server. You can do so by running the [setup_tap_wireless_int.sh](/Scripts/setup_tap_wireless_int.sh) script. The script creates a bridged network `br0`.

```bash
sudo bash AGL_Demo_Control_Panel/Scripts/setup_tap_wireless_int.sh
```


#### Start the QEMU instance with elevated privileges with these arguments,

```bash
sudo qemu-system-x86_64 ... netdev=net0, -netdev bridge, br=br0, id=net0

## for example ##

sudo qemu-system-x86_64 -device virtio-net-pci,netdev=net0,mac=52:54:00:12:35:02 -netdev bridge,br=br0,id=net0 -drive file=agl-cluster-demo-platform-flutter-qemux86-64.ext4,if=virtio,format=raw -usb -usbdevice tablet -device virtio-rng-pci -snapshot -vga virtio -soundhw hda -machine q35 -cpu kvm64 -cpu qemu64,+ssse3,+sse4.1,+sse4.2,+popcnt -enable-kvm -m 2048 -serial mon:vc -serial mon:stdio -serial null -kernel bzImage -append 'root=/dev/vda rw console=tty0 mem=2048M ip=dhcp oprofile.timer=1 console=ttyS0,115200n8 verbose fstab=no'
```
_Note_: Make sure to update the `file=` argument accordingly.


Run the server in AGL with the following commands,

```bash
kuksa-val-server --address 0.0.0.0 --insecure
```


## Running the `AGL_Demo_Control_Panel`

```bash
cd AGL_Demo_Control_Panel
python -u main.py
```

Once the main window is visible, we go to the settings page

1. Start Client
2. Enter IP address and JWT token path _(Use default values if running kuksa-val-server locally)_
3. Reconnect
4. Refresh Status
    - Red: Couldn't find the server at the specified address
    - Yellow: Faulty settings
    - Green: Connected

## # Testing Against AGL Image on RPi 4

 The `AGL_Demo_Control_Panel` can be tested against the [IC application](https://github.com/aakash-s45/ic) by running the `agl-cluster-demo-platform-flutter` image on a Raspberry Pi 4 

### Building for RPi 4

For building the `agl-cluster-demo-platform-flutter` image for the Raspberry Pi 4 I followed the following steps after setting up my [build environment](https://docs.automotivelinux.org/en/master/#01_Getting_Started/02_Building_AGL_Image/03_Downloading_AGL_Software/).

```bash
source meta-agl/scripts/aglsetup.sh -f \
-m raspberrypi4 -b build-flutter-cluster agl-demo agl-devel

source agl-init-build-env

bitbake agl-cluster-demo-platform-flutter
```

### Flashing Image to SD Card

Simply use the raspberry [Pi Imager Tool](https://www.raspberrypi.com/software/) to flash the custom image. You can also follow AGL's official documentation for the same. 

### Connecting to the Pi using Ethernet

Since the IC Flutter demo app does not provide a GUI method to find the IP address of the Pi, and also does not connect to the WiFi by default, We can enable communication using a LAN cable.

To enable the Ethernet port to find the Pi on local network, the following steps can be taken in the Gnome Settings Panel, similar settings should be available in other network configuration tools.

- Settings -> Network -> Wired ->  IPv4
- IPv4 Method -> Shared to other computers

```bash
# Find IP addr of the ethernet
ip address show eno1
ping <ip-address-for-eno1>

# Resolve all available IP addresses on network, 
# recommend turning off WiFi

arp -a

ssh root@<ip-address-raspberrypi>
```

After successfully `ssh`-ing into the session, we kill the existing `kuksa` service (since it runs on localhost) and restart `kuksa-val-server` on special ip address `0.0.0.0`.

```bash
pkill kuksa
kuksa-val-server --address 0.0.0.0 --insecure 

# optional flag "--log-level VERBOSE"
```

_Note_: Make sure that IP address entered is that of the PI4, and make sure to check `Insecure Mode` before connecting.

## # Demo Video

https://github.com/suchinton/AGL_Demo_Control_Panel/assets/75079303/b1d08461-f39b-42d4-97d8-ed7307df1fa2

## # Supported Applications

- [IC](https://github.com/aakash-s45/ic): Instrument Cluster for AGL flutter build
- 🚧 **(WIP)** [HVAC_dashboard](https://github.com/hritik-chouhan/HVAC_dashboard): A Flutter-based HVAC application made for AGL IVI dashboard
- more to come!