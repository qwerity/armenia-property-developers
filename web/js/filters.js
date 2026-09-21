const $ = (id) => document.getElementById(id);

const FIELDS = {
  q: "q", region: "f-region", district: "f-district", dev: "f-dev", kind: "f-kind", status: "f-status",
  pmin: "f-pmin", pmax: "f-pmax", budget: "f-budget", year: "f-year",
  deal: "f-deal", priced: "f-priced", tax: "f-tax", inView: "f-view", sort: "sort",
  info: "f-info", source: "f-source", hideSold: "f-hidesold", precise: "f-precise", grade: "f-grade", clean: "f-clean",
};

const universe = { values: {}, devOrder: [] };

const SELECT_FACETS = {
  region: { all: "All regions", values: (p) => [p.region] },
  district: { all: "All districts", values: (p) => [p.district] },
  dev: { all: "All developers", values: (p) => [p.developer_group] },
  kind: { all: "Any", values: (p) => [p.kind] },
  source: { all: "All sources", values: (p) => (p.sources || []).map((x) => x.name) },
};
const STATIC_FACETS = {
  status: { match: (p, v) => p.stage === v },
  year: { match: (p, v) => p.completion_year != null && p.completion_year <= Number(v), dynamicValues: true },
  info: { match: (p, v) => p.info_score >= Number(v) },
  grade: { match: (p, v) => p.developer_rep && p.developer_rep.grade <= v },
};
const CHECK_FACETS = ["deal", "priced", "tax", "inView", "hideSold", "precise", "clean"];
const EMPTY = { region: "", district: "", dev: "", kind: "", status: "", source: "", grade: "", year: null, info: null, pmin: null, pmax: null, budget: null };

/** Remember every possible option value (dataset order) so facets can be rebuilt with live counts. */
export function initFilterOptions(projects) {
  for (const [key, facet] of Object.entries(SELECT_FACETS)) {
    const set = new Set();
    for (const p of projects) for (const v of facet.values(p)) if (v) set.add(v);
    universe.values[key] = [...set].sort((a, b) => a.localeCompare(b));
  }
  const years = [...new Set(projects.map((p) => p.completion_year).filter(Boolean))].sort();
  const yearSel = $(FIELDS.year);
  yearSel.innerHTML = "";
  yearSel.append(new Option("Any", ""));
  for (const y of years) yearSel.append(new Option(String(y), String(y)));
  for (const key of CHECK_FACETS) {
    const label = $(FIELDS[key]).closest("label");
    if (!label.querySelector(".fcount")) label.insertAdjacentHTML("beforeend", ` <span class="fcount"></span>`);
  }
}

function withoutFacet(f, key) {
  const g = { ...f };
  g[key] = key in EMPTY ? EMPTY[key] : false;
  return g;
}

function rebuildSelect(key, counts) {
  const el = $(FIELDS[key]);
  const current = el.value;
  el.innerHTML = "";
  el.append(new Option(SELECT_FACETS[key].all, ""));
  for (const v of universe.values[key]) {
    const n = counts.get(v) || 0;
    if (!n && v !== current) continue;
    el.append(new Option(`${v} (${n})`, v));
  }
  el.value = current;
}

/**
 * Faceted counts: every option shows how many projects would match if it were chosen together with
 * all OTHER active filters; options that would yield nothing are hidden (the current choice is kept).
 * @param {object[]} projects all projects
 * @param {ReturnType<typeof readFilters>} f current filters
 * @param {{contains:Function}|null} bounds viewport (for "only in map view")
 */
export function refreshFacets(projects, f, bounds) {
  for (const [key, facet] of Object.entries(SELECT_FACETS)) {
    const pool = applyFilters(projects, withoutFacet(f, key), bounds);
    const counts = new Map();
    for (const p of pool) for (const v of new Set(facet.values(p))) if (v) counts.set(v, (counts.get(v) || 0) + 1);
    rebuildSelect(key, counts);
  }
  for (const [key, facet] of Object.entries(STATIC_FACETS)) {
    const pool = applyFilters(projects, withoutFacet(f, key), bounds);
    for (const opt of $(FIELDS[key]).options) {
      if (!opt.dataset.label) opt.dataset.label = opt.textContent;
      if (!opt.value) {
        opt.textContent = `${opt.dataset.label} (${pool.length})`;
        continue;
      }
      const n = pool.filter((p) => facet.match(p, opt.value)).length;
      opt.textContent = `${opt.dataset.label} (${n})`;
      opt.hidden = n === 0 && opt.value !== $(FIELDS[key]).value;
    }
  }
  for (const key of CHECK_FACETS) {
    const n = applyFilters(projects, { ...withoutFacet(f, key), [key]: true }, bounds).length;
    const box = $(FIELDS[key]);
    box.closest("label").querySelector(".fcount").textContent = `(${n})`;
    box.disabled = n === 0 && !box.checked;
  }
}

function filterLabel(el) {
  const label = el.closest("label");
  const text = [...label.childNodes].filter((n) => n.nodeType === Node.TEXT_NODE).map((n) => n.textContent).join(" ").trim();
  if (el.type === "checkbox") return text;
  const shown = el.tagName === "SELECT" ? el.selectedOptions[0]?.textContent.replace(/\s*\(\d+\)$/, "") : el.value;
  return `${text}: ${shown}`;
}

function clearField(el) {
  if (el.type === "checkbox") el.checked = false; else el.value = "";
}

/**
 * Highlight changed filters and list them as removable chips.
 * @param {ReturnType<typeof readFilters>} f
 * @param {(key:string)=>void} onClear called after a filter was cleared
 * @param {HTMLElement} [chipsEl] container for active-filter chips
 */
