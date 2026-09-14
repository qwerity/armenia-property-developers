const cache = new Map();

function metres(a, b) {
  const rad = Math.PI / 180;
  const h = Math.sin(((b.lat - a.lat) * rad) / 2) ** 2
    + Math.cos(a.lat * rad) * Math.cos(b.lat * rad) * Math.sin(((b.lng - a.lng) * rad) / 2) ** 2;
  return Math.round(12742000 * Math.asin(Math.sqrt(h)));
}

/**
 * Validate a project's address against Google: Places (New) text search for the project near its pin,
 * then Geocoder for the street address. Returns the most precise match with its distance from our pin.
 *
 * @param {object} p project
 * @returns {Promise<null|{source:"place"|"geocoder", placeId?:string, name?:string, address:string, location:{lat:number,lng:number},
 *   viewport?:google.maps.LatLngBounds, precision:string, distance_m:number, types?:string[]}>}
 */
export async function validateLocation(p) {
  if (cache.has(p.id)) return cache.get(p.id);
  const pin = { lat: p.lat, lng: p.lng };
  const candidates = [];
  const { Place } = await google.maps.importLibrary("places");
  const queries = [
    [p.title, p.address, p.district].filter(Boolean).join(", "),
    p.address && [p.address, p.district, p.region, "Armenia"].filter(Boolean).join(", "),
  ].filter(Boolean);
  for (const textQuery of [...new Set(queries)]) {
    try {
      const { places } = await Place.searchByText({
        textQuery, fields: ["id", "displayName", "formattedAddress", "location", "viewport", "types"],
        locationBias: { center: pin, radius: 3000 }, region: "am", language: "en", maxResultCount: 3,
      });
      for (const pl of places || []) {
        const loc = pl.location?.toJSON();
        if (!loc) continue;
        const residential = (pl.types || []).some((t) => /premise|subpremise|establishment|point_of_interest|street_address|apartment/.test(t));
        candidates.push({ source: "place", placeId: pl.id, name: pl.displayName, address: pl.formattedAddress, location: loc, viewport: pl.viewport,
          types: pl.types, precision: residential ? "building" : "area", distance_m: metres(pin, loc) });
      }
    } catch (err) {
      console.warn("Places text search failed", err);
    }
  }
  if (p.address) {
    try {
      const { Geocoder } = await google.maps.importLibrary("geocoding");
      const { results } = await new Geocoder().geocode({ address: `${p.address}, ${p.district || ""}, Armenia`, region: "am" });
      for (const r of (results || []).slice(0, 2)) {
        const loc = r.geometry.location.toJSON();
        const precise = r.geometry.location_type === "ROOFTOP" || r.types.includes("premise") || r.types.includes("street_address");
        candidates.push({ source: "geocoder", placeId: r.place_id, address: r.formatted_address, location: loc, viewport: r.geometry.viewport,
          types: r.types, precision: precise ? "building" : r.geometry.location_type === "RANGE_INTERPOLATED" ? "street" : "area", distance_m: metres(pin, loc) });
      }
    } catch (err) {
      console.warn("Geocoder failed", err);
    }
  }
  const rank = { building: 0, street: 1, area: 2 };
  const best = candidates
    .filter((c) => c.distance_m < 15000)
    .sort((a, b) => rank[a.precision] - rank[b.precision] || (a.source === b.source ? 0 : a.source === "place" ? -1 : 1) || a.distance_m - b.distance_m)[0] || null;
  cache.set(p.id, best);
  return best;
}
