/**
 * Turn a long <select> into a searchable combobox, as progressive enhancement.
 *
 * The <select> stays in the DOM and keeps holding the value, so everything that reads it, writes it
 * or rebuilds its options keeps working unchanged; the combobox mirrors it through a MutationObserver
 * and dispatches a normal "change" event when the reader picks something.
 */
const MIN_OPTIONS = 12;

/**
 * @param {HTMLSelectElement} select
 * @param {{min?: number, placeholder?: string}} opts  min: below this many options the select is left alone
 * @returns {{refresh: () => void} | null}
 */
export function enhanceSelect(select, { min = MIN_OPTIONS, placeholder } = {}) {
  if (!select || select.dataset.cbx) return null;
  if (select.options.length < min) return null;
  select.dataset.cbx = "1";

  const wrap = document.createElement("div");
  wrap.className = "cbx";
  const input = document.createElement("input");
  input.type = "text";
  input.className = "cbx-input";
  input.autocomplete = "off";
  input.spellcheck = false;
  input.setAttribute("role", "combobox");
  input.setAttribute("aria-expanded", "false");
  input.setAttribute("aria-autocomplete", "list");
  const list = document.createElement("ul");
  list.className = "cbx-list";
  list.hidden = true;
  list.setAttribute("role", "listbox");
  const id = select.id || `cbx-${Math.random().toString(36).slice(2)}`;
  list.id = `${id}-list`;
  input.setAttribute("aria-controls", list.id);
  if (select.labels?.[0] && !select.labels[0].contains(select)) input.setAttribute("aria-label", select.labels[0].textContent.trim());

  select.after(wrap);
  wrap.append(input, list);
  select.classList.add("cbx-native");

  let options = [];
  let active = -1;
  let open = false;

  const label = (o) => o.textContent.trim();
  const selectedLabel = () => (select.selectedIndex >= 0 ? label(select.options[select.selectedIndex]) : "");

  function readOptions() {
    options = [...select.options].filter((o) => !o.hidden).map((o) => ({ value: o.value, text: label(o) }));
    input.placeholder = placeholder || options[0]?.text || "Search…";
  }

  function render(query = "") {
    const q = query.trim().toLowerCase();
    // A query matches on the option's words, so "gm apex" finds "APEX GM Developer".
    const terms = q.split(/\s+/).filter(Boolean);
    const shown = options.filter((o) => terms.every((t) => o.text.toLowerCase().includes(t)));
    list.replaceChildren(...shown.map((o, i) => {
      const li = document.createElement("li");
      li.className = "cbx-option";
      li.textContent = o.text;
      li.dataset.value = o.value;
      li.id = `${list.id}-${i}`;
      li.setAttribute("role", "option");
      li.setAttribute("aria-selected", String(o.value === select.value));
      if (o.value === select.value) li.classList.add("on");
      li.addEventListener("mousedown", (e) => { e.preventDefault(); pick(o.value); });
      return li;
    }));
    if (!shown.length) {
      const li = document.createElement("li");
      li.className = "cbx-empty";
      li.textContent = "No match";
      list.append(li);
    }
    active = shown.findIndex((o) => o.value === select.value);
    highlight(active >= 0 ? active : 0, false);
  }

  function highlight(i, scroll = true) {
    const items = [...list.querySelectorAll(".cbx-option")];
    if (!items.length) return;
    active = Math.max(0, Math.min(i, items.length - 1));
    items.forEach((li, n) => li.classList.toggle("active", n === active));
    input.setAttribute("aria-activedescendant", items[active].id);
    if (scroll) items[active].scrollIntoView({ block: "nearest" });
  }

  function show() {
    if (open) return;
    open = true;
    readOptions();
    render("");
    list.hidden = false;
    input.setAttribute("aria-expanded", "true");
    input.value = "";
    wrap.classList.add("open");
  }

  function hide() {
    open = false;
    list.hidden = true;
    input.setAttribute("aria-expanded", "false");
    input.value = selectedLabel();
    wrap.classList.remove("open");
  }

  function pick(value) {
    select.value = value;
    select.dispatchEvent(new Event("change", { bubbles: true }));
    hide();
    input.blur();
  }

  input.addEventListener("focus", show);
  input.addEventListener("click", show);
  input.addEventListener("input", () => { if (!open) show(); render(input.value); });
  input.addEventListener("keydown", (e) => {
    if (e.key === "ArrowDown" || e.key === "ArrowUp") {
      e.preventDefault();
      if (!open) return show();
      highlight(active + (e.key === "ArrowDown" ? 1 : -1));
    } else if (e.key === "Enter") {
      const item = list.querySelectorAll(".cbx-option")[active];
      if (open && item) { e.preventDefault(); pick(item.dataset.value); }
    } else if (e.key === "Escape") {
      if (open) { e.stopPropagation(); hide(); }
    } else if (e.key === "Tab") {
      hide();
    }
  });
  input.addEventListener("blur", () => { if (open) hide(); });

  const sync = () => { readOptions(); if (open) render(input.value); else input.value = selectedLabel(); };
  select.addEventListener("change", sync);
  new MutationObserver(sync).observe(select, { childList: true, subtree: true, characterData: true });
  readOptions();
  input.value = selectedLabel();
  return { refresh: sync };
}

/** Enhance every select in `root` that is long enough to be worth searching. */
export function enhanceLongSelects(root = document, min = MIN_OPTIONS) {
  for (const select of root.querySelectorAll("select")) enhanceSelect(select, { min });
}
