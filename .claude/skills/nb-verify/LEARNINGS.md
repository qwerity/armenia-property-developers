# nb-verify learnings

Append dated, factual entries after every run (newest last). Promote durable ones into SKILL.md / templates.

## 2026-09-14/15 (initial build)
- Prices: most wrong values came from SOLD units in unit listings (redgroup API sample, arcada inventory). Always use available units only.
- Prices: etagi.am shows USD figures that are actually AMD thousands; dignisi descriptions sometimes say "AMD 3000/m²" meaning USD.
- Prices: construction.am and geoln.com prices are often 2019-2022; never trust them over myhome/developer sites.
- Locations: karucapatoxic Google embeds — use the `!2z` base64 DMS marker, not `!2d/!3d` (viewport centre, 100-400 m off).
- Locations: "pin N m from street" false alarms come from long streets or same-named streets in other towns (Tumanyan, Vahan Teryan, Monte Melkonyan); verify before moving.
- Locations: bank partner lists (acba/evoca/byblos) use placeholder pins (Republic Square, Nor Nork).
- Locations: Nominatim is shared — max 1 request per 4 s across parallel agents.
- Stages: Esri Wayback returns the newest release where a tile changed; effective imagery dates differ by region (Yerevan newest, Vedi old).
- Stages: ar-go.am lists start/end dates; construction.am has completion fields — check them first.

## 2026-09-15 (recheck batch 10)
- Locations: embeds with a named place (`!1s0x...!2s<address>`) but no `!2z` still have `!2d/!3d` = viewport centre; pins copied from it were 220-480 m off (1-sq Khanjyan 9/3, Top Buildings, Ani Premium). Use `!3d..!4d..` place marker or Nominatim building. karucapatoxic JSON-LD geo is also that viewport centre, not the `!2z` point.
- Locations: karucapatoxic pages embed maps of the developer's other buildings too; pick the `!2z` that matches the page, and a `!2z` can be a place name (e.g. sales office "30 Gyulbenkyan St") rather than DMS.
- Prices: myhome header `areaPriceStartingAt` can come from BOOKED units (Ember) or survive with 0 available (Milon Mining) — query apartments/filter and drop `isBooked`.
- Prices: redgroup `/api/projects/{id}` returns only a 12-unit sample (mostly sold); all available units come from the page's load-more POST `/projects/products` (csrf token + cookie, sold=false). redinvest.am mirror currently throws a Next.js application error.
- Prices: ar-go.am unit tables paginate via Livewire but `?page=N` GET works (order not stable — dedupe by apartment name).
- Prices: firdusresidence.am has a public GraphQL (`api.firdusresidence.am/graphql`, apiKey in main.js) with status PURCHASED/RESERVED/ACTIVE; topbuildings.am inline JSON uses `filters[0]` 1=available 2=reserved 3=sold; artco.am chooser shows availability but no prices.
- Identity: catalog URLs merged by street name alone were different projects (EcoPanel Bagrevand vs RED Sunland Bagrevand vs Step 4 townhouses; Movsesyan "Davtashen" vs RED Davtashen Town).

