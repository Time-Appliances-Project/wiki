# Recovery sources

Recovered on 7 October 2026.

`original-history.xml.gz` is an unchanged MediaWiki export from the surviving public OCP staging wiki at `https://ocpstagingweb2.opencompute.org/w/`. It contains 12 TAP pages and 847 revisions. The newest recovered revision is dated 22 February 2023. The export retains original contributor names, edit summaries, and timestamps; it contains no account passwords.

`history-manifest.json` records page coverage, revision counts, image sources, and checksums. The staging server's TLS certificate had expired at recovery time. The read-only recovery command explicitly bypassed certificate verification for this public source only.

`snapshots/` contains compressed copies of the current OCP pages used to restore more recent content. These snapshots are audit inputs, not executable site files.

`seed.xml` contains the prepared current pages in MediaWiki import format. The corresponding editable source files are in `../content/`. `content-manifest.json` distinguishes original recovered pages, pages converted from the current site, navigation, and missing-page placeholders.

## Coverage and limitations

- Original TAP pages: 12, with 847 historical revisions.
- Recovered image files: 2.
- Current main-page workstreams: 14.
- Past project-call entries: 168, spanning July 2020 through September 2026.
- Upcoming call: 169, dated 7 October 2026 in the source.
- Additional current content: Open Atomic Ethernet, Open Time Server Cluster, Unified Intelligent Infrastructure, and Time Synchronization Industry-Academia.
- Missing original source: Wireless TimeSync, PTM Readiness, Lunar Timekeeping System, and the 2023 OCP Regional Summit TAP page. These pages have explicit notices.
- Revisions after February 2023 were not recovered. The current site supplies current content, not the intervening revision history.
- Linked slides, recordings, specifications, and repositories remain external links. They are not backed up here.

Formatting and internal links were adapted in the prepared pages. Punctuation was normalized there; the compressed historical export remains unchanged. Historical page content may contain old workstream numbers and contact information.

## Attribution

OCP wiki content is attributed to the Open Compute Project Foundation and its contributors. The original wiki Main Page states Creative Commons Attribution 4.0 International, copyright 2018 Open Compute Project Foundation. See [the source licensing page](https://www.opencompute.org/wiki/Main_Page) and [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

Linked specifications, presentations, software, logos, and other third-party works retain their respective terms. No trademark rights are granted by the text license.
