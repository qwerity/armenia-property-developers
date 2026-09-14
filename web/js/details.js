import { esc, safeUrl, money, compactMoney, quarter, state, stageLabel } from "./util.js";
import { dealBadge } from "./list.js";

const DAYS = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"];

function youtubeId(url) {
  const m = String(url).match(/(?:youtube\.com\/(?:watch\?v=|embed\/|shorts\/)|youtu\.be\/)([\w-]{11})/);
  return m ? m[1] : null;
}

function hostOf(url) {
  try { return new URL(url).hostname.replace(/^www\./, ""); } catch { return url; }
}

function row(label, value) {
  return value ? `<div class="kv"><span>${esc(label)}</span><b>${value}</b></div>` : "";
}

function hoursText(wh) {
  if (!Array.isArray(wh) || !wh.length) return "";
  return wh.map((w) => {
    const days = (w.days || []).slice().sort((a, b) => DAYS.indexOf(a) - DAYS.indexOf(b));
    const span = days.length > 2 ? `${days[0]}–${days[days.length - 1]}` : days.join(", ");
    return `${span} ${w.startTime || ""}–${w.endTime || ""}`;
  }).map(esc).join("<br>");
}

function gallery(images) {
  if (!images?.length) return `<div class="hero empty">No images available</div>`;
  return `<div class="hero"><img referrerpolicy="no-referrer" src="${esc(images[0])}" data-idx="0" alt=""></div>
    ${images.length > 1 ? `<div class="thumbs">${images.slice(1).map((src, i) => `<img loading="lazy" referrerpolicy="no-referrer" src="${esc(src)}" data-idx="${i + 1}" alt="">`).join("")}</div>` : ""}`;
}

function videos(list) {
  if (!list?.length) return "";
  return `<section><h3>Videos</h3>${list.map((u) => {
    const yt = youtubeId(u);
    return yt
      ? `<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/${yt}" title="Project video" allowfullscreen loading="lazy"></iframe></div>`
      : `<a href="${esc(safeUrl(u))}" target="_blank" rel="noopener">${esc(hostOf(u))}</a>`;
  }).join("")}</section>`;
}

function links(p) {
  const items = [];
  const add = (label, url) => { if (url && safeUrl(url) !== "#") items.push(`<a class="chip" href="${esc(safeUrl(url))}" target="_blank" rel="noopener">${esc(label)}</a>`); };
  add("Project site", p.website);
  if (p.developer_website && p.developer_website !== p.website) add("Developer site", p.developer_website);
  for (const [k, v] of Object.entries(p.social || {})) add(k[0].toUpperCase() + k.slice(1), v);
  add("Google Maps", `https://www.google.com/maps/search/?api=1&query=${p.lat},${p.lng}`);
  add("Street-level (Yandex)", `https://yandex.com/maps/?ll=${p.lng},${p.lat}&z=17&l=stv,sta&panorama[point]=${p.lng},${p.lat}`);
  for (const s of p.sources || []) add(`Source: ${s.name}`, s.url);
  return items.join("");
}

function roomTable(rows) {
  if (!rows?.length) return "";
  const label = (r) => (r.rooms ? `${esc(r.rooms)}-room` : "—");
  const area = (r) => (r.area_min ? `${r.area_min}${r.area_max && r.area_max !== r.area_min ? `–${r.area_max}` : ""} m²` : "—");
  return `<section><h3>Prices by apartment type</h3><table class="ptable">
    <tr><th>Type</th><th>Area</th><th>From</th><th>To</th></tr>
    ${rows.map((r) => `<tr><td>${label(r)}</td><td>${area(r)}</td><td>${compactMoney(r.usd_from, r.amd_from)}</td><td>${compactMoney(r.usd_to, r.amd_to)}</td></tr>`).join("")}
  </table></section>`;
}

function floorTable(rows) {
  if (!rows?.length) return "";
  return `<section><h3>Price per m² by floor</h3><table class="ptable">
    <tr><th>Floors</th><th>Rooms</th><th>Price / m²</th></tr>
    ${rows.map((r) => `<tr><td>${esc(r.floors || "all")}</td><td>${esc(r.rooms || "any")}</td><td>${money(r.usd_m2, r.amd_m2)}</td></tr>`).join("")}
  </table></section>`;
}

