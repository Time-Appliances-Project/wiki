#!/usr/bin/env python3
"""Build reviewable wikitext and a MediaWiki import from saved public sources."""
import gzip
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urljoin, urlparse, parse_qs, unquote
from bs4 import BeautifulSoup, NavigableString, Comment

ROOT = Path(__file__).resolve().parents[1]
MIGRATION = ROOT / 'migration'
SOURCE = MIGRATION / 'source'
CONTENT = ROOT / 'content'
CURRENT = 'https://www.opencompute.org/projects/time-appliances-project-tap/'
STAMP = '2026-10-07T12:00:00Z'
PAGES = {}
PROVENANCE = {}


def read_source(name):
    path = SOURCE / name
    if path.exists():
        return path.read_text()
    return gzip.decompress((MIGRATION / 'snapshots' / (name + '.gz')).read_bytes()).decode()


def wiki_title(url):
    u = urlparse(urljoin(CURRENT, url))
    if u.hostname not in ('www.opencompute.org', 'opencompute.org',
                          'ocpstagingweb2.opencompute.org', 'staging2.opencompute.org'):
        return None
    title = None
    if u.path.startswith('/wiki/'):
        title = unquote(u.path[6:])
    elif u.path == '/w/index.php':
        title = parse_qs(u.query).get('title', [None])[0]
    if title:
        return title.replace('_', ' ') + (('#' + unquote(u.fragment)) if u.fragment else '')
    return None


def children(node):
    return ''.join(convert(child) for child in node.children)


def convert(node):
    if isinstance(node, Comment):
        return ''
    if isinstance(node, NavigableString):
        return str(node).replace('\xa0', ' ').replace('\u2014', ', ')
    name = node.name
    if name in ('script', 'style', 'iframe'):
        return ''
    if name in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
        text = node.get_text(' ', strip=True)
        if text == 'Resources':
            return ''
        marks = '=' * max(2, int(name[1]) - 1)
        return f'\n\n{marks} {text} {marks}\n\n'
    if name == 'a':
        label = children(node).strip()
        href = node.get('href', '')
        if not href:
            return label
        if '/cdn-cgi/l/email-protection#' in href:
            try:
                data = bytes.fromhex(href.split('#')[1])
                href = 'mailto:' + bytes(b ^ data[0] for b in data[1:]).decode()
            except (ValueError, UnicodeError):
                return label
        title = wiki_title(href)
        if title:
            return f'[[{title}|{label}]]'
        return f'[{urljoin(CURRENT, href)} {label}]'
    if name in ('b', 'strong'):
        return "'''" + children(node) + "'''"
    if name in ('i', 'em'):
        return "''" + children(node) + "''"
    if name == 'br':
        return '<br />'
    if name == 'img':
        src = node.get('src', '')
        if 'Screenshot_2020-07-01_16.35.12' in src:
            return '[[File:Screenshot 2020-07-01 16.35.12.png|right|180px|Time Appliances Project]]\n'
        return f'[{urljoin(CURRENT, src)} {node.get("alt") or "Source image"}]'
    if name == 'table':
        rows = ['\n{| class="wikitable sortable"']
        for row in node.find_all('tr', recursive=True):
            rows.append('|-')
            for cell in row.find_all(['th', 'td'], recursive=False):
                mark = '!' if cell.name == 'th' else '|'
                attrs = ' '.join(f'{a}="{cell[a]}"' for a in ('rowspan', 'colspan') if cell.has_attr(a))
                value = re.sub(r'\s*\n\s*', ' ', children(cell).strip())
                rows.append(f'{mark} ' + (attrs + ' | ' if attrs else '') + value)
        return '\n'.join(rows) + '\n|}\n\n'
    if name in ('ul', 'ol'):
        mark = '*' if name == 'ul' else '#'
        return '\n' + '\n'.join(mark + ' ' + children(li).strip()
                                 for li in node.find_all('li', recursive=False)) + '\n\n'
    if name == 'p':
        value = children(node).strip()
        value = re.sub(r'(^|\n)\s*[\u2013-] ', r'\1* ', value)
        return value + '\n\n'
    if name == 'blockquote':
        return '<blockquote>' + children(node).strip() + '</blockquote>\n\n'
    if name == 'hr':
        return '\n----\n'
    return children(node)


def clean(text):
    text = text.replace('\u2014', ', ')
    text = '\n'.join(line.rstrip() for line in text.splitlines())
    return re.sub(r'\n{3,}', '\n\n', text).strip() + '\n'


def localize(text):
    def replace(match):
        url, label = match.group(1), match.group(2)
        title = wiki_title(url)
        return f'[[{title}|{label or title}]]' if title else match.group(0)
    return re.sub(r'\[(https?://[^\s\]]+)(?:\s+([^\]]+))?\]', replace, text)


def add(title, text, source, status):
    PAGES[title] = clean(text)
    PROVENANCE[title] = {'source': source, 'status': status}


