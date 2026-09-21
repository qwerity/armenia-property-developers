import { loadData } from "./data.js";
import { state, stageLabel } from "./util.js";
import { hbar, columns, stacked, scatter, table } from "./charts.js";
import { drawGraph, typeInfo, edgeInfo, BANKRUPTCY, SUGGESTED } from "./graph.js";
import { drawTree } from "./tree.js";

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
const app = { projects: [], meta: {}, connections: null, cnSelected: null, cnView: "graph" };

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


// ---------------------------------------------------------------- connections graph
const cnNode = (id) => app.connections?.byId.get(id);

/** Nodes to draw: clusters kept whole, filtered by scope, by the page filters and by the focus pick. */
function connectionView(items) {
  const c = app.connections;
  if (!c) return { nodes: [], edges: [] };
  const scope = $("cn-scope").value;
  const focus = $("cn-focus").value;
  const inFilter = new Set(items.map((p) => p.developer_group));
  const flagged = new Set(c.nodes.filter((n) => n.bankruptcy).map((n) => n.component));
  const keep = new Set();
  for (const n of c.nodes) {
    if (n.type !== "developer") continue;
    if (scope === "linked" && n.component_developers < 2) continue;
    if (scope === "flagged" && !flagged.has(n.component)) continue;
    if (!inFilter.has(n.label)) continue;
    keep.add(n.component);
  }
  if (focus) {
    const f = cnNode(focus);
    keep.clear();
    if (f) keep.add(f.component);
  }
  // A node-link graph stops being readable past a few hundred marks, so the largest clusters are drawn
  // first and the rest are left to the tables below.
  const LIMIT = 460;
  const sizes = new Map();
  for (const n of c.nodes) sizes.set(n.component, (sizes.get(n.component) || 0) + 1);
  const order = [...keep].sort((a, b) => (c.devCount.get(b) || 0) - (c.devCount.get(a) || 0) || sizes.get(b) - sizes.get(a));
  const shown = new Set();
  let total = 0;
  for (const comp of order) {
    if (total && total + sizes.get(comp) > LIMIT) continue;
    shown.add(comp);
    total += sizes.get(comp);
  }
  const nodes = c.nodes.filter((n) => shown.has(n.component));
  const ids = new Set(nodes.map((n) => n.id));
  const leads = $("cn-family").checked;
  const edges = c.edges.filter((e) => ids.has(e.source) && ids.has(e.target) && (leads || !SUGGESTED.has(e.kind)));
  return { nodes, edges, hidden: keep.size - shown.size };
}

function link(text, href) {
  const a = document.createElement("a");
  a.href = href;
  a.textContent = text;
  a.target = "_blank";
  a.rel = "noopener";
  return a;
}

function bankruptcyBadge(b) {
  const s = document.createElement("span");
  s.className = `cn-status ${b.status}`;
  s.textContent = `${BANKRUPTCY[b.status].label_hy} · ${BANKRUPTCY[b.status].label}`;
  return s;
}