export function markChangedFilters(f, onClear, chipsEl) {
  const chips = [];
  for (const [key, id] of Object.entries(FIELDS)) {
    if (key === "q" || key === "sort") continue;
    const el = $(id);
    const label = el.closest("label");
    const active = el.type === "checkbox" ? el.checked : el.value.trim() !== "";
    label.classList.toggle("changed", active);
    if (active) chips.push({ key, text: filterLabel(el) });
  }
  if (!chipsEl) return;
  chipsEl.hidden = !chips.length;
  chipsEl.replaceChildren(...chips.map(({ key, text }) => {
    const chip = document.createElement("button");
    chip.type = "button";
    chip.className = "fchip";
    chip.title = "Remove filter";
    chip.innerHTML = `<span></span><i aria-hidden="true">×</i>`;
    chip.firstChild.textContent = text;
    chip.addEventListener("click", () => { clearField($(FIELDS[key])); onClear(key); });
    return chip;
  }));
}

export function readFilters() {
  const v = (k) => $(FIELDS[k]).value.trim();
  const n = (k) => (v(k) === "" ? null : Number(v(k)));
  const c = (k) => $(FIELDS[k]).checked;
  return {
    q: v("q").toLowerCase(), region: v("region"), district: v("district"), dev: v("dev"), kind: v("kind"),
    status: v("status"), pmin: n("pmin"), pmax: n("pmax"), budget: n("budget"), year: n("year"),
    deal: c("deal"), priced: c("priced"), tax: c("tax"), inView: c("inView"), sort: v("sort"),
    info: n("info"), source: v("source"), hideSold: c("hideSold"), precise: c("precise"), grade: v("grade"), clean: c("clean"),
  };
}

export function activeFilterCount(f) {
  return ["region", "district", "dev", "kind", "status", "source", "grade"].filter((k) => f[k]).length
    + ["pmin", "pmax", "budget", "year", "info"].filter((k) => f[k] != null).length
    + ["deal", "priced", "tax", "inView", "hideSold", "precise", "clean"].filter((k) => f[k]).length;
}

export function resetFilters() {
  for (const [k, id] of Object.entries(FIELDS)) {
    const el = $(id);
    if (k === "sort") continue;
    if (el.type === "checkbox") el.checked = false; else el.value = "";
  }
}

export function setDeveloperFilter(name) {
  $(FIELDS.dev).value = name;
}

/**
 * Filter projects. Price filters are always in USD per m² (converted at build time).
 * @param {object[]} projects
 * @param {ReturnType<typeof readFilters>} f
 * @param {{contains:(lngLat:[number, number])=>boolean}|null} bounds map viewport
 */
export function applyFilters(projects, f, bounds) {
  const terms = f.q.split(/\s+/).filter(Boolean);
  return projects.filter((p) => {
    if (terms.length && !terms.every((t) => p._search.includes(t))) return false;
    if (f.region && p.region !== f.region) return false;
    if (f.district && p.district !== f.district) return false;
    if (f.dev && p.developer_group !== f.dev) return false;
    if (f.kind && p.kind !== f.kind) return false;
    if (f.status && p.stage !== f.status) return false;
    if (f.pmin != null && !(p.usd_m2_min >= f.pmin)) return false;
    if (f.pmax != null && !(p.usd_m2_min != null && p.usd_m2_min <= f.pmax)) return false;
    if (f.budget != null && !(p.usd_from != null && p.usd_from <= f.budget)) return false;
    if (f.year != null && !(p.completion_year != null && p.completion_year <= f.year)) return false;
    if (f.deal && !(p.discount_pct > 0)) return false;
    if (f.priced && p.usd_m2_min == null && p.usd_from == null) return false;
    if (f.tax && !p.income_tax_refund) return false;
    if (f.info != null && !(p.info_score >= f.info)) return false;
    if (f.source && !(p.sources || []).some((s) => s.name === f.source)) return false;
    if (f.hideSold && p.sold_out) return false;
    if (f.precise && (p.geo_precision === "district" || p.geo_precision === "city")) return false;
    if (f.grade && !(p.developer_rep && p.developer_rep.grade <= f.grade)) return false;
    if (f.clean && (p.developer_rep?.flags || []).some((x) => /bankruptcy|criminal|lawsuit|negative news/.test(x))) return false;
    if (f.inView && bounds && !bounds.contains([p.lng, p.lat])) return false;
    return true;
  });
}

const nullsLast = (a, b, cmp) => (a == null) - (b == null) || (a == null ? 0 : cmp(a, b));

const SORTS = {
  deal: (a, b) => nullsLast(a.discount_pct, b.discount_pct, (x, y) => y - x),
  ppm: (a, b) => nullsLast(a.usd_m2_min, b.usd_m2_min, (x, y) => x - y),
  from: (a, b) => nullsLast(a.usd_from, b.usd_from, (x, y) => x - y),
  soon: (a, b) => nullsLast(a.completion, b.completion, (x, y) => x.localeCompare(y)),
  pop: (a, b) => nullsLast(a.popularity, b.popularity, (x, y) => y - x),
  name: (a, b) => a.title.localeCompare(b.title),
  rep: (a, b) => nullsLast(a.developer_rep?.score, b.developer_rep?.score, (x, y) => y - x),
  info: (a, b) => nullsLast(a.info_score, b.info_score, (x, y) => y - x),
};

export function sortProjects(list, key) {
  return [...list].sort((a, b) => (SORTS[key] || SORTS.deal)(a, b) || a.title.localeCompare(b.title));
}

export const FILTER_IDS = FIELDS;
