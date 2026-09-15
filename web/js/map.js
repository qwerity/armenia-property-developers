import { MarkerClusterer } from "https://cdn.jsdelivr.net/npm/@googlemaps/markerclusterer@2.6.2/+esm";
import { loadGoogleMaps, mapId } from "./google.js";
import { esc, money, compactMoney, quarter, stageLabel } from "./util.js";
import { gradeBadge } from "./list.js";

const CLUSTER_BELOW_ZOOM = 13;
const SELECT_ZOOM = 15;
const SELECT_ZOOM_3D = 17;
const SELECT_RANGE_PHOTO = 1800;
/** Approximate Google Maps zoom level for a 3D camera range (metres). */
const zoomFromRange = (range) => Math.log2(591657550 / Math.max(range, 1));

function popupHtml(p) {
  const img = p.images?.[0];
  return `<div class="pop">
    ${img ? `<img referrerpolicy="no-referrer" src="${esc(img)}" alt="" onerror="this.remove()">` : ""}
    <div class="pop-body">
      <div class="pop-title">${esc(p.title)}</div>
      <div class="pop-dev"><span class="dot" style="background:${p.color}"></span>${esc(p.developer_group)}${gradeBadge(p)}</div>
      <div class="muted">${esc([p.district, p.region].filter(Boolean).join(", "))}</div>
      <div class="pop-grid">
        <span>Price</span><b>${money(p.usd_m2_min, p.amd_m2_min, "/m²")}</b>
        <span>From</span><b>${compactMoney(p.usd_from, p.amd_from)}</b>
        <span>Stage</span><b>${esc(stageLabel(p))}</b>
        <span>Completion</span><b>${esc(quarter(p.completion))}</b>
        <span>Floors</span><b>${esc(p.floors || "—")}</b>
      </div>
      ${p.discount_pct != null ? `<div class="pop-deal ${p.discount_pct > 0 ? "good" : "high"}">${p.discount_pct > 0 ? "−" : "+"}${Math.abs(p.discount_pct)}% vs local median</div>` : ""}
    </div>
  </div>`;
}

const approx = (p) => p.geo_precision === "district" || p.geo_precision === "city";

/**
 * Google Maps view: 2D vector map (tilt/rotate, Street View, map types, POIs) plus photorealistic 3D mode.
 * @param {HTMLElement} container
 * @param {{onSelect:(id:string)=>void, onMove:()=>void, onZoom?:(zoom:number)=>void}} handlers
 */