/** Side panel for the selected node: what it is, how it connects, and every source behind it. */
function renderCnPanel(node) {
  const host = $("cn-panel");
  const c = app.connections;
  host.replaceChildren();
  if (!node) {
    const p = document.createElement("p");
    p.className = "cn-empty";
    p.textContent = "Select a node to see its registry record, the people behind it and the sources.";
    host.append(p);
    return;
  }
  const h = document.createElement("h3");
  h.textContent = node.label;
  const kind = document.createElement("div");
  kind.className = "cn-kind";
  kind.textContent = typeInfo[node.type]?.label || node.type;
  host.append(kind, h);
  if (node.bankruptcy) {
    host.append(bankruptcyBadge(node.bankruptcy));
    const why = document.createElement("p");
    why.className = "cn-basis";
    why.textContent = node.bankruptcy.basis || "";
    host.append(why);
  }

  const dl = document.createElement("dl");
  const row = (label, value) => {
    if (value == null || value === "") return;
    const dt = document.createElement("dt"); dt.textContent = label;
    const dd = document.createElement("dd");
    if (value instanceof Node) dd.append(value); else dd.textContent = value;
    dl.append(dt, dd);
  };
  if (node.type === "developer") {
    row("Projects", String(node.projects));
    row("Rating", node.grade ? `${node.grade} (${node.score})` : "not rated");
    row("Role", node.role);
    row("Lawsuits by individuals", node.lawsuits != null ? String(node.lawsuits) : null);
  } else if (node.type === "company") {
    row("Tax ID", node.tax_id);
    row("Registry status", node.status === "inactive" ? "not active" : node.status === "active" ? "active" : null);
    row("Legal form", node.form);
    row("Registered", node.registered);
    row("Address", node.address);
    row("Activity", node.nace);
    row("Director", node.director);
    row("Court cases", node.court_cases != null ? String(node.court_cases) : null);
  } else {
    row("Companies in the register", String(node.companies));
  }
  host.append(dl);

  const connected = c.edges
    .filter((e) => e.source === node.id || e.target === node.id)
    .map((e) => ({ other: cnNode(e.source === node.id ? e.target : e.source), e }))
    .filter((x) => x.other);
  if (connected.length) {
    const t = document.createElement("div");
    t.className = "cn-kind";
    t.textContent = "Connected to";
    const ul = document.createElement("ul");
    for (const { other, e } of connected.slice(0, 24)) {
      const li = document.createElement("li");
      const b = document.createElement("button");
      b.type = "button";
      b.className = "link";
      b.textContent = other.label;
      b.addEventListener("click", () => selectCn(other.id));
      li.append(b, document.createTextNode(` — ${e.label || edgeInfo[e.kind]?.label || e.kind}`));
      if (e.evidence) li.append(document.createTextNode(" "), link("source", e.evidence));
      ul.append(li);
    }
    host.append(t, ul);
  }

  const sources = [...(node.sources || []), ...(node.bankruptcy?.sources || [])].filter((s) => s.url);
  const cases = node.bankruptcy?.cases || [];
  const t = document.createElement("div");
  t.className = "cn-kind";
  t.textContent = "Sources";
  const ul = document.createElement("ul");
  for (const s of sources) {
    const li = document.createElement("li");
    li.append(link(s.title, s.url));
    if (s.note) li.append(document.createTextNode(` — ${s.note}`));
    ul.append(li);
  }
  for (const k of cases) {
    const li = document.createElement("li");
    li.append(k.url ? link(`Case ${k.case_number}`, k.url) : document.createTextNode(`Case ${k.case_number}`));
    if (k.claimant) li.append(document.createTextNode(` — claimant: ${k.claimant}`));
    ul.append(li);
  }
  if (node.bankruptcy?.confirmed_by) {
    const li = document.createElement("li");
    li.append(link("Confirmation (hand-checked)", node.bankruptcy.confirmed_by));
    ul.append(li);
  }
  host.append(t, ul);
}

function selectCn(id) {
  app.cnSelected = id;
  app.cnGraph?.select(id);
  renderCnPanel(id ? cnNode(id) : null);
}

/** Developer pairs in one cluster and the shortest chain that links them. */
function developerPairs(view) {
  const byId = new Map(view.nodes.map((n) => [n.id, n]));
  const adj = new Map(view.nodes.map((n) => [n.id, []]));
  for (const e of view.edges) {
    adj.get(e.source).push([e.target, e]);
    adj.get(e.target).push([e.source, e]);
  }
  const devs = view.nodes.filter((n) => n.type === "developer");
  const out = [];
  for (let i = 0; i < devs.length; i++) {
    const from = devs[i];
    const prev = new Map([[from.id, null]]);
    const queue = [from.id];
    while (queue.length) {
      const cur = queue.shift();
      for (const [next, e] of adj.get(cur) || []) {
        if (prev.has(next)) continue;
        prev.set(next, [cur, e]);
        queue.push(next);
      }
    }
    for (const to of devs.slice(i + 1)) {
      if (!prev.has(to.id)) continue;
      const chain = [];
      let cur = to.id;
      while (prev.get(cur)) { const [p, e] = prev.get(cur); chain.unshift({ node: byId.get(cur), edge: e }); cur = p; }
      const via = chain.slice(0, -1).map((x) => x.node);
      out.push({
        a: from, b: to, via,
        how: via.some((n) => n.type === "person") ? "shared owner"
          : chain.some((x) => x.edge.kind === "address") ? "same legal address"
            : "same company",
        flagged: via.some((n) => n.bankruptcy),
      });
    }
  }
  return out.sort((a, b) => (b.flagged - a.flagged) || a.via.length - b.via.length || a.a.label.localeCompare(b.a.label));
}

/** Let the graph take the viewport — 1,300 nodes need the room — and redraw it at the new size. */
function expandConnections(on) {
  app.cnExpanded = on;
  document.body.classList.toggle("cn-full", on);
  $("an-connections").classList.toggle("cn-expanded", on);
  renderConnections(filtered());
  if (on) $("an-connections").scrollIntoView({ block: "start" });
}

