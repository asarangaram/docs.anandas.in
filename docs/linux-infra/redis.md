---
title: Radis (REmote DIctionary Server)
weight: 117000
date: 2023-06-21
---

# Radis (`REmote DIctionary Server`)

__"Redis" (/ˈrɛd-ɪs/) is pronounced like the word "red" plus the word "kiss" without the "k"__

Redis is an open-source (BSD licensed), in-memory data structure store. You can use it as a mem-cached alternative to store simple key-value pairs. Moreover, you can use it as a NoSQL database, or even a message broker with the Pub-Sub pattern.

Some facts gathered:
* Data served from memory, disk used for storage
    * Redis can handle up to 2^32 keys, and was tested in practice to handle at least 250 million keys per instance. Every hash, list, set, and sorted set, can hold 2^32 elements. The limit is likely the available memory in the system.
    * 1 Million small Keys -> String Value pairs use ~ 85 MB
* 

## Install Redis

```bash
sudo apt-get install redis-server -y 
sudo systemctl enable redis-server.service

# Manage with systemctl
sudo systemctl start redis-server.service
sudo systemctl stop redis-server.service
sudo systemctl restart redis-server.service

```
> The following NEW packages will be installed:
    >  libjemalloc2 liblua5.1-0 liblzf1 lua-bitop lua-cjson redis-server redis-tools

## Configure
Changes to be done as given in [^1]

### on config file
Edit `/etc/redis/redis.conf`. 
```bash
$ sudo diff  /etc/redis/redis.conf /etc/redis/redis.conf.default.20230621
861d860
< maxmemory 128mb
893d891
< maxmemory-policy allkeys-lru
```
### System level changes
```bbash
$ sudo tail /var/log/redis/redis-server.log
# to remove warning "# WARNING overcommit_memory is set to 0! Background save may fail under low memory condition. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect." 

$ echo 'vm.overcommit_memory = 1' | sudo tee -a /etc/sysctl.conf > /dev/null
$ sudo sysctl -p
$ sudo sysctl vm.overcommit_memory=1
$ sudo sysctl -p

# to remove warning "WARNING you have Transparent Huge Pages (THP) support enabled in your kernel. This will create latency and memory usage issues with Redis. To fix this issue run the command 'echo never > /sys/kernel/mm/transparent_hugepage/enabled' as root, and add it to your /etc/rc.local in order to retain the setting after a reboot. Redis must be restarted after THP is disabled."

$  sudo vi /etc/rc.local
# add content as below
$  sudo chown root:root /etc/rc.local
$  sudo chmod 770 /etc/rc.local
```    
Content for /etc/rc.local
```bash
#!/bin/bash

echo never > /sys/kernel/mm/transparent_hugepage/enabled

systemctl restart redis-server.service

exit 0
```

If encounterred warning about TCP backlog
```bash
$ echo 'net.core.somaxconn = 512' | sudo tee -a /etc/sysctl.conf > /dev/null
$ sudo sysctl -p
```
__REBOOT TO ENSURE ALL THE CHANGES TAKES EFFECT__

## Using radis
### Radis CLI
```bash
$ redis-cli -h localhost
localhost:6379> 
localhost:6379> set testkey testvalue
OK
localhost:6379> get testkey
"testvalue"
localhost:6379> exit
$ 
```

## Something to keep in mind 
### From Config
* In high requests-per-second environments you need a high backlog in order to avoid slow clients connection issues. Note that the Linux kernel will silently truncate it to the value of /proc/sys/net/core/somaxconn so make sure to raise both the value of somaxconn and tcp_max_syn_backlog in order to get the desired effect.
* By default, TLS/SSL is disabled. If required, it need to be configured.
* You can select a different one on a per-connection basis using `SELECT <dbid>` where `dbid` is a number between 0 and `databases-1` . databases is configured in `/etc/redis/redis.conf`
* we may need to configure UFW 
* Some useful FAQ are found in [https://redis.io/docs/getting-started/faq/], few points
    * How can I reduce Redis' overall memory usage? Refer  [Memory Optimization page](https://redis.io/topics/memory-optimization).
    * To maximize CPU usage you can start multiple instances of Redis in the same box and treat them as different servers
    * 

## References 

[^1]:  [Install and Configure Redis on Ubuntu 20.04](https://www.vultr.com/docs/install-and-configure-redis-on-ubuntu-20-04)