function completeness(p) {
  if (p.info_score == null) return "";
  return `<div class="completeness"><div class="row between"><span>Information completeness</span><b>${p.info_score}%</b></div>
    <div class="bar"><i style="width:${p.info_score}%"></i></div>
    ${p.info_missing?.length ? `<span class="muted">Missing from public sources: ${p.info_missing.map(esc).join(", ")}</span>` : `<span class="muted">All key fields found</span>`}
  </div>`;
}

const CONFIDENCE = {
  verified: ["good", "Verified on source page"],
  high: ["good", "Confirmed by multiple sources"],
  medium: ["ok", "Single source / minor disagreement"],
  low: ["high", "Sources disagree — treat with caution"],
  rejected: ["high", "Source figures implausible"],
};

function confidenceBadge(p) {
  const c = CONFIDENCE[p.price_confidence];
  return c ? `<span class="badge ${c[0]}" title="${esc(c[1])}">price: ${esc(p.price_confidence)}</span>` : "";
}

function priceCheck(p) {
  const obs = p.price_obs || [];
  if (!obs.length && !p.price_verification) return "";
  const v = p.price_verification;
  return `<section><h3>Price check ${confidenceBadge(p)}</h3>
    ${v ? `<p class="small">Manual re-check: <b>${esc(v.verdict)}</b>${v.evidence_text ? ` — “${esc(v.evidence_text)}”` : ""}${v.evidence_url ? ` <a href="${esc(safeUrl(v.evidence_url))}" target="_blank" rel="noopener">source</a>` : ""}${v.notes ? `<br><span class="muted">${esc(v.notes)}</span>` : ""}</p>` : ""}
    ${obs.length ? `<table class="ptable"><tr><th>Source</th><th>Figure</th><th>$/m²</th><th></th></tr>
      ${obs.map((o) => `<tr class="${o.used ? "" : "muted"}" title="${esc((o.flags || []).join("; "))}">
        <td>${esc(o.source)}${o.kind === "implied" ? ' <span class="small">(apt ÷ area)</span>' : ""}</td>
        <td class="small">${esc(o.raw || [o.usd && `$${Math.round(o.usd)}`, o.amd && `֏${Math.round(o.amd).toLocaleString("en-US")}`].filter(Boolean).join(" / "))}</td>
        <td>${o.usd_m2 ? `$${o.usd_m2.toLocaleString("en-US")}` : "—"}</td>
        <td>${o.used ? "✓" : (o.flags?.length ? "⚠" : "")}</td></tr>`).join("")}
    </table>` : ""}
  </section>`;
}


