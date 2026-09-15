import { loadData } from "./data.js";
import { state, stageLabel } from "./util.js";
import { hbar, columns, stacked, scatter, table } from "./charts.js";

const $ = (id) => document.getElementById(id);
const STAGES = [
  { key: "finished", label: "Finished", color: "var(--viz-s1)" },
  { key: "in progress", label: "In progress", color: "var(--viz-s2)" },
  { key: "just started", label: "Just started", color: "var(--viz-s3)" },
  { key: "not started", label: "Not yet started", color: "var(--viz-s4)" },
  { key: "stalled", label: "Stalled", color: "var(--viz-s5)" },
  { key: "unknown", label: "Unknown", color: "var(--viz-unknown)" },
];
const GRADES = ["A", "B", "C", "D", "E"];
const GRADE_COLORS = { A: "var(--viz-ord-5)", B: "var(--viz-ord-4)", C: "var(--viz-ord-3)", D: "var(--viz-ord-2)", E: "var(--viz-ord-1)" };
const app = { projects: [], meta: {} };

// ---------------------------------------------------------------- numbers
const median = (xs) => {
  if (!xs.length) return null;
  const s = [...xs].sort((a, b) => a - b);
  const m = Math.floor(s.length / 2);
  return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2;
};
const quantile = (xs, q) => {
  const s = [...xs].sort((a, b) => a - b);
  if (!s.length) return null;
  const i = (s.length - 1) * q;
  return s[Math.floor(i)] + (s[Math.ceil(i)] - s[Math.floor(i)]) * (i % 1);
};
const perM2 = (usd) => (state.currency === "USD" ? usd : usd * state.rate);
function fmtMoney(usd, { compact = false, suffix = "" } = {}) {
  if (usd == null || Number.isNaN(usd)) return "—";
  const v = perM2(usd);
  const sym = state.currency === "USD" ? "$" : "֏";
  if (compact && v >= 1e6) return `${sym}${(v / 1e6).toFixed(v >= 1e7 ? 0 : 1)}M${suffix}`;
  if (compact && v >= 1e4) return `${sym}${Math.round(v / 1e3)}k${suffix}`;
  return `${sym}${Math.round(v).toLocaleString("en-US")}${suffix}`;
}
const fmtInt = (n) => Math.round(n).toLocaleString("en-US");
const pct = (a, b) => (b ? `${Math.round((a / b) * 100)}%` : "—");
const priced = (p) => p.kind === "Apartments" && p.usd_m2_min != null;
const openOnMap = (id) => () => { location.href = `index.html#p=${encodeURIComponent(id)}`; };
const mapLink = (p) => {
  const a = document.createElement("a");
  a.href = `index.html#p=${encodeURIComponent(p.id)}`;
  a.textContent = p.title;
  return a;
};

// ---------------------------------------------------------------- filters
function fillSelect(sel, values, allLabel) {
  const cur = sel.value;
  sel.replaceChildren(new Option(allLabel, ""));
  for (const [v, n] of values) sel.append(new Option(`${v} (${n})`, v));
  sel.value = values.some(([v]) => v === cur) ? cur : "";
}
const counts = (items, key) => [...items.reduce((m, p) => (p[key] ? m.set(p[key], (m.get(p[key]) || 0) + 1) : m), new Map())].sort((a, b) => b[1] - a[1]);

function readFilters() {
  return { region: $("af-region").value, district: $("af-district").value, kind: $("af-kind").value, stage: $("af-stage").value, grade: $("af-grade").value };
}

function filtered(skip) {
  const f = readFilters();
  return app.projects.filter((p) =>
    (skip === "region" || !f.region || p.region === f.region)
    && (skip === "district" || !f.district || p.district === f.district)
    && (skip === "kind" || !f.kind || p.kind === f.kind)
    && (skip === "stage" || !f.stage || p.stage === f.stage)
    && (skip === "grade" || !f.grade || (p.developer_rep && p.developer_rep.grade <= f.grade)));
}

