## Recovery coverage

Recovered on 7 October 2026 from public OCP sources.

- **12 original pages and 847 historical revisions** recovered from the surviving OCP staging wiki. The latest recovered revision is 22 February 2023.
- Current main TAP content, including 14 workstreams and all 168 past-call entries, recovered from the current OCP site.
- Current content for Open Atomic Ethernet, Open Time Server Cluster, Unified Intelligent Infrastructure, and Time Synchronization Industry-Academia.
- Two original images recovered. Slides, videos, specifications, and software remain external links.

The source export is retained unchanged in the [recovery archive](https://github.com/Time-Appliances-Project/wiki/tree/main/migration), with contributor names, timestamps, and edit summaries. The 847 historical revisions are archived MediaWiki history, not GitHub page-history entries. GitHub Wiki history begins with this migration.

## Additional recovery: PTM readiness

On 25 October 2026, all 35 hardware rows and the project team were restored to [PTM Readiness](PTM-Readiness) from the [3 August 2025 archived OCP page](https://web.archive.org/web/20250803162843/https://www.opencompute.org/wiki/PTM_Readiness). The page identifies revision 80269, last edited 1 July 2025. Table values are preserved as historical reports. Its full revision history and any subsequent updates remain unavailable.

The initial MediaWiki seed and content manifest retain the original 7 October recovery state, which predates this additional GitHub Wiki recovery. The additional source and checksums are in [the PTM recovery manifest](https://github.com/Time-Appliances-Project/wiki/blob/main/migration/ptm-readiness-recovery.json).

## Additional recovery: Wireless TimeSync

On 25 October 2026, the purpose, three objectives, and three project-team entries were restored to [Wireless TimeSync](Wireless-TimeSync) from indexed text of the original OCP page, revision 75153. Its Documents, Regular Project Calls, and Recording from Past Calls headings had no entries in that source text. The revision date, contact destinations, images, raw HTML, and full history were not recovered. [The recovery manifest](https://github.com/Time-Appliances-Project/wiki/blob/main/migration/wireless-timesync-recovery.json) records this evidence and its limits. The initial MediaWiki seed retains the earlier placeholder.

## Missing sources

The original source for these pages was not found. Their former URLs now redirect to the general OCP TAP page, and the pages are absent from the surviving February 2023 snapshot:

- [Lunar Timekeeping System](Lunar-Timekeeping-System)
- [2023 OCP Regional Summit TAP page](TAP-2023-OCP-Regional-Summit)

They are marked as incomplete. Saved page copies or MediaWiki exports can be supplied to a repository maintainer for recovery.

## Changes during migration

Recovered content was converted to Markdown, internal links were updated, merged table cells were expanded, and punctuation was normalized. The original single-page structure is restored, including the contents list, workstreams, documents, meetings, and complete past-call table. Former topic and year URLs link to sections on the main page. The missing speaker cell for call 19 was left blank so its slides remain in the correct column.

Revisions after February 2023 were not recovered. Current OCP pages supply recent content, not the intervening revision history. Historical workstream pages may contain old contact information and numbering. Meeting schedules and future-call labels reflect the source snapshot and should be maintained by contributors.

## Sources and attribution

- [Current OCP TAP site](https://www.opencompute.org/projects/time-appliances-project-tap/)
- [Surviving staging wiki](https://ocpstagingweb2.opencompute.org/wiki/Time_Appliances_Project)
- [Detailed source manifest](https://github.com/Time-Appliances-Project/wiki/blob/main/migration/content-manifest.json)
- [Copyright and licensing](Copyrights)