function reputation(p) {
  const r = p.developer_rep;
  if (!r) return "";
  const c = r.components || {};
  const res = r.research || {};
  const court = res.court || {};
  const bar = (label, val, max) => `<div class="repbar"><span>${label}</span><i><b style="width:${Math.round((val / max) * 100)}%"></b></i><em>${val}/${max}</em></div>`;
  return `<section><h3>Developer reputation <span class="grade grade-${esc(r.grade)}">${esc(r.grade)} · ${r.score}/100</span></h3>
    ${r.data === "limited" ? `<p class="small muted">Limited research data — score relies mostly on listing data.</p>` : ""}
    ${r.flags?.length ? `<p class="small uncertain">⚠ ${r.flags.map(esc).join(" · ")}</p>` : ""}
    ${bar("Track record", c.track_record, 30)}${bar("Delivery", c.delivery, 20)}${bar("Legal record", c.legal, 30)}${bar("Validation", c.validation, 10)}${bar("Transparency", c.transparency, 10)}
    ${res.legal_entities?.length ? `<div class="kv"><span>Legal entity</span><b>${res.legal_entities.map((e) => esc([e.name_hy, e.name_en].filter(Boolean).join(" / ") + (e.tax_id ? ` (ՀՎՀՀ ${e.tax_id})` : ""))).join("<br>")}</b></div>` : ""}
    ${res.founded_year ? row("Founded", esc(res.founded_year)) : ""}
    ${court.total != null ? `<div class="kv"><span>Court cases (datalex)</span><b>${court.total} total · ${court.respondent ?? 0} as defendant (${court.respondent_by_individuals ?? 0} by individuals) · ${court.claimant ?? 0} as claimant${court.bankruptcy_as_debtor ? ` · <span class="uncertain">${court.bankruptcy_as_debtor} bankruptcy</span>` : ""}${court.criminal ? ` · <span class="uncertain">${court.criminal} criminal</span>` : ""} · ${court.since_2021 ?? 0} since 2021</b></div>` : ""}
    ${res.notable_cases?.length ? `<ul class="cases">${res.notable_cases.map((k) => `<li><a href="https://datalex.am/?app=AppCaseSearch" target="_blank" rel="noopener">${esc(k.case_number)}</a> <span class="muted small">${esc(k.tab || "")} ${esc(k.filed || "")}</span> — ${esc(k.why || "")}</li>`).join("")}</ul>` : ""}
    ${res.news_issues?.length ? `<p class="small"><b>Reported issues:</b></p><ul class="cases">${res.news_issues.map((n) => `<li><a href="${esc(safeUrl(n.url))}" target="_blank" rel="noopener">${esc(n.title || n.url)}</a> <span class="muted small">${esc(n.date || "")}</span>${n.summary ? ` — ${esc(n.summary)}` : ""}</li>`).join("")}</ul>` : ""}
    ${res.positives?.length ? `<p class="small"><b>Positives:</b> ${res.positives.map((n) => `<a href="${esc(safeUrl(n.url))}" target="_blank" rel="noopener">${esc(n.title)}</a>`).join(" · ")}</p>` : ""}
  </section>`;
}

const PRECISION = { exact: "", address: "geocoded from address", street: "approximate (street level)", district: "approximate (district centre)", city: "approximate (city centre)" };

/**
 * Render the right-hand details panel for one project.
 * @param {HTMLElement} el
 * @param {object} p project
 * @param {(images:string[], idx:number)=>void} openLightbox
 * @param {(name:string)=>void} onDeveloper filter by developer
 */
