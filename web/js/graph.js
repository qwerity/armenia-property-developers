/**
 * Force-directed node-link graph for the connections card, in plain SVG.
 *
 * Marks follow the page's dataviz spec: identity is shape + colour (never colour alone), bankruptcy
 * is a reserved status colour drawn as a ring plus a glyph, links are 1–2px hairlines, every mark
 * has a hover tooltip and keyboard focus. The layout is a small velocity-Verlet simulation
 * (repulsion + springs + centring), run for a fixed number of ticks before the first paint.
 */
const NS = "http://www.w3.org/2000/svg";
const tip = () => document.getElementById("an-tip");

const TYPE = {
  developer: { color: "var(--viz-s1)", shape: "square", label: "Developer / constructor" },
  company: { color: "var(--viz-s3)", shape: "circle", label: "Registered company" },
  person: { color: "var(--viz-s2)", shape: "diamond", label: "Owner / director" },
};
export const BANKRUPTCY = {
  declared: { label: "Declared bankrupt", label_hy: "սնանկ է ճանաչվել", color: "var(--high)", dash: null },
  self_declared: { label: "Filed for its own bankruptcy", label_hy: "ինքն է հայտարարել սնանկ", color: "var(--high)", dash: "3 2" },
  case: { label: "Bankruptcy case pending", label_hy: "սնանկության գործ ընթացքում", color: "var(--ok)", dash: "3 2" },
};
const EDGE = {
  entity: { color: "var(--viz-s1)", width: 2, dash: null, label: "legal entity of" },
  founder: { color: "var(--viz-s2)", width: 1.5, dash: null, label: "owner" },
  director: { color: "var(--viz-s2)", width: 1.5, dash: "4 3", label: "director" },
  address: { color: "var(--viz-muted)", width: 1, dash: "2 3", label: "same legal address" },
  family: { color: "var(--viz-s5)", width: 1.5, dash: null, label: "family tie (documented)" },
  family_lead: { color: "var(--viz-s5)", width: 1, dash: "1 4", label: "possible relative — unverified" },
  same_person: { color: "var(--viz-s5)", width: 1, dash: "1 4", label: "probably the same person" },
};
/** Edges that are a lead to check rather than a registry fact; hidden unless the reader asks for them. */
export const SUGGESTED = new Set(["family_lead", "same_person"]);

function el(name, attrs = {}, parent) {
  const node = document.createElementNS(NS, name);
  for (const [k, v] of Object.entries(attrs)) if (v != null) node.setAttribute(k, v);
  if (parent) parent.append(node);
  return node;
}

export const radiusOf = (n) => (n.type === "developer" ? Math.min(17, 7 + Math.sqrt(n.projects || 1) * 2.2) : n.type === "company" ? 7 : 5.5);

function shapePath(node, r) {
  const { x, y } = node;
  if (TYPE[node.type]?.shape === "square") {
    const k = r * 0.92;
    return `M${x - k + 3},${y - k}h${2 * k - 6}a3,3 0 0 1 3,3v${2 * k - 6}a3,3 0 0 1 -3,3h${-2 * k + 6}a3,3 0 0 1 -3,-3v${-2 * k + 6}a3,3 0 0 1 3,-3z`;
  }
  if (TYPE[node.type]?.shape === "diamond") {
    const k = r * 1.25;
    return `M${x},${y - k}L${x + k},${y}L${x},${y + k}L${x - k},${y}z`;
  }
  return `M${x - r},${y}a${r},${r} 0 1 0 ${2 * r},0a${r},${r} 0 1 0 ${-2 * r},0z`;
}

/** Deterministic start positions: a spiral, so the same data always lays out the same way. */
function seed(nodes, w, h) {
  nodes.forEach((n, i) => {
    const a = i * 2.399963;
    const rad = Math.sqrt(i + 1) * Math.min(w, h) / (2 * Math.sqrt(nodes.length + 1));
    n.x = w / 2 + Math.cos(a) * rad;
    n.y = h / 2 + Math.sin(a) * rad;
    n.vx = n.vy = 0;
  });
}

