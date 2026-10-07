#!/usr/bin/env python3
"""Create local deployment credentials without overwriting existing secrets."""
from pathlib import Path
import os
import secrets

root = Path(__file__).resolve().parents[1]
path = root / '.env'
if path.exists():
    raise SystemExit('.env already exists; it has not been changed.')
values = {
    'MW_SERVER': 'http://localhost:8088',
    'WIKI_PORT': '8088',
    'MW_ADMIN_USER': 'TapAdmin',
    'MW_ADMIN_PASSWORD': secrets.token_urlsafe(30),
    'DB_PASSWORD': secrets.token_urlsafe(36),
    'DB_ROOT_PASSWORD': secrets.token_urlsafe(36),
}
fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
with os.fdopen(fd, 'w') as file:
    file.write(''.join(f'{k}={v}\n' for k, v in values.items()))
print('Created .env (owner readable only). Admin login: TapAdmin. Password is in .env.')
