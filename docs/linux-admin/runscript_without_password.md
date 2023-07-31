---
title: Running a script without password

---

## Why do we need?
As part of automation of services, we need to issue certain commands as sudoer. 

One typical use case I came across is to restart the ngnix once the Hugo content is rebuild. In this case, if sudo requires password, we can't trigger it in script.

🛑🛑🛑
Making scripts to run with sudo password is a security risk, and assumption here is that the machine access is restricted and secure.
🛑🛑🛑

## How it can be done?

Open sudoers file for your user

```bash
$ sudo visudo -f /etc/sudoers.d/myusername
```

update the commands that we want to call without sudo password as below. 
```
myusername ALL=(ALL) NOPASSWD: /usr/sbin/service nginx start,/usr/sbin/service nginx stop,/usr/sbin/service nginx restart
```

we can add any script that is executable as root.
```
myusername ALL=(ALL) NOPASSWD: /path/to/rootscript
```

## References
* [stack-overflow1](https://stackoverflow.com/questions/3011067/restart-nginx-without-sudo)
    * [answer1](https://stackoverflow.com/a/45071759)
    * [answer2](https://stackoverflow.com/a/9066636)
* [stack-overflow2](https://stackoverflow.com/questions/21830644/non-privileged-non-root-user-to-start-or-restart-webserver-server-such-as-ngin/22014769#22014769)