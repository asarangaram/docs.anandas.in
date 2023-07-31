---
title: How to backup SD Card using dd

---

# Using the dd utility to backup and restore the SD cards.

dd is technically a 'convert and copy' utility. As the unix like systems treat every device as file, we can use this utility to copy the storage devices. This utility copies the input file into output file. If we use any device instead of file, the file operations are implemented in their respective drivers.

Let us consider three use cases

1. Backup: Copy a SD card as an image into your hard disk (as a file, usually with extension img)
2. Restore: Restore a SD card from an image stored inyour sd card.

Both can be done using dd utility. For the backup, the input file is the device (sd card) and output file is a normal file in the hard disk. For Restore, it is vice versa.

## What is the file name of the device?
all devices connected to the computer has a entry under /dev.
On a Mac computer, Most of the storage devices will have name 'disk' followed by a number. for example, /dev/disk2 might be a harddisk or a sd card. You may see someother names like /dev/disk2s1, which are usually the logical partition. On a Mac computer, you will also see another file /dev/rdisk2 (assuming you have /dev/disk2). Both are pointing to the same device, but implements different file interface. remember the rdisk as 'raw disk'. This access the divice directly, hence it will be faster.
the disk interace may go through multiple layers, and have reduced performance. There are reasons why it exists, so don't ignore it all together. For our purpose, rdisk is a better choice.

On a Linux computer, they may be named as sd followd by alphabet. sd - remember it as 'storage device', so, the device name might be /dev/sdb or /dev/sdc. (I don't have Linux machine to check if anything equivalent to rdisk exists. If you know, please let me know in the comment.)
IMPORTANT:
THIS IDENTIFICATION OF THE DEVICE MUST BE DONE EVERYTIME, AS IT IS CREATED DINAMICALLY WHEN YOU PLUG IN THE DEVICE.

you may use diskutil to find the devices connected and locate the device you want to backup or the one you want to restore from backup.
diskutil list

- make sure you identify the device you want to backup or restore using the words 'external' and 'physical', the name of the disk and capacity of the disk. Note, selecting wrong device can damage data and may risk data corruption, particularly when you restore.

Let us assume the device we have identified is /dev/rdisk2

## How to choose the file name for the backup:
Its just a file, anyname will do. But having a naming convention and discipline to use it will help to maintain the backups in a long run.
I recommend to use file names with 3 parts, the purpose, date and index and a short description.
For backing up the Raspberry Pi images, I use
<YYYYMMDD>_<Index>\_RPi4_<description>.img
One more aspect you should consider is to have a backup folder. Make a permanent folder in which all your backup files are organized. This will help to avoid duplicate names as well to find out easilty. My recommendation is not to have too many sub folder, for ease of finding, but you have your own judgement.

You may want to have your backup in a cloud, but don't write directly into the cloud drive, it will slow down as the interface
Create a backup in the local harddisk (in a folder not connected to any cloud services), then rclone/ sync to your cloud storage.

Always refer the file with its absolute name, so that you don't need to worry about present working directory.

Let us assume, we want to use the file ~/Backups/<YYYYMMDD>_<Index>\_RPi4_<description>.img

## Options for dd
dd utility can access the file in blocks, the block size can play a bigger role in the time to backup or restore.
the switch is 'bs'. bs=32M fetches 32M Bytes if data every time and repeats till the entire file/device is copied.
If you want to copy with more reliability, you must use a smaller size, and increasing the size will speed up copying, but may not be reliable.

It depends on the class of the SD card, how old it is etc... It might also have impact on the memory usage while copying.
It seems like, we really need to expreiment to choose the correct block size for our device (Any one knows the better rule to choose the bs?)

I would suggest to start with high, 32M and reduce it if it fails.

## Commands to backup and Restore:

Now that we have found the device and decided on the file, use the following command:

### To back up:
sudo dd bs=32m if=/dev/rdisk2 of=~/Backups/<YYYYMMDD>_<Index>\_RPi4_<description>.img
### To restore,
first unmount the device
diskutil unmountDisk disk2
sudo dd bs=32m if=~/Backups/<YYYYMMDD>_<Index>\_RPi4_<description>.img of=/dev/rdisk2

## References:

https://unix.stackexchange.com/questions/189030/why-specify-block-size-when-copying-devices-of-a-finite-size
https://www.anegron.site/2020/06/19/how-to-backup-your-raspberry-pi-sd-card-on-macos/