function simulate(nodes, links, w, h, ticks) {
  const n = nodes.length;
  if (!n) return;
  ticks ||= n > 260 ? 140 : 320;  // the pairwise step is O(n²): fewer passes once a cluster is large
  const index = new Map(nodes.map((d, i) => [d.id, i]));
  const pairs = links.map((l) => [index.get(l.source), index.get(l.target)]).filter(([a, b]) => a != null && b != null);
  const deg = new Array(n).fill(0);
  for (const [a, b] of pairs) { deg[a]++; deg[b]++; }
  const repel = 1500;
  const cutoff = 260 ** 2;  // beyond this, repulsion only flings hub nodes out of their own cluster
  const linkLen = 62;
  for (let t = 0; t < ticks; t++) {
    const alpha = 0.12 * (1 - t / ticks) + 0.005;
    for (let i = 0; i < n; i++) {
      for (let j = i + 1; j < n; j++) {
        let dx = nodes[j].x - nodes[i].x;
        let dy = nodes[j].y - nodes[i].y;
        let d2 = dx * dx + dy * dy;
        if (d2 > cutoff) continue;
        if (d2 < 1e-4) { dx = (i % 7) - 3.5; dy = (j % 5) - 2.5; d2 = dx * dx + dy * dy; }
        const d = Math.sqrt(d2);
        const f = Math.min(repel / d2, 40) * alpha;
        const fx = (dx / d) * f;
        const fy = (dy / d) * f;
        nodes[i].vx -= fx; nodes[i].vy -= fy;
        nodes[j].vx += fx; nodes[j].vy += fy;
      }
    }
    for (const [a, b] of pairs) {
      const dx = nodes[b].x - nodes[a].x;
      const dy = nodes[b].y - nodes[a].y;
      const d = Math.hypot(dx, dy) || 0.01;
      const want = linkLen + Math.min(26, (deg[a] + deg[b]) * 1.6);
      // a hub is held by many springs at once, so each one pulls a little less
      const f = ((d - want) / d) * 0.22 * alpha * 10;
      nodes[a].vx += (dx * f) / Math.sqrt(deg[a]);
      nodes[a].vy += (dy * f) / Math.sqrt(deg[a]);
      nodes[b].vx -= (dx * f) / Math.sqrt(deg[b]);
      nodes[b].vy -= (dy * f) / Math.sqrt(deg[b]);
    }
    for (const d of nodes) {
      d.vx += (w / 2 - d.x) * 0.012 * alpha * 10;
      d.vy += (h / 2 - d.y) * 0.016 * alpha * 10;
      d.x += (d.vx *= 0.82);
      d.y += (d.vy *= 0.82);
    }
  }
  relax(nodes, n > 260 ? 20 : 60);
}

/** Push overlapping marks apart so no node hides another. */
function relax(nodes, rounds = 60) {
  for (let t = 0; t < rounds; t++) {
    let moved = false;
    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const a = nodes[i];
        const b = nodes[j];
        const min = radiusOf(a) + radiusOf(b) + 9;
        const dx = b.x - a.x;
        const dy = b.y - a.y;
        const d = Math.hypot(dx, dy) || 0.01;
        if (d >= min) continue;
        const push = (min - d) / 2;
        a.x -= (dx / d) * push; a.y -= (dy / d) * push;
        b.x += (dx / d) * push; b.y += (dy / d) * push;
        moved = true;
      }
    }
    if (!moved) break;
  }
}

const bbox = (nodes) => ({
  x0: Math.min(...nodes.map((n) => n.x)), x1: Math.max(...nodes.map((n) => n.x)),
  y0: Math.min(...nodes.map((n) => n.y)), y1: Math.max(...nodes.map((n) => n.y)),
});

