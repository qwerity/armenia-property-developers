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
