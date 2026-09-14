import { loadData } from "./data.js";
import { createMap } from "./map.js";
import { renderList, scrollToItem } from "./list.js";
import { renderDetails, createLightbox } from "./details.js";
import {
  initFilterOptions, refreshDistricts, readFilters, applyFilters, sortProjects,
  activeFilterCount, resetFilters, setDeveloperFilter, FILTER_IDS,
} from "./filters.js";
import { esc, debounce, state } from "./util.js";

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
  app.mapApi.select(id, { fly });
  $("list").querySelectorAll(".item.selected").forEach((el) => { el.classList.remove("selected"); el.setAttribute("aria-selected", "false"); });
  const li = $("list").querySelector(`.item[data-id="${CSS.escape(id)}"]`);
  if (li) { li.classList.add("selected"); li.setAttribute("aria-selected", "true"); scrollToItem($("list"), id); }
  hashSelect(id);
  if (matchMedia("(max-width: 900px)").matches) document.body.classList.remove("left-open");
}

function closeDetails() {
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
  $("basemap").addEventListener("click", (e) => {
    const b = e.target.closest("button[data-style]");
    if (!b) return;
    app.mapApi.setBasemap(b.dataset.style);
    $("basemap").querySelectorAll("button").forEach((x) => x.classList.toggle("on", x === b));
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
    setTimeout(() => app.mapApi.map.resize(), 220);
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
    update();
    const m = location.hash.match(/p=([^&]+)/);
    if (m) select(decodeURIComponent(m[1]));
  } catch (err) {
    console.error(err);
    $("meta-line").textContent = `Could not load data: ${err.message}`;
  }
}

main();
