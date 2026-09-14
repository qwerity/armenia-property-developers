import { loadData } from "./data.js";
import { createMap } from "./map.js";
import { renderList, scrollToItem } from "./list.js";
import { renderDetails, createLightbox } from "./details.js";
import {
  initFilterOptions, refreshDistricts, readFilters, applyFilters, sortProjects,
  activeFilterCount, resetFilters, setDeveloperFilter, FILTER_IDS,
} from "./filters.js";
import { esc, debounce, state } from "./util.js";
import { createSearch } from "./search.js";
import { validateLocation } from "./placecheck.js";

const $ = (id) => document.getElementById(id);
const app = { projects: [], developers: [], visible: [], selectedId: null, mapApi: null };

function legend() {
  const f = readFilters();
  const shown = new Set(app.visible.map((p) => p.developer_group));
  const named = app.developers.filter((d) => !d.inferred || d.count > 1);
  const others = app.developers.length - named.length;
  $("legend-list").innerHTML = named.map((d) => `
    <li class="${shown.has(d.name) ? "" : "dim"} ${f.dev === d.name ? "on" : ""}" data-dev="${esc(d.name)}" title="Filter by ${esc(d.name)}">
      <span class="dot" style="background:${d.color}"></span><span class="name">${esc(d.name)}</span><span class="n">${d.count}</span>
    </li>`).join("") + (others ? `<li class="muted small">+ ${others} single-project developers (own colors)</li>` : "");
}

function hashSelect(id) {
  const url = new URL(location.href);
  if (id) url.hash = `p=${encodeURIComponent(id)}`; else url.hash = "";
  history.replaceState(null, "", url);
}

function select(id, { fly = true } = {}) {
  const p = app.projects.find((x) => x.id === id);
  if (!p) return;
  app.selectedId = id;
  $("right").hidden = false;
  document.body.classList.add("has-right");
  renderDetails($("details"), p, openLightbox, (dev) => { setDeveloperFilter(dev); update({ fit: true }); });
  checkPlace(p);
  app.mapApi.select(id, { fly });
  $("list").querySelectorAll(".item.selected").forEach((el) => { el.classList.remove("selected"); el.setAttribute("aria-selected", "false"); });
  const li = $("list").querySelector(`.item[data-id="${CSS.escape(id)}"]`);
  if (li) { li.classList.add("selected"); li.setAttribute("aria-selected", "true"); scrollToItem($("list"), id); }
  hashSelect(id);
  if (matchMedia("(max-width: 900px)").matches) document.body.classList.remove("left-open");
}

/** Validate the selected project's address with Google and show the precise place (pin + Places UI Kit card). */
async function checkPlace(p) {
  const box = $("details").querySelector("#gplace");
  if (!box) return;
  box.innerHTML = `<p class="muted small">Checking address with Google…</p>`;
  try {
    await app.mapApi.ready;
    const best = await validateLocation(p);
    if (app.selectedId !== p.id) return;
    if (!best) {
      box.innerHTML = `<p class="muted small">Google found no matching place for this address.</p>`;
      app.mapApi.clearPlace();
      return;
    }
    const verdict = best.distance_m <= 150 ? ["good", "matches our pin"] : best.distance_m <= 600 ? ["ok", "close to our pin"] : ["high", "differs from our pin"];
    box.innerHTML = `
      <div class="kv"><span>Google match</span><b>${esc(best.name ? `${best.name} — ` : "")}${esc(best.address || "")}</b></div>
      <div class="kv"><span>Precision</span><b>${esc(best.precision)} <span class="muted small">(${esc(best.source === "place" ? "Places API" : "Geocoder")})</span></b></div>
      <div class="kv"><span>Distance</span><b><span class="badge ${verdict[0]}">${best.distance_m} m · ${verdict[1]}</span></b></div>
      <div class="row"><button class="chip" id="gplace-go">Show precise place on map</button>
      <a class="chip" target="_blank" rel="noopener" href="https://www.google.com/maps/search/?api=1&query=${best.location.lat},${best.location.lng}${best.placeId ? `&query_place_id=${encodeURIComponent(best.placeId)}` : ""}">Open in Google Maps</a></div>
      ${best.source === "place" && best.placeId ? `<gmp-place-details-compact orientation="horizontal"><gmp-place-details-place-request place="${esc(best.placeId)}"></gmp-place-details-place-request><gmp-place-standard-content></gmp-place-standard-content></gmp-place-details-compact>` : ""}`;
    app.mapApi.showPlace(best, p);
    box.querySelector("#gplace-go").onclick = () => app.mapApi.focusPlace(best);
    if (box.querySelector("gmp-place-details-compact")) await google.maps.importLibrary("places");
  } catch (err) {
    console.warn(err);
    box.innerHTML = `<p class="muted small">Google address check unavailable: ${esc(err.message)}</p>`;
  }
}

function closeDetails() {
  app.mapApi.clearPlace();
  app.selectedId = null;
  $("right").hidden = true;
  document.body.classList.remove("has-right");
  app.mapApi.select(null, { fly: false });
  $("list").querySelectorAll(".item.selected").forEach((el) => el.classList.remove("selected"));
  hashSelect(null);
}