/**
 * Lay each cluster out on its own, then shelf-pack the clusters into the frame. Simulating everything in
 * one field would let the big cluster's repulsion push the small ones off the canvas.
 */
function layout(nodes, links, w, h) {
  const groups = new Map();
  for (const n of nodes) {
    const key = n.component ?? 0;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(n);
  }
  const boxes = [];
  for (const group of groups.values()) {
    const ids = new Set(group.map((n) => n.id));
    const inner = links.filter((l) => ids.has(l.source) && ids.has(l.target));
    const side = Math.max(140, 92 * Math.sqrt(group.length));
    seed(group, side, side);
    simulate(group, inner, side, side);
    const b = bbox(group);
    for (const n of group) { n.x -= b.x0; n.y -= b.y0; }
    boxes.push({ group, w: b.x1 - b.x0 + 40, h: b.y1 - b.y0 + 40 });
  }
  boxes.sort((a, b) => b.h * b.w - a.h * a.w);
  const width = Math.max(...boxes.map((b) => b.w), Math.sqrt(boxes.reduce((s, b) => s + b.w * b.h, 0) * (w / h)));
  let [x, y, rowH] = [0, 0, 0];
  for (const box of boxes) {
    if (x && x + box.w > width) { x = 0; y += rowH + 24; rowH = 0; }
    for (const n of box.group) { n.x += x + 20; n.y += y + 20; }
    x += box.w + 24;
    rowH = Math.max(rowH, box.h);
  }
}

function showTip(node, lines, e) {
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
  t.style.left = `${Math.min(window.innerWidth - t.offsetWidth - 8, Math.max(8, x + 12))}px`;
  t.style.top = `${Math.max(8, y - t.offsetHeight - 12)}px`;
}
const hideTip = () => { tip().hidden = true; };

/**
 * Draw the graph into `host`.
 * @param {HTMLElement} host
 * @param {{nodes: object[], edges: object[]}} data  already filtered to what should be drawn
 * @param {{onSelect?: (node: object|null) => void, selected?: string, height?: number}} opts
 */
