import * as maplibregl from "../vendor/maplibre-gl/maplibre-gl.mjs";
import { esc, money, compactMoney, quarter } from "./util.js";

const ARMENIA_BOUNDS = [[43.3, 38.8], [46.7, 41.35]];
const ESRI = "https://server.arcgisonline.com/ArcGIS/rest/services";

const BASEMAPS = {
  streets: ["carto-voyager"],
  satellite: ["esri-imagery"],
  hybrid: ["esri-imagery", "esri-transport", "esri-labels"],
};

function rasterStyle() {
  const raster = (tiles, attribution, extra = {}) => ({ type: "raster", tiles, tileSize: 256, attribution, maxzoom: 19, ...extra });
  return {
    version: 8,
    sources: {
      "carto-voyager": raster(
        ["a", "b", "c", "d"].map((s) => `https://${s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}@2x.png`),
        '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> © <a href="https://carto.com/attributions">CARTO</a>',
        { tileSize: 512, maxzoom: 20 },
      ),
      "esri-imagery": raster([`${ESRI}/World_Imagery/MapServer/tile/{z}/{y}/{x}`], "Imagery © Esri, Maxar, Earthstar Geographics"),
      "esri-transport": raster([`${ESRI}/Reference/World_Transportation/MapServer/tile/{z}/{y}/{x}`], "© Esri"),
      "esri-labels": raster([`${ESRI}/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}`], "© Esri"),
    },
    layers: ["carto-voyager", "esri-imagery", "esri-transport", "esri-labels"].map((id) => ({
      id, type: "raster", source: id, layout: { visibility: BASEMAPS.hybrid.includes(id) ? "visible" : "none" },
    })),
  };
}

function toGeoJSON(projects) {
  return {
    type: "FeatureCollection",
    features: projects.map((p, i) => ({
      type: "Feature",
      id: i,
      geometry: { type: "Point", coordinates: [p.lng, p.lat] },
      properties: { pid: p.id, color: p.color, deal: p.discount_pct ?? -999, approx: p.geo_precision === "district" || p.geo_precision === "city" },
    })),
  };
}

function popupHtml(p) {
  const img = p.images?.[0];
  return `<div class="pop">
    ${img ? `<img src="${esc(img)}" alt="">` : ""}
    <div class="pop-body">
      <div class="pop-title">${esc(p.title)}</div>
      <div class="pop-dev"><span class="dot" style="background:${p.color}"></span>${esc(p.developer_group)}</div>
      <div class="muted">${esc([p.district, p.region].filter(Boolean).join(", "))}</div>
      <div class="pop-grid">
        <span>Price</span><b>${money(p.usd_m2_min, p.amd_m2_min, "/m²")}</b>
        <span>From</span><b>${compactMoney(p.usd_from, p.amd_from)}</b>
        <span>Completion</span><b>${esc(p.status === "completed" ? `Ready (${quarter(p.completion)})` : quarter(p.completion))}</b>
        <span>Floors</span><b>${esc(p.floors || "—")}</b>
      </div>
      ${p.discount_pct != null ? `<div class="pop-deal ${p.discount_pct > 0 ? "good" : "high"}">${p.discount_pct > 0 ? "−" : "+"}${Math.abs(p.discount_pct)}% vs local median</div>` : ""}
    </div>
  </div>`;
}

/**
 * Create the map with project pins.
 * @param {HTMLElement} container
 * @param {{onSelect:(id:string)=>void, onMove:()=>void}} handlers
 */
