/**
 * Minimal SVG chart helpers for the analytics page. Marks follow the dataviz spec: bars <= 24px with 4px rounded
 * data-ends, hairline grids, 2px surface gaps, >= 8px dots with a surface ring, per-mark hover tooltips.
 * All text is inserted with textContent.
 */
const NS = "http://www.w3.org/2000/svg";
const tip = () => document.getElementById("an-tip");

function el(name, attrs = {}, parent) {
  const node = document.createElementNS(NS, name);
  for (const [k, v] of Object.entries(attrs)) if (v != null) node.setAttribute(k, v);
  if (parent) parent.append(node);
  return node;
}

function text(parent, x, y, value, cls, attrs = {}) {
  const t = el("text", { x, y, class: cls, ...attrs }, parent);
  t.textContent = value;
  return t;
}

/** Path for a bar with a 4px rounded data-end and a square base. */
function barPath(x, y, w, h, horizontal) {
  const r = Math.min(4, horizontal ? h / 2 : w / 2, horizontal ? w : h);
  if (horizontal) return `M${x},${y}h${Math.max(0, w - r)}a${r},${r} 0 0 1 ${r},${r}v${h - 2 * r}a${r},${r} 0 0 1 ${-r},${r}h${-Math.max(0, w - r)}z`;
  return `M${x},${y + h}v${-Math.max(0, h - r)}a${r},${r} 0 0 1 ${r},${-r}h${w - 2 * r}a${r},${r} 0 0 1 ${r},${r}v${Math.max(0, h - r)}z`;
}

export function niceMax(v) {
  if (!v) return 1;
  const p = 10 ** Math.floor(Math.log10(v));
  return [1, 2, 2.5, 5, 10].map((m) => m * p).find((m) => m >= v) || v;
}

/** Attach a hover/focus tooltip to a mark. lines = [value, label, note]. */
export function withTip(node, lines, onClick) {
  node.setAttribute("tabindex", "0");
  const show = (e) => {
    const t = tip();
    t.replaceChildren();
    const [value, label, note] = lines;
    const b = document.createElement("b"); b.textContent = value; t.append(b);
    if (label) { const s = document.createElement("span"); s.textContent = label; t.append(s); }
    if (note) { const m = document.createElement("em"); m.textContent = note; t.append(m); }
    t.hidden = false;
    const box = node.getBoundingClientRect();
    const x = e?.clientX ?? box.left + box.width / 2;
    const y = e?.clientY ?? box.top;
    const w = t.offsetWidth;
    t.style.left = `${Math.min(window.innerWidth - w - 8, Math.max(8, x + 12))}px`;
    t.style.top = `${Math.max(8, y - t.offsetHeight - 12)}px`;
  };
  const hide = () => { tip().hidden = true; };
  node.addEventListener("pointermove", show);
  node.addEventListener("focus", () => show());
  node.addEventListener("pointerleave", hide);
  node.addEventListener("blur", hide);
  if (onClick) {
    node.addEventListener("click", onClick);
    node.addEventListener("keydown", (e) => { if (e.key === "Enter") onClick(); });
  }
}

function emptyState(container, height = 120) {
  const svg = el("svg", { viewBox: `0 0 600 ${height}`, role: "img" });
  text(svg, 300, height / 2, "No data for this filter", "empty", { "text-anchor": "middle" });
  container.replaceChildren(svg);
}

/**
 * Horizontal bars. rows: [{label, value, display, tipLabel, tipNote, color}]
 */