function refreshFilterOptions() {
  fillSelect($("af-region"), counts(filtered("region"), "region"), "All regions");
  fillSelect($("af-district"), counts(filtered("district"), "district"), "All districts");
  fillSelect($("af-kind"), counts(filtered("kind"), "kind"), "All types");
  const stageCounts = counts(filtered("stage"), "stage").map(([k, n]) => [k, n]);
  const sel = $("af-stage");
  const cur = sel.value;
  sel.replaceChildren(new Option("All stages", ""));
  for (const s of STAGES) {
    const n = stageCounts.find(([k]) => k === s.key)?.[1];
    if (n) sel.append(new Option(`${s.label} (${n})`, s.key));
  }
  sel.value = cur;
  const f = readFilters();
  $("af-reset").hidden = !Object.values(f).some(Boolean);
}

// ---------------------------------------------------------------- sections
function renderKpis(items) {
  const p = items.filter(priced);
  const prices = p.map((x) => x.usd_m2_min);
  const med = median(prices);
  $("kpi-hero").textContent = med ? fmtMoney(med) : "—";
  $("kpi-hero-sub").textContent = prices.length
    ? `${fmtInt(prices.length)} priced apartment projects · middle half ${fmtMoney(quantile(prices, 0.25))}–${fmtMoney(quantile(prices, 0.75))}`
    : "No current prices in this filter";
  const building = items.filter((x) => ["in progress", "just started"].includes(x.stage)).length;
  const devs = new Set(items.map((x) => x.developer_group).filter((d) => d && d !== "Unknown developer")).size;
  const verified = items.filter((x) => x.price_confidence === "verified").length;
  const soldOut = items.filter((x) => x.sold_out).length;
  const risky = new Set(items.filter((x) => (x.developer_rep?.flags || []).some((f) => /bankruptcy|criminal/.test(f))).map((x) => x.developer_group)).size;
  const tiles = [
    ["Projects", fmtInt(items.length), `${fmtInt(devs)} developers`],
    ["Under construction", fmtInt(building), `${pct(building, items.length)} of projects`],
    ["Prices checked on source", fmtInt(verified), `${pct(verified, items.length)} of projects`],
    ["Sold out", fmtInt(soldOut), `${pct(soldOut, items.length)} of projects`],
    ["Median apartment from", fmtMoney(median(items.map((x) => x.usd_from).filter(Boolean)), { compact: true }), "cheapest listed unit"],
    ["Developers with bankruptcy cases", fmtInt(risky), "from datalex court records"],
  ];
  $("an-kpis").replaceChildren(...tiles.map(([label, value, small]) => {
    const d = document.createElement("div");
    d.className = "kpi";
    const s = document.createElement("span"); s.textContent = label;
    const b = document.createElement("b"); b.textContent = value;
    const m = document.createElement("small"); m.textContent = small;
    d.append(s, b, m);
    return d;
  }));
}

function renderDistricts(items) {
  const groups = new Map();
  for (const p of items.filter(priced)) {
    const d = p.district || p.region || "Unknown";
    const key = p.region === "Yerevan" ? d
      : /\(other\)$/.test(d) ? `Other ${p.region}` : d === p.region ? d : `${d.replace(/\s*\(.*\)$/, "")}, ${p.region}`;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(p.usd_m2_min);
  }
  const rows = [...groups].filter(([, v]) => v.length >= 3)
    .map(([label, v]) => ({ label, n: v.length, med: median(v), q1: quantile(v, 0.25), q3: quantile(v, 0.75) }))
    .sort((a, b) => b.med - a.med)
    .slice(0, 22);
  hbar($("ch-district"), rows.map((r) => ({
    label: r.label, value: r.med, display: fmtMoney(r.med),
    tipLabel: `${r.label} · ${r.n} projects`, tipNote: `middle half ${fmtMoney(r.q1)}–${fmtMoney(r.q3)}`,
  })), { format: (v) => fmtMoney(v, { compact: true }) });
  table($("tb-district"), [
    { label: "Area", key: "label" }, { label: "Projects", key: "n", num: true },
    { label: "Median / m²", num: true, render: (r) => fmtMoney(r.med) },
    { label: "25th pct", num: true, render: (r) => fmtMoney(r.q1) }, { label: "75th pct", num: true, render: (r) => fmtMoney(r.q3) },
  ], rows);
}

