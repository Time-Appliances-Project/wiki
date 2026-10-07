#!/usr/bin/env python3
"""Check the recovery archive, prepared pages, and meeting coverage offline."""
from pathlib import Path
import gzip
import hashlib
import json
import re
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1]
migration = root / 'migration'
manifest = json.loads((migration / 'history-manifest.json').read_text())
raw = gzip.decompress((migration / 'original-history.xml.gz').read_bytes())
assert hashlib.sha256(raw).hexdigest() == manifest['sha256_uncompressed']
history = ET.fromstring(raw)
assert len(history.findall('{*}page')) == len(manifest['pages']) == 12
assert len(history.findall('.//{*}revision')) == 847
for file in manifest['files']:
    assert hashlib.sha256((migration / 'uploads' / file['file']).read_bytes()).hexdigest() == file['sha256']
pages = json.loads((migration / 'content-manifest.json').read_text())
seed = ET.parse(migration / 'seed.xml')
assert len(seed.findall('{*}page')) == len(pages)
for entry in pages:
    text = (root / 'content' / entry['file']).read_text()
    assert chr(0x2014) not in text, entry['file']
    assert '/cdn-cgi/l/email-protection' not in text, entry['file']
    assert text.count('{|') == text.count('|}'), entry['file']
    node = next(p for p in seed.findall('{*}page') if p.findtext('{*}title') == entry['title'])
    assert node.findtext('{*}revision/{*}text') == text
text = (root / 'content/Time_Appliances_Project.wiki').read_text()
past = text.split('Recordings from Past Calls', 1)[1]
numbers = [int(n) for n in re.findall(r'^\| #(\d+)', past, re.M)]
assert sorted(numbers) == list(range(1, 169)), 'A past-call entry is missing or duplicated'
assert len([p for p in pages if p['status'].startswith('missing')]) == 4
print(f'PASS: {len(pages)} prepared pages, 847 archived revisions, 2 images, all 168 past calls, 4 marked gaps.')
