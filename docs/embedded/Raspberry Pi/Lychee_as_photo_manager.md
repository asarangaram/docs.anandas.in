---
title: Lychee as Photo Manager
weight: 330000
---

Lychee is a free photo-management tool, which runs on your server. [^1] [^2]

Most of the basic requirements like, webserver, php and data base for Lychee is already taken care in [Setup XX.m d Point to correct document]. This document assumes, you have prepared RPi as per the Setup proceedure.

In this section, we shall configure our system ready for Lychee, install Lychee and test it.

**Note**: The original documentation [https://lycheeorg.github.io/docs/] has all the details, but few things are hidden / burried inside the huge documentation. This page extracts and provide the instructions specific for RPi.

## Few important requirements for our installation

1. We don't overwrite the default webserver running from /var/www/html. Lychee can be assigned a separate server [http://photo.ubuntu.local]. This way, we can add more services into our product.
2. We need bigger storage as Lychee manages Media, which may not fit into the SD card over the time. So lets fix the folder /data/www/photos/lychee for Lychee
3. Lychee uses .htaccess file. We need to permit it [^3].

---

### Prepare Directories

Apache webserver accesses the data with the user www-data:www-data. Add the current user into www-data group.

```bash
$ ll /data
...
drw-rw-r--  2 www-data www-data  4096 Aug  5 07:26 www/
...
```

If you don't see the permission, owner and group as above, make sure you correct them. The permission can be updated using chmod and the owner and group can be updated using chown.

```bash
    sudo chmod -R 664 /data/www
    sudo chown -R ubuntu:www-data /data/www
```

Note, we have given write permission to both the owner and group

### Move yourself to www-data group

```bash
$ whoami
ubuntu
$ sudo adduser ubuntu www-data
Adding user 'ubuntu' to group 'www-data' ...
Adding user ubuntu to group www-data
Done.
$ groups ubuntu # make sure it displays www-data
ubuntu : ... www-data ...
```

### Switch group and create /data/www/photos

```bash
$ newgrp www-data
$ mkdir -p /data/www/photos
$ ll /data/www
...
drwxrwxr-x 2 ubuntu www-data 4096 Aug  5 07:49 photos/
...
```

If the permission, owner and group are as above, move ahead.

### create a new site pointing to /data/www/photos/lychee/public

```bash
cd /etc/apache2/sites-available
cp 000-default.conf 001-lychee.conf
```

Replace the content of 001-lychee.conf by

```bash
<VirtualHost *:80>

 DocumentRoot /data/www/photos/lychee/public
 ServerName photos.ubuntu.local

 <Directory /data/www/photos/lychee/public>
  Options Indexes FollowSymLinks
  AllowOverride All
  Require all granted
 </Directory>

 ErrorLog ${APACHE_LOG_DIR}/photo-error.log
 CustomLog ${APACHE_LOG_DIR}/photo-access.log combined

 RewriteEngine on
 RewriteOptions Inherit
 # RewriteCond %{SERVER_NAME} = photo.ubuntu.local
 # RewriteRule ^ https://%{SERVER_NAME}%{REQUEST_URI} [END,NE,R=permanent]

</VirtualHost>
```

Enable this site.

```bash
sudo a2ensite 001-lychee
sudo systemctl reload apache2
```

### Download the Lychee

```bash
cd /data/www/photos
wget https://github.com/LycheeOrg/Lychee/releases/download/v4.3.4/Lychee.zip
unzip Lychee.zip
mv Lychee lychee
cd lychee
composer install --no-dev
cp .env.example .env
vi .env
```

Change APP_URL to [http://photos.ubuntu.local] and TIMEZONE to Asia/Kolkata in the .env file. Don't change anything else.

```bash
php artisan key:generate
php artisan migrate
```

now handover this folder to the user www-data.

```bash
sudo chown -R www-data:www-data .
```

## Start browsing

In the browser, (from the device you have connected to rpi_internet), access [http://photos.ubuntu.local] and follow the instructions to setup and use.

Note, other than photos, everything else will be redirected to apache default page.

---

END OF THE DOCUMENT

[^1]: https://lycheeorg.github.io
[^2]: https://github.com/LycheeOrg/Lychee
[^3]: https://help.ubuntu.com/community/EnablingUseOfApacheHtaccessFiles
