#!/usr/bin/env python3
"""Validate the initial GitHub Wiki migration snapshot without dependencies."""
from pathlib import Path
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
    if name.startswith('Recordings-'):
        rows = [line for line in text.splitlines() if re.match(r'^\| #\d+', line)]
        for row in rows:
            assert len(re.split(r'(?<!\\)\|', row)) == 7, (name, row)
        numbers += [int(n) for n in re.findall(r'^\| #(\d+)', text, re.M)]
assert sorted(numbers) == list(range(1, 169)), 'Recording rows missing or duplicated'
for name in ('Wireless-TimeSync', 'PTM-Readiness', 'Lunar-Timekeeping-System', 'TAP-2023-OCP-Regional-Summit'):
    assert 'original source has not yet been recovered' in pages[name].read_text()
for image in (root / 'migration/uploads').iterdir():
    assert image.read_bytes() == (root / 'wiki/images' / image.name).read_bytes()
print(f'PASS: {len(pages)} Markdown files, local link targets, 168 recording rows, images, and four marked gaps.')
