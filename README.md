# AGL_Demo_Control_Panel

A PyQt5 application to simulate CAN Bus signals using Kuksa.val for the AGL Demo platform. This application is to be used in parallel to the relevant AGL Images or any application that subscribe to VSS signals using Kuksa.val server or Kuksa-databroaker.

## # Installation

Clone the repository
```bash
git clone https://github.com/suchinton/AGL_Demo_Control_Panel.git
```
Install the Python dependencies by running
```
pip install req.txt
```

## # Usage

First we run the kuksa-val-server on the machine, you can also run the docker image for the same. 

If you are using an AGL image (using a VM) to test the application, you need to set up a bridged network to communicate with the server. You can do so by running the `setup_tap_wireless_int.sh` script.

```bash
sudo bash AGL_Demo_Control_Panel/Scripts/setup_tap_wireless_int.sh
```

and start the QEMU instance with elevated privileges with these arguments,

```bash
sudo qemu-system-x86_64 -device virtio-net-pci,netdev=net0,mac=52:54:00:12:35:02 -netdev bridge,br=br0,id=net0 -drive file=agl-cluster-demo-platform-flutter-qemux86-64.ext4,if=virtio,format=raw -usb -usbdevice tablet -device virtio-rng-pci -snapshot -vga virtio -soundhw hda -machine q35 -cpu kvm64 -cpu qemu64,+ssse3,+sse4.1,+sse4.2,+popcnt -enable-kvm -m 2048 -serial mon:vc -serial mon:stdio -serial null -kernel bzImage -append 'root=/dev/vda rw console=tty0 mem=2048M ip=dhcp oprofile.timer=1 console=ttyS0,115200n8 verbose fstab=no'
```

_Note_: make sure to update the `file=` argument accordingly.


run the sever with the following commands.

```bash
kuksa-val-server --address 0.0.0.0 --insecure
```

![Demo Video](https://raw.githubusercontent.com/suchinton/blogs/main/images/WPR/Week3/DemoVideo.mp4)

### Running the `AGL_Demo_Control_Panel`

```bash
$ cd AGL_Demo_Control_Panel
$ python -u main.py
```

## # Supported Applications

- [IC](https://github.com/aakash-s45/ic): Instrument Cluster for AGL flutter build
- 🚧 **(WIP)** [HVAC_dashboard](https://github.com/hritik-chouhan/HVAC_dashboard): A Flutter based HVAC application made for AGL IVI dashboard
- more to come!