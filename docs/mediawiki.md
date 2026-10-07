# Optional MediaWiki deployment

The live TAP wiki is hosted entirely on [GitHub Wiki](https://github.com/Time-Appliances-Project/wiki/wiki). These instructions are optional, for running a separate MediaWiki copy of the recovery archive.

The restoration includes 12 original pages and 847 historical revisions through February 2023, plus current TAP content recovered on 7 October 2026. The main page includes all 168 past-call entries and 14 workstreams. Four missing source pages are clearly identified. See [recovery coverage](../migration/README.md).

## Run MediaWiki

Requires Docker with Docker Compose and Python 3 for credential generation.

```sh
git clone https://github.com/Time-Appliances-Project/wiki.git
cd wiki
python3 scripts/configure.py
docker compose up -d --build
```

Open <http://localhost:8088>. Initial startup creates the database and imports the recovered history and current pages. It may take a few minutes. Check progress with `docker compose logs -f wiki`.

Log in as `TapAdmin` with the `MW_ADMIN_PASSWORD` stored in your local `.env`. This file is private and excluded from Git. Use **Edit** or **Edit source** on a page, or the edit link beside a section. Administrators can create contributor accounts at **Special:CreateAccount**. Reading is public; editing is restricted to accounts created by an administrator. Email delivery is not configured.

Edits live in the database and survive container restarts. The repository is the recovery and deployment package, not a live copy of database edits. Startup imports content only once and does not overwrite later edits.

To stop the wiki, use `docker compose stop`. Start it again with `docker compose up -d`. Do not use `docker compose down -v` unless you intend to erase its database and uploaded files.

## Public hosting

GitHub stores this repository. MediaWiki itself needs a running PHP application and a persistent database. GitHub Pages cannot run it. This package uses MediaWiki 1.43.11 LTS, the classic Vector interface, the bundled visual editor, and MariaDB 10.11.

The simplest public deployment is to run this same package on an always-on machine and connect it to a hostname through Cloudflare Tunnel:

1. Run the wiki and verify local access.
2. In Cloudflare, create a tunnel and install its connector on that machine.
3. Add a published application route, such as `wiki.example.org`, with service `http://localhost:8088` when the connector runs on the host.
4. Set `MW_SERVER=https://wiki.example.org` in `.env`, then run `docker compose up -d`.
5. Open the public URL and verify login and editing. Avoid cache rules that cache HTML, login, or API responses.

If the connector runs in a separate container, `localhost` refers to that container. Join it to the wiki's Docker network and use `http://wiki:80` instead. Keep tunnel credentials outside Git. The wiki becomes unavailable whenever its host or connector stops.

See [Cloudflare Tunnel setup](https://developers.cloudflare.com/tunnel/get-started/) and [MediaWiki maintenance](https://www.mediawiki.org/wiki/Manual:Maintaining_a_MediaWiki_installation).

## Backups and updates

```sh
python3 scripts/backup.py
```

The backup script briefly stops the wiki, saves its database, configuration, uploads, and `.env`, then restarts it. Backups are placed in `backups/`, which is excluded from Git. They contain credentials and must be stored privately. Copy completed backups to a different machine or private storage. See [restore instructions](restore.md).

Before upgrading MediaWiki, create a backup. Update its version in `Dockerfile`, rebuild, and run `docker compose exec wiki php maintenance/run.php update --quick`. Review MediaWiki's release notes and supported versions before upgrading. No scheduled upgrades or backups are enabled automatically.

## Recovery files

- `content/`: prepared MediaWiki source, one file per page.
- `migration/original-history.xml.gz`: original historical export, unchanged.
- `migration/seed.xml`: current content for the initial import.
- `migration/uploads/`: recovered images.
- `migration/*-manifest.json`: sources, coverage, and checksums.
- `scripts/validate_recovery.py`: offline archive and meeting-coverage checks.

Run `python3 scripts/validate_recovery.py` to verify the recovery package. `scripts/recover.py` re-fetches the surviving staging export; it is not needed to run the wiki. `scripts/build_content.py` was used for the one-time conversion, requires Beautiful Soup 4, and reads the saved snapshots. Rebuilding these initial pages does not publish edits to a running wiki.

## Attribution

Recovered OCP wiki content is attributed to the Open Compute Project Foundation and its contributors under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), as stated on the original wiki Main Page. Imported history preserves contributor attribution, with an `ocp` prefix distinguishing historical identities from local accounts. See [source details and licensing](../migration/README.md). Linked documents, software, and logos retain their respective terms.
