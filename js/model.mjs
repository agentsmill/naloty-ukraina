// Pure calculations shared by the map and the regression tests.
export const DAY = 86_400_000;
export const dim = (y, m) => new Date(Date.UTC(y, m, 0)).getUTCDate();
export const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));

export function normalizeDaily(rows, today = new Date().toISOString().slice(0, 10)) {
  if (!Array.isArray(rows)) throw new Error('Nieprawidłowy format danych');
  const days = new Map();
  for (const r of rows) {
    if (!r || !/^\d{4}-\d{2}-\d{2}$/.test(r.d) || !Number.isFinite(Date.parse(r.d)) ||
        new Date(r.d).toISOString().slice(0, 10) !== r.d || r.d > today ||
        !Number.isInteger(r.uav) || r.uav < 0) continue;
    const previous = days.get(r.d);
    if (!previous || (r.id ?? 0) >= (previous.id ?? 0)) days.set(r.d, r);
  }
  return [...days.values()].sort((a, b) => a.d.localeCompare(b.d));
}

export function dailyMonths(rows, since) {
  const months = new Map();
  for (const r of rows) {
    if (r.d < since) continue;
    const k = r.d.slice(0, 7);
    if (!months.has(k)) months.set(k, [+k.slice(0, 4), +k.slice(5), 0, true, 0]);
    const s = months.get(k);
    s[2] += r.uav;
    s[4]++; // Reports present, never the last day number.
  }
  return [...months.values()];
}

export function cumulativeAt(timestamp, series, daily, dailySince) {
  let sum = 0;
  for (const [y, m, count, , days] of series) {
    const start = Date.UTC(y, m - 1, 1);
    if (daily && start >= Date.parse(dailySince)) continue;
    sum += count * clamp((timestamp - start) / ((days || dim(y, m)) * DAY));
  }
  // A report is credited on its reporting date. No invented hourly launch data.
  if (daily) for (const r of daily) {
    if (r.d >= dailySince && Date.parse(r.d) <= timestamp) sum += r.uav;
  }
  return sum;
}

export function flightState(elapsed, duration, stop = 1) {
  const progress = clamp(elapsed / duration, 0, stop);
  return { progress, done: elapsed >= duration * stop - 1e-9 };
}

export function seededRandom(seed) {
  let n = 2166136261;
  for (const c of String(seed)) n = Math.imul(n ^ c.charCodeAt(0), 16777619);
  return () => { n = (Math.imul(n, 1664525) + 1013904223) >>> 0; return n / 4294967296; };
}

export function buildSalvo(event, makeRoute, mainD, mainM) {
  const random = seededRandom(event.d), queue = [];
  let westN = 0, wd = 0, wm = 0;
  for (const [src, city, count, type] of event.west) {
    const drone = type === 'd', r = makeRoute(src, city, drone);
    const stopped = Math.round(count * (event.kill || 0));
    const order = Array.from({length: count}, (_, i) => i);
    for (let i = order.length - 1; i > 0; i--) {
      const j = Math.floor(random() * (i + 1));
      [order[i], order[j]] = [order[j], order[i]];
    }
    const intercepted = new Set(order.slice(0, stopped));
    for (let i = 0; i < count; i++) queue.push({r, kind: drone ? 'w' : 'm',
      at: count > 1 ? i / (count - 1) * 2 : 0,
      stop: intercepted.has(i) ? .34 + random() * .42 : 1,
      scale: drone ? .92 : 1, west: true, weight: 1});
    westN += count;
    if (drone) wd += count; else wm += count;
  }
  for (const [count, routes, kind, group, delay] of [
    [Math.max(0, (event.nat?.d || 0) - wd), mainD, 'd', 5, 0],
    [Math.max(0, (event.nat?.m || 0) - wm), mainM, 'm', 1, 1.5]
  ]) {
    for (let i = 0; i < count; i += group) queue.push({
      r: routes[Math.floor(random() * routes.length)], kind,
      at: delay + random() * (kind === 'd' ? 2.5 : 1.2), stop: 1,
      scale: kind === 'd' ? .7 : 1, west: false, weight: Math.min(group, count - i)
    });
  }
  queue.sort((a, b) => a.at - b.at);
  return {queue, westN, endH: Math.max(0, ...queue.map(q => q.at + q.r.durH * q.stop))};
}