function renderConnections(items) {
  const c = app.connections;
  if (!c) return;
  const view = connectionView(items);
  const host = $("ch-connections");
  const treeHost = $("ch-connections-tree");
  const asTree = app.cnView === "tree";
  host.hidden = asTree;
  treeHost.hidden = !asTree;
  $("cn-note").textContent = view.hidden
    ? `${view.hidden} more cluster${view.hidden === 1 ? "" : "s"} match but are not drawn — narrow the filters or pick a developer to focus.`
    : "";
  const draw = asTree ? drawTree : drawGraph;
  app.cnGraph = draw(asTree ? treeHost : host, view, {
    onSelect: (n) => selectCn(n?.id || null),
    selected: app.cnSelected,
    expanded: app.cnExpanded,
    onExpand: () => expandConnections(!app.cnExpanded),
    height: app.cnExpanded ? Math.max(420, window.innerHeight - 250) : undefined,
  });
  if (app.cnSelected && !view.nodes.some((n) => n.id === app.cnSelected)) app.cnSelected = null;
  renderCnPanel(app.cnSelected ? cnNode(app.cnSelected) : null);

  $("cn-legend").replaceChildren(...[
    ...Object.entries(typeInfo).map(([, t]) => {
      const s = document.createElement("span");
      const i = document.createElement("i");
      i.style.background = t.color;
      i.style.borderRadius = t.shape === "circle" ? "50%" : t.shape === "diamond" ? "2px" : "3px";
      if (t.shape === "diamond") i.style.transform = "rotate(45deg)";
      s.append(i, document.createTextNode(t.label));
      return s;
    }),
    ...($("cn-family").checked ? [["family", edgeInfo.family], ["family_lead", edgeInfo.family_lead]] : []).map(([, e]) => {
      const s = document.createElement("span");
      const i = document.createElement("i");
      i.style.background = "none";
      i.style.borderTop = `2px ${e.dash ? "dotted" : "solid"} var(--viz-s5)`;
      i.style.height = "0";
      i.style.width = "14px";
      s.append(i, document.createTextNode(e.label));
      return s;
    }),
    ...Object.entries(BANKRUPTCY).map(([key, b]) => {
      const s = document.createElement("span");
      s.className = "cn-status-key";
      const i = document.createElement("i");
      i.className = `${key === "case" ? "case" : ""} ${b.dash ? "dashed" : ""}`.trim();
      s.append(i, document.createTextNode(`${b.label} · ${b.label_hy}`));
      return s;
    }),
  ]);

  $("cn-nodes").replaceChildren(...view.nodes.slice(0, 600).map((n) => new Option(n.label)));

  const pairs = developerPairs(view);
  table($("tb-connections"), [
    { label: "Developer", render: (r) => r.a.label },
    { label: "Connected to", render: (r) => r.b.label },
    { label: "How", key: "how" },
    { label: "Through", render: (r) => r.via.map((n) => n.label).join(" → ") || "—" },
    { label: "Bankruptcy in the chain", render: (r) => (r.flagged ? "yes" : "no") },
  ], pairs.slice(0, 60));

  const flags = view.nodes.filter((n) => n.bankruptcy)
    .sort((a, b) => Object.keys(BANKRUPTCY).indexOf(a.bankruptcy.status) - Object.keys(BANKRUPTCY).indexOf(b.bankruptcy.status));
  table($("tb-bankrupt"), [
    { label: "Company", render: (n) => (n.sources?.[0]?.url ? link(n.label, n.sources[0].url) : n.label) },
    { label: "Status", render: (n) => `${BANKRUPTCY[n.bankruptcy.status].label_hy} · ${BANKRUPTCY[n.bankruptcy.status].label}` },
    {
      label: "Developer",
      render: (n) => {
        const own = (n.developers || []).map((d) => cnNode(d)?.label).filter(Boolean);
        if (own.length) return own.join(", ");
        // an owner's other company: name the developers it shares a cluster with
        const near = app.connections.nodes
          .filter((x) => x.type === "developer" && x.component === n.component).map((x) => x.label);
        return near.length ? `same owners as ${near.slice(0, 3).join(", ")}` : "—";
      },
    },
    { label: "Registry", render: (n) => (n.status === "inactive" ? "not active" : "active") },
    { label: "Basis", render: (n) => n.bankruptcy.basis },
    {
      label: "Cases", render: (n) => {
        const f = document.createDocumentFragment();
        (n.bankruptcy.cases || []).slice(0, 3).forEach((k, i) => {
          if (i) f.append(document.createTextNode(", "));
          f.append(k.url ? link(k.case_number, k.url) : document.createTextNode(k.case_number));
        });
        return f.childNodes.length ? f : "—";
      },
    },
    { label: "Bulletin", render: (n) => link("azdarar.am", (n.sources || []).find((s) => /azdarar/.test(s.url))?.url || "https://www.azdarar.am/") },
  ], flags);
}

