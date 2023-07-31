---
title: Setup Raspberry Pi
weight: 310000
---
# Setup RPi
## Hardware Required

1. Raspberry Pi 4B
2. power Adapter
3. LAN Cable

## Installing Ubuntu

- Burn Ubuntu 20.04 using Raspberry Pi Imager on a 16GB Micro SD card

- Insert the Micro SD Card into RaspBerry Pi, and LAN port into router.

- Identify the IP address from the router or use an IP scanner to find the IP address.

- Login to Ubuntu from Terminal using the IP address

```bash
    ssh ubuntu@192.168.1.27
    password: ubuntu
```

- On the first run, you need to change the password. Remember the new password. The system will automatically log out once the password is changed.
- Login again with new password

```bash
    ssh ubuntu@192.168.1.27
    password: <password>
```

- Update OS

```bash
    sudo apt update
    sudo apt upgrade
```

- Install utilities

```bash
    sudo apt install net-tools
    sudo apt  install tree
    sudo apt install unzip
    sudo apt install elinks
```

- ffmpeg and imagemagick

These packages are useful to deal with media.

```bash
    sudo apt install exif ffmpeg imagemagick
```

Now the system is ready for further installations.

## Network related

### Setup Web Server

```bash
sudo apt install apache2
```

This installs the apache webserver and also starts the service. you may open [http://192.168.1.27] from the web browser to confirm this. This will display a default page.

We still need to move the document root folder to the storage mounted in /data, which we shall do it later. This is sufficient to proceed further.

To check the status of apache running, run the following

```bash
sudo apache2ctl start
sudo apache2ctl status

or

sudo systemctl status apache2.service -l --no-pager
```

To restart the apache service

```bash
    sudo service apache2 restart
```

Whenever you edit /etc/apache2/apache2.conf, check the syntax by running

```bash
sudo apachectl configtest
```

To list down the modules enabled in apache,

```bash
apache2ctl -M
```

### Wireless access point

Now we are going to configure the RPi as an access point, into which we can connect other devices.

Install network-manager and check the status of the network devices using network manager command line interface (nmcli)

```bash
    $ sudo apt install network-manager
    $ nmcli d
    DEVICE         TYPE      STATE         CONNECTION
    wlan0          wifi      disconnected  --
    eth0           ethernet  unmanaged     --
    lo             loopback  unmanaged     --
    p2p-dev-wlan0  wifi-p2p  unmanaged     --
```

We are connected through LAN. We shall create an Access point on wlan0. Run the following command. [^1]

```bash
    $ sudo nmcli con add type wifi ifname wlan0 con-name Hotspot autoconnect yes ssid rpi_internet
    $ sudo nmcli con modify Hotspot 802-11-wireless.mode ap 802-11-wireless.band a ipv4.method shared
    $ sudo nmcli con modify Hotspot wifi-sec.key-mgmt wpa-psk
    $ sudo nmcli con modify Hotspot wifi-sec.psk "veryveryhardpassword1234"
    $ sudo nmcli con up Hotspot
    Connection successfully activated ....
```

Change the ssid and password as per your preference

Now, we can connect to the new network and browse the internet too. Internet through LAN is shared with the WiFi devices.

The connection file is stored in /etc/NetworkManager/system-connections/Hotspot.nmconnection.

**Recommendation**: Restart once to confirm that the access point is working
After booting, if the Access point is not up, we can enable it either by

```bash
sudo nmcli con up Hotspot
```

or by

```bash
UUID=$(grep uuid /etc/NetworkManager/system-connections/Hotspot | cut -d= -f2)
nmcli con up uuid $UUID
```

### DNS

At this point, you should be able to connect to the WiFi network and browse internet. We want to have a intranet that can be accessed with domain name, instead of the IP address. So, we need to work little more on DNS

We need to change the internal IP of the RPi as well the IP it assigned to clients by changing the dhcp settings. [^2]

Edit the file /etc/NetworkManager/system-connections/Hotspot.nmconnection to include the following line

```abc
[ipv4]
dns-search=
method=shared
address1=192.168.125.1/24,192.168.125.1
```

now restart the network manager

```bash
sudo service network-manager restart
```

you should be able to browse to connect any device, browse the internet. you may also browse to [http://192.168.125.1] and see the apache default page.

Let us name the device as 'ubuntu' by editing /etc/hostname

edit /etc/hosts and add the following[^3]. We may add more subdomains later.

```text
127.0.0.1 www.ubuntu.local
127.0.0.1 photos.ubuntu.local
127.0.0.1 listen.ubuntu.local
```

The Network manager runs its own dnsmasq, which we need to configure to redirect the traffic to .local domain from the WiFi clients.[^4]
create a file /etc/NetworkManager/dnsmasq-shared.d/hosts.conf and add the following line.

```http
address=/.local/192.168.125.1
```

Now, you can access from the browser with any of the following, all redirect to the default apachie page.

```http
http://www.ubuntu.local
http://photos.ubuntu.local
http://listen.ubuntu.local
```

### PHP

```bash
    sudo apt install php
    sudo apt install composer
```

To list down the php modules, use the following command.

```bash
    php -m
```

Check if the following modules are present, if not install them using apt.

```bash
sudo apt install php7.4-common
sudo apt install php7.4-bcmath
sudo apt install php7.4-gd
sudo apt install php7.4-json
sudo apt install php7.4-mbstring
sudo apt install php-imagick
sudo apt install php7.4-xml
```

To Test the PHP installation, create a file file /var/www/html/test.php with the following content and browse it through external browser. [http://www.ubuntu.local/test.php]

```php
<?php phpinfo(); ?>
```

### Database

We shall install sqlite3 for data base services. We also need to install its php module.

```bash
    sudo apt install sqlite3
    sudo apt install php-sqlite3
```

---

Now we have everything to start setting up our services.
Remember:

- LAN is used only for updating the software, and data transfer to and from the RPi
- The web pages can still be accessed after removing the LAN cable, and connecting to rpi_internet.

the server name is \*.ubuntu.local

## Storage

The Micro SD card we have used is Not sufficient to store all the data. Hence we shall add a new Harddisk of 1TB to manage the data. Note, This procedure is to setup the Hard disk as a new device. If you already have content in the device, make sure you back it up. All the data will be lost in this step.

- Connect the harddisk into the USB 3.0 port.
- From the SSH terminal, run the following command to identify the device.

```bash
    $ fdisk -l | grep '^Disk'
    ....
    Disk /dev/sda: 931.53 GiB, 1000204883968 bytes, 1953525164 sectors
    Disk model: Hard Drive
    ...
```

From the list, identify the disk, e.g., /dev/sda

### Create Partition

> The basic fdisk commands you need are:
>
> - m – print help
> - p – print the partition table
> - n – create a new partition
> - d – delete a partition
> - q – quit without saving changes
> - w – write the new partition table and exit

- Run,

```bash
    sudo fdisk /dev/sda
```

Use 'd' to delete older partition if any.
Use 'n' to create a new partition. Preferably a single partition.
Use 'w' to write into disk.
Use 'p' to print and identify the partition. e.g., /dev/sda1

### Format the disk

```bash
sudo mkfs.ext3 /dev/sda1
```

This will take sometime to format the disk

### Mount

Mounting the harddisk on a folder is done as below.

```bash
    $ sudo mkdir /data
    $ sudo mount /dev/sda1 /data
    $ df | grep \/data
    /dev/sda1      960385036   74392 911472568   1% /data
    $ sudo chown -R ubuntu /data # this will give permission to the user 'ubuntu' to read and write
```

### Label the device

```bash
    sudo e2label /dev/sda1 data
```

### Add to File System Table (fstab)

Open the file /etc/fstab and add the following line.

```bash
    LABEL=data /data ext3 defaults 0 1
```

This will make sure the device is registered in the file system table and mounted during boot.

**Recommendation**: Restart once to confirm that the auto mount works

**Recommendation**: You may backup the SD card at this point. This backup will save lot of time, if you mess up the service installations in further steps, you may recover the installation from this point.

[^1]: https://gist.github.com/narate/d3f001c97e1c981a59f94cd76f041140#file-create-hotspot-md
[^2]: https://people.freedesktop.org/~lkundrak/nm-docs/nm-settings.html
[^3]: https://debian-handbook.info/browse/stable/sect.hostname-name-service.html
[^4]: https://askubuntu.com/questions/992743/hotspot-with-dnsmasq-to-resolve-local-hosts
[^5]: https://codeburst.io/configuring-a-subdomain-in-apache2-f7a8b316b42c
[^6]: https://www.digitalocean.com/community/tutorials/apache-configuration-error-ah00558-could-not-reliably-determine-the-server-s-fully-qualified-domain-name#setting-a-global-servername-directive
[^7]: https://help.ubuntu.com/community/EnablingUseOfApacheHtaccessFiles
