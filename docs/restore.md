# Restore a MediaWiki backup

Use a new checkout on a fresh host or a separate Docker Compose project with empty volumes. Restoring over an existing wiki replaces its content, so retain a current backup before doing that.

1. Copy the backup directory privately to the new host. Check that it contains `COMPLETE`, `database.sql.gz`, `files.tar.gz`, and `.env`.
2. Copy its `.env` into the checkout and set mode `600`. Keep the same database credentials during restoration. Change `MW_SERVER` only if the public hostname changes.
3. Build the wiki image: `docker compose build wiki`.
4. Start the database: `docker compose up -d --wait database`.
5. Import SQL and restore the saved configuration and uploads using the commands below. Replace `/private/backup` with the actual backup directory.

```sh
gzip -dc /private/backup/database.sql.gz | docker compose exec -T database sh -c 'exec mariadb --user=root --password="$MARIADB_ROOT_PASSWORD" tapwiki'
```

The files archive stores `config/` and `images/` at its top level. Restore each into its persistent volume before starting the wiki:

```sh
cat /private/backup/files.tar.gz | docker compose run --rm -T --no-deps --entrypoint sh wiki -c 'mkdir -p /tmp/tap-restore; tar -xzf - -C /tmp/tap-restore; cp -a /tmp/tap-restore/config/. /var/www/config/; cp -a /tmp/tap-restore/images/. /var/www/html/images/; chown -R www-data:www-data /var/www/config /var/www/html/images'
docker compose up -d --wait
```

The archive's `content-imported` marker prevents initial recovery content from being imported again. Verify the main page, a recent edit, history, login, and uploaded files before routing public traffic to the restored host.