function renderHistogram(items) {
  const prices = items.filter(priced).map((p) => p.usd_m2_min);
  const step = 250;
  const cap = 4500;
  const bins = [];
  for (let lo = 500; lo < cap; lo += step) bins.push({ lo, hi: lo + step, n: 0 });
  bins.push({ lo: cap, hi: Infinity, n: 0 });
  const below = { lo: 0, hi: 500, n: 0 };
  for (const v of prices) {
    if (v < 500) { below.n++; continue; }
    (bins.find((b) => v >= b.lo && v < b.hi) || bins[bins.length - 1]).n++;
  }
  const all = [below, ...bins];
  const label = (b) => (b.hi === Infinity ? `${fmtMoney(b.lo, { compact: true })}+` : b.lo === 0 ? `<${fmtMoney(b.hi, { compact: true })}` : fmtMoney(b.lo, { compact: true }));
  columns($("ch-hist"), all.map((b) => ({
    label: label(b), value: b.n,
    tipLabel: b.hi === Infinity ? `${fmtMoney(b.lo)} and above` : `${fmtMoney(b.lo)}–${fmtMoney(b.hi)} per m²`,
  })), { format: (v) => String(Math.round(v)), labelEvery: 4 });
  table($("tb-hist"), [
    { label: "Band", render: (b) => (b.hi === Infinity ? `${fmtMoney(b.lo)}+` : `${fmtMoney(b.lo)}–${fmtMoney(b.hi)}`) },
    { label: "Projects", key: "n", num: true },
  ], all.filter((b) => b.n));
}

function renderPipeline(items) {
  const years = new Map();
  for (const p of items) if (p.completion_year) years.set(p.completion_year, (years.get(p.completion_year) || 0) + 1);
  const thisYear = new Date().getFullYear();
  const keys = [...years.keys()].filter((y) => y >= thisYear - 5 && y <= thisYear + 6).sort();
  const earlier = [...years].filter(([y]) => y < thisYear - 5).reduce((s, [, n]) => s + n, 0);
  const cols = keys.map((y) => ({
    label: String(y), value: years.get(y), color: y < thisYear ? "var(--viz-past)" : "var(--viz-seq)",
    tipLabel: `${y}${y < thisYear ? " (delivered or overdue)" : y === thisYear ? " (this year)" : ""}`,
  }));
  columns($("ch-pipeline"), cols, { format: (v) => String(Math.round(v)) });
  table($("tb-pipeline"), [{ label: "Completion year", key: "label" }, { label: "Projects", key: "value", num: true }],
    [...(earlier ? [{ label: `before ${thisYear - 5}`, value: earlier }] : []), ...cols]);
}

function renderStages(items) {
  const f = readFilters();
  const byDistrict = Boolean(f.region || f.district);
  const key = (p) => (byDistrict ? p.district : p.region) || "Unknown";
  const groups = new Map();
  for (const p of items) {
    const k = key(p);
    if (!groups.has(k)) groups.set(k, new Map());
    const m = groups.get(k);
    m.set(p.stage || "unknown", (m.get(p.stage || "unknown") || 0) + 1);
  }
  let rows = [...groups].map(([label, m]) => ({ label, total: [...m.values()].reduce((a, b) => a + b, 0), m }))
    .sort((a, b) => b.total - a.total);
  if (rows.length > 12) {
    const tail = rows.slice(11);
    const other = new Map();
    for (const r of tail) for (const [k, v] of r.m) other.set(k, (other.get(k) || 0) + v);
    rows = [...rows.slice(0, 11), { label: `Other (${tail.length})`, total: tail.reduce((s, r) => s + r.total, 0), m: other }];
  }
  const present = STAGES.filter((s) => rows.some((r) => r.m.get(s.key)));
  $("lg-stage").replaceChildren(...present.map((s) => {
    const span = document.createElement("span");
    const i = document.createElement("i"); i.style.background = s.color;
    span.append(i, document.createTextNode(s.label));
    return span;
  }));
  stacked($("ch-stage"), rows.map((r) => ({ label: r.label, parts: present.map((s) => ({ key: s.key, value: r.m.get(s.key) || 0 })) })), present);
  table($("tb-stage"), [{ label: byDistrict ? "District" : "Region", key: "label" },
    ...present.map((s) => ({ label: s.label, num: true, render: (r) => r.m.get(s.key) || 0 })),
    { label: "Total", key: "total", num: true }], rows);
}