function update({ fit = false, pinsOnly = false } = {}) {
  const f = readFilters();
  const base = applyFilters(app.projects, { ...f, inView: false }, null);
  app.visible = sortProjects(f.inView ? applyFilters(base, f, app.mapApi.bounds()) : base, f.sort);
  if (!pinsOnly) {
    app.mapApi.setProjects(base).then(() => {
      if (app.selectedId && base.some((p) => p.id === app.selectedId)) app.mapApi.select(app.selectedId, { fly: false });
      if (fit) app.mapApi.fitTo(base);
    });
  }
  renderList($("list"), app.visible, app.selectedId, (id) => select(id));
  const n = activeFilterCount(f);
  $("active-filters").hidden = n === 0;
  $("active-filters").textContent = n;
  $("count").textContent = `${app.visible.length} of ${app.projects.length} projects`;
  legend();
}

function bindControls() {
  const onChange = () => update();
  $(FILTER_IDS.q).addEventListener("input", debounce(onChange, 120));
  $(FILTER_IDS.region).addEventListener("change", () => { refreshDistricts(app.projects); update({ fit: true }); });
  for (const k of ["district", "dev"]) $(FILTER_IDS[k]).addEventListener("change", () => update({ fit: true }));
  for (const k of ["kind", "status", "year", "deal", "priced", "tax", "inView", "sort", "info", "source", "hideSold", "precise", "grade", "clean"]) $(FILTER_IDS[k]).addEventListener("change", onChange);
  for (const k of ["pmin", "pmax", "budget"]) $(FILTER_IDS[k]).addEventListener("input", debounce(onChange, 250));
  $("reset").addEventListener("click", () => { resetFilters(); refreshDistricts(app.projects); update({ fit: true }); });

  $("currency").addEventListener("click", (e) => {
    const b = e.target.closest("button[data-cur]");
    if (!b) return;
    state.currency = b.dataset.cur;
    $("currency").querySelectorAll("button").forEach((x) => x.classList.toggle("on", x === b));
    update({ pinsOnly: true });
    if (app.selectedId) select(app.selectedId, { fly: false });
  });
  $("viewmode").addEventListener("click", async (e) => {
    const b = e.target.closest("button[data-mode]");
    if (!b) return;
    $("viewmode").querySelectorAll("button").forEach((x) => x.classList.toggle("on", x === b));
    await app.mapApi.setView(b.dataset.mode);
    $("ctrl3d").hidden = b.dataset.mode !== "photo";
  });
  $("ctrl3d").addEventListener("click", (e) => {
    const b = e.target.closest("button[data-cam]");
    if (b) app.mapApi.camera3d(b.dataset.cam);
  });
  $("legend-list").addEventListener("click", (e) => {
    const li = e.target.closest("li[data-dev]");
    if (!li) return;
    setDeveloperFilter(readFilters().dev === li.dataset.dev ? "" : li.dataset.dev);
    update({ fit: true });
  });
  $("legend-toggle").addEventListener("click", () => {
    const collapsed = $("legend").classList.toggle("collapsed");
    $("legend-toggle").textContent = collapsed ? "show" : "hide";
  });
  $("close-right").addEventListener("click", closeDetails);
  $("toggle-left").addEventListener("click", () => {
    const mobile = matchMedia("(max-width: 900px)").matches;
    document.body.classList.toggle(mobile ? "left-open" : "left-collapsed");
    setTimeout(() => app.mapApi.map && google.maps.event.trigger(app.mapApi.map, "resize"), 220);
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !e.defaultPrevented && $("lightbox").hidden && !$("right").hidden) closeDetails();
    if (e.key === "/" && document.activeElement?.tagName !== "INPUT") { e.preventDefault(); $("q").focus(); }
  });
}

let openLightbox = () => {};

async function main() {
  openLightbox = createLightbox($("lightbox"));
  if (matchMedia("(max-width: 900px)").matches) {
    $("legend").classList.add("collapsed");
    $("legend-toggle").textContent = "show";
  }
  app.mapApi = createMap($("map"), {
    onSelect: (id) => select(id, { fly: false }),
    onMove: () => { if (readFilters().inView) update({ pinsOnly: true }); },
  });
  try {
    const { meta, projects, developers } = await loadData();
    Object.assign(app, { projects, developers });
    state.rate = meta.amd_per_usd || state.rate;
    $("meta-line").textContent = `${projects.length} projects · ${developers.length} developers · data ${meta.generated} · 1 USD = ${meta.amd_per_usd} AMD`;
    initFilterOptions(projects, developers);
    bindControls();
    app.mapApi.ready.then(() => createSearch($("q"), {
      projects: () => app.projects,
      onProject: (id) => select(id),
      onPlace: (place) => { app.mapApi.showPlace(place); app.mapApi.focusPlace(place); },
      bias: () => app.mapApi.map?.getBounds() || null,
    })).catch((err) => { $("meta-line").textContent = err.message; });
    update();
    const m = location.hash.match(/p=([^&]+)/);
    if (m) select(decodeURIComponent(m[1]));
  } catch (err) {
    console.error(err);
    $("meta-line").textContent = `Could not load data: ${err.message}`;
  }
}

main();
