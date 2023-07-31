---
title: Nutx
weight: 153000
---

[NuttX](https://nuttx.apache.org):

**Created from my notes while setting up environment for working on
`M5Stack C`**

## Prerequisites

pre-requisite list given in [Official Documentation][1]
was not that easy to setup. Particularly, kconfig-fronends.
Found another document [NuttX companion][2].
This has somewhat clear proceedrue that works in MacOS.

Before proceeding, [install esp-idf][3], now install the prerequisites given
in [NuttX companion][2].

```bash
  brew install autoconf
```

```bash
  mkdir ~/esp/nuttx
  mkdir ~/esp/nuttx/buildtools
  export NUTTXTOOLS=~/esp/nuttx/buildtools
  export NUTTXTOOLS_PATH=$NUTTXTOOLS/bin:$NUTTXTOOLS/usr/bin
  export PATH=$NUTTXTOOLS_PATH:$PATH
  # All the necessary tools, are found in this git repository.
  cd ~/esp/nuttx
  git clone https://bitbucket.org/nuttx/tools.git tools
```

```bash
  # kconfig-frontends
  pushd tools/kconfig-frontends
  # Apply the patch for MacOS
  patch < ../kconfig-macos.diff -p 1
  ./configure --prefix=$NUTTXTOOLS --enable-mconf --disable-shared --enable-static --disable-gconf --disable-qconf --disable-nconf
  touch aclocal.m4 Makefile.in
  make
  make install
  popd
```

```bash
#Install gperf
pushd tools/
curl http://ftp.gnu.org/pub/gnu/gperf/gperf-3.1.tar.gz -o gperf-3.1.tar.gz
tar zxf gperf-3.1.tar.gz
cd gperf-3.1
./configure --prefix=$NUTTXTOOLS
make
make install
popd
```

```bash
# install genromfs
pushd tools/
tar zxf genromfs-0.5.2.tar.gz
cd genromfs-0.5.2
make install PREFIX=$NUTTXTOOLS
popd
```

## Download and build

I downloaded the latest version from github.

```bash
$ cd ~/esp/nuttx
$ mkdir nuttx
$ cd nuttx
$ git clone https://github.com/apache/incubator-nuttx.git nuttx
$ git clone https://github.com/apache/incubator-nuttx-apps apps
$ git -C nuttx log -1 | head -1
  commit 04d81b24e3ea87d15b514ce85f2eaf2e28e72bd2
$ git -C apps log -1 | head -1
  commit f6f4de1ca2874e615fe1722a8cf2dbcadba63804
```

If you are working on a fresh window, you must
source the ESP-IDF tools.

```bash
$ export IDF_PATH=~/esp/esp-idf
$ source $IDF_PATH/export.sh
```

Now, configure and build the NuttX.

```bash
$ ./tools/configure.sh -l esp32-devkitc:nsh
$ make
#don't forget to modify the PORT below.
$ make download ESPTOOL_PORT=/dev/tty.usbserial-5952CA19FA ESPTOOL_BAUD=150000
```

Note, I have not invoked menuconfig, so a default nsh is included in the build.

Open the terminal to interact with this nsh terminal.

```bash
$ screen /dev/tty.usbserial-5952CA19FA 115200
# Remember you should press
# Ctrl+A then k, y to abort screen
I (13) boot: ESP-IDF v4.2.1-64-gd9ec7df39 2nd stage bootloader
I (13) boot: compile time 14:47:12
I (13) boot: chip revision: 1
I (16) boot_comm: chip revision: 1, min. bootloader chip revision: 0
I (23) boot.esp32: SPI Speed      : 40MHz
I (27) boot.esp32: SPI Mode       : DIO
I (32) boot.esp32: SPI Flash Size : 4MB
I (36) boot: Enabling RNG early entropy source...
I (42) boot: Partition Table:
I (45) boot: ## Label            Usage          Type ST Offset   Length
I (53) boot:  0 nvs              WiFi data        01 02 00009000 00006000
I (60) boot:  1 phy_init         RF data          01 01 0000f000 00001000
I (68) boot:  2 factory          factory app      00 00 00010000 00100000
I (75) boot: End of partition table
I (79) boot_comm: chip revision: 1, min. application chip revision: 0
I (86) esp_image: segment 0: paddr=0x00010020 vaddr=0x3f400020 size=0x01a74 (  6772) map
I (98) esp_image: segment 1: paddr=0x00011a9c vaddr=0x3ffb1370 size=0x00064 (   100) load
I (104) esp_image: segment 2: paddr=0x00011b08 vaddr=0x40080000 size=0x016d0 (  5840) load
I (116) esp_image: segment 3: paddr=0x000131e0 vaddr=0x00000000 size=0x0ce38 ( 52792)
I (142) esp_image: segment 4: paddr=0x00020020 vaddr=0x400d0020 size=0x0e71c ( 59164) map
I (165) boot: Loaded app from partition at offset 0x10000
I (165) boot: Disabling RNG early entropy source...
�
NuttShell (NSH) NuttX-10.1.0-RC1
nsh>
```

on this interacive terminal, it is possible to use few commands. To get the possible commands,

```bash
nsh> help
help usage:  help [-v] [<cmd>]

  .         cat       dd        false     ls        ps        sleep     uname
  [         cd        df        free      mkdir     pwd       source    umount
  ?         cp        echo      help      mkrd      rm        test      unset
  basename  cmp       exec      hexdump   mount     rmdir     time      usleep
  break     dirname   exit      kill      mv        set       true      xd

Builtin Apps:
  nsh  sh
```

For example, ls command returns the following

```bash
  nsh> ls /proc
  /proc:
  0/
  1/
  meminfo
  fs/
  self/
  uptime
  version
```

Few things to note,

1. we have not added any application yet.
2. The nsh terminal gets refreshed more frequently. (**TODO**: investigate this problem)
3. Lets cover how to configure and use nsh in a separate session.

## Understanding menuconfig:

It is possible to configure the nuttx to include
other applications from apps. This is done through
menuconfig.

```bash
$ make menuconfig
```

For demonstration, I have enabled hello world program.

```
Application Configuration  ---> Examples  ---> [*] "Hello, World!" example
(hello) Program name
```

Now, build, flash and then interact in serial monotor.

```bash
$ make
$ make download ESPTOOL_PORT=/dev/tty.usbserial-5952CA19FA ESPTOOL_BAUD=150000
$ screen /dev/tty.usbserial-5952CA19FA 115200
...
...
NuttShell (NSH) NuttX-10.1.0-RC1
nsh> hello
Hello, World!!
...
...
# Ctrl+ A, k, y <-- to terminate
```

Notes:

- This document suggest to install few more brew packages for later use. I have not installed during initial setup. Buiding and running NuttX didn't get affected by it. However, they may be required for certain configuration. (**TODO**: Revise this docuemnt once identified)

[1]: https://nuttx.apache.org/docs/latest/quickstart/install.html
[2]: https://nuttx-companion.readthedocs.io/en/latest/index.html
[3]: [Setup XX.m d Point to correct document]
