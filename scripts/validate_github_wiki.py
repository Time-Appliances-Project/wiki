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
for name in ('Lunar-Timekeeping-System',):
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
wireless = json.loads((root / 'migration/wireless-timesync-recovery.json').read_text())
source = (root / wireless['snapshot']).read_bytes()
assert hashlib.sha256(source).hexdigest() == wireless['sha256']
restored = pages['Wireless-TimeSync'].read_text()
for block in wireless['restored_blocks']:
    assert block in source.decode() and block in restored
for heading in wireless['empty_sections']:
    assert f'## {heading}\n\n*No entries were present in the recovered source text.*' in restored
assert '75153' in restored and wireless['original_url'] in restored
for image in (root / 'migration/uploads').iterdir():
    assert image.read_bytes() == (root / 'wiki/images' / image.name).read_bytes()
audit = json.loads((root / 'migration/wiki-audit-2026-10-25.json').read_text())
assert hashlib.sha256((root / audit['source_evidence']).read_bytes()).hexdigest() == audit['source_sha256']
summit = pages['TAP-2023-OCP-Regional-Summit'].read_text()
assert len(re.findall(r'^\| [12] \|', summit, re.M)) == 2
assert summit.count('[Video](') == summit.count('[Slides](') == 2
for slug in ('workstreams', 'upcoming-calls', 'recordings-from-past-calls'):
    assert f'<a name="{slug}"></a>' in pages['Home'].read_text()
assert pages['TAP-Instrumentation'].read_text().count('Link not yet recovered') == 3
assert '[Join the meeting (historical link)](https://teams.microsoft.com/' in pages['TAP-PTP-Servos'].read_text()
print(f'PASS: {len(pages)} Markdown files, local links, 168 recording rows, 35 PTM rows, Wireless TimeSync source text, images, Regional Summit sessions, section navigation, and marked remaining gaps.')
