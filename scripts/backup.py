#!/usr/bin/env python3
"""Back up MediaWiki database, configuration, and uploads with writes stopped."""
import datetime
import gzip
import os
from pathlib import Path
import shutil
import subprocess

root = Path(__file__).resolve().parents[1]
os.chdir(root)
dest = root / 'backups' / datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
dest.mkdir(parents=True, mode=0o700)
compose = ['docker', 'compose']
subprocess.run(compose + ['stop', 'wiki'], check=True)
try:
    with gzip.open(dest / 'database.sql.gz', 'wb') as file:
        dump = subprocess.Popen(compose + ['exec', '-T', 'database', 'sh', '-c',
            'exec mariadb-dump --single-transaction --user=root --password="$MARIADB_ROOT_PASSWORD" tapwiki'],
            stdout=subprocess.PIPE)
        shutil.copyfileobj(dump.stdout, file)
        if dump.wait() != 0:
            raise RuntimeError('Database dump failed')
    with (dest / 'files.tar.gz').open('wb') as file:
        subprocess.run(compose + ['run', '--rm', '-T', '--no-deps', '--entrypoint', 'tar',
            'wiki', '-czf', '-', '-C', '/var/www', 'config', '-C', '/var/www/html', 'images'],
            stdout=file, check=True)
    shutil.copy2(root / '.env', dest / '.env')
    (dest / 'COMPLETE').write_text('Database, configuration, uploads, and environment saved.\n')
    print(f'Backup complete: {dest}. Contains secrets; store privately.')
finally:
    subprocess.run(compose + ['start', 'wiki'], check=True)
