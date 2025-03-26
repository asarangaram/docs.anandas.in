AI on Rpi


An attempt to setup a working environment with the following hardware

1. Raspberry Pi 5
2. AI Hat with 26 TOPS


Last month my Raspberry Pi 4B died without any reason. Hence I decided to replace it with Raspberry Pi5. While shopping online, I noticed a AI HAT available with it. Thought of trying it and document what I could do with it in this page.

Although the official OS for Raspberry Pi is Raspberry Pi OS, I am somehow not comfortable with it. I always use Ubuntu server with lightweight session and Windows Manager. The AI Hat has support only for Raspberry Pi OS and I may need to get help from the community to make it working with Ubuntu.

So I decided to use two MicroSD card, one with Raspberry Pi OS and another with Ubuntu Server. I used  Raspberry Pi Imager v 1.8.5 to burn the MicroSD cards.  

### Setting up Ubuntu

#### Some Fundamentals here.
A Display Server provides the foundation for a graphical environment and X11 is the traditionally and most widely used one on Ubuntu. Wayland is the modern replacement but doesn't seems to support all the apps for now. So, I go with X11 for now, but keep an eye on Wayland progress,  


```
sudo apt full-upgrade
```

