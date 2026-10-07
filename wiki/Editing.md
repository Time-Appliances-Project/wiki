## Edit a page

1. Sign in to GitHub using an account with write access to this repository.
2. Open the wiki page and click **Edit** in the upper-right corner.
3. Update the Markdown text and use **Preview** to check it.
4. Enter a short edit message and click **Save page**.

Changes are live immediately. Use **Page History** to compare revisions and recover earlier text. You do not need Docker, a terminal, a separate wiki account, or a website deployment.

## Edit the calls sections

The **edit** links after Upcoming Calls and Recordings from Past Calls open the GitHub editor for the entire main page. GitHub Wiki does not provide a separate section editor. Find the relevant heading in the editor, change the table below it, preview, and save.

## Add a project call

- Edit [Meetings](Home#regular-project-calls) to update the upcoming call.
- After the call, edit the [Recordings from Past Calls](Home#recordings-from-past-calls) table on the main page. Copy a row and update its index, date, topic, speaker, recording URL, and slides URL. Add the newest call at the top.
- Keep one row per line. Escape a literal vertical bar in a cell as `\|`.
- If a recording or slides are unavailable, leave their links blank rather than inventing a URL.
- Keep all years in this same table. Use your browser’s Find command to locate a call or year.

## Create a page or add an image

Click **New page**, give it a descriptive title, and save it. Add a link from the relevant workstream page or sidebar. Use the editor's attachment control for an image or document, then preview its link before saving.

## Formatting

```markdown
## Section heading
- List item
[Link to a page](Home#workstreams)
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

Pull this repository to back up current wiki edits and history. The `wiki/` directory in the main repository is a recovery snapshot and does not automatically follow browser edits. Do not republish that snapshot over newer wiki changes.
