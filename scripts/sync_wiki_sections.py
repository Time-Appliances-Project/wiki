#!/usr/bin/env python3
"""Publish editable sections into the live wiki's continuous Home page.

Only the explicitly marked regions are replaced. Always run against a fresh
checkout of the live wiki, never the recovery snapshot when publishing.
"""
import argparse
import json
import os
from pathlib import Path

SECTIONS = {
    'workstreams': 'Workstreams',
    'upcoming-calls': 'Upcoming-Calls',
    'recordings-from-past-calls': 'Recordings-from-Past-Calls',
}


def render(home, pages):
    for section, page in SECTIONS.items():
        start = f'<!-- BEGIN SECTION: {section} -->'
        end = f'<!-- END SECTION: {section} -->'
        if home.count(start) != 1 or home.count(end) != 1:
            raise ValueError(f'Missing or duplicate section markers: {section}')
        before, remainder = home.split(start)
        if end not in remainder:
            raise ValueError(f'Reversed section markers: {section}')
        _, after = remainder.split(end)
        content = pages[page].strip()
        if not content or '<!-- BEGIN SECTION:' in content or '<!-- END SECTION:' in content:
            raise ValueError(f'Empty or invalid section source: {page}')
        home = before + start + '\n\n' + content + '\n\n' + end + after
    return home


def relevant_event():
    if os.environ.get('GITHUB_EVENT_NAME') != 'gollum':
        return True
    event = json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text())
    names = {page['page_name'].replace(' ', '-') for page in event.get('pages', [])}
    return bool(names.intersection(SECTIONS.values()))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('wiki', type=Path)
    args = parser.parse_args()
    if not relevant_event():
        print('No editable-section source changed; leaving Home untouched.')
        return
    home_path = args.wiki / 'Home.md'
    home = home_path.read_text()
    pages = {page: (args.wiki / f'{page}.md').read_text() for page in SECTIONS.values()}
    updated = render(home, pages)
    if updated != home:
        home_path.write_text(updated)
        print('Updated the editable sections in Home; other content preserved.')
    else:
        print('Home already matches all editable sections.')


if __name__ == '__main__':
    main()
