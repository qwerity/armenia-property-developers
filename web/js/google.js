/**
 * Google Maps JavaScript API bootstrap (official dynamic library import loader, weekly channel).
 * Reads the key from window.APP_CONFIG (web/config.js, generated from .env).
 * @returns {Promise<typeof google.maps>}
 */
export function loadGoogleMaps() {
  if (window.google?.maps?.importLibrary) return Promise.resolve(window.google.maps);
  const cfg = window.APP_CONFIG || {};
  if (!cfg.googleMapsApiKey) return Promise.reject(new Error("Missing Google Maps key: run scraper/make_config.py"));
  // Official inline bootstrap (https://developers.google.com/maps/documentation/javascript/load-maps-js-api), unminified.
  return new Promise((resolve, reject) => {
    const params = new URLSearchParams({ key: cfg.googleMapsApiKey, v: "weekly", language: "en", region: "AM", callback: "__gmapsReady", loading: "async" });
    window.__gmapsReady = () => resolve(window.google.maps);
    const script = document.createElement("script");
    script.src = `https://maps.googleapis.com/maps/api/js?${params}`;
    script.async = true;
    script.onerror = () => reject(new Error("Google Maps JavaScript API failed to load"));
    // Google rejects the key asynchronously, often after the first tiles are already painted, so the
    // promise may be settled by then: tell the page directly as well.
    window.gm_authFailure = () => {
      reject(new Error("Google Maps rejected the API key (check referrer restrictions / enabled APIs)"));
      window.dispatchEvent(new CustomEvent("gmaps-auth-failed", { detail: { url: location.href.split("#")[0] } }));
    };
    document.head.append(script);
  });
}

export const mapId = () => (window.APP_CONFIG || {}).googleMapId || "DEMO_MAP_ID";
