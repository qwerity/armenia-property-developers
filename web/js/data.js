import { colorFor } from "./util.js";

const NEUTRAL = "#8a8f98";

/**
 * Load projects.json and attach derived UI fields (color, search text).
 * @returns {Promise<{meta: object, projects: object[], developers: {name:string,color:string,count:number,inferred:boolean}[]}>}
 */
export async function loadData(url = "data/projects.json") {
  const res = await fetch(url, { cache: "no-cache" });
  if (!res.ok) throw new Error(`Failed to load ${url}: HTTP ${res.status}`);
  const { meta, projects } = await res.json();
  const valid = projects.filter((p) => Number.isFinite(p.lat) && Number.isFinite(p.lng));

  const counts = new Map();
  for (const p of valid) {
    const g = p.developer_group || "Unknown developer";
    const c = counts.get(g) || { name: g, count: 0, inferred: !!p.developer_inferred };
    c.count += 1;
    c.inferred = c.inferred && !!p.developer_inferred;
    counts.set(g, c);
  }
  const developers = [...counts.values()].sort(
    (a, b) => (a.inferred - b.inferred) || (b.count - a.count) || a.name.localeCompare(b.name),
  );
  developers.forEach((d, i) => { d.color = d.name === "Unknown developer" ? NEUTRAL : colorFor(i); });
  const colorOf = new Map(developers.map((d) => [d.name, d.color]));

  for (const p of valid) {
    p.developer_group ||= "Unknown developer";
    p.color = colorOf.get(p.developer_group);
    p._search = [p.title, p.title_am, p.title_ru, p.developer, p.developer_group, p.district, p.region, p.address]
      .filter(Boolean).join(" ").toLowerCase();
  }
  return { meta, projects: valid, developers };
}