export function createMap(container, { onSelect, onMove }) {
  const map = new maplibregl.Map({
    container,
    style: rasterStyle(),
    bounds: ARMENIA_BOUNDS,
    maxBounds: [[40.5, 37.0], [49.5, 43.0]],
    attributionControl: { compact: true },
  });
  map.addControl(new maplibregl.NavigationControl({ visualizePitch: false }), "top-right");
  map.addControl(new maplibregl.ScaleControl({ unit: "metric" }), "bottom-right");
  map.addControl(new maplibregl.GeolocateControl({ trackUserLocation: false }), "top-right");

  let byId = new Map();
  let projectsByIndex = [];
  const popup = new maplibregl.Popup({ closeButton: false, closeOnClick: false, offset: 12, maxWidth: "300px" });
  const ready = new Promise((resolve) => map.on("load", resolve));

  ready.then(() => {
    map.addSource("projects", { type: "geojson", data: toGeoJSON([]) });
    map.addLayer({
      id: "pins-halo", type: "circle", source: "projects",
      paint: {
        "circle-radius": ["interpolate", ["linear"], ["zoom"], 7, 7, 12, 11, 16, 16],
        "circle-color": "#ffffff",
        "circle-opacity": ["case", ["boolean", ["feature-state", "selected"], false], 1, ["boolean", ["feature-state", "hover"], false], 0.9, 0.85],
        "circle-stroke-width": ["case", ["boolean", ["feature-state", "selected"], false], 4, 0],
        "circle-stroke-color": "#111827",
      },
    });
    map.addLayer({
      id: "pins", type: "circle", source: "projects",
      paint: {
        "circle-radius": ["interpolate", ["linear"], ["zoom"], 7, 5, 12, 8.5, 16, 13],
        "circle-color": ["get", "color"],
        "circle-opacity": ["case", ["get", "approx"], 0.45, 1],
        "circle-stroke-color": ["get", "color"],
        "circle-stroke-width": ["case", ["get", "approx"], 2, 0],
      },
    });

    let hoverId = null;
    map.on("mousemove", "pins", (e) => {
      const f = e.features?.[0];
      if (!f) return;
      map.getCanvas().style.cursor = "pointer";
      if (hoverId !== null && hoverId !== f.id) map.setFeatureState({ source: "projects", id: hoverId }, { hover: false });
      hoverId = f.id;
      map.setFeatureState({ source: "projects", id: hoverId }, { hover: true });
      const p = byId.get(f.properties.pid);
      if (p) popup.setLngLat([p.lng, p.lat]).setHTML(popupHtml(p)).addTo(map);
    });
    map.on("mouseleave", "pins", () => {
      map.getCanvas().style.cursor = "";
      if (hoverId !== null) map.setFeatureState({ source: "projects", id: hoverId }, { hover: false });
      hoverId = null;
      popup.remove();
    });
    map.on("click", "pins", (e) => {
      const f = e.features?.[0];
      if (f) onSelect(f.properties.pid);
    });
    map.on("moveend", onMove);
  });

  let selectedIdx = null;
  let setToken = 0;
  return {
    map,
    ready,
    /** Replace the rendered pins with this project subset. */
    async setProjects(projects) {
      const token = ++setToken;
      await ready;
      if (token !== setToken) return;
      projectsByIndex = projects;
      byId = new Map(projects.map((p) => [p.id, p]));
      map.getSource("projects").setData(toGeoJSON(projects));
      selectedIdx = null;
    },
    async select(id, { fly = true } = {}) {
      await ready;
      if (selectedIdx !== null) map.setFeatureState({ source: "projects", id: selectedIdx }, { selected: false });
      const idx = projectsByIndex.findIndex((p) => p.id === id);
      selectedIdx = idx >= 0 ? idx : null;
      if (selectedIdx === null) return;
      map.setFeatureState({ source: "projects", id: selectedIdx }, { selected: true });
      const p = projectsByIndex[idx];
      const panel = document.getElementById("right");
      const right = panel && !panel.hidden && panel.offsetWidth < container.offsetWidth ? panel.offsetWidth : 0;
      if (fly) map.flyTo({ center: [p.lng, p.lat], zoom: Math.max(map.getZoom(), 16), speed: 1.6, padding: { right, left: 0, top: 0, bottom: 0 }, essential: true });
    },
    async setBasemap(name) {
      await ready;
      const visible = BASEMAPS[name] || BASEMAPS.hybrid;
      for (const id of ["carto-voyager", "esri-imagery", "esri-transport", "esri-labels"]) {
        map.setLayoutProperty(id, "visibility", visible.includes(id) ? "visible" : "none");
      }
    },
    fitTo(projects) {
      if (!projects.length) return;
      const b = new maplibregl.LngLatBounds();
      projects.forEach((p) => b.extend([p.lng, p.lat]));
      map.fitBounds(b, { padding: 60, maxZoom: 15, duration: 800 });
    },
    bounds: () => map.getBounds(),
    closePopup: () => popup.remove(),
  };
}
