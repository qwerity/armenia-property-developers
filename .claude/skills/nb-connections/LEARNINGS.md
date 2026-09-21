# nb-connections learnings

## 2026-09-20 — first build
- karg.am mirrors e-register.moj.am and, unlike e-register's own site (a JS app with no public search API),
  serves plain HTML: `/search?q=`, `/company/<tax id>`, `/founder/<key>`. Founder pages list every company a
  person holds with share, status and address — that is where cross-developer links come from.
- Company cards only expose founders for part of the register; when the BOR section is missing the company
  still links through its legal address and its director name.
- azdarar.am (official bulletin, the authority for "սնանկ է ճանաչվել") resets the connection from outside
  Armenia — it is linked for the reader, never crawled. Bankruptcy status is therefore derived from datalex
  bankruptcy cases plus the register's active/inactive flag, and can be overridden with a source in
  `scraper/connections_manual.json`.
- datalex bankruptcy rows carry no verdict, so a case against a company is only "declared bankrupt" when the
  register also shows the company as no longer active; everything else stays "case pending".
- Entity names in the reputation research are often brand names; exact-name matching on the registry (after
  stripping «», ՍՊԸ/ՓԲԸ and bracketed notes) resolves most of them, and anything ambiguous is left unresolved
  with a search link rather than guessed.

## 2026-09-21 — sources and limits
- azdarar.am runs two generations side by side: the current platform searches at
  `https://azdarar.am/hy/public-announcement/search-result/?query=…` (notices since 2025-03-01) and the
  archive at `https://www.azdarar.am/search`, with details under `/announcments/cat|org/<id>/<id>/`.
  The earlier `/announcments/search?keyword=` link used in the first build does not exist — fixed.
  Every host of the site (www, apex, personal-legal-old, plain HTTP) resets the connection from outside
  Armenia, including for WebFetch, so `scraper/azdarar.py` is a local-run tool and the reader also gets a
  Google `site:azdarar.am` link, which is how the Կվադրա Քոնսթրաքշն notice was actually found.
- e-register.moj.am's own company search is a logged-in app (`/api/*` redirects to login), so karg.am
  stays the only machine-readable mirror.
- karg.am owner names carry no patronymic (3 of 341 have three tokens), so kinship cannot be inferred
  from the ownership register; datalex party names do carry patronymics but they are the buyers suing,
  not the owners. Family ties therefore need a document, and only shared surnames inside one cluster are
  worth publishing as a lead (39 of them, 11 of which are one person listed twice).
