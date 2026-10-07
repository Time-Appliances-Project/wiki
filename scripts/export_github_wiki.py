#!/usr/bin/env python3
"""One-time conversion of the recovered MediaWiki sources to GitHub Wiki Markdown.

Requires the local recovery instance at localhost:8088 and markdownify/requests.
Does not publish or overwrite the live GitHub Wiki.
"""
import copy
import json
import re
import shutil
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse, quote

import requests
from bs4 import BeautifulSoup, Comment
from markdownify import markdownify

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'wiki'
BASE = 'https://github.com/Time-Appliances-Project/wiki/wiki/'
RAW = 'https://raw.githubusercontent.com/wiki/Time-Appliances-Project/wiki/images/'
ALIASES = {
    'Time Appliances Project': 'Home', 'Time Appliance Project': 'Home',
    'Main Page': 'Home', 'Help:Editing': 'Editing',
    'TAP:Copyrights': 'Copyrights', 'TAP:Restoration notes': 'Restoration-notes',
    'TAP Data Center PTP Profile': 'TAP-PTP-Profile',
    'Time Appliances Project APIs': 'TAP-Precision-Time-APIs',
}
SECTIONS = {
    'Welcome': 'Project-overview', 'Mission Statement': 'Project-overview',
    'Project Leadership': 'Project-overview', 'Liaisons': 'Project-overview',
    'Workstreams': 'Workstreams', 'OCP Marketplace': 'Documents',
    'Get Involved': 'Project-overview', 'Documents': 'Documents',
    'Presentations & Events': 'Presentations-and-events', 'OCP Events': 'Presentations-and-events',
    'GTC': 'Presentations-and-events', 'TAP Media References': 'Media-and-references',
    'References & External Links': 'Media-and-references',
    'Regular Project Calls': 'Meetings', 'Upcoming Calls': 'Meetings',
    'Recordings from Past Calls': 'Recordings', 'Call Calendar': 'Meetings',
}


def slug(title):
    return ALIASES.get(title, title.replace(':', '-').replace(' ', '-'))


def anchor(value):
    return re.sub(r'[^\w\- ]', '', value.replace('_', ' ').lower()).replace(' ', '-')


def link(href):
    u = urlparse(href)
    if u.hostname and u.hostname not in ('localhost', '127.0.0.1'):
        return href
    if u.path.startswith('/index.php/'):
        title = unquote(u.path[len('/index.php/'):]).replace('_', ' ')
    elif u.path == '/index.php':
        title = parse_qs(u.query).get('title', [''])[0].replace('_', ' ')
    elif href.startswith('#'):
        return '#' + anchor(unquote(u.fragment))
    else:
        return href
    if title.startswith('File:'):
        return RAW + quote(title.split(':', 1)[1].replace(' ', '_'))
    if title == 'Special:Import':
        return 'Restoration-notes'
    fragment = unquote(u.fragment).replace('_', ' ')
    if title in ('Time Appliances Project', 'Time Appliance Project') and fragment in SECTIONS:
        return SECTIONS[fragment] + ('#' + anchor(fragment) if fragment != 'Recordings from Past Calls' else '')
    return slug(title) + ('#' + anchor(fragment) if fragment else '')


def normalize_tables(soup):
    """Expand row/column spans so every table is editable as plain Markdown."""
    for table in soup.find_all('table'):
        grid = []
        for row_index, row in enumerate(table.find_all('tr')):
            while len(grid) <= row_index:
                grid.append([])
            col = 0
            cells = row.find_all(['th', 'td'], recursive=False)
            # The source's call #19 omits its blank speaker cell.
            if cells and cells[0].get_text(strip=True) == '#19' and len(cells) == 4:
                blank = soup.new_tag('td')
                cells.insert(3, blank)
            for cell in cells:
                while col < len(grid[row_index]) and grid[row_index][col] is not None:
                    col += 1
                rows = int(cell.get('rowspan', 1))
                cols = int(cell.get('colspan', 1))
                for r in range(row_index, row_index + rows):
                    while len(grid) <= r:
                        grid.append([])
                    for c in range(col, col + cols):
                        while len(grid[r]) <= c:
                            grid[r].append(None)
                        grid[r][c] = copy.copy(cell)
                col += cols
        if not grid:
            continue
        width = max(map(len, grid))
        new = soup.new_tag('table')
        for index, cells in enumerate(grid):
            row = soup.new_tag('tr')
            for cell in cells + [None] * (width - len(cells)):
                out = soup.new_tag('th' if index == 0 else 'td')
                if cell is not None:
                    for child in list(cell.contents):
                        out.append(copy.copy(child))
                row.append(out)
            new.append(row)
        table.replace_with(new)


