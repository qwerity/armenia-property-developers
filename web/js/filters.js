const $ = (id) => document.getElementById(id);

const FIELDS = {
  q: "q", region: "f-region", district: "f-district", dev: "f-dev", kind: "f-kind", status: "f-status",
  pmin: "f-pmin", pmax: "f-pmax", budget: "f-budget", year: "f-year",
  deal: "f-deal", priced: "f-priced", tax: "f-tax", inView: "f-view", sort: "sort",
  info: "f-info", source: "f-source", hideSold: "f-hidesold", precise: "f-precise", grade: "f-grade", clean: "f-clean",
};

function fillSelect(el, values, allLabel, counts) {
  const current = el.value;
  el.innerHTML = "";
  el.append(new Option(allLabel, ""));
  for (const v of values) el.append(new Option(counts ? `${v} (${counts.get(v)})` : v, v));
  el.value = values.includes(current) ? current : "";
}

function countBy(items, key) {
  const m = new Map();
  for (const p of items) if (p[key]) m.set(p[key], (m.get(p[key]) || 0) + 1);
  return m;
}

/** Populate filter dropdowns from the dataset. */
export function initFilterOptions(projects, developers) {
  const regions = countBy(projects, "region");
  fillSelect($(FIELDS.region), [...regions.keys()].sort(), "All regions", regions);
  refreshDistricts(projects);
  const devSel = $(FIELDS.dev);
  devSel.innerHTML = "";
  devSel.append(new Option("All developers", ""));
  for (const d of developers) devSel.append(new Option(`${d.name} (${d.count})`, d.name));
  const kinds = countBy(projects, "kind");
  fillSelect($(FIELDS.kind), [...kinds.keys()].sort(), "Any", kinds);
  const sources = new Map();
  for (const p of projects) for (const s of p.sources || []) if (s.name) sources.set(s.name, (sources.get(s.name) || 0) + 1);
  fillSelect($(FIELDS.source), [...sources.keys()].sort(), "All sources", sources);
  const stages = countBy(projects, "stage");
  for (const opt of $(FIELDS.status).options) {
    if (opt.value) opt.textContent = `${opt.textContent.replace(/ \(\d+\)$/, "")} (${stages.get(opt.value) || 0})`;
  }
  const years = [...new Set(projects.map((p) => p.completion_year).filter(Boolean))].sort();
  fillSelect($(FIELDS.year), years.map(String), "Any");
}

/** Rebuild the district list so it only offers districts inside the chosen region. */
export function refreshDistricts(projects) {
  const region = $(FIELDS.region).value;
  const pool = region ? projects.filter((p) => p.region === region) : projects;
  const districts = countBy(pool, "district");
  fillSelect($(FIELDS.district), [...districts.keys()].sort(), "All districts", districts);
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
