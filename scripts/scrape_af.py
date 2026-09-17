#!/usr/bin/env python3
"""
Pobiera poranne podsumowania Sił Powietrznych ZSU z publicznego podglądu Telegrama
(https://t.me/s/kpszsu) i zapisuje dzienne liczby do data/daily.json.

Uruchamiane codziennie przez GitHub Actions. Bez kluczy, bez logowania.
Źródło: oficjalny kanał @kpszsu — te same posty, z których ISIS i dataset
Petra Ivaniuka liczą miesięczne sumy.

Format wpisu:
  {"d":"2026-09-17","uav":157,"uav_down":131,"msl":14,"dirs":"Київщина, Запоріжжя та Одещина","id":78621}
  uav       — wystrzelone BSP typu Shahed łącznie z wabikami (tak raportują SP)
  uav_down  — "збито/подавлено" (strącone + zagłuszone), wszystkie cele razem
  msl       — suma rakiet z podaną liczbą; od 10.08.2026 SP części typów nie liczą, więc to dolne ograniczenie
"""
import json, re, sys, time, html, os, urllib.request
from datetime import date, datetime, timedelta

CH = "kpszsu"
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "daily.json")
UA = "Mozilla/5.0 (compatible; naloty-ukraina/1.0; +github pages)"

def fetch(before=None):
    url = f"https://t.me/s/{CH}" + (f"?before={before}" if before else "")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "ignore")

def posts(h):
    out = []
    for b in re.findall(r'<div class="tgme_widget_message_wrap.*?</time>', h, re.S):
        i = re.search(r'data-post="%s/(\d+)"' % CH, b)
        d = re.search(r'datetime="([^"]+)"', b)
        t = re.search(r'class="tgme_widget_message_text[^"]*"[^>]*>(.*?)</div>', b, re.S)
        if not (i and d and t): continue
        txt = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t.group(1)))).strip()
        out.append((int(i.group(1)), d.group(1), txt))
    return out

RE_UAV = re.compile(r"(\d{1,4})\s+ударн\w*\s+БпЛА", re.I)
RE_DOWN = re.compile(r"збито/подавлено\s+(\d{1,4})", re.I)
RE_MSL = re.compile(r"(\d{1,3})\s+(?:крилат|балістич|аеробаліст|зенітн|керован|протикорабель|авіаційн|ракет)\w*", re.I)
RE_DIRS = re.compile(r"Основн\w+ напрям\w+ удару\s*[-–—:]\s*([^.!]+)", re.I)

def parse(txt):
    if "ніч на" not in txt and "ЗБИТО/ПОДАВЛЕНО" not in txt.upper(): return None
    m = RE_UAV.search(txt)
    if not m: return None
    rec = {"uav": int(m.group(1))}
    d = RE_DOWN.search(txt); rec["uav_down"] = int(d.group(1)) if d else None
    msl = sum(int(x) for x in RE_MSL.findall(txt.split("ударн")[0]))
    rec["msl"] = msl
    dirs = RE_DIRS.search(txt); rec["dirs"] = dirs.group(1).strip() if dirs else ""
    return rec

def scrape(since, max_pages=400, sleep=0.35):
    found, before, pages = {}, None, 0
    while pages < max_pages:
        h = fetch(before); pages += 1
        ps = posts(h)
        if not ps: break
        for pid, dt, txt in ps:
            day = dt[:10]
            if day < since: return found
            rec = parse(txt)
            if rec:
                rec["d"] = day; rec["id"] = pid
                # jeśli tego dnia jest kilka podsumowań, zostaw to z największą liczbą BSP
                if day not in found or rec["uav"] > found[day]["uav"]: found[day] = rec
        before = min(p[0] for p in ps)
        time.sleep(sleep)
    return found

def main():
    since = sys.argv[1] if len(sys.argv) > 1 else (date.today() - timedelta(days=10)).isoformat()
    old = []
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as f: old = json.load(f)
    merged = {r["d"]: r for r in old}
    new = scrape(since)
    merged.update(new)
    rows = sorted(merged.values(), key=lambda r: r["d"])
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, separators=(",", ":"))
    print(f"od {since}: nowych/zmienionych {len(new)}, łącznie {len(rows)} dni, ostatni {rows[-1]['d'] if rows else '-'}")

if __name__ == "__main__":
    main()
