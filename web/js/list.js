import { esc, money, compactMoney, quarter, stageLabel } from "./util.js";

function dealBadge(p) {
  if (p.discount_pct == null) return "";
  if (Math.abs(p.discount_pct) < 1) return `<span class="badge ok" title="Within 1% of the local median">≈ median</span>`;
  const cls = p.discount_pct >= 10 ? "good" : p.discount_pct > 0 ? "ok" : "high";
  const sign = p.discount_pct > 0 ? "−" : "+";
  const where = p.bench_scope === "district" ? p.district : p.region;
  return `<span class="badge ${cls}" title="Starting $/m² vs. median of ${p.bench_n} projects in ${esc(where)}">${sign}${Math.abs(p.discount_pct)}% vs ${esc(where)}</span>`;
}

function itemHtml(p, selectedId) {
  const img = p.images?.[0];
  return `<li class="item${p.id === selectedId ? " selected" : ""}" data-id="${esc(p.id)}" role="option" tabindex="0" aria-selected="${p.id === selectedId}">
    <div class="thumb" style="--c:${p.color}">${img ? `<img loading="lazy" referrerpolicy="no-referrer" src="${esc(img)}" data-pid="${esc(p.id)}" data-try="0" alt="">` : ""}</div>
    <div class="body">
      <div class="title">${esc(p.title)}${p.sold_out ? ' <span class="badge high">sold out</span>' : ""}</div>
      <div class="sub"><span class="dot" style="background:${p.color}"></span>${esc(p.developer_group)}</div>
      <div class="sub muted">${esc([p.district, p.region].filter(Boolean).filter((v, i, a) => a.indexOf(v) === i).join(", "))} · <span class="stage stage-${esc((p.stage || "unknown").replace(" ", "-"))}">${esc(stageLabel(p))}</span>${p.stage !== "finished" && p.completion ? ` · ${esc(quarter(p.completion))}` : ""}</div>
      <div class="prices">
        <strong${p.price_confidence === "low" ? ' class="uncertain" title="Sources disagree on this price"' : ""}>${money(p.usd_m2_min, p.amd_m2_min, "/m²")}${p.price_confidence === "low" ? "?" : ""}</strong>
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
  el.querySelectorAll(".thumb img").forEach((img) => img.addEventListener("error", () => nextImage(img, projects)));
  el.onclick = (e) => {
    const li = e.target.closest(".item");
    if (li) onSelect(li.dataset.id);
  };
  el.onkeydown = (e) => {
    const li = e.target.closest(".item");
    if (li && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); onSelect(li.dataset.id); }
  };
}

/** Try the project's next image when one fails (dead link / hotlink block); hide the <img> when none work. */
function nextImage(img, projects) {
  const p = projects.find((x) => x.id === img.dataset.pid);
  const i = Number(img.dataset.try) + 1;
  if (p && i < Math.min(p.images.length, 4)) {
    img.dataset.try = String(i);
    img.src = p.images[i];
  } else {
    img.remove();
  }
}

export function scrollToItem(el, id) {
  el.querySelector(`.item[data-id="${CSS.escape(id)}"]`)?.scrollIntoView({ block: "nearest", behavior: "smooth" });
}

export { dealBadge };
