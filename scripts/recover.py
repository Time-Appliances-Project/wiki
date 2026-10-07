#!/usr/bin/env python3
"""Recover the surviving public OCP MediaWiki export. Never writes to OCP."""
import gzip
import hashlib
import json
import subprocess
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'migration'
BASE = 'https://ocpstagingweb2.opencompute.org/w/'


def request(path, params=None):
    # This public, read-only staging archive has an expired TLS certificate.
    cmd = ['curl', '--insecure', '--fail', '--silent', '--show-error',
           '--max-time', '90', BASE + path]
    for key, value in (params or {}).items():
        cmd += ['--data-urlencode', f'{key}={value}']
    return subprocess.check_output(cmd)


def api(**params):
    return json.loads(request('api.php?' + urllib.parse.urlencode(
        dict(format='json', **params))))


def main():
    DEST.mkdir(exist_ok=True)
    titles = ['Time Appliances Project', 'Time Appliance Project',
              'Time Appliances Project APIs']
    titles += [p['title'] for p in api(action='query', list='allpages',
              apprefix='TAP', aplimit=500)['query']['allpages']]
    raw = request('index.php?title=Special:Export',
                  {'pages': '\n'.join(titles), 'history': '1'})
    root = ET.fromstring(raw)
    if root.tag.split('}')[-1] != 'mediawiki':
        raise RuntimeError('Response is not a MediaWiki export')
    with gzip.GzipFile(filename=str(DEST / 'original-history.xml.gz'),
                       mode='wb', mtime=0) as f:
        f.write(raw)
    manifest = {'source': BASE, 'retrieved': '2026-10-07',
                'tls_note': 'Public staging certificate expired; read without TLS verification.',
                'sha256_uncompressed': hashlib.sha256(raw).hexdigest(), 'pages': []}
    for page in root.findall('{*}page'):
        revs = page.findall('{*}revision')
        manifest['pages'].append({'title': page.findtext('{*}title'),
            'revisions': len(revs),
            'latest': max(r.findtext('{*}timestamp') for r in revs)})
    files = api(action='query', titles='|'.join(titles), prop='images', imlimit=500)
    names = sorted({i['title'] for p in files['query']['pages'].values()
                    for i in p.get('images', [])})
    (DEST / 'uploads').mkdir(exist_ok=True)
    manifest['files'] = []
    if names:
        info = api(action='query', titles='|'.join(names), prop='imageinfo',
                   iiprop='url|sha1|size')
        for page in info['query']['pages'].values():
            if not page.get('imageinfo'):
                continue
            image = page['imageinfo'][0]
            url = image['url'].replace('https://staging2.opencompute.org/w/', BASE)
            data = subprocess.check_output(['curl', '-kfLsS', '--max-time', '30', url])
            name = page['title'].split(':', 1)[1].replace(' ', '_')
            (DEST / 'uploads' / name).write_bytes(data)
            manifest['files'].append({'title': page['title'], 'url': url,
                'file': name, 'sha256': hashlib.sha256(data).hexdigest()})
    (DEST / 'history-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