export function drawGraph(host, data, opts = {}) {
  const w = Math.max(320, host.clientWidth || 900);
  const h = opts.height || Math.max(440, Math.min(820, 330 + data.nodes.length * 6));
  host.replaceChildren();
  const svg = el("svg", { viewBox: `0 0 ${w} ${h}`, class: "graph", role: "img",
    "aria-label": `Ownership connections: ${data.nodes.length} nodes, ${data.edges.length} links` }, host);
  if (!data.nodes.length) {
    const t = el("text", { x: w / 2, y: h / 2, "text-anchor": "middle", class: "empty" }, svg);
    t.textContent = "No connections in this filter";
    return { select() {} };
  }
  const nodes = data.nodes.map((n) => ({ ...n }));
  const byId = new Map(nodes.map((n) => [n.id, n]));
  const links = data.edges.filter((e) => byId.has(e.source) && byId.has(e.target));
  layout(nodes, links, w, h);

  // keep everything inside the frame
  const pad = 34;
  const { x0, x1, y0, y1 } = bbox(nodes);
  // Positions carry no units, so x and y may be stretched separately to use the frame — but only up to
  // 2:1, past which a cluster starts to read as a line.
  let kx = Math.min((w - 2 * pad) / Math.max(1, x1 - x0), 2.6);
  let ky = Math.min((h - 2 * pad) / Math.max(1, y1 - y0), 2.6);
  kx = Math.min(kx, ky * 2);
  ky = Math.min(ky, kx * 2);
  for (const n of nodes) {
    n.x = pad + (n.x - x0) * kx + (w - 2 * pad - (x1 - x0) * kx) / 2;
    n.y = pad + (n.y - y0) * ky + (h - 2 * pad - (y1 - y0) * ky) / 2;
  }
  relax(nodes, nodes.length > 260 ? 12 : 30);

  const view = el("g", {}, svg);
  const linkLayer = el("g", { class: "links" }, view);
  const nodeLayer = el("g", { class: "nodes" }, view);
  const labelLayer = el("g", { class: "labels" }, view);

  const neighbours = new Map(nodes.map((n) => [n.id, new Set()]));
  const lineOf = new Map();
  for (const e of links) {
    const a = byId.get(e.source);
    const b = byId.get(e.target);
    neighbours.get(a.id).add(b.id);
    neighbours.get(b.id).add(a.id);
    const spec = EDGE[e.kind] || EDGE.address;
    const line = el("line", { x1: a.x, y1: a.y, x2: b.x, y2: b.y, stroke: spec.color, "stroke-width": spec.width,
      "stroke-dasharray": spec.dash, "stroke-linecap": "round", class: "link", opacity: 0.55 }, linkLayer);
    lineOf.set(e, line);
    const hit = el("line", { x1: a.x, y1: a.y, x2: b.x, y2: b.y, stroke: "transparent", "stroke-width": 10, class: "hit" }, linkLayer);
    hit.addEventListener("pointermove", (ev) => showTip(hit, [`${a.label} — ${b.label}`, e.label || spec.label, e.detail || ""], ev));
    hit.addEventListener("pointerleave", hideTip);
  }

  const marks = new Map();
  for (const n of nodes) {
    const r = radiusOf(n);
    const g = el("g", { class: "node", tabindex: 0, role: "button", "aria-label": `${n.label}, ${TYPE[n.type]?.label || n.type}` }, nodeLayer);
    const bank = n.bankruptcy && BANKRUPTCY[n.bankruptcy.status];
    if (bank) {
      el("path", { d: shapePath(n, r + 4.5), fill: "none", stroke: bank.color, "stroke-width": 2, "stroke-dasharray": bank.dash }, g);
    }
    el("path", { d: shapePath(n, r), fill: TYPE[n.type]?.color || "var(--viz-unknown)", stroke: "var(--viz-surface)",
      "stroke-width": 2, opacity: n.status === "inactive" ? 0.45 : 1 }, g);
    if (bank) {
      const glyph = el("text", { x: n.x + r + 6, y: n.y - r - 2, class: "g-flag", fill: bank.color }, g);
      glyph.textContent = "!";
    }
    marks.set(n.id, g);
    const facts = [
      n.type === "developer" ? `${n.projects} project${n.projects === 1 ? "" : "s"}${n.grade ? ` · rating ${n.grade}` : ""}` : null,
      n.type === "company" ? [n.tax_id && `tax ID ${n.tax_id}`, n.status === "inactive" ? "not active in the register" : null].filter(Boolean).join(" · ") : null,
      n.type === "person" ? `${n.companies} compan${n.companies === 1 ? "y" : "ies"} in the register` : null,
    ].filter(Boolean).join(" · ");
    const note = bank ? `${bank.label} (${bank.label_hy})` : n.address || "";
    const show = (ev) => showTip(g, [n.label, facts, note], ev);
    g.addEventListener("pointermove", show);
    g.addEventListener("focus", () => show());
    g.addEventListener("pointerleave", hideTip);
    g.addEventListener("blur", hideTip);
    const pick = () => opts.onSelect?.(n);
    g.addEventListener("click", pick);
    g.addEventListener("keydown", (ev) => { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); pick(); } });

  }

  // Labels last, so they can be laid out greedily: developers first, then flagged companies, then the
  // rest, each one skipped when its box would cover a label that is already on the page.
  const boxes = [];
  const labels = new Map();
  const fits = (x, y, wide, tall) => !boxes.some((b) => Math.abs(b.x - x) * 2 < b.w + wide && Math.abs(b.y - y) * 2 < b.h + tall);
  const rank = (n) => (n.type === "developer" ? 0 : n.bankruptcy ? 1 : 2);
  const labelAll = nodes.length <= 80;
  for (const n of [...nodes].sort((a, b) => rank(a) - rank(b))) {
    const bank = n.bankruptcy && BANKRUPTCY[n.bankruptcy.status];
    if (!(n.type === "developer" || bank || labelAll)) continue;
    const max = n.type === "developer" ? 26 : 20;
    const value = n.label.length > max ? `${n.label.slice(0, max - 1)}…` : n.label;
    const r = radiusOf(n);
    const wide = value.length * 6.4 + 6;
    const tall = 14;
    // keep the text inside the frame: hug the edge instead of spilling out of the viewBox
    const anchor = n.x - wide / 2 < 4 ? "start" : n.x + wide / 2 > w - 4 ? "end" : "middle";
    const x = anchor === "start" ? Math.max(4, n.x - r) : anchor === "end" ? Math.min(w - 4, n.x + r) : n.x;
    const centre = anchor === "start" ? x + wide / 2 : anchor === "end" ? x - wide / 2 : x;
    const spot = [n.y + r + 11, n.y - r - 5, n.y + r + 24, n.y - r - 18].find((y) => fits(centre, y, wide, tall));
    if (spot == null) continue;
    const y = spot;
    boxes.push({ x: centre, y, w: wide, h: tall });
    const label = el("text", { x, y, "text-anchor": anchor,
      class: `g-label${bank ? " flagged" : ""}${n.type === "developer" ? " dev" : ""}` }, labelLayer);
    label.textContent = value;
    labels.set(n.id, label);
  }

  function select(id) {
    const near = id ? new Set([id, ...(neighbours.get(id) || [])]) : null;
    for (const [nid, g] of marks) g.classList.toggle("dim", Boolean(near) && !near.has(nid));
    for (const [nid, label] of labels) label.classList.toggle("dim", Boolean(near) && !near.has(nid));
    for (const [e, line] of lineOf) {
      const on = !near || near.has(e.source) && near.has(e.target);
      line.setAttribute("opacity", on ? (near ? 0.9 : 0.55) : 0.12);
    }
  }
  if (opts.selected) select(opts.selected);
  svg.addEventListener("click", (ev) => { if (ev.target === svg) opts.onSelect?.(null); });

  // pan with a drag on the background, zoom with the wheel (ctrl/⌘ or over the plot)
  let zoom = 1;
  let [tx, ty] = [0, 0];
  const apply = () => view.setAttribute("transform", `translate(${tx} ${ty}) scale(${zoom})`);
  svg.addEventListener("wheel", (ev) => {
    ev.preventDefault();
    const rect = svg.getBoundingClientRect();
    const px = ((ev.clientX - rect.left) / rect.width) * w;
    const py = ((ev.clientY - rect.top) / rect.height) * h;
    const next = Math.min(4, Math.max(0.5, zoom * (ev.deltaY < 0 ? 1.12 : 1 / 1.12)));
    tx = px - ((px - tx) / zoom) * next;
    ty = py - ((py - ty) / zoom) * next;
    zoom = next;
    apply();
  }, { passive: false });
  let drag = null;
  svg.addEventListener("pointerdown", (ev) => {
    if (ev.target.closest(".node")) return;
    drag = { x: ev.clientX, y: ev.clientY, tx, ty };
    svg.setPointerCapture(ev.pointerId);
    svg.style.cursor = "grabbing";
  });
  svg.addEventListener("pointermove", (ev) => {
    if (!drag) return;
    const rect = svg.getBoundingClientRect();
    tx = drag.tx + ((ev.clientX - drag.x) / rect.width) * w;
    ty = drag.ty + ((ev.clientY - drag.y) / rect.height) * h;
    apply();
  });
  const endDrag = () => { drag = null; svg.style.cursor = ""; };
  svg.addEventListener("pointerup", endDrag);
  svg.addEventListener("pointercancel", endDrag);

  return { select, nodes };
}

export const typeInfo = TYPE;
export const edgeInfo = EDGE;
