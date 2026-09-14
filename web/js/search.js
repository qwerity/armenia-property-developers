import { esc, debounce } from "./util.js";

const ARMENIA_BIAS = { north: 41.35, south: 38.8, west: 43.3, east: 46.7 };
const MAX_PROJECTS = 6;
const MAX_PLACES = 5;

/**
 * Combined search dropdown: matching projects first, then Google Places (New) autocomplete suggestions
 * restricted to Armenia. Keeps the input's existing "filter the list" behaviour.
 *
 * @param {HTMLInputElement} input
 * @param {{projects:()=>object[], onProject:(id:string)=>void, onPlace:(place:{name:string,address:string,location:google.maps.LatLngLiteral,viewport?:google.maps.LatLngBounds})=>void, bias:()=>google.maps.LatLngBounds|null}} opts
 */
export function createSearch(input, { projects, onProject, onPlace, bias }) {
  const box = document.createElement("div");
  box.className = "suggest";
  box.hidden = true;
  box.setAttribute("role", "listbox");
  input.after(box);
  input.setAttribute("aria-autocomplete", "list");
  let token = null;
  let places = null;
  let items = [];
  let active = -1;
  let seq = 0;

  async function placesLib() {
    places ||= await google.maps.importLibrary("places");
    return places;
  }

  function render() {
    box.innerHTML = items.length
      ? items.map((it, i) => `<div class="sg ${i === active ? "on" : ""} sg-${it.kind}" data-i="${i}" role="option">
          <span class="sg-ico">${it.kind === "project" ? `<i class="dot" style="background:${it.color}"></i>` : "📍"}</span>
          <span class="sg-main">${esc(it.main)}<small>${esc(it.sub || "")}</small></span></div>`).join("")
        + (items.some((it) => it.kind === "place") ? `<div class="sg-attr">powered by Google</div>` : "")
      : "";
    box.hidden = !items.length;
  }

  async function update() {
    const q = input.value.trim();
    const my = ++seq;
    if (q.length < 2) {
      items = [];
      render();
      return;
    }
    const lower = q.toLowerCase();
    const projectItems = projects().filter((p) => p._search.includes(lower)).slice(0, MAX_PROJECTS)
      .map((p) => ({ kind: "project", id: p.id, main: p.title, sub: `${p.developer_group} · ${p.district || p.region || ""}`, color: p.color }));
    items = projectItems;
    active = -1;
    render();
    try {
      const { AutocompleteSessionToken, AutocompleteSuggestion } = await placesLib();
      token ||= new AutocompleteSessionToken();
      const { suggestions } = await AutocompleteSuggestion.fetchAutocompleteSuggestions({
        input: q, sessionToken: token, includedRegionCodes: ["am"], locationBias: bias() || ARMENIA_BIAS, language: "en",
      });
      if (my !== seq) return;
      const placeItems = suggestions.filter((s) => s.placePrediction).slice(0, MAX_PLACES).map((s) => ({
        kind: "place", prediction: s.placePrediction,
        main: s.placePrediction.mainText?.text || s.placePrediction.text.text, sub: s.placePrediction.secondaryText?.text || "",
      }));
      items = [...projectItems, ...placeItems];
      render();
    } catch (err) {
      console.warn("Places autocomplete failed", err);
    }
  }

  async function choose(i) {
    const it = items[i];
    if (!it) return;
    box.hidden = true;
    if (it.kind === "project") {
      onProject(it.id);
      return;
    }
    const place = it.prediction.toPlace();
    await place.fetchFields({ fields: ["displayName", "formattedAddress", "location", "viewport"] });
    token = null; // a place details call ends the autocomplete session
    onPlace({ name: place.displayName, address: place.formattedAddress, location: place.location?.toJSON(), viewport: place.viewport });
  }

  input.addEventListener("input", debounce(update, 180));
  input.addEventListener("focus", () => { if (items.length) box.hidden = false; });
  input.addEventListener("keydown", (e) => {
    if (box.hidden || !items.length) return;
    if (e.key === "ArrowDown" || e.key === "ArrowUp") {
      e.preventDefault();
      active = (active + (e.key === "ArrowDown" ? 1 : -1) + items.length) % items.length;
      render();
    } else if (e.key === "Enter" && active >= 0) {
      e.preventDefault();
      choose(active);
    } else if (e.key === "Escape") {
      box.hidden = true;
    }
  });
  box.addEventListener("mousedown", (e) => {
    const el = e.target.closest(".sg[data-i]");
    if (el) {
      e.preventDefault();
      choose(Number(el.dataset.i));
    }
  });
  document.addEventListener("click", (e) => { if (e.target !== input && !box.contains(e.target)) box.hidden = true; });
}