## 2026-09-15 (full recheck, in progress)
- construction.am sometimes uses a default Kentron point (40.18876, 44.51346) instead of the site — treat exact matches as suspect (candidate audit rule).
- mge.am townhouse "price per m²" divides by land area (300/400 m²), not house area (~133 m²) — read the listing description.
- A pin exactly matching a mis-merged source's map marker signals a bad merge (kp-214 took comfortbuild.am's Nazarbekyan 41/1 marker).
- Coordinator agents that split work into sub-agents consume the 20-agent concurrency limit; launch big rechecks with ≤ 12 top-level agents or tell them not to spawn.
- Recrawl hazard: extra/catalog project ids are index-based (e.g. constructionam-17); a fresh crawl that reorders a source detaches manual checks keyed by id. Make ids stable (hash of source_url) before the next /nb-recrawl.
- Yandex Maps search pages (plain curl) expose org names + coordinates — a good location fallback that avoids Nominatim.
- Old portal map pins (construction.am, 2023) can be ~1.4 km off while looking exact; earlier "correct" verdicts based only on them are weak.
- Leningradyan St is now Kirk Kerkorian St in geocoders.
- Sold-out projects on redgroup/karucapatoxic/Elite Group still show their last prices — verdict must be "unverifiable", not "confirmed".
- Nominatim fails on slash sub-lot addresses ("45/1", "2nd block 46/1"); Overpass tag search finds them but rate-limits fast. Matching only "house 45" lands on wrong buildings.
- novostroiki-yerevan.com USD figures can use a wrong rate (~459 AMD/USD) → ~20 % too low.
- myhome "from" per-m² can come from a building with 0 available units; check the unit list.
- Bank partner cards can be linked to the wrong project entirely (acba #10181 on Park Royal = Baza Residence).
- Developer unit APIs: app.parkroyal.am/front/api/v1/areas, buildings.bedeck.am/api/buildingRooms/get (no prices); Metrum embeds unit data in page.
- Possible duplicate: bedeckam-440 vs kp-66 (Bedeck, Pirumyanner 13).
- myhome.am apartments API unit status: 0 available, 1 booked, 2 sold — "price from" often comes from a booked unit. sahakyanshin.com keeps prices on sold flats; novabuilding.am /apartments has per-unit status.
- Aggregators merge by street name (Davit Bek 103 vs 105; Davtashen Yerevan vs Davtashen-Nairi Kotayk) — check developer + floors before trusting a merge.
- Garegin Hovsepyan St exists in Nork-Marash and Shengavit.
- Developer "find us" links often show the sales office, not the site (firdus.am, 1-sq.am, spitaktnak.am).
- Possible duplicate: promgroupam-533 Double Towers = argoam-1092 Dabl Tauers.
- redgroup.am API returns only a 12-unit sample (often mostly sold); the full available list comes from the project page's "load more" request. Sunday Towers per-apartment prices at api.sundaytowers.am.
- karucapatoxic price.min can be years old — check priceUpdated; dignisi "from" is the lowest floor-tier list price, not an available unit.
- Non-residential entries found (Best Resort Aghveran hotel, Basic Center mall, AM Group facade portfolio) — candidates to exclude from the map.
- karucapatoxic JSON-LD geo can be far from its map marker; novostroiki copies it, so their agreement proves nothing. kamertoon.am JSON-LD is ~1.1 km off; charagayt pins rounded to 4 dp (~270 m); redgroup gives Duryan House 3/4/5 one shared pin.
- Evoca lists projects under legal-entity names (S.K. Group = Prime Park, comfortbuildam-720) — shared phone reveals duplicates.
- redgroup/redinvest default unit tab is owner resale ("from owner"), not developer stock — resale ads on sold-out buildings produced wrong prices (Moldovakan 39/37, Duryan House 4).
- ar-go "from X" can be below all listed available units; its unit table shows ≤10 rows.
- Embedded maps on developer/bank pages often show the sales office (apex-gm, armconstruct, solarcity).
- Yandex search resolves "Davtashen Nth district NN/N" house addresses that Nominatim can't; it exposed construction.am pins 160–245 m off.
- myhome building points can be the street centre (Firdus Prime = Nominatim Khanjyan street result).
- artresidence.am unit data: /api/v2/front/areas/search?projects=…&statuses=…; metruminvest.am embeds unit status+price (price list includes other projects' names).
- Same building listed under different addresses (myhome "Clubhouse" G. Hovsepyan 22/11 = Art Residence ClubHouse 50/2) — match by unit count and areas.
- redgroup.am full available list: POST /projects/products with the CSRF token from the project page (the /api/projects/{id} sample caused all RED price errors).
- Neighbouring phases with similar names get merged (Atlantis Yerevan/Prime, Cascade Park/Cascade Club, Leningradyan 19/12 vs 23/2).
- dignisi pins can be 280–290 m off; milonmining.am reuses one coordinate for several projects; ar-go unit tables paginate (?page=2).
- maps.app.goo.gl / goo.gl/maps short links redirect only with curl's default UA (browser UA gets a JS page).
- Merges on shared names: municipality "Nairi", neighbouring street numbers (Antarayin 160/5 vs 154–156), same-name phases in different districts (Felicity Nor Nork vs Davtashen).
- ACBA constructors page moved to /hy/individual/loans/mortgage-loans/8979 (ng-state data unchanged).
- Build rule needed: "unverifiable" (sold out / stale-only) must clear the displayed current price, keeping it as last known — otherwise stale prices stay live.
- karucapatoxic `!2z` marker can also be wrong (Arare Abovyan ~350 m); capitalbuild.am "View on Google Maps" wrong for White Sky and Bestland (2.7 km). Confirm with a second map or satellite before moving.
- A portal pin on a central square with no matching street nearby is a geocoder fallback (NARMARK on Abovyan Square).
- etagi offer counts can exceed a building's flats and mark unfinished buildings finished — weak source.
- Short street names geocode to the wrong town ("F. Verfel" → Gyumri, "Ghapantsyan" → Ashtarak); always include "Yerevan".
- Yandex constructor maps: marker coords via yandex.ru/map-widget/v1/?um=constructor:…; Mountain Plaza's map points to Switzerland (placeholder).
- artco/charagayt/ntc sites: apartment_status_id 1 available, 2 sold, 3 reserved.
- Sales-agent home pages laid out as card grids (citynest.am) leak the next card's label into a project's address ("Etchmiadzin 11/4" is on Arshakunyats Ave, Yerevan).
- myhome.am page "End of construction" vs API completion can differ by up to 2 years.
- Full recheck schema lacked a stage field; agents found finished/in-progress mislabels (Haus V1, Gulikevkhyan, Alma-Ata 1/4). Add "stage" to templates/full.md.
- primedevelopers.am catalogue lists sold units with prices (only floor plans mark them sold).
- Skyline public API: backend.skyline-evn.am/api/v1/public/flats (all available flats with prices).
- Dignisi coordinates are sometimes district-level geocodes (Toon 27, 620 m off).
- ARGO (ar-go.am) Yandex maps can land on the wrong village (Babajanyan 18 km off); reliable only when the embed names the complex.
- rebrand.ly and Yandex maps/-/ short links resolve to exact coordinates (Firdus Square, MyTown).
- myhome.am/novostroiki share one placeholder point for several Acharyan addresses (37/22, 39/23, 43/20).
- Developer sold-out flags vs aggregator unit lists can disagree (metruminvest marks Renet sold out; myhome lists 21 available) — trust unit-level status.
- Developer unit feeds lead aggregators: metruminvest.am (delivery date is MM/DD/YYYY), avan.am, api.milonmining.am. karucapatoxic/dignisi lag (Avan Towers 530k vs 379k; Masis Central 358k vs 418k).
- ar-go.am keeps "from" prices on projects badged Sold (Վաճառված).
- redinvest.am project pages now serve a generic page; use the matching redgroup.am page.
- karucapatoxic `!2z` marker can be the sales office (kp-39 → Garegin Nzhdeh 23/6) — cross-check with JSON-LD/other maps.
- myhome/novostroiki coordinates are sometimes OSM street midpoints — treat exact midpoint matches as street-level.
- Points shared by several projects or in a company's schema.org contact data are offices (milonmining API, verelq777, novelabovyan).
- Dead developer sites (2026-09): avanhills.am, shinstroyhouse.am, faithbuilt.am.
- Full recheck 2026-09-15 result: price 323 confirmed / 69 corrected / 356 unverifiable; location 621 correct / 83 moved / 44 unlocatable; 13 duplicate merges; 76 pins moved, 137 price changes, 6 stage fixes.
- Build bugs found and fixed while applying: (1) a newer "correct" location verdict reverted earlier corrected pins → now keeps the corrected coordinates; (2) numbers-only stage checks wiped earlier stage verdicts → stage checks merge field by field; (3) "unverifiable" now clears stale current prices (kept as last_known_*).
