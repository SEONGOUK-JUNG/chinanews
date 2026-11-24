# -*- coding: utf-8 -*-
"""5-2/5-3: copy snapshots into the clone and accumulate today's chart points."""
import json, os, shutil, datetime

SCRATCH = os.path.dirname(os.path.abspath(__file__))
DATA = r"C:\Users\USER\Desktop\chinanews-kr\data"
PUB = os.path.join(SCRATCH, "pub", "data")
CH = os.path.join(PUB, "commodity_charts")
rep = {}

# ---- 5-2 snapshots from the local data dir ----
for f in ("commodities.json", "sector_adjustments.json", "news_latest.json",
          "china_news_latest.json", "chart_map.json",
          "units.json"):
    s = os.path.join(DATA, f)
    if os.path.exists(s):
        shutil.copyfile(s, os.path.join(PUB, f))
        rep[f] = "copied"

# Never overwrite a newer published macro snapshot with stale local data.
for f in ("macro_latest.json", "rates_property_latest.json"):
    s, dest = os.path.join(DATA, f), os.path.join(PUB, f)
    if not os.path.exists(s):
        rep[f] = "missing local -> live version kept"
        continue
    local = json.load(open(s, encoding="utf-8"))
    remote = json.load(open(dest, encoding="utf-8")) if os.path.exists(dest) else {}
    if local.get("updated_at_kst", "") >= remote.get("updated_at_kst", ""):
        shutil.copyfile(s, dest)
        rep[f] = "copied (macro/rates)"
    else:
        rep[f] = "older local -> live version kept"

# stocks/fx: publish the RECOVERED objects, never the truncated originals
for f in ("stocks_latest.json", "fx_latest.json"):
    s = os.path.join(SCRATCH, f)
    if os.path.exists(s):
        shutil.copyfile(s, os.path.join(PUB, f))
        rep[f] = "copied (recovered)"
    else:
        rep[f] = "SKIPPED -> live version kept"

com = json.load(open(os.path.join(PUB, "commodities.json"), encoding="utf-8"))
ref_date = com["ref_date"]
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat(timespec="seconds")

# ---- 5-3 accumulate onto the LIVE chart history ----
def add_point(chart_id, value, name=None, unit=None):
    p = os.path.join(CH, chart_id + ".json")
    if os.path.exists(p):
        doc = json.load(open(p, encoding="utf-8"))
    else:
        doc = {"name": name or chart_id, "unit": unit or "",
               "adjustment_applied": True, "candles": []}
    candles = doc.get("candles", [])
    for c in candles:
        if c.get("time") == ref_date:      # same date -> update value only
            c["value"] = value
            break
    else:
        candles.append({"time": ref_date, "value": value})
    candles.sort(key=lambda c: c["time"])
    doc["candles"] = candles
    doc["count"] = len(candles)
    doc["updated_at_kst"] = now
    json.dump(doc, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return chart_id

done, skipped = [], []

# featured 16
for it in com["featured"]:
    cid = it.get("chart_id")
    if cid:
        done.append(add_point(cid, it["price_today"], it["display_name"], it["unit"]))

# chart_map extras (heatmap items)
cm_path = os.path.join(PUB, "chart_map.json")
if os.path.exists(cm_path):
    cmap = json.load(open(cm_path, encoding="utf-8"))
    index = {}
    for a in com["all_items"]:
        index.setdefault(a["display_name"], a)      # first match wins
    for item in cmap.get("items", []):
        hit = index.get(item["name"])
        if not hit:
            skipped.append(item["name"]); continue
        done.append(add_point(item["chart_id"], hit["price_today"], item["name"], item.get("unit")))

# _index.json counts
ip = os.path.join(CH, "_index.json")
if os.path.exists(ip):
    idx = json.load(open(ip, encoding="utf-8"))
    lst = idx["items"] if isinstance(idx, dict) and "items" in idx else idx
    known = {e.get("id") for e in lst}
    for cid in done:
        p = os.path.join(CH, cid + ".json")
        n = len(json.load(open(p, encoding="utf-8"))["candles"])
        if cid in known:
            for e in lst:
                if e.get("id") == cid:
                    e["count"] = n
        else:
            d = json.load(open(p, encoding="utf-8"))
            lst.append({"id": cid, "name": d.get("name", cid), "unit": d.get("unit", ""),
                        "file": cid + ".json", "count": n})
    json.dump(idx, open(ip, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    rep["_index.json"] = "updated"

rep["ref_date"] = ref_date
rep["charts_updated"] = len(done)
rep["chart_map_missing"] = skipped
print(json.dumps(rep, ensure_ascii=False, indent=1))
