# CodeMaths — Lean 4 Lessons (site)

Plain static HTML/CSS/JS — no build step, no framework, Tailwind loaded via CDN. Lesson content is generated *into* `index.html` from Markdown files (see below) so search engines still see it as plain HTML, with search/sort/pagination and the About page routed client-side as progressive enhancement (`js/search.js`, `js/router.js`).

## Local development

No build tooling required to serve the site. From this directory:

```sh
python3 -m http.server 8000
```

Then open `http://localhost:8000`. (Client-side navigation to `/about` via the nav link works fine; loading `/about` directly in a fresh tab needs a server with SPA fallback, which Python's simple server doesn't do — App Platform's `error_document` config handles this in production. See "Adding a lesson" below for the one command that needs Python + PyYAML, which this container already has.)

## Adding a lesson

Lessons live as one Markdown file each in [`../lessons/`](../lessons/), not hand-written HTML. Add a new lesson in two steps:

1. Create `../lessons/<NN>-<slug>.md` (the `NN-` prefix controls display order — files are sorted by filename):

   ```markdown
   ---
   title: Getting Started with Lean 4
   youtube_id: dQw4w9WgXcQ
   tags:
     - basics
     - setup
   repo_url: https://github.com/tehsil-digital/codemaths   # optional — omit the field to skip the "Code repo" button
   ---
   A short description of the lesson. Plain text (HTML-escaped automatically) —
   this is the body, everything after the second `---`.
   ```

   `title` and `youtube_id` are required. `tags` and `repo_url` are optional.

2. Regenerate `index.html` from the repo root:

   ```sh
   python3 scripts/build_lessons.py
   ```

   This rewrites only the generated lesson cards (between the `<!-- LESSON_CARDS:START/END -->` markers) and the JSON-LD `<script>` block in `site/index.html` — it never touches CSS, JS, or anything else in the page. Commit both the new `.md` file and the regenerated `site/index.html`.

Markdown was chosen over a single JSON file specifically so descriptions can be normal multi-line prose instead of an escaped JSON string, and so each lesson is its own reviewable diff. The GitHub Actions deploy workflow also runs this script before deploying, so even an unbuilt `index.html` gets regenerated at deploy time — but committing the built HTML keeps local preview and Git history accurate.

Removing a lesson: delete its `.md` file and re-run the build script.

## Deploying to DigitalOcean App Platform (free, via GitHub Actions)

App Platform's free tier includes up to 3 static sites per account (1 GiB outbound transfer/month each), with automatic HTTPS and a CDN. Deploys are meant to be handled by `.github/workflows/deploy.yml`, which runs `digitalocean/app_action` against the spec in [`../.do/app.yaml`](../.do/app.yaml) on every push to `main`. The app spec already points at `codemaths.xyz` as the primary domain.

**Note:** the workflow file itself isn't pushed to this branch yet — the bot that made these commits doesn't have `workflows` permission on the GitHub App installation, so GitHub rejects any push touching `.github/workflows/*`. See the PR description for the exact file content to add, and two ways to get it in.

One-time setup (only you can do these — they need account/domain access this agent doesn't have):

1. **Create a DigitalOcean API token**: [cloud.digitalocean.com/account/api/tokens](https://cloud.digitalocean.com/account/api/tokens) → Generate New Token → give it write access.
2. **Add it as a GitHub secret** on this repo, named `DIGITALOCEAN_ACCESS_TOKEN`:
   ```sh
   gh secret set DIGITALOCEAN_ACCESS_TOKEN --repo tehsil-digital/codemaths
   ```
   (or Settings → Secrets and variables → Actions → New repository secret, in the GitHub UI).
3. **Point `codemaths.xyz` at DigitalOcean.** At your domain registrar, either delegate the domain's nameservers to DigitalOcean (`ns1.digitalocean.com`, `ns2.digitalocean.com`, `ns3.digitalocean.com`), or add the CNAME/A record App Platform gives you after the first deploy (Settings → Domains on the app, once it exists). DNS propagation can take up to 24-48 hours.
4. Push to `main` (or run the workflow manually from the Actions tab) — the first run creates the app from `.do/app.yaml`; every push after that updates it in place.

No manual `doctl` or control-panel app creation needed — the workflow creates the app itself on first run. If you'd rather do a one-off manual deploy: `doctl apps create --spec .do/app.yaml` (after `doctl auth init`).

## Getting indexed by Google

- Submit the sitemap (`/sitemap.xml`) in [Google Search Console](https://search.google.com/search-console) once `codemaths.xyz` is live and DNS has propagated.
- `index.html`, `sitemap.xml`, and `robots.txt` are already pointed at `https://codemaths.xyz/` — Google won't index a site whose sitemap references the wrong host.
- Because lesson content is plain HTML (not injected by JavaScript after load), it's crawlable even without JS execution.