function fillFocus() {
  const sel = $("cn-focus");
  const devs = app.connections.nodes.filter((n) => n.type === "developer")
    .sort((a, b) => a.label.localeCompare(b.label));
  sel.replaceChildren(new Option("All clusters", ""));
  for (const d of devs) {
    sel.append(new Option(d.component_developers > 1 ? `${d.label} (${d.component_developers} linked)` : d.label, d.id));
  }
}

async function loadConnections() {
  try {
    const res = await fetch("data/connections.json", { cache: "no-cache" });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    data.byId = new Map(data.nodes.map((n) => [n.id, n]));
    data.devCount = new Map(data.nodes.filter((n) => n.type === "developer").map((n) => [n.component, n.component_developers]));
    app.connections = data;
    fillFocus();
    const src = $("cn-sources");
    const m = data.meta;
    src.replaceChildren(document.createTextNode(
      `Registry data crawled ${m.crawled}: ${m.companies} companies and ${m.people} owners for ${m.developers} developers. `
      + `${m.matched_by_tax_id} developer-to-company links rest on a tax ID and ${m.matched_by_name} on an exact name match in the register — each link carries the evidence it was made from. `
      + `${m.unresolved_entities} legal entities could not be matched to a registry company at all and are left out rather than guessed. Sources: `));
    data.meta.sources.forEach((s, i) => {
      if (i) src.append(document.createTextNode(" · "));
      src.append(link(s.title, s.url));
    });
    renderConnections(filtered());
  } catch (err) {
    console.error(err);
    document.getElementById("an-connections").hidden = true;
  }
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
  renderConnections(items);
}

function bind() {
  for (const id of ["af-region", "af-district", "af-kind", "af-stage", "af-grade"]) $(id).addEventListener("change", render);
  $("af-reset").addEventListener("click", () => {
    for (const id of ["af-region", "af-district", "af-kind", "af-stage", "af-grade"]) $(id).value = "";
    render();
  });
  $("cn-view").addEventListener("click", (e) => {
    const b = e.target.closest("button[data-view]");
    if (!b) return;
    app.cnView = b.dataset.view;
    $("cn-view").querySelectorAll("button").forEach((x) => x.classList.toggle("on", x === b));
    renderConnections(filtered());
  });
  $("cn-search").addEventListener("change", (e) => {
    const q = e.target.value.trim().toLowerCase();
    if (!q) return;
    const hit = app.connections?.nodes.find((n) => n.label.toLowerCase() === q)
      || app.connections?.nodes.find((n) => n.label.toLowerCase().includes(q));
    if (!hit) return;
    selectCn(hit.id);
    app.cnGraph?.camera?.focus(app.cnGraph.nodes?.find((n) => n.id === hit.id));
  });
  for (const id of ["cn-scope", "cn-focus", "cn-family"]) {
    $(id).addEventListener("change", () => {
      if (id === "cn-focus") app.cnSelected = $("cn-focus").value || null;
      renderConnections(filtered());
    });
  }
  $("af-currency").addEventListener("click", (e) => {
    const b = e.target.closest("button[data-cur]");
    if (!b) return;
    state.currency = b.dataset.cur;
    $("af-currency").querySelectorAll("button").forEach((x) => x.classList.toggle("on", x === b));
    render();
  });
  document.addEventListener("keydown", (e) => {
    if (e.key !== "Escape") return;
    if (app.cnExpanded) expandConnections(false);
    else if (app.cnSelected) selectCn(null);
  });
  // The layout is computed for the width it is drawn at, so a resized window needs a redraw.
  let resizing;
  window.addEventListener("resize", () => {
    clearTimeout(resizing);
    resizing = setTimeout(() => render(), 250);
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
    loadConnections();
  } catch (err) {
    console.error(err);
    $("an-meta").textContent = `Could not load data: ${err.message}`;
  }
}

main();
