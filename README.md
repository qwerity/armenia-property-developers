# Armenia new builds

Every public new-building project in Armenia on one map, with prices, construction stage, contacts
and a developer reputation rating — plus an analytics dashboard and a one-file SQLite database.

- **Map** (`index.html`) — Google Maps 2D / 3D / photorealistic 3D, pins coloured per developer,
  faceted filters, project details with images, videos, contacts, price check and developer rating.
- **Analytics** (`analytics.html`) — prices by district, price distribution, delivery pipeline,
  stages, price against completion date, developer ratings, data quality, below-median deals, and a
  connections graph of developers, their companies and the people who own them (graph or tree view),
  with bankruptcies marked.
- **Database** (`db/armenia-new-builds.sqlite`) — the whole dataset in SQL form, documented in
  [`db/db.md`](db/db.md).

Current snapshot: 735 projects, 366 developers, 140 sources, data generated 2026-09-15.

## Repository layout

| Path | What it is |
| --- | --- |
| `web/` | The static site: two HTML pages, CSS, plain ES modules, `web/data/projects.json` and `web/data/connections.json` |
| `scraper/` | Crawlers, the merge/normalize/score pipeline, verification data, source registry |
| `db/` | Generated SQLite database and its documentation |
| `build.py` | Builds `dist/` for static hosting |
| `deploy.sh` | Syncs `dist/` to S3 and invalidates CloudFront |
| `serve.py` | Local dev server on http://localhost:5190 (IPv4 + IPv6) |
| `.claude/skills/` | Self-improving data commands (`/nb-status`, `/nb-recrawl`, …), see [COMMANDS.md](COMMANDS.md) |

There is no framework and no bundler: the pages load ES modules directly, so the build is a copy
step plus a generated `config.js`.

## Requirements

- Python 3.10+ (standard library only for building and serving)
- A Google Maps JavaScript API key with **Maps JavaScript API**, **Places API (New)**,
  **Geocoding API** and **Map Tiles API** (for photorealistic 3D) enabled

## Local development

```bash
cp web/config.example.js web/config.js   # then paste your key, or:
echo 'GOOGLE_MAP_API_KEY=your-key' > .env && python3 scraper/make_config.py
python3 serve.py 5190
```

Open http://localhost:5190. The Maps key must allow `localhost` under **Website restrictions**, or
Google shows "Oops! Something went wrong".

## Build

```bash
GOOGLE_MAP_API_KEY=your-key python3 build.py
```

Writes `dist/` (~12 MB): both pages, CSS, JS, `data/projects.json`, the SQLite database under
`db/`, a generated `config.js`, and `version.json` recording the commit and dataset date. The key
is read from the environment first, then from `.env`, so CI can inject it as a secret. Options:
`--out <dir>`, `--no-db`.

`dist/` is git-ignored — it is a build artifact, rebuilt on every deploy.

## Deploy to S3 + CloudFront

One-time setup:

1. Create a **private** S3 bucket (no public access, no static website hosting).
2. Create a CloudFront distribution with that bucket as origin, using **Origin Access Control**,
   and add the generated bucket policy.
3. Set **Default root object** to `index.html`.
4. Leave **Compress objects automatically** on — the dataset is 5.9 MB of JSON and compresses to
   roughly a tenth of that.
5. Add your CloudFront domain to the API key's **Website restrictions**
   (`https://d1234.cloudfront.net/*` and your custom domain), otherwise the map refuses to load.

Then, for each release:

```bash
GOOGLE_MAP_API_KEY=your-key python3 build.py
S3_BUCKET=my-bucket CLOUDFRONT_DISTRIBUTION_ID=E123ABC bash deploy.sh
```

`deploy.sh` syncs assets with a one-hour cache and the pages, config and dataset with a five-minute
cache, then invalidates `/*`. Nothing is fingerprinted, so the invalidation is what makes a deploy
visible immediately.

`analytics.html` is a real file, so no CloudFront function or 404 rewrite is needed. If you prefer
extensionless URLs, add a CloudFront Function that appends `.html`.

### Note on the API key

The key ships in `config.js` and is readable by anyone — that is normal for browser Maps keys, and
the protection is the referrer restriction plus per-API quotas, not secrecy. Restrict the key to
your domains and to the four APIs above, and set daily quota caps. `.env` and `web/config.js` are
git-ignored and have never been committed.

### GitHub Actions

`.github/workflows/build.yml` builds `dist/` on every push and uploads it as an artifact. If the
repository has `GOOGLE_MAP_API_KEY`, `AWS_ROLE_ARN`, `S3_BUCKET` and `CLOUDFRONT_DISTRIBUTION_ID`
configured, pushes to `main` also deploy; without them the deploy job is skipped.

## Data

The site reads a single file, `web/data/projects.json`, built by the scraper pipeline:

```bash
python3 scraper/pipeline.py status          # dataset health
python3 scraper/pipeline.py crawl           # re-crawl sources
python3 scraper/pipeline.py build           # rebuild projects.json + a change report
python3 scraper/export_db.py                # rebuild the SQLite database
python3 scraper/connections.py crawl        # rebuild the ownership graph (registry + court records)
```

Prices are asking prices published by developers and aggregators, reconciled across sources and
re-checked by hand; 353 projects have no current public price and keep their last known figure
instead. Developer ratings combine track record, delivery, datalex.am court records, cross-source
validation and transparency. Full definitions, caveats and example queries are in
[`db/db.md`](db/db.md); the data commands are described in [COMMANDS.md](COMMANDS.md).

The connections graph (`web/data/connections.json`) links each developer to its registered companies and
to the people who own or run them, using the state register of legal entities and its beneficial-owner data
(e-register.moj.am, read through karg.am) plus bankruptcy cases from datalex.am. Every node carries the
links it was built from, so each claim can be checked at the source; bankruptcy notices are published on
azdarar.am, which blocks requests from outside Armenia and is therefore linked rather than crawled. A
company is marked as declared bankrupt only when a bankruptcy case is matched by the register showing the
company as no longer active; a case with the company as its own claimant is shown as a self-filed
bankruptcy, and anything else as a pending case. Of the developer-to-company links, 195 rest on a tax id
recorded in the reputation research and 147 on an exact name match in the register — the view labels which
is which — and 80 legal entities that could not be matched are left out rather than guessed.
