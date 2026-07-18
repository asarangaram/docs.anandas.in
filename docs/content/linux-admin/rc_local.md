# rc-local.service
On ubuntu, I noticed that this service is failed. Refer the following links to understand the issue and resolve.


[Reference 1](http://realtechtalk.com/Debian_Ubuntu_Mint_rclocal_service_startup_error_solution_rclocalservice_Failed_at_step_EXEC_spawning_etcrclocal_Exec_format_error-2242-articles) | [Reference 2](https://www.linuxbabe.com/linux-server/how-to-enable-etcrc-local-with-systemd) | [Reference 3](https://linuxhint.com/use-etc-rc-local-boot/) | 


Following is my understanding:

1. rc means Run Control.
1. The file `rc.local` does not contain information on system startup components, but only superuser/root defined components. 
1. Not all root startup programs are described in rc.local but only those which don’t interfere with system components
1. the file rc.local is executed after normal services are started.
1. The failure mostly related to not ending the script with `exit 0` or your default script is not /bin/sh. Adding `#!/bin/sh -e` at the begining of the script and `exit 0` at the end of the script. sometime the script is not executable and not owned by root.
    ```
    #!/bin/sh -e
    COMMANDS
    exit 0
    ```
1. We may add service to enable it via servicectl.
1. you can create the file, if it doesnt' exists (as given in Reference 3).
1. This is one of the mechanism available. crontab can also be used for the same purpose

My view:
I prefer to use this to run start up scripts for the applications I host in the server. But for the services, setting up via systemctr seems more convenient to maintain.

