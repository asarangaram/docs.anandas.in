---
title: m5 Stick setup
weight: 152000
---

[ESP-IDF](https://www.espressif.com/en/products/sdks/esp-idf):

## Setup for M5StickC and M5Stack (Linux)

{{< youtube 05GKbdcH92Y >}}

**Created from my notes while setting up environment for working on `M5Stack C`**

This page explains how to install [ESP-IDF from github][1] and setup it to build
and run the projects. Focus is on to setup it from terminal.

There are methods to setup and use it from VS code or Eclipse. Refer
appropriate documentation for it if required.
Most of the documentations are up to date for Linux, while lagging on MacOS.

## Important Notes

- Decide on which version to start with from [here][2]. This decision is based
  on which chip you have. I am using ESP32. Other available chips as
  on **May 2021** are ESP32 S2 and ESP32 C3.
- Refer [ESP-IDF Programming Guide][3] for up to date info. It is simple to
  follow
- The info in this page are tested on [M5Stack C]
- This procedure is for `MacOS 11.3.1 ESP-IDF v4.2.1`

## Steps

Switch to bash terminal, if you are in zsh. Most of the steps we use
works fine in bash, not zsh.

### Pre-requisites

Check which Python is default. As python 2 is deprecated, it is better we
switch to python 3.

```bash
$ python --version
Python 2.7.16
```

MacOS also has python3 pre-installed.

```bash
$ python3 --version
Python 3.8.2
```

As this version is good enough, we don't install python, instead
create an alias so that python point to python3 in our bash environment.

```bash
$ alias python=python3 # Add this line into .bashrc
$ python --version
Python 3.8.2
```

We also need pip. The macOS system has pip3, but it may not have been aliased
to pip. Let's setup alias and check version. (you may also create softlink)

```bash
$ alias pip="python -m pip" #A dd this line into .bashrc
$ pip --version
pip 21.1.1 from /Library/Python/3.8/site-packages/pip (python 3.8)
```

Install HomeBrew, if you have not done earlier.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

The script installs:
`/usr/local/bin/brew
  /usr/local/share/doc/homebrew
  /usr/local/share/man/man1/brew.1
  /usr/local/share/zsh/site-functions/_brew
  /usr/local/etc/bash_completion.d/brew
  /usr/local/Homebrew`

and creates the following directories:
`/usr/local/bin
  /usr/local/etc
  /usr/local/include
  /usr/local/lib
  /usr/local/sbin
  /usr/local/share
  /usr/local/var
  /usr/local/opt
  /usr/local/share/zsh
  /usr/local/share/zsh/site-functions
  /usr/local/var/homebrew
  /usr/local/var/homebrew/linked
  /usr/local/Cellar
  /usr/local/Caskroom
  /usr/local/Frameworks
  `

Using HomeBrew, install the following packages.

```bash
brew install cmake ninja dfu-util ccache
```

**Note:** HomeBrew installs latest version of Python3 as needed and point to it
when you install other packages, so, always watch which version is being used.
you may continue using the version given by HomeBrew as long as it satisfies
the requirement.

Connect your device into the USB port of the Mac. The driver for CP210x
already exists on MacOS, no need to install it again.  
 Try,

```bash
$ ls -1 /dev/cu.*
...
/dev/cu.usbserial-5952CA19FA
```

### Download and Install

Close the ESP-IDF from its github path into a work-dir.

```bash
$ mkdir ~/esp
$ cd ~/esp
$ git clone -b v4.2.1 --recursive https://github.com/espressif/esp-idf.git
```

Note, I am downloading **v4.2.1**, and also note `--recursive`

```bash

```

This script is designed such that it first installed `xtensa-esp32-elf` into
`~/.espressif` folder, then installed dependency packages as listed in
`~/esp/esp-idf/requirements.txt`. It creates a Python VENV.

When ever you want to use this setup, you should do the following

```bash
$ export IDF_PATH=~/esp/esp-idf
$ source $IDF_PATH/export.sh
```

### Verify (Hello World example)

Now to confirm that the tools works as expect, let us compile a example program.

```bash
mkdir ~/esp/workdir
cd ~/esp/workdir
cp -rf $IDF_PATH/examples/get-started/hello_world ./
cd hello_world
$ make # This opens menu, once you update and save, it builds.
```

Update the following in the menu.

```
Serial flasher config  ---> Default serial port : /dev/cu.usbserial-5952CA19FA
Serial flasher config  ---> Default baud rate : Other baud rate
Other baud rate value  --> 150000
```

On completion, this prints the step for flashing. Note, the port and
baud rate are already updated correctly.

```bash
$ make flash
$ make monitor # Remember you need to press Ctrl+] to quit.
```

Serial port Monitor shows the following repeatedly.

```bash
$ idf.py monitor -p /dev/tty.usbserial-5952CA19FA
Restarting in 10 seconds...
Restarting in 9 seconds...
Restarting in 8 seconds...
Restarting in 7 seconds...
Restarting in 6 seconds...
Restarting in 5 seconds...
Restarting in 4 seconds...
Restarting in 3 seconds...
Restarting in 2 seconds...
Restarting in 1 seconds...
Restarting in 0 seconds...
Restarting now.
I (12) boot: ESP-IDF v4.2.1 2nd stage bootloader
I (12) boot: compile time 16:34:36
I (12) boot: chip revision: 1
I (14) boot_comm: chip revision: 1, min. bootloader chip revision: 0
I (21) boot.esp32: SPI Speed      : 40MHz
I (26) boot.esp32: SPI Mode       : DIO
I (30) boot.esp32: SPI Flash Size : 4MB
I (35) boot: Enabling RNG early entropy source...
I (40) boot: Partition Table:
I (44) boot: ## Label            Usage          Type ST Offset   Length
I (51) boot:  0 nvs              WiFi data        01 02 00009000 00006000
I (58) boot:  1 phy_init         RF data          01 01 0000f000 00001000
I (66) boot:  2 factory          factory app      00 00 00010000 00100000
I (73) boot: End of partition table
I (78) boot_comm: chip revision: 1, min. application chip revision: 0
I (85) esp_image: segment 0: paddr=0x00010020 vaddr=0x3f400020 size=0x05b34 ( 23348) map
I (102) esp_image: segment 1: paddr=0x00015b5c vaddr=0x3ffb0000 size=0x02070 (  8304) load
I (106) esp_image: segment 2: paddr=0x00017bd4 vaddr=0x40080000 size=0x00404 (  1028) load
0x40080000: _WindowOverflow4 at /Users/work/esp/esp-idf/components/freertos/xtensa/xtensa_vectors.S:1730

I (112) esp_image: segment 3: paddr=0x00017fe0 vaddr=0x40080404 size=0x08038 ( 32824) load
I (135) esp_image: segment 4: paddr=0x00020020 vaddr=0x400d0020 size=0x13004 ( 77828) map
0x400d0020: _stext at ??:?

I (165) esp_image: segment 5: paddr=0x0003302c vaddr=0x4008843c size=0x01af8 (  6904) load
0x4008843c: rtc_init at /Users/work/esp/esp-idf/components/soc/src/esp32/rtc_init.c:31

I (174) boot: Loaded app from partition at offset 0x10000
I (174) boot: Disabling RNG early entropy source...
I (174) cpu_start: Pro cpu up.
I (178) cpu_start: Application information:
I (183) cpu_start: Project name:     hello-world
I (188) cpu_start: App version:      v4.2.1
I (193) cpu_start: Compile time:     May 27 2021 16:34:29
I (199) cpu_start: ELF file SHA256:  4474a2091fb1a5ba...
I (205) cpu_start: ESP-IDF:          v4.2.1
I (210) cpu_start: Starting app cpu, entry point is 0x400815e4
0x400815e4: call_start_cpu1 at /Users/work/esp/esp-idf/components/esp32/cpu_start.c:287

I (210) cpu_start: App cpu up.
I (220) heap_init: Initializing. RAM available for dynamic allocation:
I (227) heap_init: At 3FFAE6E0 len 00001920 (6 KiB): DRAM
I (233) heap_init: At 3FFB28B0 len 0002D750 (181 KiB): DRAM
I (239) heap_init: At 3FFE0440 len 00003AE0 (14 KiB): D/IRAM
I (246) heap_init: At 3FFE4350 len 0001BCB0 (111 KiB): D/IRAM
I (252) heap_init: At 40089F34 len 000160CC (88 KiB): IRAM
I (258) cpu_start: Pro cpu start user code
I (277) spi_flash: detected chip: gd
I (277) spi_flash: flash io: dio
I (277) cpu_start: Starting scheduler on PRO CPU.
I (0) cpu_start: Starting scheduler on APP CPU.
Hello world!
This is esp32 chip with 2 CPU cores, WiFi/BT/BLE, silicon revision 1, 4MB embedded flash
Free heap: 299924
Restarting in 10 seconds...
Restarting in 9 seconds...
Restarting in 8 seconds...
Restarting in 7 seconds...
Restarting in 6 seconds...
```

This confirms that the hello world works correctly on the ESP32 device.

### Verify (Blink)

On the Hello World program, we need to use serial port UART monitor to confirm that the application is running. You don't see any output in the onboard
display. You may use blink example to to trigger the RED LED
(on the device) by configuring GPIO10 as LED port.

on successful flashing, you will see the LED blinks
ON/OFF with 1 sec interval.

Next session, lets explore more examples.

[1]: https://github.com/espressif/esp-idf
[2]: https://github.com/espressif/esp-idf#setting-up-esp-idf
[3]: https://docs.espressif.com/projects/esp-idf/en/stable/esp32/
[DATE]: 26/May/2021
