## Setup network
### Basic tools

```
sudo apt install vim net-tools wireless-tools network-manager iw
```
### Wireless 

```
iwconfig
# assuming **wlx881100802445** as device id
sudo iwlist wlx881100802445 scan | grep ESSID
# Use SSID with password
sudo nmcli dev wifi connect "<SSID>" password "xxxxxxxx" ifname wlx881100802445
nmcli connection show
sudo nmcli connection modify "<SSID>" connection.autoconnect yes
sudo nmcli connection modify "<SSID>" connection.interface-name wlx881100802445
```
### To Test speed
```
curl -s https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py | python3 -
```
 install speedtest-cli (If needed)
 ```
 sudo speedtest-cli --source <local_ip_of_interface>
 ```
### Reconnect
```
nmcli device disconnect wlx881100802445
nmcli device connect wlx881100802445
```
this will work for ethernet too
## Mount disks

* `lsblk` gives the list of disks connected
* `blkid` gives the UUID and label.
* `/etc/fstab` is where the disks are registerred
```
# /dev/nvme1n1: LABEL="data-disk" UUID="a36d3595-ef77-4f2b-96ab-8d1db1caa691" BLOCK_SIZE="4096" TYPE="ext4"
# /dev/sda1: LABEL="backup-disk" UUID="cb9f2f7b-cf68-40fb-b30e-dac9f223a156" BLOCK_SIZE="4096" TYPE="ext4" PARTLABEL="backup-disk" PARTUUID="623244ce-c389-467b-8b4f-a265f1821e27"
/dev/disk/by-uuid/a36d3595-ef77-4f2b-96ab-8d1db1caa691 /disks/nvm_bkup  ext4  defaults,noatime,nodiratime,errors=remount-ro,nodev,nosuid,noexec  0 2
/dev/disk/by-uuid/cb9f2f7b-cf68-40fb-b30e-dac9f223a156 /disks/sata_bkup ext4  defaults,noatime,nodiratime,errors=remount-ro,nodev,nosuid,noexec  0 2
```
* 