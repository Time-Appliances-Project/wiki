#!/usr/bin/env python3
"""Validate the initial GitHub Wiki migration snapshot without dependencies."""
from pathlib import Path
import gzip
import hashlib
import json
import re
from urllib.parse import unquote, urlparse

root = Path(__file__).resolve().parents[1]
pages = {p.stem: p for p in (root / 'wiki').glob('*.md')}
numbers = []
for name, path in pages.items():
    text = path.read_text()
    assert chr(0x2014) not in text, path
    assert 'localhost' not in text and '/index.php/' not in text, path
    for target in re.findall(r'\]\(([^\s)]+)', text):
        url = urlparse(target)
        if not url.scheme and url.path:
            assert unquote(url.path) in pages, (name, target)
    assert 'NewPP limit report' not in text, path
    if name == 'Home':
        past = re.split(r'^### Recordings from Past Calls[^\n]*\n', text, maxsplit=1, flags=re.M)[1].split('\n## ', 1)[0]
        rows = [line for line in past.splitlines() if re.match(r'^\| #\d+', line)]
        for row in rows:
            assert len(re.split(r'(?<!\\)\|', row)) == 7, (name, row)
        numbers += [int(n) for n in re.findall(r'^\| #(\d+)', past, re.M)]
assert sorted(numbers) == list(range(1, 169)), 'Recording rows missing or duplicated'
for name in ('Wireless-TimeSync', 'Lunar-Timekeeping-System', 'TAP-2023-OCP-Regional-Summit'):
    assert 'original source has not yet been recovered' in pages[name].read_text()
ptm = json.loads((root / 'migration/ptm-readiness-recovery.json').read_text())
source = gzip.decompress((root / ptm['snapshot']).read_bytes())
assert hashlib.sha256(source).hexdigest() == ptm['sha256_uncompressed']
restored = pages['PTM-Readiness'].read_text()
# Split on pipes without discarding empty cells in the historical TGPIO column.
rows = [[cell.strip() for cell in line.split('|')[1:-1]]
        for line in restored.splitlines() if re.match(r'^\| \d+ \|', line)]
assert rows == ptm['rows'] and len(rows) == ptm['row_count'] == 35
assert ptm['archive_url'] in restored and '1 July 2025' in restored
for image in (root / 'migration/uploads').iterdir():
    assert image.read_bytes() == (root / 'wiki/images' / image.name).read_bytes()
print(f'PASS: {len(pages)} Markdown files, local link targets, 168 recording rows, 35 recovered PTM rows, images, and three marked gaps.')
