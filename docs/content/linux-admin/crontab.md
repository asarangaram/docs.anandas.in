---
title: crontab

---

# crontab
`crontab` is a command used in Unix-like operating systems to manage cron jobs. A cron job is a task or command that is scheduled to run at specific intervals automatically. The `crontab` command is used to create, view, edit, and delete cron jobs for a particular user.

## common commands
* `crontab -e`: Edit the user's `crontab` file.
* `crontab -l`: View the user's current `crontab` file.
* ❗`crontab -r`: Remove the user's `crontab` file (deletes all cron jobs for that user).
* `crontab -u <username> -e`: Edit the `crontab` file of a specific user (requires appropriate permissions).

## Scheduling syntax
The syntax consists of five fields representing minute, hour, day of the month, month, and day of the week.
we can use 
* wildcard * refers to every ?? (based on field location)
* values 10, 15 etc 
    * Minute (0-59)
    * Hour (0-23)
    * Day of the month (1-31)
    * Month (1-12 or three-letter month names) 
        * jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec (case insensitive, check crontab implementation)
    * Day of the week (0-7 or three-letter daynames, where both 0 and 7 represent Sunday)
        * Sun, Mon, Tue, Wed, Thu, Fri, Sat
* Step values: */3
    * every 3rd min or month etc… 

## System wide
The system-wide `crontab` file `/etc/crontab` allows system administrators to schedule tasks that apply to all users on the system.
 
## Email support (not tested)
To set the email recipient for all cron jobs, add the following line at the top of the crontab file

```
MAILTO=<email_address> 
* * * * * command1
* * * * * command2
* * * * * command3
```

To set the email recipient for a specific cron job, include the `MAILTO` line right before the cron job entry.
```
* * * * * MAILTO=<email_address> command
```
The cron daemon relies on a functioning mail transfer agent (MTA) to send emails. Check that an MTA is installed and properly configured on your system. Refer [HERE TODO]

## Envoronment

One of the problem encounteed is setting up the cron when the script depends on the environment variables. As the cron job runs the sctipt from a non-interactive shell, no rc files (e.g., .bashrc) will be sourced / loaded. Hence it runs with minimum environment variable. This means some of the executables that are not installed by apt can't be invoked as $PATH is not updated. 

To solve this, we could to explicity source the necessary rc files, like .bashrc before calling the script as part of cron definiton like `source /home/<username>/.bashrc && /path/to/script"`. There are two issues in this approach.
1. we hardcode the username, as it can't resolove ~ at this point. we need to use either $LOGNAME or $(whoami) to get he user name and the home directory `eval echo ~$(whoami)`. Such things are bit messy, hence the better way is to source the rc files in the script to avoid cluttering the cron file.
2. In some system the bash will be configured to load the .bashrc only when loading in interactive mode with the following lines or similar. We need to ensure that these lines are commented out or the required environment is set before these lines so that they are available in non interactive mode.
```bash
case $- in
    *i*) ;;
      *) return;;
esac
```

[here](https://www.baeldung.com/linux/run-cron-job-manually) is a way to debug the cron job manually.