function renderScatter(items) {
  const pts = items.filter((p) => priced(p) && p.completion)
    .map((p) => ({ p, d: new Date(p.completion) }))
    .filter(({ d }) => !Number.isNaN(d.getTime()) && d.getFullYear() >= 2018 && d.getFullYear() <= 2032)
    .map(({ p, d }) => ({
      x: d, y: p.usd_m2_min, label: `${p.title} · ${p.district || p.region || ""}`,
      note: `${stageLabel(p)} · ready ${p.completion.slice(0, 7)}${p.developer_rep ? ` · developer ${p.developer_rep.grade}` : ""}`,
      onClick: openOnMap(p.id),
    }));
  scatter($("ch-scatter"), pts, { formatY: (v) => fmtMoney(v, { compact: true }) });
}

function renderGrades(items) {
  const n = new Map(GRADES.map((g) => [g, 0]));
  let none = 0;
  for (const p of items) {
    const g = p.developer_rep?.grade;
    if (g) n.set(g, n.get(g) + 1); else none++;
  }
  const cols = GRADES.map((g) => ({ label: g, value: n.get(g), color: GRADE_COLORS[g], tipLabel: `Developer rating ${g}` }));
  columns($("ch-grades"), cols, { format: (v) => String(Math.round(v)) });
  table($("tb-grades"), [{ label: "Rating", key: "label" }, { label: "Projects", key: "value", num: true }],
    [...cols, { label: "Not rated", value: none }]);
}

function qualityRow(title, parts, total) {
  const wrap = document.createElement("div");
  wrap.className = "q-row";
  const head = document.createElement("div");
  head.className = "q-head";
  const t = document.createElement("span"); t.textContent = title;
  const good = parts.filter((x) => x.good).reduce((s, x) => s + x.n, 0);
  const g = document.createElement("b"); g.textContent = `${pct(good, total)} good`;
  head.append(t, g);
  const bar = document.createElement("div");
  bar.className = "q-bar";
  const keys = document.createElement("div");
  keys.className = "q-keys";
  for (const part of parts.filter((x) => x.n)) {
    const seg = document.createElement("div");
    seg.style.flex = String(part.n);
    seg.style.background = part.color;
    seg.title = `${part.label}: ${part.n} (${pct(part.n, total)})`;
    bar.append(seg);
    const k = document.createElement("span");
    const i = document.createElement("i"); i.style.background = part.color;
    k.append(i, document.createTextNode(`${part.label} ${part.n}`));
    keys.append(k);
  }
  wrap.append(head, bar, keys);
  return wrap;
}

function renderQuality(items) {
  const total = items.length;
  const c = (fn) => items.filter(fn).length;
  $("ch-quality").replaceChildren(
    qualityRow("Price", [
      { label: "Checked on source", n: c((p) => p.price_confidence === "verified"), color: "var(--viz-ord-5)", good: true },
      { label: "Several sources agree", n: c((p) => p.price_confidence === "high"), color: "var(--viz-ord-3)", good: true },
      { label: "One source", n: c((p) => ["medium", "low", "rejected"].includes(p.price_confidence)), color: "var(--viz-ord-1)" },
      { label: "No current price", n: c((p) => !p.price_confidence || p.price_confidence === "none"), color: "var(--viz-unknown)" },
    ], total),
    qualityRow("Location", [
      { label: "Exact", n: c((p) => p.geo_precision === "exact"), color: "var(--viz-ord-5)", good: true },
      { label: "Address", n: c((p) => p.geo_precision === "address"), color: "var(--viz-ord-3)", good: true },
      { label: "Street", n: c((p) => p.geo_precision === "street"), color: "var(--viz-ord-1)" },
      { label: "District / town", n: c((p) => ["district", "city"].includes(p.geo_precision)), color: "var(--viz-unknown)" },
    ], total),
    qualityRow("Information completeness", [
      { label: "90–100%", n: c((p) => p.info_score >= 90), color: "var(--viz-ord-5)", good: true },
      { label: "70–89%", n: c((p) => p.info_score >= 70 && p.info_score < 90), color: "var(--viz-ord-3)", good: true },
      { label: "50–69%", n: c((p) => p.info_score >= 50 && p.info_score < 70), color: "var(--viz-ord-1)" },
      { label: "Below 50%", n: c((p) => p.info_score < 50), color: "var(--viz-unknown)" },
    ], total),
    qualityRow("Developer research", [
      { label: "Full court + registry research", n: c((p) => p.developer_rep?.data === "full"), color: "var(--viz-ord-5)", good: true },
      { label: "Limited", n: c((p) => p.developer_rep && p.developer_rep.data !== "full"), color: "var(--viz-ord-1)" },
      { label: "No developer identified", n: c((p) => !p.developer_rep), color: "var(--viz-unknown)" },
    ], total),
  );
}

