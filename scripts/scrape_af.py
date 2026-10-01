#!/usr/bin/env python3
"""
Pobiera poranne podsumowania Sił Powietrznych ZSU z publicznego podglądu Telegrama
(https://t.me/s/kpszsu) i zapisuje dzienne liczby do data/daily.json.

Uruchamiane codziennie przez GitHub Actions. Bez kluczy, bez logowania.
Źródło: oficjalny kanał @kpszsu. Seria obejmuje poranne raporty, nie pełne doby.

Format wpisu:
  {"d":"2026-09-17","uav":157,"uav_down":124,"down_total":131,"msl":null,"msl_min":4,"id":78627}
  uav       — wystrzelone BSP typu Shahed łącznie z wabikami (tak raportują SP)
  uav_down  — wyłącznie BSP z podaną liczbą; null, gdy raport nie rozdziela typów
  down_total — wszystkie cele razem, nigdy automatycznie przypisywane BSP
  msl       — wystrzelone rakiety; null, gdy podano typ bez liczby
  msl_min   — znana minimalna liczba wystrzelonych rakiet
"""
import json, re, sys, time, html, os, urllib.request
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

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
        body = re.sub(r"<br\s*/?>", "\n", t.group(1), flags=re.I)
        txt = html.unescape(re.sub(r"<[^>]+>", " ", body))
        txt = re.sub(r"[^\S\n]+", " ", txt).strip()
        out.append((int(i.group(1)), d.group(1), txt))
    return out

RE_UAV = re.compile(r"(?<!\d)(\d{1,4})(?:-[а-яіїєґ]{1,3})?\s+ударн\w*\s+БпЛА", re.I)
RE_DOWN = re.compile(r"збито\s*/\s*подавлено\s+(\d{1,4})", re.I)
RE_MSL = re.compile(r"(?<![\d-])(\d{1,3})\s+(?:(?:крилат|балістич|аеробаліст|зенітн|керован|протикорабель|протирадіолокаційн|авіаційн)[\w/]*\s+){0,3}ракет\w*", re.I)
RE_UAV_COUNT = re.compile(r"(\d{1,4})\s+(?:(?:ударн|ворож|розвідувальн)\w*\s+)?(?:БпЛА|безпілотник\w*)", re.I)
RE_DIRS = re.compile(r"Основн\w+ напрям\w+ удару\s*[-–—:]\s*([^.!]+)", re.I)

def missile_counts(text):
    counts = RE_MSL.findall(text)
    rest = RE_MSL.sub("", text)
    # Singular Ukrainian forms state one missile without a digit.
    singular = re.findall(r"\bракетою\b", rest, re.I)
    known = sum(map(int, counts)) + len(singular)
    rest = re.sub(r"\bракетою\b", "", rest, flags=re.I)
    return known, not re.search(r"\bракет\w*", rest, re.I)

def parse(txt):
    start = re.search(r"(?:У|В)\s+ніч\s+на\s+\d", txt, re.I)
    if not start: return None
    body = txt[start.start():]
    launch = re.split(r"Повітряний напад|За попередн|протиповітряною обороною|збито\s*/\s*подавлено", body, maxsplit=1, flags=re.I)[0]
    m = RE_UAV.search(launch)
    if not m: return None
    rec = {"uav": int(m.group(1)), "uav_down": None, "down_total": None}
    headline = RE_DOWN.search(txt[:start.start()])
    d = headline or RE_DOWN.search(body)
    if d:
        if headline or re.match(r"\s+ціл\w*", body[d.end():], re.I):
            rec["down_total"] = int(d.group(1))
        result = RE_DOWN.search(body)
        result_text = body[result.start():] if result else txt[:start.start()]
        result_text = re.split(r"Зафіксовано|влучання", result_text, maxsplit=1, flags=re.I)[0]
        uav = RE_UAV_COUNT.search(result_text)
        if uav and int(uav.group(1)) <= rec["uav"]: rec["uav_down"] = int(uav.group(1))
    # Bullet detail takes precedence over a repeated aggregate in the introduction.
    bullets = re.findall(r"^\s*[-–—•]\s+([^\n;]+)", launch, re.M)
    missile_lines = [line for line in bullets if re.search(r"ракет\w*", line, re.I)]
    if missile_lines:
        counts = [missile_counts(line) for line in missile_lines]
        known = sum(count for count, _ in counts)
        complete = all(complete for _, complete in counts)
    else:
        known, complete = missile_counts(launch)
    rec["msl_min"] = known
    rec["msl"] = known if complete else None
    rec["msl_complete"] = complete
    dirs = RE_DIRS.search(txt); rec["dirs"] = dirs.group(1).strip() if dirs else ""
    return rec

MONTHS = {name: i + 1 for i, name in enumerate(("січня", "лютого", "березня", "квітня", "травня", "червня", "липня", "серпня", "вересня", "жовтня", "листопада", "грудня"))}

def report_day(txt, published):
    local = datetime.fromisoformat(published).astimezone(ZoneInfo("Europe/Kyiv")).date()
    match = re.search(r"ніч\s+на\s+(\d{1,2})\s+(\w+)", txt, re.I)
    if match and match.group(2).lower() in MONTHS:
        month = MONTHS[match.group(2).lower()]
        year = local.year - (month == 12 and local.month == 1)
        return date(year, month, int(match.group(1))).isoformat()
    return local.isoformat()

def scrape(since, max_pages=400, sleep=0.35):
    found, before, pages = {}, None, 0
    while pages < max_pages:
        h = fetch(before); pages += 1
        ps = posts(h)
        if not ps: break
        for pid, dt, txt in ps:
            if datetime.fromisoformat(dt).astimezone(ZoneInfo("Europe/Kyiv")).date().isoformat() < since: return found
            rec = parse(txt)
            if rec:
                day = report_day(txt, dt)
                if day < since: continue
                rec["d"] = day; rec["id"] = pid
                rec["source"] = f"https://t.me/{CH}/{pid}"
                rec["coverage"] = "morning"
                # Latest correction of the same morning report wins, even if smaller.
                if day not in found or pid > found[day]["id"]: found[day] = rec
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
    if not new: raise RuntimeError("Nie znaleziono raportów; dotychczasowy plik pozostaje bez zmian")
    merged.update(new)
    rows = sorted(merged.values(), key=lambda r: r["d"])
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT + ".tmp", "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, separators=(",", ":"))
    os.replace(OUT + ".tmp", OUT)
    print(f"od {since}: nowych/zmienionych {len(new)}, łącznie {len(rows)} dni, ostatni {rows[-1]['d'] if rows else '-'}")

if __name__ == "__main__":
    main()
