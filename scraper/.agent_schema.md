OUTPUT SCHEMA — JSON array, one object per project (a building / complex / phase marketed by the developer, in Armenia only):
{"source": "<site domain, e.g. 4acapital.am>", "source_url": "<project page URL>", "title": "<project name, English/Latin if available>",
 "developer": "<company name>", "developer_url": "<developer homepage>", "city": "<Yerevan / Tsaghkadzor / ...>", "district": "<Yerevan district or community>",
 "address": "<street + number as precise as possible, in English or original>", "lat": number|null, "lng": number|null,
 "price_min_usd_m2": number|null, "price_min_amd_m2": number|null, "price_currency_raw": "<raw price text>",
 "completion": "YYYY-MM | 'IV 2027' | '2027' | null", "status": "under construction|completed|planned|null", "floors": "<e.g. 12 or 9,15>",
 "type": "residential|commercial|mixed|resort|null", "phones": [], "email": "", "website": "<project site or page>",
 "social": {"facebook": "", "instagram": "", "youtube": "", "telegram": ""}, "images": ["absolute urls, max 12"], "videos": ["youtube/vimeo urls"],
 "description": "<plain-text summary/paraphrase, <=700 chars: size, apartments, amenities, parking, etc.>",
 "apartments": [{"rooms": "2", "area_min": 60, "area_max": 80, "price_from": 90000, "currency": "USD"}]  (optional)}

HOW TO GET COORDINATES: look for Google Maps embeds/links (!2d<lng>!3d<lat>, @lat,lng, q=lat,lng, ll=), Yandex maps (ll=lng,lat / pt=), Leaflet/Mapbox init JS (setView([lat,lng]), data-lat/data-lng attributes, JSON-LD geo, WP plugin JSON. If none, leave lat/lng null but ALWAYS give the best street address + city (the merge step geocodes with Nominatim).
FETCHING: curl/python with full browser headers (UA "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36", Accept "text/html,application/xhtml+xml", Accept-Language "en-US,en;q=0.9,hy;q=0.8,ru;q=0.7"). Prefer /en/ pages; fall back to hy/ru. Check WordPress REST (/wp-json/wp/v2/<post-type>), sitemap.xml, Next/Nuxt JSON payloads, XHR APIs before HTML scraping. If a site is pure client-side JS, you MAY use the Browser pane tools (mcp__Claude_Browser__*) in your OWN tab (tabs_create) and close it afterwards; don't touch other tabs.
RULES: polite (<=2 req/s per host, cache pages under your own dir in the scratchpad), no logins/captchas/forms, don't download binaries. Include completed projects too (status=completed) — the map marks them. Skip pure service pages (architecture/design services) and projects outside Armenia. Deduplicate within your file. Write the file incrementally (rewrite after each developer) so partial results survive.
REPORT at end: projects per developer, how many with coords / address-only / price / images, and developers that failed (why).
