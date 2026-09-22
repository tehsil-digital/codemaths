# CodeMaths — Lean 4 Lessons (site)

Plain static HTML/CSS/JS — no build step, no framework. All lesson content lives directly in `index.html` so search engines can crawl it without running JavaScript; the search box in `js/search.js` just hides/shows cards client-side.

## Local development

No build tooling required. From this directory:

```sh
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

## Adding a lesson

Duplicate one `<li class="lesson-card">...</li>` block in `index.html` and fill in:

- The YouTube video ID in both the thumbnail `<img src>` (`https://i.ytimg.com/vi/<ID>/hqdefault.jpg`) and the two `<a href="https://www.youtube.com/watch?v=<ID>">` links
- The lesson title (appears in the `<h2>` and the thumbnail `alt` text)
- A short description
- `<li>` tags under `.lesson-tags` for topics (used by search)
- The "Code repo" link — remove that `<a>` entirely if there's no companion repo for that lesson

No other file needs to change — search and layout pick up new cards automatically.

## Deploying to DigitalOcean App Platform (free)

App Platform's free tier includes up to 3 static sites per account (1 GiB outbound transfer/month each), with automatic HTTPS and a CDN. Config for this is already checked in at `../.do/app.yaml`.

1. Push this repo to GitHub (already done if you're reading this from the repo).
2. In the [DigitalOcean control panel](https://cloud.digitalocean.com/apps), click **Create App** → **GitHub** → select the `codemaths` repo and the `main` branch.
3. DigitalOcean should detect `.do/app.yaml` automatically. If asked manually: component type **Static Site**, source directory `site`, no build command, output directory `/`.
4. On the plan-selection step, choose the **Static Sites — Free** tier.
5. Deploy. DigitalOcean gives you a URL like `https://codemaths-lean-lessons-xxxxx.ondigitalocean.app`.
6. Once you have a real domain (custom or the DO-assigned one), update the placeholder URLs (`https://codemaths.tehsil.digital/`) in `index.html` (`canonical`, `og:url`), `sitemap.xml`, and `robots.txt` to match, then commit and push — App Platform redeploys automatically.

Alternatively, deploy via the CLI: `doctl apps create --spec .do/app.yaml` (run from the repo root, after `doctl auth init`).

## Getting indexed by Google

- Submit the sitemap (`/sitemap.xml`) in [Google Search Console](https://search.google.com/search-console) once the site is live at its real URL.
- Keep `robots.txt` and `sitemap.xml` pointed at the real domain (see step 6 above) — Google won't index a site whose sitemap references the wrong host.
- Because lesson content is plain HTML (not injected by JavaScript after load), it's crawlable even without JS execution.