function renderDevelopers(items) {
  const groups = new Map();
  for (const p of items) {
    const g = p.developer_group;
    if (!g || g === "Unknown developer" || g.endsWith("(developer n/a)")) continue;
    if (!groups.has(g)) groups.set(g, []);
    groups.get(g).push(p);
  }
  const rows = [...groups].map(([name, ps]) => ({
    name, n: ps.length,
    building: ps.filter((p) => ["in progress", "just started"].includes(p.stage)).length,
    med: median(ps.filter(priced).map((p) => p.usd_m2_min)),
    rep: ps[0].developer_rep,
  })).sort((a, b) => b.n - a.n || a.name.localeCompare(b.name)).slice(0, 20);
  table($("tb-developers"), [
    { label: "Developer", key: "name" },
    { label: "Projects", key: "n", num: true },
    { label: "Under construction", key: "building", num: true },
    { label: "Median / m²", num: true, render: (r) => fmtMoney(r.med) },
    { label: "Rating", render: (r) => (r.rep ? `${r.rep.grade} (${r.rep.score})${r.rep.data === "full" ? "" : "?"}` : "—") },
    { label: "Legal flags", render: (r) => (r.rep?.flags || []).filter((f) => !/not checked/.test(f)).join("; ") || "none found" },
  ], rows);
}

function renderDeals(items) {
  const rows = items.filter((p) => priced(p) && p.price_confidence === "verified" && p.discount_pct > 0 && !p.sold_out)
    .sort((a, b) => b.discount_pct - a.discount_pct).slice(0, 20);
  table($("tb-deals"), [
    { label: "Project", render: mapLink },
    { label: "Area", render: (p) => p.district || p.region },
    { label: "Price / m²", num: true, render: (p) => fmtMoney(p.usd_m2_min) },
    { label: "Local median", num: true, render: (p) => fmtMoney(p.bench_usd_m2) },
    { label: "Below median", num: true, render: (p) => `${p.discount_pct}%` },
    { label: "Stage", render: (p) => stageLabel(p) },
    { label: "Developer", render: (p) => `${p.developer_group}${p.developer_rep ? ` · ${p.developer_rep.grade}` : ""}` },
  ], rows);
}

function render() {
  refreshFilterOptions();
  const items = filtered();
  document.getElementById("an-main").style.opacity = "1";
  renderKpis(items);
  renderDistricts(items);
  renderHistogram(items);
  renderPipeline(items);
  renderStages(items);
  renderScatter(items);
  renderGrades(items);
  renderQuality(items);
  renderDevelopers(items);
  renderDeals(items);
}

function bind() {
  for (const id of ["af-region", "af-district", "af-kind", "af-stage", "af-grade"]) $(id).addEventListener("change", render);
  $("af-reset").addEventListener("click", () => {
    for (const id of ["af-region", "af-district", "af-kind", "af-stage", "af-grade"]) $(id).value = "";
    render();
  });
  $("af-currency").addEventListener("click", (e) => {
    const b = e.target.closest("button[data-cur]");
    if (!b) return;
    state.currency = b.dataset.cur;
    $("af-currency").querySelectorAll("button").forEach((x) => x.classList.toggle("on", x === b));
    render();
  });
}

async function main() {
  try {
    const { meta, projects } = await loadData();
    app.meta = meta;
    app.projects = projects;
    state.rate = meta.amd_per_usd || state.rate;
    $("an-meta").textContent = `${projects.length} projects · data ${meta.generated} · 1 USD = ${meta.amd_per_usd} AMD · prices are asking prices of available units`;
    bind();
    render();
  } catch (err) {
    console.error(err);
    $("an-meta").textContent = `Could not load data: ${err.message}`;
  }
}

main();
