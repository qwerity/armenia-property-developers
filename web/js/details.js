import { esc, safeUrl, money, compactMoney, quarter, state } from "./util.js";
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
  return `<div class="hero"><img src="${esc(images[0])}" data-idx="0" alt=""></div>
    ${images.length > 1 ? `<div class="thumbs">${images.slice(1).map((src, i) => `<img loading="lazy" src="${esc(src)}" data-idx="${i + 1}" alt="">`).join("")}</div>` : ""}`;
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
        <div><span>Completion</span><b>${esc(p.completion ? quarter(p.completion) : (p.completion_text || "—"))}</b><small>${esc(p.sold_out ? "sold out" : p.status)}</small></div>
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
      </section>
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
