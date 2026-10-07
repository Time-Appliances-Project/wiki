# Time Appliances Project wiki

**[Open the TAP wiki](https://github.com/Time-Appliances-Project/wiki/wiki)**

The TAP community wiki is hosted and edited directly on GitHub. No server, Docker, Cloudflare account, or deployment is needed for normal use.

## Read and edit

- [Project overview](https://github.com/Time-Appliances-Project/wiki/wiki/Project-overview)
- [Workstreams](https://github.com/Time-Appliances-Project/wiki/wiki/Workstreams)
- [Meetings](https://github.com/Time-Appliances-Project/wiki/wiki/Meetings)
- [Recordings](https://github.com/Time-Appliances-Project/wiki/wiki/Recordings)
- [Documents](https://github.com/Time-Appliances-Project/wiki/wiki/Documents)
- [How to edit](https://github.com/Time-Appliances-Project/wiki/wiki/Editing)

Sign in to GitHub, open a wiki page, click **Edit**, make the change, preview it, and click **Save page**. Repository collaborators with write access can edit and create pages. Reading is public. GitHub keeps the history of edits made since this migration.

The long original TAP page is organized into topic pages and recordings by year. The restored recording archive includes all 168 past-call entries listed by OCP on 7 October 2026. Four pages with missing source material are explicitly marked. See [restoration notes](https://github.com/Time-Appliances-Project/wiki/wiki/Restoration-notes).

## Live wiki and recovery repository

The **live wiki** is a separate Git repository. Browser edits are saved there immediately. Clone or pull it to back up the current pages and their history:

```sh
git clone https://github.com/Time-Appliances-Project/wiki.wiki.git
```

This **main repository** stores the initial migration snapshot and the recovery materials:

| Location | Purpose |
| --- | --- |
| `wiki/` | Initial GitHub Wiki Markdown and image snapshot |
| `content/` | Prepared MediaWiki source for the recovered pages |
| `migration/original-history.xml.gz` | Unchanged original export with 12 pages and 847 historical revisions |
| `migration/snapshots/` | Current OCP pages used during recovery |
| `migration/*-manifest.json` | Source coverage and checksums |

The 847 recovered revisions are archived MediaWiki history, not entries in GitHub's page history. Later original revisions were not recovered. Linked videos, slides, specifications, and repositories remain external links.

The `wiki/` snapshot does **not** automatically track subsequent browser edits. Edit the live Wiki for ordinary maintenance. Do not push the initial snapshot over newer wiki changes. No scheduled synchronization or automation overwrites the live Wiki.

## Validate the migration

```sh
python3 scripts/validate_recovery.py
python3 scripts/validate_github_wiki.py
```

These checks verify archive checksums, recording coverage, image preservation, internal page targets, and marked recovery gaps. `scripts/export_github_wiki.py` is a one-time conversion tool, requires `markdownify` and `requests`, and uses a local recovery instance to render MediaWiki source. It does not publish to GitHub.

## Optional MediaWiki copy

The original MediaWiki deployment files remain available for archival portability. See [optional MediaWiki deployment](docs/mediawiki.md) if you want to run that separate copy. They are not required for the GitHub Wiki.

## Attribution

Recovered OCP wiki content is attributed to the Open Compute Project Foundation and its contributors under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), as stated on the original wiki Main Page. Contributor names, timestamps, and summaries remain in the original export. Formatting and internal links have been adapted for GitHub Wiki. Linked specifications, presentations, software, and logos retain their respective terms. See [recovery sources](migration/README.md).
