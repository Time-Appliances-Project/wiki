#!/bin/sh
set -eu
cd /var/www/html
mkdir -p /var/www/config /tmp/mediawiki-cache
chown -R www-data:www-data /var/www/config /tmp/mediawiki-cache images
if [ ! -f /var/www/config/LocalSettings.php ]; then
  # The installer refuses to run when a settings file already exists in the web root.
  mv LocalSettings.php /tmp/tap-settings-loader.php
  trap 'mv /tmp/tap-settings-loader.php /var/www/html/LocalSettings.php' EXIT
  php maintenance/run.php install \
    --dbtype=mysql --dbserver=database --dbname=tapwiki --dbuser=tapwiki \
    --dbpass="$DB_PASSWORD" --server="$MW_SERVER" --scriptpath='' \
    --lang=en --skins=Vector --confpath=/var/www/config \
    --pass="$MW_ADMIN_PASSWORD" 'Time Appliances Project' "$MW_ADMIN_USER"
  mv /tmp/tap-settings-loader.php LocalSettings.php
  trap - EXIT
  chmod 640 /var/www/config/LocalSettings.php
  chown www-data:www-data /var/www/config/LocalSettings.php
fi
if [ ! -f /var/www/config/content-imported ]; then
  gzip -dc /opt/tap/original-history.xml.gz > /tmp/tap-history.xml
  php maintenance/run.php importDump --quiet --username-prefix=ocp /tmp/tap-history.xml
  rm /tmp/tap-history.xml
  php maintenance/run.php importDump --quiet /opt/tap/seed.xml
  php maintenance/run.php importImages --user="$MW_ADMIN_USER" /opt/tap/uploads
  cp /opt/tap/uploads/Screenshot_2020-07-01_16.35.12.png images/tap-logo.png
  php maintenance/run.php rebuildrecentchanges
  php maintenance/run.php initSiteStats --update
  touch /var/www/config/content-imported
fi
chown -R www-data:www-data images /tmp/mediawiki-cache
exec docker-php-entrypoint "$@"
