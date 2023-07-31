---
title: Manage Users

---

These commands help **to create and configure users** on Linux. (Tested on Ubuntu.)

# Commands
| Purpose                           | Command                                        | Remarks                                                                                                                                 |
| --------------------------------- | ---------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| create new user                   | `useradd`                                      | you can create user directory (`-m`, `-d`), `useradd --help`. Avoid creating user 'root'.                                               |
| give sudo permission              | `usermod`                                      | sudo usermod -aG sudo <user>                                                                                                            |
| set password                      | `passwd`                                       | If useradd didn't prompt with password, set password with this command. _Always create password for the user before giving sudo access_ |
| list users                        | `cut -d: -f1 /etc/passwd`                      |                                                                                                                                         |
| list users with sudo permission   | `grep '^sudo:.*$' /etc/group `\|` cut -d: -f4` |                                                                                                                                         |
| changing the default shell        | `chsh`                                         |                                                                                                                                         |
| to generate ssh key               | `ssh-keygen`                                   | use `ssh-keygen -t rsa -b 2048`. create ssh key (private+public pair), as it will help to setup github/gitlab accounts.                 |
| to copy ssh key to remote machine | `ssh-copy-id`                                  | `ssh-copy-id username@remote_host`                                                                                                      |
| To create home directory          | `sudo mkhomedir_helper <user>`                 |

{{% notice tip %}} setup ssh public key for the computer from where you access. If you are creating second account that you want to access from same account of the client, the quicker (but hacking ) way is to copy the public key from the current user into the new user account and change the permission before logging in with newuser. This will simplify some annoying steps. once you give sudo permission to someone, they either need to logout and log in.; reboot is optional.

{{% /notice %}}
