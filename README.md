# The User, Plural — workshop website

A responsive, buildless website for **The User, Plural: Heterogeneity and Interaction in User Simulation**, a one-day workshop co-located with COLING 2027 in Macau, China. The website uses HTML, CSS, and a small JavaScript navigation enhancement. It needs no package installation, and its content remains available without JavaScript.

- Repository: [UserPlural/website](https://github.com/UserPlural/website)
- Expected GitHub Pages address: [userplural.github.io/website/](https://userplural.github.io/website/)

The address above is the expected project-site URL. If the site is not yet live, enable GitHub Pages using the branch-publication steps below.

## Content and status

The website's scientific content has been compared with the accepted proposal. It retains the proposal's four research directions, emphasis on interactional fidelity and user heterogeneity, fit-for-purpose validity, and scope boundary. The workshop includes offline and interactive uses of user simulation. Multi-agent work is in scope when its primary object is user behavior or user-facing AI; macro-scale social simulation is outside the scope.

Confirmed information and provisional plans have separate labels. The exact workshop day, submission URL, final submission rules, speaker lineup, and sponsorship arrangements remain unannounced. ARR commitments and direct submissions through OpenReview are planned; the workshop-specific portal URL will be announced when ready. Dates marked provisional should be checked against subsequent official COLING instructions before being announced as final.

## Files and editing

| File | Purpose |
| --- | --- |
| `index.html` | Workshop text, organizers, dates, links, and status labels |
| `assets/styles.css` | Layout, typography, responsive behavior, and print styles |
| `assets/site.js` | Navigation enhancement |
| `assets/favicon.svg` | Browser icon |
| `.nojekyll` | Direct static-file publication |
| `scripts/check_site.py` | Offline link and asset check; requires Python 3 |
| `.github/workflows/pages.yml` | Optional manually triggered publication workflow |

Edit the visible text in `index.html`; no build step follows. Named HTML comments identify the content sections. When confirming information, update its status label, associated date or link, and explanatory note together. Add the workshop-specific OpenReview URL only when it is ready. Preserve the accepted proposal's scientific framing when editing the overview and research themes.

Use relative asset paths such as `assets/styles.css`, so the site works under the `/website/` project path. When adding public files, update the publication workflow's file allowlist and the validation script as needed.

## Preview and check

From the repository root:

```sh
python3 scripts/check_site.py
python3 -m http.server 8000
```

Open [localhost:8000](http://localhost:8000/). Stop the server with Control-C. To check the project path from a clone named `website`, start the server in the clone's parent directory and open [localhost:8000/website/](http://localhost:8000/website/).

Inspect the phone and desktop layouts, navigation, keyboard focus, and content. The script checks required files, duplicate IDs, local assets, internal anchors, relative paths, and obvious placeholder links. It does not verify external services or workshop facts.

## Publish from the `main` branch

1. Place `index.html`, `assets/`, and `.nojekyll` at the root of [UserPlural/website](https://github.com/UserPlural/website), then commit them to `main`. Do not upload an enclosing `the-user-plural` directory. The README, validation script, and optional workflow can also live at the repository root. If uploading through GitHub and the file picker hides `.nojekyll`, use **Add file → Create new file** to add that empty file. [GitHub site setup](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site).
2. Open [Settings → Pages](https://github.com/UserPlural/website/settings/pages). Under **Build and deployment**, choose **Source → Deploy from a branch**, select **main** and **/(root)**, then **Save**. Subsequent commits to `main` publish automatically. [GitHub publishing-source instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).
3. Follow the deployment in [Actions](https://github.com/UserPlural/website/actions). Once it succeeds, open **Settings → Pages → Visit site**. The expected address is [https://userplural.github.io/website/](https://userplural.github.io/website/). Check that the page loads, styles and favicon appear, the mobile menu works, and navigation links reach their sections. GitHub says publication can take up to ten minutes. [GitHub publication and verification](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site).

GitHub project sites use the account name and repository name in their default address. A future custom domain may change that address. [GitHub Pages URL conventions](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages).

Keep only intended public material in this repository. `.nojekyll` disables Jekyll processing; it does not hide other files. [GitHub static-file publishing](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site).

## Optional manual Actions publication

Use this alternative if maintainers prefer to publish each update explicitly. The included workflow stages only `index.html`, the three files in `assets/`, and `.nojekyll` for the deployed site.

1. Commit the site files, `scripts/check_site.py`, and `.github/workflows/pages.yml` to `main`.
2. In [Settings → Pages](https://github.com/UserPlural/website/settings/pages), set **Source → GitHub Actions** instead of branch publication.
3. Open **Actions → Publish workshop website → Run workflow**, choose `main`, and run it. The workflow has no push trigger and only publishes from the default branch.
4. Follow the deployment link and verify the live site. Run the workflow again when each subsequent content update is ready to publish.

The workflow uses GitHub's Pages actions and the `github-pages` environment. If the organization requires approval for that environment, use its existing review process. [GitHub custom workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

Deployment guidance checked against GitHub documentation on October 14, 2026.