export function createMap(container, { onSelect, onMove, onZoom = () => {} }) {
  const state = { map: null, map3d: null, libs: {}, markers: new Map(), clusterer: null, info: null, projects: [], selectedId: null, placeMarker: null, placeLine: null, t3d: 0 };
  const host2d = document.createElement("div");
  const host3d = document.createElement("div");
  host2d.className = "gmap";
  host3d.className = "gmap3d";
  host3d.hidden = true;
  container.append(host2d, host3d);

  const ready = (async () => {
    await loadGoogleMaps();
    const [{ Map, InfoWindow }, marker] = await Promise.all([google.maps.importLibrary("maps"), google.maps.importLibrary("marker")]);
    state.libs = { Map, InfoWindow, ...marker };
    state.map = new Map(host2d, {
      mapId: mapId(),
      mapTypeId: "roadmap",
      renderingType: google.maps.RenderingType.VECTOR,
      center: { lat: 40.07, lng: 45.0 },
      zoom: container.offsetWidth > 900 ? 8 : 7,
      restriction: { latLngBounds: { north: 43.0, south: 37.0, west: 40.5, east: 49.5 }, strictBounds: false },
      zoomControlOptions: { position: google.maps.ControlPosition.LEFT_TOP },
      cameraControlOptions: { position: google.maps.ControlPosition.LEFT_TOP },
      streetViewControlOptions: { position: google.maps.ControlPosition.LEFT_TOP },
      fullscreenControlOptions: { position: google.maps.ControlPosition.LEFT_TOP },
      rotateControlOptions: { position: google.maps.ControlPosition.LEFT_TOP },
      mapTypeControl: true,
      mapTypeControlOptions: { style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR, position: google.maps.ControlPosition.TOP_CENTER,
        mapTypeIds: ["roadmap", "satellite", "hybrid", "terrain"] },
      streetViewControl: true,
      fullscreenControl: true,
      cameraControl: true,
      scaleControl: true,
      rotateControl: true,
      headingInteractionEnabled: true,
      tiltInteractionEnabled: true,
      clickableIcons: true,
      gestureHandling: "greedy",
    });
    const spacer = document.createElement("div");
    spacer.style.cssText = "height:52px;width:120px;pointer-events:none";
    state.map.controls[google.maps.ControlPosition.TOP_LEFT].push(spacer); // room for the app's menu + 2D/3D toggle
    state.info = new InfoWindow({ headerDisabled: true, disableAutoPan: true, maxWidth: 300 });
    state.clusterer = new MarkerClusterer({ map: state.map, markers: [], algorithmOptions: { maxZoom: CLUSTER_BELOW_ZOOM - 1, radius: 60 } });
    state.map.addListener("idle", onMove);
    state.map.addListener("zoom_changed", () => onZoom(state.map.getZoom()));
    onZoom(state.map.getZoom());
  })();

  function pinFor(p, selected = false) {
    const pin = new state.libs.PinElement({
      background: p.color, borderColor: selected ? "#111827" : "rgba(0,0,0,.35)", glyphColor: "#ffffff", scale: selected ? 1.35 : 0.95,
    });
    if (approx(p)) pin.style.opacity = "0.55";
    return pin;
  }

  function buildMarker(p) {
    const m = new state.libs.AdvancedMarkerElement({ position: { lat: p.lat, lng: p.lng }, title: p.title, content: pinFor(p), gmpClickable: true });
    m.addEventListener("gmp-click", () => onSelect(p.id));
    const hover = (el) => {
      el.addEventListener("mouseenter", () => { state.info.setContent(popupHtml(p)); state.info.open({ map: state.map, anchor: m, shouldFocus: false }); });
      el.addEventListener("mouseleave", () => state.info.close());
    };
    hover(m.content);
    m._hover = hover;
    return m;
  }

  function setPin(m, p, selected) {
    m.content = pinFor(p, selected);
    m._hover(m.content);
    m.zIndex = selected ? 1000 : null;
  }

  async function sync3d() {
    if (!state.map3d || container.querySelector(".gmap3d").hidden) return;
    const [maps3d, { PinElement }] = await Promise.all([google.maps.importLibrary("maps3d"), google.maps.importLibrary("marker")]);
    const Marker = maps3d.Marker3DInteractiveElement || maps3d.MarkerInteractiveElement;
    state.map3d.querySelectorAll(".proj3d").forEach((el) => el.remove());
    const c = state.map3d.center;
    const deg = Math.min(0.5, Math.max(0.02, ((state.map3d.range || 3000) / 111000) * 1.5));
    const near = state.projects
      .filter((p) => !c || (Math.abs(p.lat - c.lat) < deg && Math.abs(p.lng - c.lng) < deg * 1.3))
      .sort((a, b) => (a.id === state.selectedId ? -1 : b.id === state.selectedId ? 1 : 0))
      .slice(0, 250);
    for (const p of near) {
      const selected = p.id === state.selectedId;
      const opts = { position: { lat: p.lat, lng: p.lng, altitude: 90 }, altitudeMode: "RELATIVE_TO_GROUND", title: p.title,
        drawsWhenOccluded: true, sizePreserved: true, zIndex: selected ? 1000 : 1 };
      if (Marker === maps3d.Marker3DInteractiveElement) Object.assign(opts, { extruded: true, label: selected ? p.title : undefined });
      const m = new Marker(opts);
      m.append(new PinElement({ background: p.color, borderColor: selected ? "#111827" : "#ffffff", glyphColor: "#fff", scale: selected ? 1.4 : 1 }));
      m.classList.add("proj3d");
      m.addEventListener("gmp-click", () => onSelect(p.id));
      state.map3d.append(m);
    }
  }

  return {
    get map() { return state.map; },
    ready,
    /** Replace rendered markers with this project subset. */
    setProjects(projects) {
      state.pending = this._setProjects(projects);
      return state.pending;
    },
    async _setProjects(projects) {
      await ready;
      state.projects = projects;
      for (const p of projects) if (!state.markers.has(p.id)) state.markers.set(p.id, buildMarker(p));
      state.clusterer.clearMarkers(true);
      state.clusterer.addMarkers(projects.map((p) => state.markers.get(p.id)), false);
      sync3d();
    },
    async select(id, { fly = true } = {}) {
      await ready;
      await state.pending;
      const prevP = state.projects.find((x) => x.id === state.selectedId);
      if (prevP && state.markers.get(prevP.id)) setPin(state.markers.get(prevP.id), prevP, false);
      state.selectedId = id;
      const p = state.projects.find((x) => x.id === id);
      if (!p) return;
      if (state.markers.get(id)) setPin(state.markers.get(id), p, true);
      if (fly) {
        // street-context zoom; the tilted 3D-buildings view needs a closer camera for buildings to extrude
        const tilted = (state.map.getTilt() || 0) > 0;
        state.map.moveCamera({ center: { lat: p.lat, lng: p.lng }, zoom: tilted ? SELECT_ZOOM_3D : SELECT_ZOOM, tilt: state.map.getTilt() || 0, heading: state.map.getHeading() || 0 });
        const panel = document.getElementById("right");
        if (panel && !panel.hidden && panel.offsetWidth < container.offsetWidth) state.map.panBy(panel.offsetWidth / 2, 0);
        if (state.map3d && !container.querySelector(".gmap3d").hidden) {
          state.map3d.flyCameraTo({ endCamera: { center: { lat: p.lat, lng: p.lng, altitude: 0 }, range: SELECT_RANGE_PHOTO, tilt: 65, heading: state.map3d.heading || 0 }, durationMillis: 2200 });
        }
      }
      sync3d();
    },
    fitTo(projects) {
      if (!projects.length || !state.map) return;
      const b = new google.maps.LatLngBounds();
      projects.forEach((p) => b.extend({ lat: p.lat, lng: p.lng }));
      state.map.fitBounds(b, 60);
    },
    bounds() {
      const b = state.map?.getBounds();
      return b ? { contains: ([lng, lat]) => b.contains({ lat, lng }) } : null;
    },
    /**
     * View mode: "2d" flat street map, "3d" tilted street map with extruded buildings (vector roadmap),
     * "photo" photorealistic 3D (Map3DElement, satellite/hybrid only).
     */
    async setView(mode) {
      await ready;
      if (mode !== "photo") {
        await this.set3d(false);
        state.map.setMapTypeId("roadmap");
        const zoom = mode === "3d" ? Math.max(state.map.getZoom() || 0, 17) : state.map.getZoom();
        state.map.moveCamera({ tilt: mode === "3d" ? 60 : 0, heading: mode === "3d" ? state.map.getHeading() || 0 : 0, zoom });
        return;
      }
      await this.set3d(true);
    },
    /** Toggle photorealistic 3D (Map3DElement), carrying over the camera centre. */
    async set3d(on) {
      await ready;
      if (on) {
        const { Map3DElement } = await google.maps.importLibrary("maps3d");
        const sel = state.projects.find((x) => x.id === state.selectedId);
        const mc = state.map.getCenter();
        const c = sel ? { lat: () => sel.lat, lng: () => sel.lng } : mc;
        const range = Math.min(60000, Math.max(400, 591657550 / 2 ** (state.map.getZoom() || 14)));
        if (!state.map3d) {
          state.map3d = new Map3DElement({ center: { lat: c.lat(), lng: c.lng(), altitude: 0 }, range, tilt: 62, heading: state.map.getHeading() || 0, mode: "HYBRID", gestureHandling: "GREEDY", defaultUIHidden: true });
          host3d.append(state.map3d);
          state.map3d.addEventListener("gmp-steadychange", (e) => { if (e.isSteady) sync3d(); });
          state.map3d.addEventListener("gmp-rangechange", () => onZoom(zoomFromRange(state.map3d.range)));
        } else {
          state.map3d.center = { lat: c.lat(), lng: c.lng(), altitude: 0 };
          state.map3d.range = range;
        }
        host2d.hidden = true;
        host3d.hidden = false;
        onZoom(zoomFromRange(state.map3d.range));
        await sync3d();
      } else {
        if (state.map3d?.center) state.map.setCenter({ lat: state.map3d.center.lat, lng: state.map3d.center.lng });
        host3d.hidden = true;
        host2d.hidden = false;
        onZoom(state.map.getZoom());
      }
    },
    /** Show a Google-validated place pin, with a dashed line to the project pin. */
    async showPlace(place, project) {
      await ready;
      this.clearPlace();
      if (!place?.location) return;
      const pin = new state.libs.PinElement({ background: "#1a73e8", borderColor: "#0b3d91", glyphColor: "#fff", glyphText: "G", scale: 1.1 });
      state.placeMarker = new state.libs.AdvancedMarkerElement({ map: state.map, position: place.location, title: `Google: ${place.name || ""}`, content: pin, zIndex: 999 });
      if (project) {
        state.placeLine = new google.maps.Polyline({
          map: state.map, path: [{ lat: project.lat, lng: project.lng }, place.location], strokeOpacity: 0,
          icons: [{ icon: { path: "M 0,-1 0,1", strokeOpacity: 1, scale: 3, strokeColor: "#1a73e8" }, offset: "0", repeat: "12px" }],
        });
      }
    },
    focusPlace(place) {
      if (!place || !state.map) return;
      if (place.viewport) state.map.fitBounds(place.viewport);
      else if (place.location) state.map.moveCamera({ center: place.location, zoom: 18 });
    },
    clearPlace() {
      if (state.placeMarker) state.placeMarker.map = null;
      state.placeLine?.setMap(null);
      state.placeMarker = state.placeLine = null;
    },
    /** Camera controls for the 3D view (default 3D UI is hidden so controls can live top-left). */
    camera3d(action) {
      const m = state.map3d;
      if (!m) return;
      const clampTilt = (t) => Math.max(0, Math.min(80, t));
      const ops = {
        "zoom-in": () => { m.range = Math.max(150, m.range * 0.6); },
        "zoom-out": () => { m.range = Math.min(200000, m.range * 1.6); },
        "rotate-left": () => { m.heading = ((m.heading || 0) - 30 + 360) % 360; },
        "rotate-right": () => { m.heading = ((m.heading || 0) + 30) % 360; },
        "tilt-up": () => { m.tilt = clampTilt((m.tilt || 0) + 10); },
        "tilt-down": () => { m.tilt = clampTilt((m.tilt || 0) - 10); },
        north: () => { m.heading = 0; },
        orbit: () => m.flyCameraAround({ camera: { center: m.center, range: m.range, tilt: m.tilt, heading: m.heading }, durationMillis: 12000, repeatCount: 1 }),
      };
      ops[action]?.();
    },
    closePopup: () => state.info?.close(),
  };
}
