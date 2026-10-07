FROM mediawiki:1.43.11
COPY config/LocalSettings.php /var/www/html/LocalSettings.php
COPY config/CustomSettings.php /opt/tap/CustomSettings.php
COPY config/uploads.conf /etc/apache2/conf-available/tap-uploads.conf
COPY scripts/container-start.sh /usr/local/bin/tap-start
COPY migration/original-history.xml.gz migration/seed.xml /opt/tap/
COPY migration/uploads/ /opt/tap/uploads/
RUN chmod +x /usr/local/bin/tap-start && a2enmod headers && a2enconf tap-uploads
ENTRYPOINT ["tap-start"]
CMD ["apache2-foreground"]
