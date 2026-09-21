/**
 * Tree view of the connections data: one collapsible branch per developer, plain HTML.
 *
 * The data is a graph, not a hierarchy, so each tree is a breadth-first spanning tree rooted at a
 * developer: its registered companies, the people who own them, and those people's other companies.
 * Each node appears once per tree; when a branch reaches another developer it is named as a link
 * instead of being nested again. Every row keeps its registry link and its bankruptcy mark.
 */
import { BANKRUPTCY, typeInfo, edgeInfo } from "./graph.js";

const MAX_DEPTH = 4;
const CHILD_LIMIT = 40;

const el = (name, cls, parent) => {
  const node = document.createElement(name);
  if (cls) node.className = cls;
  if (parent) parent.append(node);
  return node;
};

function typeMark(node) {
  const i = el("i", `cn-mark cn-mark-${node.type}`);
  i.style.background = typeInfo[node.type]?.color || "var(--viz-unknown)";
  return i;
}

/** What this edge says about the child, in a few words. */
function relation(edge, child) {
  if (edge.kind === "entity") return edge.match === "tax_id" ? "legal entity · matched by tax ID" : "legal entity · matched by name";
  if (edge.kind === "address") return `same legal address${child.address ? ` · ${child.address}` : ""}`;
  if (edge.kind === "founder") return edge.label && edge.label.endsWith("%") ? `owner · ${edge.label}` : "owner";
  return edgeInfo[edge.kind]?.label || edge.kind;
}

function facts(node) {
  if (node.type === "developer") {
    return [`${node.projects} project${node.projects === 1 ? "" : "s"}`, node.grade && `rating ${node.grade}`].filter(Boolean).join(" · ");
  }
  if (node.type === "company") {
    return [node.tax_id && `ՀՎՀՀ ${node.tax_id}`, node.status === "inactive" ? "not active in the register" : null,
      node.registered && `registered ${node.registered.slice(0, 4)}`].filter(Boolean).join(" · ");
  }
  return `${node.companies} compan${node.companies === 1 ? "y" : "ies"} in the register`;
}

/**
 * Render the tree.
 * @param {HTMLElement} host
 * @param {{nodes: object[], edges: object[]}} data  the same filtered view the graph gets
 * @param {{onSelect?: (node: object) => void, selected?: string}} opts
 */
export function drawTree(host, data, opts = {}) {
  host.replaceChildren();
  if (!data.nodes.length) {
    el("p", "cn-empty", host).textContent = "No connections in this filter";
    return { select() {} };
  }
  const byId = new Map(data.nodes.map((n) => [n.id, n]));
  const adj = new Map(data.nodes.map((n) => [n.id, []]));
  for (const e of data.edges) {
    if (!byId.has(e.source) || !byId.has(e.target)) continue;
    adj.get(e.source).push([e.target, e]);
    adj.get(e.target).push([e.source, e]);
  }
  const roots = data.nodes.filter((n) => n.type === "developer")
    .sort((a, b) => (b.component_developers - a.component_developers) || (b.projects - a.projects) || a.label.localeCompare(b.label));

  const rows = new Map();  // node id -> the row element that owns it, for select()
  const wrap = el("div", "cn-tree", host);

  for (const root of roots) {
    const seen = new Set([root.id]);
    const details = el("details", "cn-branch", wrap);
    details.open = roots.length <= 12;
    const summary = el("summary", "cn-row cn-root", details);
    summary.append(typeMark(root));
    const name = el("b", null, summary);
    name.textContent = root.label;
    const meta = el("span", "cn-meta", summary);
    meta.textContent = facts(root);
    if (root.component_developers > 1) {
      const tag = el("span", "cn-tag", summary);
      tag.textContent = `${root.component_developers} linked developers`;
    }
    summary.addEventListener("click", () => opts.onSelect?.(root));
    rows.set(root.id, summary);

    /** One level of children, each as a row plus its own subtree. */
    const level = (parentId, depth, container, cameFrom) => {
      if (depth > MAX_DEPTH) return;
      const order = { entity: 0, founder: 1, director: 1, address: 2 };
      const children = adj.get(parentId)
        .filter(([childId]) => childId !== cameFrom)
        .sort((a, b) => (order[a[1].kind] ?? 3) - (order[b[1].kind] ?? 3) || byId.get(a[0]).label.localeCompare(byId.get(b[0]).label))
        .slice(0, CHILD_LIMIT);
      if (!children.length) return;
      const list = el("ul", "cn-list", container);
      for (const [childId, edge] of children) {
        if (seen.has(childId) && byId.get(childId).type !== "developer") continue;  // already placed in this tree
        const child = byId.get(childId);
        if (child.type === "developer" && depth > 1) {
          // another developer reached through shared people or addresses: name it, do not nest it
          const li = el("li", "cn-item", list);
          const link = el("button", "cn-name link", li);
          link.type = "button";
          link.textContent = `↳ links to ${child.label}`;
          link.addEventListener("click", () => opts.onSelect?.(child));
          continue;
        }
        const li = el("li", "cn-item", list);
        const row = el("div", "cn-row", li);
        row.append(typeMark(child));
        const button = el("button", "cn-name", row);
        button.type = "button";
        button.textContent = child.label;
        button.addEventListener("click", () => opts.onSelect?.(child));
        const rel = el("span", "cn-rel", row);
        rel.textContent = relation(edge, child);
        const f = facts(child);
        if (f) {
          const m = el("span", "cn-meta", row);
          m.textContent = f;
        }
        const bank = child.bankruptcy && BANKRUPTCY[child.bankruptcy.status];
        if (bank) {
          const badge = el("span", `cn-status ${child.bankruptcy.status}`, row);
          badge.textContent = `${bank.label_hy} · ${bank.label}`;
        }
        const source = (child.sources || []).find((s) => (s.url || "").startsWith("http"));
        if (source) {
          const a = el("a", "cn-src", row);
          a.href = source.url;
          a.target = "_blank";
          a.rel = "noopener";
          a.title = source.title;
          a.textContent = "source";
        }
        seen.add(childId);
        if (!rows.has(childId)) rows.set(childId, row);
        level(childId, depth + 1, li, parentId);
      }
      if (adj.get(parentId).length - 1 > CHILD_LIMIT) {
        const li = el("li", "cn-item cn-more", list);
        li.textContent = `+ ${adj.get(parentId).length - CHILD_LIMIT} more`;
      }
    };
    level(root.id, 1, details, null);
  }

  function select(id) {
    for (const [nid, row] of rows) row.classList.toggle("on", nid === id);
    const row = rows.get(id);
    if (row) {
      row.closest("details")?.setAttribute("open", "");
      row.scrollIntoView({ block: "nearest" });
    }
  }
  if (opts.selected) select(opts.selected);
  return { select };
}
