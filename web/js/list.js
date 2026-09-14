import { esc, money, compactMoney, quarter } from "./util.js";

function dealBadge(p) {
  if (p.discount_pct == null) return "";
  const cls = p.discount_pct >= 10 ? "good" : p.discount_pct > 0 ? "ok" : "high";
  const sign = p.discount_pct > 0 ? "−" : "+";
  const where = p.bench_scope === "district" ? p.district : p.region;
  return `<span class="badge ${cls}" title="Starting $/m² vs. median of ${p.bench_n} projects in ${esc(where)}">${sign}${Math.abs(p.discount_pct)}% vs ${esc(where)}</span>`;
}

function itemHtml(p, selectedId) {
  const img = p.images?.[0];
  return `<li class="item${p.id === selectedId ? " selected" : ""}" data-id="${esc(p.id)}" role="option" tabindex="0" aria-selected="${p.id === selectedId}">
    <div class="thumb" style="--c:${p.color}">${img ? `<img loading="lazy" src="${esc(img)}" alt="">` : ""}</div>
    <div class="body">
      <div class="title">${esc(p.title)}${p.sold_out ? ' <span class="badge high">sold out</span>' : ""}</div>
      <div class="sub"><span class="dot" style="background:${p.color}"></span>${esc(p.developer_group)}</div>
      <div class="sub muted">${esc([p.district, p.region].filter(Boolean).filter((v, i, a) => a.indexOf(v) === i).join(", "))} · ${esc(p.status === "completed" ? "Ready" : quarter(p.completion))}</div>
      <div class="prices">
        <strong>${money(p.usd_m2_min, p.amd_m2_min, "/m²")}</strong>
        ${p.usd_from != null ? `<span class="muted">from ${compactMoney(p.usd_from, p.amd_from)}</span>` : ""}
        ${dealBadge(p)}
        <span class="info-meter" title="Information completeness ${p.info_score}%"><i style="width:${p.info_score}%"></i></span>
      </div>
    </div>
  </li>`;
}

/**
 * Render the project list; clicking or pressing Enter on an item calls onSelect(id).
 * @param {HTMLElement} el
 * @param {object[]} projects
 * @param {string|null} selectedId
 * @param {(id: string) => void} onSelect
 */
export function renderList(el, projects, selectedId, onSelect) {
  el.innerHTML = projects.length
    ? projects.map((p) => itemHtml(p, selectedId)).join("")
    : `<li class="empty">No projects match these filters.</li>`;
  el.onclick = (e) => {
    const li = e.target.closest(".item");
    if (li) onSelect(li.dataset.id);
  };
  el.onkeydown = (e) => {
    const li = e.target.closest(".item");
    if (li && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); onSelect(li.dataset.id); }
  };
}

export function scrollToItem(el, id) {
  el.querySelector(`.item[data-id="${CSS.escape(id)}"]`)?.scrollIntoView({ block: "nearest", behavior: "smooth" });
}

export { dealBadge };
