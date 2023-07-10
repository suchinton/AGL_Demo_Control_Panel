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

---

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
---

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

---

## # Demo Video

https://github.com/suchinton/AGL_Demo_Control_Panel/assets/75079303/b1d08461-f39b-42d4-97d8-ed7307df1fa2

---

## # Supported Applications

- [IC](https://github.com/aakash-s45/ic): Instrument Cluster for AGL flutter build
- 🚧 **(WIP)** [HVAC_dashboard](https://github.com/hritik-chouhan/HVAC_dashboard): A Flutter-based HVAC application made for AGL IVI dashboard
- more to come!

--- 

## # Troubleshooting

If on the `Navigation` page, the map does not render properly or appears to be black, try the following steps:

1. Uninstall the requirements

```bash
pip uninstall -r requirements.txt
```
2. Uninstall PyQtWebEngine-Qt5
   
```bash
pip uninstall PyQtWebEngine-Qt5
```
3. Remove sandboxing for QtWebEngine

```bash
export QTWEBENGINE_CHROMIUM_FLAGS="--no-sandbox"
```
4. Reinstall python dependencies

```bash
pip install -r requirements.txt
```
