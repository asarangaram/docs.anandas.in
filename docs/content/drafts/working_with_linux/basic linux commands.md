## Manage Users 
| Purpose  |  Command | Remarks|
|---|---|---|
| create new user | `useradd` | you can create user directory (`-m`, `-d`), `useradd --help`|
| give sudo permission  |  `usermod` |  sudo usermod -aG sudo <user> |
|  set password |  `passwd` | If useradd didn't prompt with password, set password with this command  |
| list users | `cut -d: -f1 /etc/passwd` | |
| list users with sudo permission | `grep '^sudo:.*$' /etc/group `\|` cut -d: -f4` | |
| changing the default shell | `chsh` | |
| to generate ssh key | `ssh-keygen` | use `ssh-keygen -t rsa -b 2048`|
| to copy ssh key to remote machine | `ssh-copy-id` | `ssh-copy-id username@remote_host` |
| To create home directory | `sudo mkhomedir_helper <user>` | 


Things to do while creating new users:
* Create a user 
* setup ssh public key for the computer from where you access. If you are creating second account that you want to access from same account of the client, the  quicker (but hacking ) way is to copy the public key from the current user into the new user account and change the permission before logging in with newuser. This will simplify some annoying steps
* suggesting to create a user with sudo permission other than root and use it to ssh, instead of using root account.
Note: once you give sudo permission to someone, they either need to logout and log in. Reboot is an option, but may not required for this.
* Always create password for the user before giving sudo access
* by default, the new user may have some shell assigned as default shell based on the distribution. If it is not bash, you won't be able to use the scripts I provide. (I use bash as a default shell always on Linux). setting bash as a default shell is one more thing to be done for the new user.
* we need to install the public key of the machines from which we shall connect into authroized keys. Also, we need to create key (private+public pair) using ssh-keygen tool so that we can provide public key for external access like gitlab, github etc.



# How to remove apache and install nginx?

I use `nginx` as webserver. By default, the `apache` is installed and listens the ports required. So, we need to disable it and install `nginx`. While disabling the `apache` service is sufficient, I found that sometime the software update tries to restart the service. As I couldn't find find a easier way to stop the auto start of `apache` now and then and conflict with `nginx` setup, I remove `apache` completely and then install. Anyways I will not use `apache` and Nginx together.

Few utility commands, useful at this stage.

| command | purpose |
|---|---|
| `apt update && apt upgrade -y` | to update and upgrade the system, now and then we may need to run this. |
| `lsof -i -P -n \| grep LISTEN` | To list the ports being listen to and by what service |
| `systemctl list-units --type=service` | list the services running |
| `systemctl list-units --all` | list services including inactive |

## Remove apache
```
systemctl stop apache2
sudo systemctl disable apache2

sudo apt-get purge apache2 apache2-utils apache2.2-bin apache2-common
sudo apt-get autoremove
whereis apache2
sudo rm -rf /etc/apache2 /usr/sbin/apache2 /usr/lib/apache2 /usr/share/apache2 /usr/share/man/man8/apache2.8.gz
whereis apache2

```

## Install nginx
```
sudo apt update
sudo apt-get install nginx
sudo service nginx start # required if it fails to auto start
```