export function hbar(container, rows, { width = 760, labelWidth = 190, barH = 18, gap = 10, format = String } = {}) {
  if (!rows.length) return emptyState(container);
  const top = 22;
  const height = top + rows.length * (barH + gap) + 4;
  const plotW = width - labelWidth - 70;
  const max = niceMax(Math.max(...rows.map((r) => r.value)));
  const svg = el("svg", { viewBox: `0 0 ${width} ${height}`, role: "img" });
  const grid = el("g", { class: "grid" }, svg);
  for (let i = 0; i <= 4; i++) {
    const x = labelWidth + (plotW * i) / 4;
    el("line", { x1: x, x2: x, y1: top - 6, y2: height - 4 }, grid);
    text(svg, x, 12, format((max * i) / 4), "lbl", { "text-anchor": i === 0 ? "start" : "middle" });
  }
  rows.forEach((r, i) => {
    const y = top + i * (barH + gap);
    const w = Math.max(2, (r.value / max) * plotW);
    text(svg, labelWidth - 8, y + barH / 2 + 4, r.label.length > 26 ? `${r.label.slice(0, 25)}…` : r.label, "cat", { "text-anchor": "end" });
    const bar = el("path", { d: barPath(labelWidth, y, w, barH, true), fill: r.color || "var(--viz-seq)", class: "mark" }, svg);
    text(svg, labelWidth + w + 6, y + barH / 2 + 4, r.display ?? format(r.value), "val");
    const hit = el("rect", { x: 0, y: y - gap / 2, width, height: barH + gap, class: "hit" }, svg);
    withTip(hit, [r.display ?? format(r.value), r.tipLabel ?? r.label, r.tipNote], r.onClick);
    hit.addEventListener("pointerenter", () => bar.setAttribute("opacity", ".78"));
    hit.addEventListener("pointerleave", () => bar.removeAttribute("opacity"));
  });
  container.replaceChildren(svg);
}

/**
 * Vertical columns. cols: [{label, value, color, tipNote}]
 */
export function columns(container, cols, { width = 520, height = 220, format = String, labelEvery = 1 } = {}) {
  if (!cols.length || !cols.some((c) => c.value)) return emptyState(container, height);
  const left = 34, bottom = 24, top = 18;
  const plotW = width - left - 6;
  const plotH = height - top - bottom;
  const max = niceMax(Math.max(...cols.map((c) => c.value)));
  const band = plotW / cols.length;
  const bw = Math.min(24, band - 2);
  const svg = el("svg", { viewBox: `0 0 ${width} ${height}`, role: "img" });
  const grid = el("g", { class: "grid" }, svg);
  for (let i = 0; i <= 4; i++) {
    const y = top + plotH - (plotH * i) / 4;
    el("line", { x1: left, x2: width - 6, y1: y, y2: y }, grid);
    text(svg, left - 6, y + 4, format((max * i) / 4), "lbl", { "text-anchor": "end" });
  }
  cols.forEach((c, i) => {
    const cx = left + band * i + band / 2;
    const h = (c.value / max) * plotH;
    if (h > 0) {
      el("path", { d: barPath(cx - bw / 2, top + plotH - h, bw, h, false), fill: c.color || "var(--viz-seq)", class: "mark" }, svg);
    }
    if (i % labelEvery === 0) text(svg, cx, height - 8, c.label, "lbl", { "text-anchor": "middle" });
    const hit = el("rect", { x: cx - band / 2, y: top, width: band, height: plotH, class: "hit" }, svg);
    withTip(hit, [format(c.value), c.tipLabel ?? c.label, c.tipNote]);
  });
  el("line", { x1: left, x2: width - 6, y1: top + plotH, y2: top + plotH, class: "axis" }, svg);
  container.replaceChildren(svg);
}

/**
 * Stacked horizontal bars (counts). rows: [{label, parts: [{key, value}]}], series: [{key, label, color}]
 */
export function stacked(container, rows, series, { width = 760, labelWidth = 170, barH = 18, gap = 10 } = {}) {
  if (!rows.length) return emptyState(container);
  const top = 22;
  const height = top + rows.length * (barH + gap) + 4;
  const plotW = width - labelWidth - 50;
  const max = niceMax(Math.max(...rows.map((r) => r.parts.reduce((s, p) => s + p.value, 0))));
  const svg = el("svg", { viewBox: `0 0 ${width} ${height}`, role: "img" });
  const grid = el("g", { class: "grid" }, svg);
  for (let i = 0; i <= 4; i++) {
    const x = labelWidth + (plotW * i) / 4;
    el("line", { x1: x, x2: x, y1: top - 6, y2: height - 4 }, grid);
    text(svg, x, 12, String(Math.round((max * i) / 4)), "lbl", { "text-anchor": i === 0 ? "start" : "middle" });
  }
  rows.forEach((r, i) => {
    const y = top + i * (barH + gap);
    const total = r.parts.reduce((s, p) => s + p.value, 0);
    text(svg, labelWidth - 8, y + barH / 2 + 4, r.label, "cat", { "text-anchor": "end" });
    let x = labelWidth;
    const visible = r.parts.filter((p) => p.value > 0);
    visible.forEach((p, j) => {
      const s = series.find((q) => q.key === p.key);
      const w = (p.value / max) * plotW;
      const segW = Math.max(1, w - (j < visible.length - 1 ? 2 : 0));
      const isLast = j === visible.length - 1;
      const node = isLast
        ? el("path", { d: barPath(x, y, segW, barH, true), fill: s.color, class: "mark" }, svg)
        : el("rect", { x, y, width: segW, height: barH, fill: s.color, class: "mark" }, svg);
      withTip(node, [`${p.value} projects`, `${r.label} · ${s.label}`, `${Math.round((p.value / total) * 100)}% of ${total}`]);
      x += w;
    });
    text(svg, x + 6, y + barH / 2 + 4, String(total), "val");
  });
  container.replaceChildren(svg);
}