def main():
    CONTENT.mkdir(exist_ok=True)
    history = ET.fromstring(gzip.decompress((MIGRATION / 'original-history.xml.gz').read_bytes()))
    for page in history.findall('{*}page'):
        title = page.findtext('{*}title')
        latest = max(page.findall('{*}revision'), key=lambda r: r.findtext('{*}timestamp'))
        text = latest.findtext('{*}text') or ''
        if not text.lstrip().upper().startswith('#REDIRECT'):
            text = "''Recovered from the OCP wiki snapshot dated " + latest.findtext('{*}timestamp')[:10] + ". See [[TAP:Restoration notes]] for coverage.''\n\n" + text
        add(title, localize(text), 'original-history.xml.gz', 'recovered original wikitext')

    soup = BeautifulSoup(read_source('current-tap.html'), 'html.parser')
    article = soup.select_one('article .entry-content')
    start = next(p for p in article.find_all('p') if p.get_text().startswith('Welcome to the OCP'))
    nodes = [start, *start.next_siblings]
    text = '== Welcome ==\n\n' + ''.join(convert(n) for n in nodes)
    # Recover familiar navigation and current leadership without stale employer data.
    leadership = '\n== Project Leadership ==\n\n'
    for lead in soup.select('.single-project-hero__leads'):
        label = lead.select_one('.single-project-hero__leads-label').get_text(' ', strip=True)
        leadership += '* ' + label + ': ' + ', '.join(convert(a) for a in lead.find_all('a')) + '\n'
    text = text.replace('== Liaisons ==', leadership + '\n== Liaisons ==')
    involvement = "\n== Get Involved ==\n\n* [https://ocp-all.groups.io/g/ocp-tap TAP mailing list]\n* [https://ocp-calendar.pages.dev/ Time Appliances calendar]\n* [https://github.com/Time-Appliances-Project TAP repositories]\n"
    text = text.replace('== Documents ==', involvement + '\n== Documents ==')
    add('Time Appliances Project', text, CURRENT, 'current OCP content converted to editable wikitext')

    records = json.loads((MIGRATION / 'source-manifest.json').read_text())
    for record in records:
        if record['status'] != '200' or record['resolved_url'].rstrip('/') == CURRENT.rstrip('/'):
            continue
        title = record['title'].replace('_', ' ')
        page = BeautifulSoup(read_source(Path(record['file']).name), 'html.parser')
        block = page.select_one('article .entry-content')
        if not block or len(block.get_text(strip=True)) < 50:
            block = page.select_one('.project-about__body')
        add(title, '[[Time Appliances Project|Back to TAP]]\n\n' + convert(block),
            record['resolved_url'], 'current OCP content converted to editable wikitext')

    missing = {
        'Wireless TimeSync': 'Precision Time Synchronization over Wireless',
        'PTM Readiness': 'Precision Time Measurement Readiness Status',
        'Lunar Timekeeping System': 'Lunar Timekeeping System (LTS)',
        'TAP 2023 OCP Regional Summit': '2023 OCP Regional Summit TAP track',
    }
    for title, label in missing.items():
        url = 'https://www.opencompute.org/wiki/' + title.replace(' ', '_')
        add(title, f'[[Time Appliances Project|Back to TAP]]\n\n== {label} ==\n\n'
            "This page's original source has not yet been recovered. Its former OCP URL now redirects to the general TAP page. "
            'It is not present in the recovered February 2023 snapshot.\n\n'
            f'[{url} Former page URL]\n\n'
            'If you have a saved copy or MediaWiki export, an administrator can restore it using [[Special:Import]].\n',
            url, 'missing source; explicitly marked placeholder')
    add('TAP Data Center PTP Profile', '#REDIRECT [[TAP PTP Profile]]', 'restoration', 'alias')
    add('Main Page', '#REDIRECT [[Time Appliances Project]]', 'restoration', 'navigation')
    add('MediaWiki:Mainpage', 'Time Appliances Project', 'restoration', 'navigation')
    add('MediaWiki:Sidebar', '''* navigation
** Time Appliances Project|TAP home
** Time Appliances Project#Workstreams|Workstreams
** Time Appliances Project#Regular_Project_Calls|Project calls
** Time Appliances Project#Recordings_from_Past_Calls|Recordings
** Help:Editing|How to edit
** TAP:Restoration notes|Restoration notes
** Special:RecentChanges|Recent changes
* SEARCH
* TOOLBOX
* LANGUAGES
''', 'restoration', 'navigation')
    add('Help:Editing', '''== Edit a page ==
Log in, open a page, and select Edit or Edit source. Each section also has its own edit link. Add a short edit summary and save. History lets you compare revisions and undo changes.

== Accounts ==
Reading is public. Editing requires an account. Administrators create contributor accounts at [[Special:CreateAccount]]. Password reset by email is not configured; contact an administrator if you need a reset.

== Add a meeting ==
On [[Time Appliances Project]], edit Upcoming Calls or Recordings from Past Calls. Copy an existing table row and replace the number, date, title, speaker, recording URL, and slide URL. Use Show preview before saving.

== Add a page or attachment ==
Search for the new page title, then follow the creation link. Upload permitted attachments at [[Special:Upload]] and link them using <nowiki>[[File:example.pdf]]</nowiki>.

== Formatting ==
* Section: <nowiki>== Section title ==</nowiki>
* Local link: <nowiki>[[Page title|Link label]]</nowiki>
* External link: <nowiki>[https://example.org Link label]</nowiki>
* List: start each line with <nowiki>*</nowiki>.

Edits are stored immediately in the wiki database. The repository contains the initial recovery and deployment files, not a live copy of subsequent edits. Administrators should run the backup script regularly.
''', 'restoration', 'editor guidance')
    add('TAP:Copyrights', '''Recovered OCP wiki content is attributed to the Open Compute Project Foundation and its contributors. The original wiki Main Page states Creative Commons Attribution 4.0 International, copyright 2018 Open Compute Project Foundation.

* [https://creativecommons.org/licenses/by/4.0/ License terms]
* [https://www.opencompute.org/wiki/Main_Page Original licensing page]
* [[TAP:Restoration notes|Recovery sources and changes]]

The restored site preserves contributor attribution in imported revision history. Current pages have been reformatted and internal links updated. Linked specifications, presentations, software, logos, and other third-party works retain their own terms. The content license does not grant trademark rights.
''', 'OCP wiki Main Page', 'source attribution')

    total_revisions = sum(len(p.findall('{*}revision')) for p in history.findall('{*}page'))
    add('TAP:Restoration notes', f'''== Recovery coverage ==
Recovered on 7 October 2026 from public OCP sources.

* {len(history.findall('{*}page'))} original pages and {total_revisions} historical revisions from the surviving OCP staging wiki. The latest recovered revision is 22 February 2023.
* Main TAP page updated from the current OCP site, including 14 workstreams, 168 past-call rows, and upcoming call 169.
* Current resources recovered for Open Atomic Ethernet, Open Time Server Cluster, Unified Intelligent Infrastructure, and Time Synchronization Industry-Academia.
* Two original image files recovered. External slides, videos, documents, and source repositories remain links.

The 2023 snapshot does not contain later revisions. Missing pages are clearly marked, not represented as restored. Existing recovered workstream pages may contain historical contact information or numbering.

== Missing pages ==
* [[Wireless TimeSync]]
* [[PTM Readiness]]
* [[Lunar Timekeeping System]]
* [[TAP 2023 OCP Regional Summit]]

== Changes during migration ==
Source text was converted to editable wikitext where necessary. Old OCP wiki links now point to local pages. Punctuation was normalized. The original historical export is retained separately, unchanged. Imported contributors are prefixed with ocp to distinguish historical identities from accounts on this wiki.

== Sources ==
* [{CURRENT} Current OCP TAP page]
* [https://ocpstagingweb2.opencompute.org/wiki/Time_Appliances_Project Surviving staging wiki]
* [https://github.com/Time-Appliances-Project/wiki Repository and recovery manifest]
''', 'restoration', 'recovery scope')

    manifest = []
    nsmap = {'MediaWiki': 8, 'Help': 12, 'TAP': 4}
    export = ET.Element('mediawiki', {'xmlns': 'http://www.mediawiki.org/xml/export-0.11/',
                                     'version': '0.11', 'xml:lang': 'en'})
    for title, text in sorted(PAGES.items()):
        filename = title.replace(' ', '_').replace(':', '__') + '.wiki'
        (CONTENT / filename).write_text(text)
        manifest.append({'title': title, 'file': filename, **PROVENANCE[title]})
        page = ET.SubElement(export, 'page')
        ET.SubElement(page, 'title').text = title
        ET.SubElement(page, 'ns').text = str(nsmap.get(title.split(':')[0], 0))
        revision = ET.SubElement(page, 'revision')
        ET.SubElement(revision, 'timestamp').text = STAMP
        contributor = ET.SubElement(revision, 'contributor')
        ET.SubElement(contributor, 'username').text = 'TAP migration'
        ET.SubElement(revision, 'comment').text = 'Restore editable TAP content; sources documented in TAP:Restoration notes'
        model = 'wikitext'
        ET.SubElement(revision, 'model').text = model
        ET.SubElement(revision, 'format').text = 'text/x-wiki'
        ET.SubElement(revision, 'text', {'xml:space': 'preserve'}).text = text
    ET.ElementTree(export).write(MIGRATION / 'seed.xml', encoding='utf-8', xml_declaration=True)
    (MIGRATION / 'content-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    # Compact audit snapshots, never served by the wiki web server.
    current_sources = [SOURCE / 'current-tap.html'] + [ROOT / r['file'] for r in records
        if r['resolved_url'].rstrip('/') != CURRENT.rstrip('/') and r['status'] == '200']
    snapshot_dir = MIGRATION / 'snapshots'
    snapshot_dir.mkdir(exist_ok=True)
    for source in current_sources:
        if not source.exists():
            continue
        with gzip.GzipFile(filename=str(snapshot_dir / (source.name + '.gz')), mode='wb', mtime=0) as f:
            f.write(source.read_bytes())
    print(f'Prepared {len(PAGES)} wiki pages and {total_revisions} original historical revisions.')


if __name__ == '__main__':
    main()
