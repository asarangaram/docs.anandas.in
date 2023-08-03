## `fdisk`

`fdisk` stands for "fixed disk" or "format disk."

The purpose of `fdisk` is to create, delete, resize, and manage disk partitions on a storage device such as a hard drive or solid-state drive.

=== List

   To list all detected hard disks: 
```bash
fdisk -l | grep '^Disk'
```
  
  
  
  



Step #1 : Partition the new disk using fdisk command 

Following command will 

\# 

Output: 

Disk /dev/sda: 251.0 GB, 251000193024 bytes   
Disk /dev/sdb: 251.0 GB, 251000193024 bytes 

A device name refers to the entire hard disk. For more information see [Linux partition naming convention and IDE drive mappings](http://safari-reader://www.cyberciti.biz/faq/linux-partition-naming-convention-and-ide-drive-mappings/). 

To partition the disk – /dev/sdb, enter: 

\# fdisk /dev/sdb 

The basic fdisk commands you need are: 

* m – print help 
    
* p – print the partition table  
    
* n – create a new partition 
    
* d – delete a partition 
    
* q – quit without saving changes 
    
* w – write the new partition table and exit 
    

Step#2 : Format the new disk using mkfs.ext3 command 

To format Linux partitions using ext2fs on the new disk: 

\# mkfs.ext4 /dev/sdb1 

Step#3 : Mount the new disk using mount command 

First create a mount point /disk1 and use mount command to mount /dev/sdb1, enter: 

\# mkdir /disk1 

\# mount /dev/sdb1 /disk1 

\# df -H 

Step#4 : Update /etc/fstab file 

Open /etc/fstab file, enter: 

\# vi /etc/fstab 

Append as follows: 

/dev/sdb1               /disk1           ext3    defaults        1 2 

Save and close the file. 

Task: Label the partition 

You can label the partition using e2label. For example, if you want to label the new partition /backup, enter 

\# e2label /dev/sdb1 /backup 

You can use label name instead of partition name to mount disk using /etc/fstab: 

LABEL=/backup /disk1 ext3 defaults 1 2  

LABEL=/www /mnt/www ext4 defaults 1 2