export function renderDetails(el, p, openLightbox, onDeveloper) {
  const phones = (p.phones || []).map((t) => `<a href="tel:${esc(t.replace(/[^\d+]/g, ""))}">${esc(t)}</a>`).join("<br>");
  const place = [p.address, p.district, p.region].filter(Boolean).filter((v, i, a) => a.indexOf(v) === i).join(", ");
  el.innerHTML = `
    ${gallery(p.images)}
    <div class="dpad">
      <h2>${esc(p.title)}</h2>
      ${p.title_am && p.title_am !== p.title ? `<div class="muted small">${esc(p.title_am)}</div>` : ""}
      <button class="devline link" data-dev="${esc(p.developer_group)}"><span class="dot" style="background:${p.color}"></span>${!p.developer_inferred ? esc(p.developer_group)
        : p.developer_group.endsWith("(developer n/a)") ? "Developer not listed"
        : `${esc(p.developer_group)} <span class="muted small">&nbsp;(inferred from contacts)</span>`}</button>
      <div class="muted">${esc(place)}</div>

      ${completeness(p)}
      <div class="stats">
        <div><span>Price / m²</span><b>${money(p.usd_m2_min, p.amd_m2_min)}${p.usd_m2_max && p.usd_m2_max !== p.usd_m2_min ? ` – ${money(p.usd_m2_max, p.amd_m2_max)}` : ""}</b></div>
        <div><span>Apartments from</span><b>${compactMoney(p.usd_from, p.amd_from)}</b>${p.min_area_m2 ? `<small>${p.min_area_m2} m²</small>` : ""}</div>
        <div><span>Completion</span><b>${esc(p.completion ? quarter(p.completion) : (p.completion_text || "—"))}</b><small>${esc(stageLabel(p))}${p.progress_pct != null && p.stage !== "finished" ? ` · ~${p.progress_pct}% of build time` : ""}${p.sold_out ? " · sold out" : ""}</small></div>
      </div>
      ${p.discount_pct != null ? `<div class="bench">${dealBadge(p)} <span class="muted small">local median ${money(p.bench_usd_m2, p.bench_usd_m2 * state.rate, "/m²")} across ${p.bench_n} projects</span></div>` : ""}

      <section>
        <h3>Details</h3>
        ${row("Type", esc(p.kind))}
        ${row("Floors", esc(p.floors))}
        ${row("Income-tax refund", p.income_tax_refund ? "Eligible" : "")}
        ${row("Price updated", esc(p.price_updated))}
        ${row("Original currency", esc(p.currency_raw))}
        ${row("Start of construction", esc(p.start))}
        ${row("Address (hy)", esc(p.address_am))}
        ${row("Coordinates", `${p.lat.toFixed(5)}, ${p.lng.toFixed(5)}${PRECISION[p.geo_precision] ? ` <span class="muted small">(${PRECISION[p.geo_precision]})</span>` : ""}`)}
        ${row("Stage check", p.stage_check ? `${esc(p.stage_check.evidence || "")}${p.stage_check.imagery ? `<br><span class="muted small">Satellite: ${esc(p.stage_check.imagery)}</span>` : ""}${p.stage_check.evidence_url ? ` <a href="${esc(safeUrl(p.stage_check.evidence_url))}" target="_blank" rel="noopener">source</a>` : ""}` : "")}
        ${row("Location check", p.location_note ? `${esc(p.location_note)}${p.location_check?.evidence_url ? ` <a href="${esc(safeUrl(p.location_check.evidence_url))}" target="_blank" rel="noopener">source</a>` : ""}` : "")}
      </section>
      <section><h3>Google address check</h3><div id="gplace"></div></section>
      ${reputation(p)}
      ${priceCheck(p)}
      ${roomTable(p.prices_by_rooms)}
      ${floorTable(p.prices_by_floor)}

      ${p.description || p.description_site || p.developer_about ? `<section><h3>About</h3>
        ${p.description_site ? `<p class="sourcesdesc">${esc(p.description_site)}</p>` : ""}
        ${p.description ? `<p>${esc(p.description)}</p>` : ""}
        ${p.developer_about ? `<p class="muted">${esc(p.developer_about)}</p>` : ""}
      </section>` : ""}

      <section>
        <h3>Contacts${p.contacts_via_developer ? ' <span class="small">(developer office)</span>' : ""}</h3>
        ${row("Phone", phones)}
        ${row("Email", p.email ? `<a href="mailto:${esc(p.email)}">${esc(p.email)}</a>` : "")}
        ${row("Sales office", esc(p.sales_address))}
        ${row("Hours", hoursText(p.working_hours))}
      </section>

      ${videos(p.videos)}
      <section><h3>Links</h3><div class="chips">${links(p)}</div></section>
    </div>`;

  el.querySelectorAll("img[data-idx]").forEach((img) => {
    img.addEventListener("click", () => openLightbox(p.images, Number(img.dataset.idx)));
    img.addEventListener("error", () => img.remove(), { once: true });
  });
  el.querySelector(".devline")?.addEventListener("click", (e) => onDeveloper(e.currentTarget.dataset.dev));
  el.scrollTop = 0;
}

/** Wire the full-screen image viewer; returns an open(images, idx) function. */
export function createLightbox(root) {
  const img = root.querySelector("img");
  let images = [];
  let idx = 0;
  const show = () => { img.src = images[idx]; };
  const step = (d) => { idx = (idx + d + images.length) % images.length; show(); };
  const close = () => { root.hidden = true; img.removeAttribute("src"); };
  root.querySelector(".close").onclick = close;
  root.querySelector(".prev").onclick = () => step(-1);
  root.querySelector(".next").onclick = () => step(1);
  root.addEventListener("click", (e) => { if (e.target === root) close(); });
  document.addEventListener("keydown", (e) => {
    if (root.hidden) return;
    if (e.key === "Escape") { e.preventDefault(); close(); }
    if (e.key === "ArrowLeft") step(-1);
    if (e.key === "ArrowRight") step(1);
  });
  return (list, start = 0) => {
    if (!list?.length) return;
    images = list;
    idx = Math.min(Math.max(start, 0), list.length - 1);
    root.hidden = false;
    show();
  };
}
