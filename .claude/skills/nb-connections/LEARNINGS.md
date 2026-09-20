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
