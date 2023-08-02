---
title: Ports in Linux

---

The Internet Assigned Numbers Authority (IANA) is responsible for maintaining the official list of `well-known ports` (or registerred ports) and their associated applications/services. The IANA assigns port numbers in the range of 0 to 1023 for well-known ports. 

The registry is called '**Service Name and Transport Protocol Port Number Registry**' and it is available <a href="https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml" target="_blank">here</a>.


### Most Common Ports:
| Port  | Service          |
| :---: | :---------------- |
| **Port  21**: | FTP (File Transfer Protocol) - used for file transfers. | 
| **Port  22**: | SSH (Secure Shell) - used for secure remote access to servers.| 
| **Port  25**: | SMTP (Simple Mail Transfer Protocol) - used for email transmission. | 
| **Port  53**: | DNS (Domain Name System) - used for domain name resolution.| 
| **Port  80**: | HTTP (Hypertext Transfer Protocol) - used for web browsing.| 
| **Port 443**: | HTTPS (Hypertext Transfer Protocol Secure) - used for secure web browsing (encrypted) | 
| **Port 110**: | POP3 (Post Office Protocol version 3) - used for receiving email from a server.


Most popular applications uses a specific port as their default, as a convention. When installing the applications, these allow the user to override, in case of conflict.

!!! info inline ""

    This is not a exhaustive list, but the applications used in my products. 

| Port  | Application      |
| :---: | ---------------- |
| 1313  | Hugo server      |
| 3306  | MySQL            |
| 5000  | Flask            |
| 5432  | PostgreSQL       |
| 6379  | Redis            |


When troubleshooting network connectivity or security issues, knowing the well-known ports associated with specific applications can be helpful. However, keep in mind that applications and services may use different port numbers, especially custom ones. To verify the exact port usage on a system, you can use the following utilities.


=== "lsof"

    !!! info inline ""

        List Open Files

    ```bash
    # to install
    sudo apt install lsof 
    # to check ports
    sudo lsof -i -P -n | grep LISTEN
    ```

=== "netstat"

    !!! info inline ""

        Network Statistics utilty. 

    ```bash
    # to install
    sudo apt install net-tools 
    # to check ports
    netstat -tulpn | grep LISTEN
    ```

=== "ss"

    !!! info inline ""

        Socket-related Statistics utility 
    
    ```bash
    # to install
    sudo apt install iproute2
    # to check ports
    sudo ss -tulwn | grep LISTEN
    ```