def convert(html):
    soup = BeautifulSoup(html, 'html.parser')
    for node in soup.find_all(string=lambda text: isinstance(text, Comment)):
        node.extract()
    for node in soup.select('script, style, .mw-editsection, .toc, .mw-empty-elt'):
        node.decompose()
    for node in soup.find_all('a', href=True):
        node['href'] = link(node['href'])
        node.attrs.pop('title', None)
    for node in soup.find_all('img'):
        src = unquote(node.get('src', ''))
        names = [p.name for p in (ROOT / 'migration/uploads').iterdir()]
        name = next((name for name in names if name in src), None)
        if name:
            node['src'] = RAW + quote(name)
            node['alt'] = 'Time Appliances Project' if name.startswith('Screenshot') else 'OCP TAP Tech Talk 2022'
            # Use compact native HTML for the logo; it remains editable on GitHub.
            if name.startswith('Screenshot'):
                node['width'] = '135'
                node['height'] = '129'
    for node in soup.find_all('dl'):
        node.name = 'div'
    for node in soup.find_all(['dd', 'dt']):
        node.name = 'p'
    normalize_tables(soup)
    text = markdownify(str(soup), heading_style='ATX', bullets='-',
                       strip=['span'], escape_underscores=False, table_infer_header=True)
    logo = RAW + 'Screenshot_2020-07-01_16.35.12.png'
    text = re.sub(r'\[!\[Time Appliances Project\]\([^)]*\)\]\([^)]*\)',
                  f'<img src="{logo}" alt="Time Appliances Project" width="135">', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = '\n'.join(line.rstrip() for line in text.splitlines()).strip()
    return text.replace(chr(0x2014), ', ') + '\n'


def save(name, text):
    (DEST / (name + '.md')).write_text(text.strip() + '\n')


def main():
    DEST.mkdir(exist_ok=True)
    (DEST / 'images').mkdir(exist_ok=True)
    for image in (ROOT / 'migration/uploads').iterdir():
        shutil.copy2(image, DEST / 'images' / image.name)
    manifest = json.loads((ROOT / 'migration/content-manifest.json').read_text())
    rendered = {}
    for item in manifest:
        title = item['title']
        if title.startswith('MediaWiki:') or title in ('Help:Editing', 'TAP:Restoration notes'):
            continue
        source = (ROOT / 'content' / item['file']).read_text()
        if source.startswith('#REDIRECT'):
            continue
        response = requests.post('http://localhost:8088/api.php', data={
            'action': 'parse', 'title': title, 'text': source, 'prop': 'text',
            'disabletoc': 1, 'disableeditsection': 1, 'format': 'json'}, timeout=45)
        response.raise_for_status()
        rendered[title] = response.json()['parse']['text']['*']
        if title != 'Time Appliances Project':
            result = convert(rendered[title])
            result = result.replace('an administrator can restore it using [Special:Import](Restoration-notes)',
                                    'a maintainer can recover it; see [restoration notes](Restoration-notes)')
            if title == 'TAP:Copyrights':
                result = result.replace('in imported revision history', 'in the archived MediaWiki export')
            save(slug(title), result)

    soup = BeautifulSoup(rendered['Time Appliances Project'], 'html.parser')
    root = soup.select_one('.mw-parser-output')
    groups = {}
    destination = 'Project-overview'
    for element in list(root.children):
        if getattr(element, 'name', None) in ('h2', 'h3'):
            heading = element.get_text(' ', strip=True)
            destination = SECTIONS.get(heading, destination)
        groups.setdefault(destination, []).append(str(element))
    recordings = BeautifulSoup(''.join(groups.pop('Recordings')), 'html.parser')
    table = recordings.find('table')
    rows = table.find_all('tr')
    years = {}
    for row in rows[1:]:
        cells = row.find_all(['th', 'td'], recursive=False)
        year = re.search(r'20\d\d', cells[1].get_text()).group()
        years.setdefault(year, []).append(row)
    for year, year_rows in sorted(years.items(), reverse=True):
        fragment = '<table>' + str(rows[0]) + ''.join(map(str, year_rows)) + '</table>'
        save('Recordings-' + year, f'[All recordings](Recordings) · [Meeting information](Meetings)\n\n'
             f'## {year} project calls\n\n' + convert(fragment))
    for name, parts in groups.items():
        save(name, '[TAP home](Home)\n\n' + convert(''.join(parts)))
    save('Recordings', '''TAP project-call recordings and slide links, grouped by year.

The restored archive contains all 168 past-call entries listed by OCP on 7 October 2026. A missing recording or slide link means the source did not provide one.

''' + '\n'.join(f'- [{year} recordings](Recordings-{year}) ({len(rows)} calls)'
               for year, rows in sorted(years.items(), reverse=True)) +
         '\n\n[Meeting schedule and joining information](Meetings) · [How to add a recording](Editing#add-a-project-call)\n')
    save('Home', '''# Time Appliances Project

Welcome to the TAP community wiki. The project brings together people working on precise time synchronization, timing appliances, and datacenter infrastructure.

| Explore | Contents |
| --- | --- |
| [Project overview](Project-overview) | Mission, leadership, liaisons, and getting involved |
| [Workstreams](Workstreams) | The 14 TAP workstreams and their resources |
| [Meetings](Meetings) | Schedule, upcoming calls, and joining information |
| [Recordings](Recordings) | 168 past project calls, organized by year |
| [Documents](Documents) | Specifications, reference designs, and document repositories |
| [Presentations and events](Presentations-and-events) | Summit sessions and presentations |
| [Media and references](Media-and-references) | Videos, articles, and technical references |

## Contribute

Sign in to GitHub and click **Edit** on a page to make a change. Repository collaborators with write access can edit and create pages. See [editing instructions](Editing).

## Recovery archive

This wiki was restored from public OCP sources on 7 October 2026. The original MediaWiki export, including **847 historical revisions**, is preserved in the [repository](https://github.com/Time-Appliances-Project/wiki). Four pages still need their original source recovered; see [restoration notes](Restoration-notes).

[OCP project page](https://www.opencompute.org/projects/time-appliances-project-tap/) · [TAP mailing list](https://ocp-all.groups.io/g/ocp-tap) · [TAP repositories](https://github.com/Time-Appliances-Project)
''')
    save('Editing', '''## Edit a page

1. Sign in to GitHub using an account with write access to this repository.
2. Open the wiki page and click **Edit** in the upper-right corner.
3. Update the Markdown text and use **Preview** to check it.
4. Enter a short edit message and click **Save page**.

Changes are live immediately. Use **Page History** to compare revisions and recover earlier text. You do not need Docker, a terminal, a separate wiki account, or a website deployment.

## Add a project call

- Edit [Meetings](Meetings) to update the upcoming call.
- After the call, open the appropriate year from [Recordings](Recordings), copy a table row, and update its index, date, topic, speaker, recording URL, and slides URL.
- Keep one row per line. Escape a literal vertical bar in a cell as `\\|`.
- If a recording or slides are unavailable, leave their links blank rather than inventing a URL.
- When starting a new year, create its page and add a link from Recordings.

## Create a page or add an image

Click **New page**, give it a descriptive title, and save it. Add a link from the relevant workstream page or sidebar. Use the editor's attachment control for an image or document, then preview its link before saving.

## Formatting

```markdown
## Section heading
- List item
[Link to a page](Workstreams)
[External link](https://example.org)

| Date | Topic | Speaker | Slides |
| --- | --- | --- | --- |
| Oct 7, 2026 | Topic title | Speaker name | [Slides](https://example.org) |
```

## Access and backups

Reading is public. Editing is limited to repository collaborators with write access. A repository administrator can add contributors through the repository's access settings. Do not broaden wiki editing to all GitHub users unless the project intentionally wants that policy.

The live wiki has its own Git repository, separate from the main repository:

```sh
git clone https://github.com/Time-Appliances-Project/wiki.wiki.git
```

Pull this repository to back up current wiki edits and history. The `wiki/` directory in the main repository is the initial migration snapshot and does not automatically follow browser edits. Do not republish that initial snapshot over newer wiki changes.
''')
    save('Restoration-notes', '''## Recovery coverage

Recovered on 7 October 2026 from public OCP sources.

- **12 original pages and 847 historical revisions** recovered from the surviving OCP staging wiki. The latest recovered revision is 22 February 2023.
- Current main TAP content, including 14 workstreams and all 168 past-call entries, recovered from the current OCP site.
- Current content for Open Atomic Ethernet, Open Time Server Cluster, Unified Intelligent Infrastructure, and Time Synchronization Industry-Academia.
- Two original images recovered. Slides, videos, specifications, and software remain external links.

The source export is retained unchanged in the [recovery archive](https://github.com/Time-Appliances-Project/wiki/tree/main/migration), with contributor names, timestamps, and edit summaries. The 847 historical revisions are archived MediaWiki history, not GitHub page-history entries. GitHub Wiki history begins with this migration.

## Missing sources

The original source for these pages was not found. Their former URLs now redirect to the general OCP TAP page, and the pages are absent from the surviving February 2023 snapshot:

- [Wireless TimeSync](Wireless-TimeSync)
- [PTM Readiness](PTM-Readiness)
- [Lunar Timekeeping System](Lunar-Timekeeping-System)
- [2023 OCP Regional Summit TAP page](TAP-2023-OCP-Regional-Summit)

They are marked as incomplete. Saved page copies or MediaWiki exports can be supplied to a repository maintainer for recovery.

## Changes during migration

Recovered content was converted to Markdown, internal links were updated, merged table cells were expanded, and punctuation was normalized. The long main page was divided into topic pages and recordings by year for easier editing. The missing speaker cell for call 19 was left blank so its slides remain in the correct column.

Revisions after February 2023 were not recovered. Current OCP pages supply recent content, not the intervening revision history. Historical workstream pages may contain old contact information and numbering. Meeting schedules and future-call labels reflect the source snapshot and should be maintained by contributors.

## Sources and attribution

- [Current OCP TAP site](https://www.opencompute.org/projects/time-appliances-project-tap/)
- [Surviving staging wiki](https://ocpstagingweb2.opencompute.org/wiki/Time_Appliances_Project)
- [Detailed source manifest](https://github.com/Time-Appliances-Project/wiki/blob/main/migration/content-manifest.json)
- [Copyright and licensing](Copyrights)
''')
    save('_Sidebar', '''**Time Appliances Project**

- [Home](Home)
- [Project overview](Project-overview)
- [Workstreams](Workstreams)
- [Meetings](Meetings)
- [Recordings](Recordings)
- [Documents](Documents)
- [Presentations and events](Presentations-and-events)
- [Media and references](Media-and-references)

**Contribute**

- [How to edit](Editing)
- [Restoration notes](Restoration-notes)
- [Repository](https://github.com/Time-Appliances-Project/wiki)
''')
    save('_Footer', 'OCP wiki content: Open Compute Project Foundation and contributors. '
         '[Licensing](Copyrights) · [Recovery sources](Restoration-notes) · [How to edit](Editing)')
    for title in ('Time Appliances Project', 'Time Appliance Project', 'Main Page',
                  'Time Appliances Project APIs', 'TAP Data Center PTP Profile'):
        filename = title.replace(' ', '-')
        save(filename, f'This page is available at [{slug(title)}]({slug(title)}).')
    print(f'Prepared {len(list(DEST.glob("*.md")))} Markdown files and two images.')


if __name__ == '__main__':
    main()
