# The User, Plural — workshop website

A responsive website for **The User, Plural: Heterogeneity and Interaction in User Simulation**, a one-day workshop co-located with COLING 2027 in Macau, China. Eight static HTML pages share a stylesheet, self-hosted fonts, and a small JavaScript navigation enhancement. There is no build step, package installation, or runtime dependency, and the content remains available without JavaScript.

- Repository: [UserPlural/userplural.github.io](https://github.com/UserPlural/userplural.github.io)
- Live website: [userplural.github.io](https://userplural.github.io/)
- Official workshop contact: [theuserplural@gmail.com](mailto:theuserplural@gmail.com)

The repository has been renamed to `userplural.github.io` and serves the root address above. GitHub Pages uses branch publication: changes merged or committed to the `main` branch at the repository root publish automatically. Keep that configuration unless deliberately switching to the optional manual Actions workflow below.

## Content and status

The website's scientific content has been compared with the accepted proposal. It retains the proposal's four research directions, emphasis on interactional fidelity and user heterogeneity, fit-for-purpose validity, and scope boundary. The workshop includes offline and interactive uses of user simulation. Multi-agent work is in scope when its primary object is user behavior or user-facing AI; macro-scale social simulation is outside the scope.

The workshop accepts both archival and non-archival submissions and supports hybrid in-person and online presentation and attendance, as confirmed by the organizers. Paper preparation and review follow the linked ACL/ARR requirements. Direct submissions and ARR commitments through OpenReview are accepted routes; the workshop-specific portal URL will be announced when ready. All unconfirmed workshop dates remain TBD. May 9–14, 2027 refers to the COLING conference, not the workshop day. The program, final speaker lineup, and reviewer application form will be announced separately. The reviewer roster is not published at this stage. No sponsorship arrangements have been announced.

## Files and editing

| File | Purpose |
| --- | --- |
| `index.html` | Workshop home, overview, and latest status |
| `themes.html` | Research themes and scientific scope |
| `cfp.html` | Call for papers and its preparation status |
| `dates.html` | Important dates: unconfirmed milestones are TBD |
| `submissions.html` | Submission information and portal status |
| `program.html` | Program and speaker announcements |
| `organizers.html` | Organizer portraits and reviewer invitation |
| `contact.html` | Official workshop contact details |
| `assets/styles.css` | Layout, typography, responsive behavior, and print styles |
| `assets/site.js` | Navigation menu and organizer bio dialog |
| `assets/favicon.svg` | Browser icon |
| `assets/fonts/` | Self-hosted Newsreader and Atkinson Hyperlegible Next, with their SIL Open Font License files |
| `assets/` | Shared public assets, including approved images when present |
| `.nojekyll` | Direct static-file publication |
| `website/*.html` | Redirects from the eight former `/website/` page addresses |
| `scripts/check_site.py` | Offline link and asset check; requires Python 3 |
| `.github/workflows/pages.yml` | Optional manually triggered publication workflow |

Edit the relevant HTML file directly; no build step follows. Keep shared navigation, the workshop title, contact details, and footer information consistent across the eight pages. The official contact address is `theuserplural@gmail.com`. When confirming information, update its status label, associated date or link, and explanatory note everywhere that information appears. Add the workshop-specific OpenReview URL only when it is ready. Preserve the accepted proposal's scientific framing when editing the overview and research themes.

Use relative links such as `themes.html` and `assets/styles.css`. Keep all eight content pages in the repository root, where they serve directly from `https://userplural.github.io/`. The optional publication workflow lists those pages explicitly and copies the entire audited `assets/` directory and the `website/` redirects. When adding another page, update that allowlist, the navigation, and the validation script as needed. Keep image credits and license notices with any approved photographs.

## Design

Headings use Newsreader; body text and navigation use Atkinson Hyperlegible Next, a typeface designed for legibility. Both are served from `assets/fonts/` rather than a font CDN, so pages load fully without third-party requests. Colors and type sizes are defined once at the top of `assets/styles.css`.

The homepage illustration is an inline SVG in `index.html`. It is an illustration, not data: interactions that start from the same point diverge as users clarify, change goals, or leave, while a dashed line marks the “average” user. Its lines draw in once on page load; the animation is skipped for visitors who prefer reduced motion.

## Preview and check

From the repository root:

```sh
python3 scripts/check_site.py
python3 -m http.server 8000
```

Open [localhost:8000](http://localhost:8000/), serving from the repository root. Stop the server with Control-C. The local clone directory can retain its current name; it does not determine the published address. The pages inside `website/` deliberately redirect to the absolute production URLs, including during a local preview.

Inspect every page at phone and desktop widths, including navigation, keyboard focus, links between pages, and content. The script checks required files, duplicate IDs, local assets, internal anchors, relative paths, and obvious placeholder links. It does not verify external services or workshop facts.

## Root address and former links

The repository was renamed from `website` to `userplural.github.io`, preserving its history. GitHub requires the `<owner>.github.io` repository name for an account's root site. [GitHub Pages URL conventions](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages).

If a local clone still uses the old remote, update it with `git remote set-url origin https://github.com/UserPlural/userplural.github.io.git`. The local directory itself does not need to be renamed. The required Pages source remains **Deploy from a branch → main → /(root)**.

GitHub does not automatically redirect renamed project-site URLs. The eight pages in `website/` provide explicit HTML redirects from the old `/website/` addresses to the corresponding root pages, with visible fallback links. Keep them to preserve existing bookmarks. Do not recreate a separate repository named `website` for this purpose; doing so would remove GitHub's redirect for the renamed repository itself. [GitHub repository rename behavior](https://docs.github.com/en/repositories/creating-and-managing-repositories/renaming-a-repository).

## Update the live site from the `main` branch

1. Edit the relevant root HTML pages and shared assets in [UserPlural/userplural.github.io](https://github.com/UserPlural/userplural.github.io), preview them, and commit or merge the changes to `main`. Keep all eight content pages, `assets/`, `website/`, and `.nojekyll` at the repository root. Only the compatibility redirects belong inside `website/`; do not nest the full site in an enclosing folder. The README, validation script, and optional workflow can also live in the repository. [GitHub site setup](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site).
2. The existing [Settings → Pages](https://github.com/UserPlural/userplural.github.io/settings/pages) configuration should remain **Source → Deploy from a branch**, **main**, **/(root)**. No settings change is required for a normal content update. If restoring the configuration, select those values and **Save**. [GitHub publishing-source instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).
3. Follow the deployment in [Actions](https://github.com/UserPlural/userplural.github.io/actions). Once it succeeds, open [https://userplural.github.io/](https://userplural.github.io/). Check all eight pages, styles, images, favicon, mobile navigation, the official contact link, and redirects from the old `/website/` addresses. GitHub says publication can take up to ten minutes. [GitHub publication and verification](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site).

The `userplural.github.io` repository serves the account's root address without a repository-name path. A future custom domain may change that address. [GitHub Pages URL conventions](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages).

Keep only intended public material in this repository. `.nojekyll` disables Jekyll processing; it does not hide other files. [GitHub static-file publishing](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site).

## Optional manual Actions publication

Use this alternative if maintainers prefer to publish each update explicitly. The included workflow stages the eight root HTML pages, the audited `assets/` directory, the `website/` redirects, and `.nojekyll`. It excludes the README, validation script, and other repository files from the deployed artifact.

1. Commit the site files, `scripts/check_site.py`, and `.github/workflows/pages.yml` to `main`.
2. In [Settings → Pages](https://github.com/UserPlural/userplural.github.io/settings/pages), set **Source → GitHub Actions** instead of branch publication.
3. Open **Actions → Publish workshop website → Run workflow**, choose `main`, and run it. The workflow has no push trigger and only publishes from the default branch.
4. Follow the deployment link and verify the live site. Run the workflow again when each subsequent content update is ready to publish.

The workflow uses GitHub's Pages actions and the `github-pages` environment. If the organization requires approval for that environment, use its existing review process. [GitHub custom workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

## Photographs

The homepage photograph is [Macau skyline from Taipa (2013)](https://commons.wikimedia.org/wiki/File:Macau_skyline_2013_(panorama).JPG), by [Mimihitam](https://commons.wikimedia.org/wiki/User:Mimihitam), licensed under [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/). The original file is included without modification and scaled proportionally for display. Preserve its visible attribution and `assets/photo-credit.txt`. This license applies to the photograph.

Organizer portraits are copied from each organizer’s official profile, as requested by the workshop organizers. Each organizer’s bio sits in their card in `organizers.html`; with JavaScript, **Read bio** opens it in a dialog, and without JavaScript it shows inline. Preserve the profile links and the source records in `assets/organizers/sources.txt`; no reuse license is asserted for those portraits.

Submission guidance follows the current [ARR call](https://aclrollingreview.org/cfp), [ACL formatting requirements](https://acl-org.github.io/ACLPUB/formatting.html), [official templates](https://github.com/acl-org/acl-style-files), [Responsible NLP checklist](https://aclrollingreview.org/responsibleNLPresearch/), and [ARR commitment guidance](https://aclrollingreview.org/authors#step-5-commitment). Maintain those links when requirements change. Ensure the direct-submission form includes the checklist fields.

Deployment guidance checked against GitHub documentation on October 14, 2026.