/**
 * Scatter with a time x-axis. points: [{x: Date, y: number, label, note, onClick}]
 */
export function scatter(container, points, { width = 900, height = 300, formatY = String, xDomain } = {}) {
  if (!points.length) return emptyState(container, height);
  const left = 52, bottom = 26, top = 14, right = 12;
  const plotW = width - left - right;
  const plotH = height - top - bottom;
  const xs = points.map((p) => p.x.getTime());
  const [x0, x1] = xDomain || [Math.min(...xs), Math.max(...xs)];
  const ymax = niceMax(Math.max(...points.map((p) => p.y)));
  const sx = (t) => left + ((t - x0) / Math.max(1, x1 - x0)) * plotW;
  const sy = (v) => top + plotH - (v / ymax) * plotH;
  const svg = el("svg", { viewBox: `0 0 ${width} ${height}`, role: "img" });
  const grid = el("g", { class: "grid" }, svg);
  for (let i = 0; i <= 4; i++) {
    const y = top + plotH - (plotH * i) / 4;
    el("line", { x1: left, x2: width - right, y1: y, y2: y }, grid);
    text(svg, left - 6, y + 4, formatY((ymax * i) / 4), "lbl", { "text-anchor": "end" });
  }
  const y0 = new Date(x0).getFullYear();
  const yN = new Date(x1).getFullYear();
  for (let yr = y0; yr <= yN + 1; yr++) {
    const t = new Date(`${yr}-01-01`).getTime();
    if (t < x0 || t > x1) continue;
    const x = sx(t);
    el("line", { x1: x, x2: x, y1: top, y2: top + plotH }, grid);
    text(svg, x, height - 8, String(yr), "lbl", { "text-anchor": "middle" });
  }
  const now = Date.now();
  if (now > x0 && now < x1) {
    el("line", { x1: sx(now), x2: sx(now), y1: top, y2: top + plotH, stroke: "var(--viz-axis)", "stroke-width": 1 }, svg);
    text(svg, sx(now) + 4, top + 10, "today", "lbl");
  }
  el("line", { x1: left, x2: width - right, y1: top + plotH, y2: top + plotH, class: "axis" }, svg);
  for (const p of points) {
    const cx = sx(p.x.getTime());
    const cy = sy(p.y);
    el("circle", { cx, cy, r: 4, fill: p.color || "var(--viz-seq)", class: "dot" }, svg);
    const hit = el("circle", { cx, cy, r: 9, class: "hit" }, svg);
    withTip(hit, [formatY(p.y), p.label, p.note], p.onClick);
  }
  container.replaceChildren(svg);
}

/** Build a data table. columns: [{key, label, num, render}] */
export function table(container, cols, rows) {
  const t = document.createElement("table");
  t.className = "dt";
  const head = t.createTHead().insertRow();
  for (const c of cols) {
    const th = document.createElement("th");
    th.textContent = c.label;
    if (c.num) th.className = "num";
    head.append(th);
  }
  const body = t.createTBody();
  for (const r of rows) {
    const tr = body.insertRow();
    for (const c of cols) {
      const td = tr.insertCell();
      if (c.num) td.className = "num";
      const v = c.render ? c.render(r) : r[c.key];
      if (v instanceof Node) td.append(v); else td.textContent = v ?? "—";
    }
  }
  if (!rows.length) {
    const td = body.insertRow().insertCell();
    td.colSpan = cols.length;
    td.textContent = "No data for this filter";
  }
  container.replaceChildren(t);
}
