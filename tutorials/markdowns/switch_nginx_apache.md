## Introduction
In Wordpress, for the WP Mail SMTP plugin, the *Authentication plugin* for Google triggers a *403 Forbidden Error* upon redirect after Google allows the access. Thus, the idea is to switch off Nginx and take a look at ONLY Apache. The reason for doing this is to check for errors in the redirecting / configuration. Albeit, the end result has been found as a WordPress plugin issue - WP Security, this is a good procedure to go through to learn more about the Nginx-Apache setup itself.

## Instructions - Switch to Apache Only
There are four major parts of this, the last step is most important to avoid *redirect loop*.
*  disable nginx
*  restore the apache settings without nginx
*  enable the apache2-only `.conf` file
*  disable the `.htaccess` WordPress HTTP redirects as the apache already does the redirect

1.  Login to server, stop nginx: `sudo systemctl stop nginx`
2.  Disable the mods for apache2: `sudo a2dismod rpaf actions fastcgi`
3.  Enable the php mod for apache2: `sudo a2enmod php7.2`
4.  Go to apache2 conf directory: `cd /etc/apache2/`
5.  Check the name of the `sites-enabled` and then disable it: `sudo a2dissite 001-default.conf`
6.  Check the name of the SSL certified `.conf` file inside `sites-available`, this should have `<VirtualHost *:443>` at the top
7.  Enable above `.conf`: `sudo a2ensite 001-default-le-ssl.conf`
8.  Go to the wordpress folder, `cd /var/www/html/wordpress`
9.  Open up the `.htaccess` file: `sudo nano .htaccess`
10.  Comment out the blocks for redirecting HTTP to HTTPS -- this is already handled in the `.conf` file in step 7  
    `<IfModule mod_rewrite.c>`  
    `# RewriteEngine on`  
    `# RewriteCond %{HTTP:X-Forwarded-Proto} !https`  
    `#wpmu rewritecond sinto-ling.ca`  
    `# RewriteCond %{HTTP_HOST} ^sinto\-ling\.ca [OR]`  
    `# RewriteCond %{HTTP_HOST} ^www\.sinto\-ling\.ca [OR]`  
    `#end wpmu rewritecond sinto-ling.ca`  
    `# RewriteRule ^(.*)$ https://%{HTTP_HOST}/$1 [R=301,L]`  
    `</IfModule>`  

11.  Save and close the `.htaccess`
12.  Restart apache2: `sudo systemctl restart apache2`
13.  Check that the *static*-only sites work (e.g. only WordPress sites, not the Django site)

## Instructions - Switch back to Nginx-Apache setup
Pretty much reverse four major parts above.
*  enable the `.htaccess` WordPress HTTP redirects
*  enable the `:8080`-virtual-hosted `.conf` file
*  re-enable the nginx-associated apache2 mods
*  enable nginx, recycle apache2

1.  Login to server, navigate to WordPress directory: `cd /var/www/html/wordpress`
2.  Open up the `.htaccess` file: `sudo nano .htaccess`
3.  Uncomment the blocks for redirecting HTTP to HTTPS  
    `<IfModule mod_rewrite.c>`  
    `RewriteEngine on`  
    `RewriteCond %{HTTP:X-Forwarded-Proto} !https`  
    `#wpmu rewritecond sinto-ling.ca`  
    `RewriteCond %{HTTP_HOST} ^sinto\-ling\.ca [OR]`  
    `RewriteCond %{HTTP_HOST} ^www\.sinto\-ling\.ca [OR]`  
    `#end wpmu rewritecond sinto-ling.ca`  
    `RewriteRule ^(.*)$ https://%{HTTP_HOST}/$1 [R=301,L]`  
    `</IfModule>`  
4.  Save and close the `.htaccess`
5.  Go to apache2 conf directory: `cd /etc/apache2/`
6.  Disable the SSL-certified config file: `sudo a2dissite 001-default-le-ssl.conf`
7.  Check the name of the `:8080` config file inside `sites-available`, this should have `<VirtualHost *:8080>` at the top
8.  Enable above `.conf`: `sudo a2ensite 001-default.conf`
9.  Disable the `php7.2` mod as this does not work with nginx: `sudo a2dismod php7.2`
10.  Enable the nginx-associated apache mods: `sudo a2enmod actions rpaf fastcgi`
11.  Start nginx: `sudo systemctl start nginx`
12.  Refresh apache: `sudo systemctl restart apache2
13.  Check that all sites are now up and running

## Links
[Nginx-Apache Tutorial](https://www.digitalocean.com/community/tutorials/how-to-configure-nginx-as-a-web-server-and-reverse-proxy-for-apache-on-one-ubuntu-18-04-server)  