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
