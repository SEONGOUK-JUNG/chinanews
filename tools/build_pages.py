#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CHINANEWS static SEO page builder (stdlib only, Python 3.8+).

Reads data/*.json and writes crawlable HTML pages:
  commodity/<slug>.html          ko/commodity/<slug>.html     (one per commodity)
  commodities/index.html         ko/commodities/index.html    (A-Z by sector)
  daily/<YYYY-MM-DD>.html        ko/daily/<YYYY-MM-DD>.html   (daily market brief)
  daily/index.html               ko/daily/index.html          (archive)
  ko/index.html                                               (Korean copy of the terminal)
  sitemap.xml

Idempotent: files are rewritten only when content changes.
Run from anywhere:  python3 tools/build_pages.py [--root REPO_DIR]
"""
import argparse
import datetime as dt
import hashlib
import html
import json
import os
import re
import sys

SITE = "https://chinanews.kr"
KST = dt.timezone(dt.timedelta(hours=9))

# ----------------------------------------------------------------------------
# i18n strings
# ----------------------------------------------------------------------------
T = {
    "en": {
        "site": "CHINANEWS",
        "home": "Home",
        "terminal": "Terminal",
        "az": "Commodities A–Z",
        "daily": "Daily Brief",
        "press": "Press",
        "other_lang": "한국어",
        "other_href": "/ko/",
        "price_today": "{name} Price Today",
        "title_cm": "{name} Price Today — China Spot Price {date} | CHINANEWS",
        "desc_cm": "{name} China spot price on {date}: {last}{unit} ({chg} vs. previous session). Daily price history, sector peers and 1-year range.",
        "h1_cm": "{name} — China Spot Price",
        "asof": "As of {date}",
        "last": "Last",
        "prev": "Previous",
        "chg": "Change",
        "sector": "Sector",
        "unit": "Unit",
        "quotes": "Quotes",
        "summary_up": "{name} rose {chg} to {last}{unit} on {date}, up from {prev}{unit} in the previous session.",
        "summary_down": "{name} fell {chg} to {last}{unit} on {date}, down from {prev}{unit} in the previous session.",
        "summary_flat": "{name} was unchanged at {last}{unit} on {date}.",
        "range": "Price range",
        "hist": "Recent price history",
        "hist_note": "Daily observations since late May 2026; earlier points are month-start/month-end observations.",
        "stat_1m": "1 month",
        "stat_3m": "3 months",
        "stat_1y": "1 year",
        "wk52": "52-week",
        "high": "High",
        "low": "Low",
        "ago": "ago",
        "date": "Date",
        "price": "Price",
        "peers": "Other {sector} commodities",
        "all_in_sector": "All {sector} →",
        "cm_index_title": "China Commodities Price List — {n} Spot Prices by Sector | CHINANEWS",
        "cm_index_desc": "Daily China spot prices for {n} commodities across chemicals, metals, energy, steel, textiles, agriculture and building materials. Updated {date}.",
        "cm_index_h1": "China Commodities — Spot Price List",
        "cm_index_intro": "{n} commodities quoted on China's domestic spot market, grouped by sector. Click any item for its price history, 52-week range and sector peers. Prices in CNY unless noted; updated {date}.",
        "name": "Commodity",
        "daily_title": "China Commodities Daily — {date}: {up} up, {down} down | CHINANEWS",
        "daily_desc": "China spot market {date}: {up} commodities up, {down} down, {flat} unchanged. Top gainer {g1} ({g1p}), top decliner {l1} ({l1p}). Indices, FX and sector breakdown.",
        "daily_h1": "China Commodities Daily Brief — {date}",
        "pulse": "Market pulse",
        "up": "Up",
        "down": "Down",
        "flat": "Unchanged",
        "gainers": "Top gainers",
        "losers": "Top decliners",
        "by_sector": "By sector",
        "avg_chg": "Avg. change",
        "count": "Items",
        "indices": "Equity indices",
        "fx": "FX",
        "macro": "China macro indicators",
        "value": "Value",
        "previous": "Previous",
        "ref": "Period",
        "daily_intro": "On {date}, {up} of {total} commodities tracked on China's domestic spot market rose, {down} fell and {flat} were unchanged. {lead}",
        "lead_gain": "The strongest move was {g1} ({g1p}), followed by {g2} ({g2p}). The weakest was {l1} ({l1p}).",
        "daily_index_title": "China Commodities Daily Brief — Archive | CHINANEWS",
        "daily_index_desc": "Archive of daily China spot-market briefs: advance/decline counts, top movers, sector breakdown, indices and FX.",
        "daily_index_h1": "Daily Brief Archive",
        "latest": "Latest",
        "disclaimer": "Prices are indicative China domestic spot quotations compiled for reference only — not investment advice and not an offer to trade. Verify with your counterparty before transacting.",
        "footer_about": "CHINANEWS is a China markets terminal by BRIDGE GROUP (ABridge · Ecobridge), covering {n} commodity spot prices, Chinese and Korean equity indices, FX and macro data, updated daily.",
        "breadcrumb_home": "Home",
        "see_terminal": "Open live terminal →",
    },
    "ko": {
        "site": "CHINANEWS",
        "home": "홈",
        "terminal": "터미널",
        "az": "원자재 전체 목록",
        "daily": "일일 시황",
        "press": "보도자료",
        "other_lang": "English",
        "other_href": "/",
        "price_today": "{name} 가격",
        "title_cm": "{name} 가격 — 중국 현물가 {date} | CHINANEWS",
        "desc_cm": "{date} {name} 중국 현물가 {last}{unit} (전일 대비 {chg}). 일별 가격 추이, 52주 범위, 같은 업종 품목 비교.",
        "h1_cm": "{name} — 중국 현물가",
        "asof": "{date} 기준",
        "last": "당일가",
        "prev": "전일가",
        "chg": "등락률",
        "sector": "업종",
        "unit": "단위",
        "quotes": "시세",
        "summary_up": "{date} {name} 현물가는 전일 {prev}{unit}에서 {chg} 오른 {last}{unit}를 기록했습니다.",
        "summary_down": "{date} {name} 현물가는 전일 {prev}{unit}에서 {chg} 내린 {last}{unit}를 기록했습니다.",
        "summary_flat": "{date} {name} 현물가는 {last}{unit}로 전일과 같았습니다.",
        "range": "가격 범위",
        "hist": "최근 가격 추이",
        "hist_note": "2026년 5월 말부터 일별 관측치, 그 이전은 월초·월말 관측치입니다.",
        "stat_1m": "1개월",
        "stat_3m": "3개월",
        "stat_1y": "1년",
        "wk52": "52주",
        "high": "최고",
        "low": "최저",
        "ago": "전",
        "date": "날짜",
        "price": "가격",
        "peers": "{sector} 업종의 다른 품목",
        "all_in_sector": "{sector} 전체 →",
        "cm_index_title": "중국 원자재 가격표 — {n}종 현물가 업종별 | CHINANEWS",
        "cm_index_desc": "화학·비철금속·에너지·철강·방직·농산물·건축자재 {n}종 중국 현물가 일일 갱신. {date} 기준.",
        "cm_index_h1": "중국 원자재 현물가 전체 목록",
        "cm_index_intro": "중국 내수 현물시장에서 거래되는 원자재 {n}종을 업종별로 정리했습니다. 품목을 누르면 가격 추이·52주 범위·같은 업종 품목을 볼 수 있습니다. 별도 표기 없으면 위안(CNY) 기준, {date} 갱신.",
        "name": "품목",
        "daily_title": "중국 원자재 일일 시황 — {date}: 상승 {up}·하락 {down} | CHINANEWS",
        "daily_desc": "{date} 중국 현물시장: 상승 {up}종, 하락 {down}종, 보합 {flat}종. 최대 상승 {g1}({g1p}), 최대 하락 {l1}({l1p}). 증시·환율·업종별 동향.",
        "daily_h1": "중국 원자재 일일 시황 — {date}",
        "pulse": "시장 펄스",
        "up": "상승",
        "down": "하락",
        "flat": "보합",
        "gainers": "상승 상위",
        "losers": "하락 상위",
        "by_sector": "업종별",
        "avg_chg": "평균 등락",
        "count": "품목 수",
        "indices": "주요 지수",
        "fx": "환율",
        "macro": "중국 거시지표",
        "value": "값",
        "previous": "이전",
        "ref": "기준",
        "daily_intro": "{date} 중국 내수 현물시장에서 집계 대상 {total}종 가운데 {up}종이 올랐고 {down}종이 내렸으며 {flat}종은 보합이었습니다. {lead}",
        "lead_gain": "가장 크게 오른 품목은 {g1}({g1p}), 그다음은 {g2}({g2p})였고, 가장 크게 내린 품목은 {l1}({l1p})이었습니다.",
        "daily_index_title": "중국 원자재 일일 시황 — 아카이브 | CHINANEWS",
        "daily_index_desc": "중국 현물시장 일일 시황 모음: 상승·하락 종목 수, 등락 상위, 업종별 동향, 지수·환율.",
        "daily_index_h1": "일일 시황 아카이브",
        "latest": "최신",
        "disclaimer": "표시 가격은 참고용 중국 내수 현물 호가로, 투자 조언이나 거래 제안이 아닙니다. 실제 거래 전 거래 상대방과 반드시 확인하십시오.",
        "footer_about": "CHINANEWS는 BRIDGE GROUP(에이브릿지·에코브릿지)이 운영하는 중국 시장 터미널로, 원자재 현물가 {n}종과 중국·한국 증시 지수, 환율, 거시지표를 매일 갱신합니다.",
        "breadcrumb_home": "홈",
        "see_terminal": "실시간 터미널 열기 →",
    },
}

# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------
def esc(s):
    return html.escape("" if s is None else str(s), quote=True)


def load(path, default=None):
    try:
        with open(path, "rb") as f:
            raw = f.read().replace(b"\x00", b"")
        return json.loads(raw.decode("utf-8", "replace"))
    except Exception:
        return default


def fmt_num(v, digits=2):
    if v is None:
        return "—"
    try:
        v = float(v)
    except Exception:
        return esc(v)
    if abs(v) >= 1000:
        return "{:,.0f}".format(v) if v == int(v) else "{:,.2f}".format(v)
    s = "{:,.{d}f}".format(v, d=digits)
    return s


def fmt_pct(v):
    if v is None:
        return "—"
    try:
        v = float(v)
    except Exception:
        return esc(v)
    sign = "+" if v > 0 else ""
    return "{}{:.2f}%".format(sign, v)


def pct_class(v):
    try:
        v = float(v)
    except Exception:
        return "flat"
    return "up" if v > 0 else ("down" if v < 0 else "flat")


def slugify(s):
    s = s.lower()
    s = re.sub(r"\(.*?\)", " ", s)  # drop parenthetical
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def write_if_changed(path, content):
    data = content.encode("utf-8")
    if os.path.exists(path):
        with open(path, "rb") as f:
            if f.read() == data:
                return False
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)
    return True


def unit_suffix(unit):
    return (" " + unit) if unit else ""


# ----------------------------------------------------------------------------
# page chrome
# ----------------------------------------------------------------------------
CSS = """
:root{--bg:#000;--bg-1:#080808;--bg-2:#0d0d0d;--panel:#0a0a0a;--line:#1f1f1f;--line-2:#2a2a2a;--text:#e8e8e8;--bright:#fff;--muted:#a8a8a8;--dim:#777;--orange:#E8C078;--up:#ff3b3b;--down:#1aff66;--flat:#9a9a9a;--blue:#3b82f6}
*{box-sizing:border-box}html{font-size:15px}
body{margin:0;background:var(--bg);color:var(--text);font-family:"Inter","Noto Sans KR","Malgun Gothic","Apple SD Gothic Neo",-apple-system,sans-serif;line-height:1.55;-webkit-font-smoothing:antialiased}
a{color:var(--orange);text-decoration:none}a:hover{text-decoration:underline}
.top{background:var(--bg-1);border-bottom:1px solid var(--line);height:42px;display:flex;align-items:center;padding:0 16px;gap:18px;font-size:13px}
.top .logo{font-weight:800;color:var(--orange);letter-spacing:.3px;display:flex;align-items:center;gap:7px}
.top nav{display:flex;gap:2px;flex:1;overflow-x:auto}
.top nav a{padding:0 11px;line-height:42px;color:#c8c8c8;font-weight:600;white-space:nowrap}
.top nav a:hover{color:#fff;background:var(--bg-2);text-decoration:none}
.top .lang{color:var(--muted);white-space:nowrap}
.wrap{max-width:1040px;margin:0 auto;padding:22px 18px 50px}
.crumbs{font-size:12px;color:var(--muted);margin-bottom:14px}.crumbs a{color:var(--muted)}.crumbs a:hover{color:var(--orange)}
h1{font-size:26px;line-height:1.3;margin:0 0 6px;color:var(--bright);font-weight:800;letter-spacing:-.3px}
h2{font-size:14px;color:var(--orange);text-transform:uppercase;letter-spacing:1.2px;margin:30px 0 10px;padding-bottom:6px;border-bottom:1px solid var(--line-2)}
h2.ko{text-transform:none;letter-spacing:.2px}
.sub{color:var(--muted);font-size:13px;margin-bottom:18px}
.lead{font-size:16px;color:var(--text);margin:0 0 14px;line-height:1.7}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:1px;background:var(--line);margin:14px 0 6px}
.cell{background:var(--panel);padding:12px 14px}.cell .k{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.8px}.cell .v{font-size:22px;font-weight:700;color:var(--bright);font-family:"JetBrains Mono",Consolas,monospace;margin-top:4px}
.cell .v.small{font-size:15px;color:var(--text);font-family:inherit;font-weight:600}
.up{color:var(--up)}.down{color:var(--down)}.flat{color:var(--flat)}
table{width:100%;border-collapse:collapse;font-size:13.5px}
th{text-align:left;color:var(--muted);font-weight:600;font-size:11px;text-transform:uppercase;letter-spacing:.8px;padding:7px 10px;border-bottom:1px solid var(--line-2);background:var(--bg-1)}
td{padding:7px 10px;border-bottom:1px solid var(--line);vertical-align:middle}
td.num,th.num{text-align:right;font-family:"JetBrains Mono",Consolas,monospace;font-variant-numeric:tabular-nums}
tr:hover td{background:var(--bg-2)}
.tblwrap{overflow-x:auto;border:1px solid var(--line);background:var(--panel)}
.note{font-size:12px;color:var(--dim);margin-top:6px}
.spark{width:100%;height:150px;display:block;background:var(--panel);border:1px solid var(--line)}
.peers{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}.peers a{font-size:12.5px;padding:4px 9px;border:1px solid var(--line-2);border-radius:3px;background:var(--bg-2);color:var(--text)}.peers a:hover{border-color:var(--orange);text-decoration:none}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:18px}@media(max-width:720px){.cols{grid-template-columns:1fr}}
.cta{display:inline-block;margin-top:10px;padding:8px 14px;border:1px solid var(--orange);border-radius:3px;font-weight:700;font-size:13px}
footer{border-top:1px solid var(--line);margin-top:40px;padding:18px 0 0;font-size:12px;color:var(--muted);line-height:1.6}
footer nav a{margin-right:14px}
.disc{font-size:11.5px;color:var(--dim);margin-top:10px}
.sector-h{margin-top:26px}
.archive li{padding:6px 0;border-bottom:1px solid var(--line)}
"""

BEACON = '''<script>
/* CHINANEWS visit counter — no personal data: date, page path, country code, device class, language only */
(function(){try{
  var KEY='chinanews_hit', today=new Date(Date.now()+9*3600e3).toISOString().slice(0,10);
  var first=!localStorage.getItem('chinanews_seen'); if(first) localStorage.setItem('chinanews_seen','1');
  var newToday=localStorage.getItem(KEY)!==today; if(newToday) localStorage.setItem(KEY,today);
  var ua=navigator.userAgent, plat=/iPad|Tablet/i.test(ua)?'tablet':(/Mobi|Android|iPhone/i.test(ua)?'mobile':'desktop');
  var lang=location.pathname.indexOf('/ko/')===0?'ko':'en';
  var body=JSON.stringify({path:location.pathname,platform:plat,lang:lang,isNew:first,isNewToday:newToday,ref:document.referrer||''});
  var url='https://chinanews-ai.koreagwangju.workers.dev/hit';
  if(navigator.sendBeacon){ navigator.sendBeacon(url, new Blob([body],{type:'text/plain'})); }
  else{ fetch(url,{method:'POST',headers:{'Content-Type':'text/plain'},body:body,keepalive:true}).catch(function(){}); }
}catch(e){}})();
</script>
'''

LOGO_SVG = ('<svg width="18" height="18" viewBox="0 0 32 32" aria-hidden="true">'
            '<line x1="16" y1="3" x2="16" y2="29" stroke="#ff3b3b" stroke-width="2.4" stroke-linecap="round"/>'
            '<rect x="7" y="9" width="18" height="14" rx="2" fill="#E8C078"/></svg>')


def head(lang, title, desc, path, alt_path, ld=None, og_type="website"):
    """<head> block. path/alt_path are absolute site paths ('/commodity/x.html')."""
    en_path, ko_path = (path, alt_path) if lang == "en" else (alt_path, path)
    ld_json = ""
    if ld:
        ld_json = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False, separators=(",", ":")) + "</script>\n"
    return (
        '<!DOCTYPE html>\n<html lang="{lang}">\n<head>\n<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '<title>{title}</title>\n'
        '<meta name="description" content="{desc}">\n'
        '<link rel="canonical" href="{site}{path}">\n'
        '<link rel="alternate" hreflang="en" href="{site}{en}">\n'
        '<link rel="alternate" hreflang="ko" href="{site}{ko}">\n'
        '<link rel="alternate" hreflang="x-default" href="{site}{en}">\n'
        '<link rel="icon" href="/icon.svg" type="image/svg+xml">\n<link rel="alternate" type="application/rss+xml" title="CHINANEWS Daily Brief" href="/feed.xml">\n'
        '<meta name="theme-color" content="#0d1117">\n'
        '<meta property="og:type" content="{ogt}">\n'
        '<meta property="og:site_name" content="CHINANEWS">\n'
        '<meta property="og:title" content="{title}">\n'
        '<meta property="og:description" content="{desc}">\n'
        '<meta property="og:url" content="{site}{path}">\n'
        '<meta property="og:image" content="{site}/og-image.png">\n'
        '<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n<meta property="og:image:alt" content="CHINANEWS - China markets terminal and supply desk">\n'
        '<meta property="og:locale" content="{loc}">\n'
        '<meta name="twitter:card" content="summary_large_image">\n'
        '<meta name="twitter:title" content="{title}">\n'
        '<meta name="twitter:description" content="{desc}">\n'
        '<meta name="twitter:image" content="{site}/og-image.png">\n'
        '{ld}'
        '<style>{css}</style>\n'
        '<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon=\'{{"token": "60582f662b3c4e8a821e4dec6018e061"}}\'></script>\n'
        '<script data-goatcounter="https://chinanews-kr.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>\n'
        '</head>\n'
    ).format(lang=lang, title=esc(title), desc=esc(desc), site=SITE, path=path, en=en_path, ko=ko_path,
             ogt=og_type, loc="ko_KR" if lang == "ko" else "en_US", ld=ld_json, css=CSS).replace('</head>', BEACON + '</head>', 1)


def topbar(lang, alt_path):
    t = T[lang]
    p = "/ko" if lang == "ko" else ""
    home = "/ko/" if lang == "ko" else "/"
    return (
        '<header class="top"><a class="logo" href="{home}">{logo}CHINANEWS</a>'
        '<nav><a href="{home}">{h}</a><a href="{p}/commodities/">{az}</a><a href="{p}/daily/">{d}</a>'
        '<a href="{p}/supply/" style="color:var(--orange)">{sup}</a>'
        '<a href="/press/abridge-sic-cvd-20260615.html">{pr}</a></nav>'
        '<a class="lang" href="{alt}" hreflang="{al}">{ol}</a></header>\n'
    ).format(home=home, logo=LOGO_SVG, h=t["home"], term=t["terminal"], p=p, az=t["az"], d=t["daily"], pr=t["press"], sup=SUP[lang]["nav"],
             alt=alt_path, al="en" if lang == "ko" else "ko", ol=t["other_lang"])


def footer(lang, n_items):
    t = T[lang]
    p = "/ko" if lang == "ko" else ""
    home = "/ko/" if lang == "ko" else "/"
    return (
        '<footer><nav><a href="{home}">{h}</a><a href="{p}/commodities/">{az}</a><a href="{p}/daily/">{d}</a><a href="{p}/supply/">{sup}</a>'
        '<a href="/press/abridge-sic-cvd-20260615.html">{pr}</a><a href="{alt}">{ol}</a></nav>'
        '<p>{about}</p><p class="disc">{disc}</p>'
        '<p>© BRIDGE GROUP · <a href="http://www.abridge.co.kr/" rel="noopener">ABridge</a> · <a href="https://www.ecobridge.biz/" rel="noopener">Ecobridge</a> · <a href="https://dealbridge.asia/" rel="noopener">DealBridge</a></p></footer>\n'
        '</div>\n</body>\n</html>\n'
    ).format(home=home, h=t["home"], term=t["terminal"], p=p, az=t["az"], d=t["daily"], pr=t["press"], sup=SUP[lang]["nav"], alt=t["other_href"], ol=t["other_lang"],
             about=esc(t["footer_about"].format(n=n_items)), disc=esc(t["disclaimer"]))


def crumbs(lang, items):
    """items: list of (label, href|None)"""
    t = T[lang]
    home = "/ko/" if lang == "ko" else "/"
    parts = ['<a href="{}">{}</a>'.format(home, esc(t["breadcrumb_home"]))]
    for label, href in items:
        parts.append('<a href="{}">{}</a>'.format(href, esc(label)) if href else '<span>{}</span>'.format(esc(label)))
    return '<div class="crumbs">' + " › ".join(parts) + "</div>\n"


def breadcrumb_ld(lang, items):
    home = "/ko/" if lang == "ko" else "/"
    lst = [{"@type": "ListItem", "position": 1, "name": T[lang]["breadcrumb_home"], "item": SITE + home}]
    for i, (label, href) in enumerate(items, start=2):
        e = {"@type": "ListItem", "position": i, "name": label}
        if href:
            e["item"] = SITE + href
        lst.append(e)
    return {"@type": "BreadcrumbList", "itemListElement": lst}


ORG_LD = {"@type": "Organization", "@id": "https://chinanews.kr/#org", "name": "BRIDGE GROUP", "alternateName": ["브릿지그룹", "ABridge Co., Ltd.", "㈜에이브릿지", "Ecobridge", "㈜에코브릿지", "DealBridge"], "url": "https://chinanews.kr/", "logo": "https://chinanews.kr/og-image.png", "description": "Korean trading group (Gwangju) supplying rare earths, gallium, germanium, terbium, tungsten, hafnium, yttrium, 5N/6N high-purity copper, semiconductor materials and Chinese semiconductor components direct from licensed Chinese producers; operator of the chinanews.kr China markets terminal.", "foundingLocation": {"@type": "Place", "name": "Gwangju, South Korea"}, "address": {"@type": "PostalAddress", "streetAddress": "21, Bunam-gil 26beon-gil, Buk-gu", "addressLocality": "Gwangju", "addressCountry": "KR"}, "telephone": "+82-1661-0400", "email": "koreagwangju@gmail.com", "contactPoint": [{"@type": "ContactPoint", "contactType": "sales", "telephone": "+82-1661-0400", "email": "koreagwangju@gmail.com", "areaServed": "Worldwide", "availableLanguage": ["ko", "en", "zh"]}], "areaServed": ["KR", "CN", "US", "EU", "JP", "TW", "SG", "VN", "IN"], "knowsAbout": ["rare earth oxides", "neodymium", "dysprosium", "terbium", "yttrium oxide", "gallium", "germanium", "tungsten", "hafnium", "high-purity copper 6N", "silicon carbide", "Chinese semiconductors", "China commodity spot prices"], "sameAs": ["http://www.abridge.co.kr/", "https://www.ecobridge.biz/", "https://dealbridge.asia/", "https://www.linkedin.com/company/109672150/"], "founder": {"@type": "Person", "name": "Seong Ouk Jung", "alternateName": ["SEONG OUK JUNG", "정성욱"], "jobTitle": "Founder & Chairman, BRIDGE GROUP", "worksFor": {"@id": "https://chinanews.kr/#org"}, "sameAs": ["https://www.linkedin.com/in/seong-ouk-jung-33996a2ba"]}}


def h2(lang, text):
    return '<h2 class="{}">{}</h2>\n'.format("ko" if lang == "ko" else "", esc(text))


# ----------------------------------------------------------------------------
# sparkline
# ----------------------------------------------------------------------------
def sparkline(candles, up_is_red=True):
    pts = [(c.get("time"), c.get("value")) for c in candles if c.get("value") is not None]
    if len(pts) < 2:
        return ""
    vals = [float(v) for _, v in pts]
    lo, hi = min(vals), max(vals)
    W, H, PAD = 1000, 150, 10
    span = (hi - lo) or 1.0
    n = len(vals)
    coords = []
    for i, v in enumerate(vals):
        x = PAD + (W - 2 * PAD) * i / (n - 1)
        y = PAD + (H - 2 * PAD) * (1 - (v - lo) / span)
        coords.append("{:.1f},{:.1f}".format(x, y))
    color = "#ff3b3b" if vals[-1] >= vals[0] else "#1aff66"
    first, last = pts[0][0], pts[-1][0]
    return (
        '<svg class="spark" viewBox="0 0 {W} {H}" preserveAspectRatio="none" role="img" aria-label="price trend {f} to {l}">'
        '<polyline fill="none" stroke="{c}" stroke-width="2" points="{p}"/>'
        '<text x="{W1}" y="14" fill="#a8a8a8" font-size="11" text-anchor="end">{hi}</text>'
        '<text x="{W1}" y="{H1}" fill="#a8a8a8" font-size="11" text-anchor="end">{lo}</text>'
        '<text x="12" y="{H1}" fill="#777" font-size="11">{f}</text>'
        '</svg>'
    ).format(W=W, H=H, W1=W - 12, H1=H - 6, c=color, p=" ".join(coords), hi=fmt_num(hi), lo=fmt_num(lo), f=esc(first), l=esc(last))


def hist_stats(candles, last_price):
    """Return dict with 1m/3m/1y change and 52w high/low computed from candles."""
    pts = [(c.get("time"), float(c.get("value"))) for c in candles if c.get("value") is not None and c.get("time")]
    if not pts:
        return None
    pts.sort()
    end = dt.date.fromisoformat(pts[-1][0][:10])
    cur = float(last_price) if last_price is not None else pts[-1][1]

    def at(days):
        target = end - dt.timedelta(days=days)
        best = None
        for t, v in pts:
            d = dt.date.fromisoformat(t[:10])
            if d <= target:
                best = (t, v)
            else:
                break
        return best

    out = {}
    for key, days in (("1m", 30), ("3m", 91), ("1y", 365)):
        b = at(days)
        if b and b[1]:
            out[key] = {"date": b[0], "value": b[1], "pct": (cur - b[1]) / b[1] * 100.0}
    yr = [v for t, v in pts if dt.date.fromisoformat(t[:10]) >= end - dt.timedelta(days=365)]
    if yr:
        out["hi"] = max(yr)
        out["lo"] = min(yr)
    out["n"] = len(pts)
    out["first"] = pts[0][0]
    return out


# ----------------------------------------------------------------------------
# data model
# ----------------------------------------------------------------------------
class Item(object):
    __slots__ = ("ko", "en", "slug", "sector_ko", "sector_en", "unit", "chart_id", "quotes", "candles")

    def __init__(self):
        self.quotes = []
        self.candles = []
        self.unit = ""
        self.chart_id = None

    def name(self, lang):
        return self.ko if lang == "ko" else (self.en or self.ko)

    def sector(self, lang):
        return self.sector_ko if lang == "ko" else (self.sector_en or self.sector_ko)

    @property
    def main(self):
        return self.quotes[0]

    def href(self, lang):
        return ("/ko" if lang == "ko" else "") + "/commodity/" + self.slug + ".html"


def build_items(cm, i18n, chart_map, charts_dir):
    names_map = (i18n or {}).get("names", {})
    sectors_map = (i18n or {}).get("sectors", {})
    # aliases from featured (raw name -> display)
    alias = {}
    unit_of = {}
    chart_of = {}
    for f in cm.get("featured", []):
        raw = f.get("sunsirs_name") or f.get("display_name")
        disp = f.get("display_name") or raw
        if raw:
            alias[raw] = disp
        if disp:
            unit_of[disp] = f.get("unit", "")
            chart_of[disp] = f.get("chart_id")
    for c in (chart_map or {}).get("items", []):
        if c.get("name") and c.get("chart_id"):
            chart_of.setdefault(c["name"], c["chart_id"])
            if c.get("unit"):
                unit_of.setdefault(c["name"], c["unit"])

    items = {}
    order = []
    for row in cm.get("all_items", []):
        raw = (row.get("display_name") or "").strip()
        if not raw:
            continue
        ko = alias.get(raw, raw)
        ko = re.sub(r"\s+", " ", ko)
        it = items.get(ko)
        if it is None:
            it = Item()
            it.ko = ko
            it.en = names_map.get(ko) or names_map.get(raw) or ""
            it.sector_ko = (row.get("sector") or "").strip() or "기타"
            it.sector_en = sectors_map.get(it.sector_ko) or ("Other" if it.sector_ko == "기타" else it.sector_ko)
            it.unit = unit_of.get(ko, "")
            it.chart_id = chart_of.get(ko) or chart_of.get(raw)
            items[ko] = it
            order.append(ko)
        it.quotes.append({
            "sector_ko": (row.get("sector") or "").strip(),
            "prev": row.get("price_prev"),
            "last": row.get("price_today"),
            "chg": row.get("change_pct"),
        })

    # featured items that are not in all_items (e.g. metals quoted separately)
    for f in cm.get("featured", []):
        disp = f.get("display_name")
        if disp and disp not in items and f.get("price_today") is not None:
            it = Item()
            it.ko = disp
            it.en = names_map.get(disp, "")
            it.sector_ko = f.get("sector") or f.get("category") or "기타"
            it.sector_en = sectors_map.get(it.sector_ko) or (i18n or {}).get("categories", {}).get(it.sector_ko) or it.sector_ko
            it.unit = f.get("unit", "")
            it.chart_id = f.get("chart_id")
            it.quotes.append({"sector_ko": it.sector_ko, "prev": f.get("price_prev"), "last": f.get("price_today"), "chg": f.get("change_pct")})
            items[disp] = it
            order.append(disp)

    # slugs (stable, unique)
    used = {}
    for ko in order:
        it = items[ko]
        if it.chart_id:
            base = slugify(it.chart_id)
        elif it.en:
            base = slugify(it.en)
        else:
            base = ""
        if not base:
            base = "k-" + hashlib.md5(ko.encode("utf-8")).hexdigest()[:8]
        slug = base
        if slug in used:
            slug = base + "-" + hashlib.md5(ko.encode("utf-8")).hexdigest()[:6]
        used[slug] = ko
        it.slug = slug
        if it.chart_id:
            c = load(os.path.join(charts_dir, it.chart_id + ".json"))
            if c and isinstance(c.get("candles"), list):
                it.candles = [x for x in c["candles"] if x.get("value") is not None]
                if not it.unit and c.get("unit"):
                    it.unit = c["unit"]
    return [items[k] for k in order]


# ----------------------------------------------------------------------------
# commodity page
# ----------------------------------------------------------------------------
def render_commodity(lang, it, items_by_sector, ref_date, n_items):
    t = T[lang]
    name = it.name(lang)
    sector = it.sector(lang)
    q = it.main
    unit = unit_suffix(it.unit)
    chg = q["chg"]
    path = it.href(lang)
    alt = it.href("ko" if lang == "en" else "en")
    sector_anchor = "s-" + slugify(it.sector_en or "other") if (it.sector_en) else "s-other"
    idx_href = ("/ko" if lang == "ko" else "") + "/commodities/#" + sector_anchor

    title = t["title_cm"].format(name=name, date=ref_date)
    desc = t["desc_cm"].format(name=name, date=ref_date, last=fmt_num(q["last"]), unit=unit, chg=fmt_pct(chg))
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": SITE + path, "url": SITE + path, "name": title, "description": desc,
         "inLanguage": lang, "dateModified": ref_date, "isPartOf": {"@id": SITE + "/#website"},
         "publisher": {"@id": SITE + "/#org"}},
        breadcrumb_ld(lang, [(t["az"], ("/ko" if lang == "ko" else "") + "/commodities/"), (sector, idx_href), (name, None)]),
        ORG_LD,
    ]}

    out = [head(lang, title, desc, path, alt, ld), "<body>\n", topbar(lang, alt), '<div class="wrap">\n',
           crumbs(lang, [(t["az"], ("/ko" if lang == "ko" else "") + "/commodities/"), (sector, idx_href), (name, None)])]
    out.append("<h1>{}</h1>\n".format(esc(t["h1_cm"].format(name=name))))
    sub = t["asof"].format(date=ref_date)
    if lang == "en" and it.en and it.ko != it.en:
        sub += " · " + esc(it.ko)
    elif lang == "ko" and it.en:
        sub += " · " + esc(it.en)
    out.append('<div class="sub">{}</div>\n'.format(sub))

    try:
        c = float(chg)
    except Exception:
        c = 0.0
    key = "summary_up" if c > 0 else ("summary_down" if c < 0 else "summary_flat")
    out.append('<p class="lead">{}</p>\n'.format(esc(t[key].format(name=name, date=ref_date, last=fmt_num(q["last"]), prev=fmt_num(q["prev"]), chg="{:.2f}%".format(abs(c)), unit=unit))))

    out.append('<div class="grid">')
    out.append('<div class="cell"><div class="k">{}</div><div class="v">{}<span style="font-size:12px;color:var(--muted);margin-left:5px">{}</span></div></div>'.format(esc(t["last"]), fmt_num(q["last"]), esc(it.unit or "CNY")))
    out.append('<div class="cell"><div class="k">{}</div><div class="v">{}</div></div>'.format(esc(t["prev"]), fmt_num(q["prev"])))
    out.append('<div class="cell"><div class="k">{}</div><div class="v {}">{}</div></div>'.format(esc(t["chg"]), pct_class(chg), fmt_pct(chg)))
    out.append('<div class="cell"><div class="k">{}</div><div class="v small"><a href="{}">{}</a></div></div>'.format(esc(t["sector"]), idx_href, esc(sector)))
    out.append("</div>\n")

    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import supply_content as SC
        sslug = SC.COMMODITY_TO_SUPPLY.get(it.ko)
    except Exception:
        sslug = None
    if sslug:
        if lang == "ko":
            msg = "{}을(를) 구매하시나요? 중국 생산자 직거래 견적을 받아보세요 — 성적서·샘플 제공, 수출허가 대행.".format(name)
            cta = "견적 요청 →"
        else:
            msg = "Buying {}? Get a producer-backed quotation from China — COA, samples and export-licence handling included.".format(name)
            cta = "Request a quote →"
        out.append('<div class="rfqcta">{} <a class="cta" style="margin:0 0 0 10px;padding:5px 12px" href="{}#rfq">{}</a></div>\n'.format(esc(msg), supply_href(lang, sslug), esc(cta)))

    if len(it.quotes) > 1:
        out.append(h2(lang, t["quotes"]))
        out.append('<div class="tblwrap"><table><thead><tr><th>#</th><th>{}</th><th class="num">{}</th><th class="num">{}</th><th class="num">{}</th></tr></thead><tbody>'.format(esc(t["sector"]), esc(t["prev"]), esc(t["last"]), esc(t["chg"])))
        for i, qq in enumerate(it.quotes, 1):
            sk = qq["sector_ko"]
            out.append('<tr><td>{}</td><td>{}</td><td class="num">{}</td><td class="num">{}</td><td class="num {}">{}</td></tr>'.format(i, esc(sk if lang == "ko" else (it.sector_en if sk == it.sector_ko else sk)), fmt_num(qq["prev"]), fmt_num(qq["last"]), pct_class(qq["chg"]), fmt_pct(qq["chg"])))
        out.append("</tbody></table></div>\n")

    if it.candles:
        st = hist_stats(it.candles, q["last"])
        out.append(h2(lang, t["hist"]))
        out.append(sparkline(it.candles[-120:]))
        if st:
            out.append('<div class="grid">')
            for k, lbl in (("1m", t["stat_1m"]), ("3m", t["stat_3m"]), ("1y", t["stat_1y"])):
                if k in st:
                    out.append('<div class="cell"><div class="k">{} {}</div><div class="v small"><span class="{}">{}</span> <span style="color:var(--muted)">· {}</span></div></div>'.format(esc(lbl), esc(t["ago"]) if lang == "en" else "", pct_class(st[k]["pct"]), fmt_pct(st[k]["pct"]), fmt_num(st[k]["value"])))
            if "hi" in st:
                out.append('<div class="cell"><div class="k">{} {}</div><div class="v small">{}</div></div>'.format(esc(t["wk52"]), esc(t["high"]), fmt_num(st["hi"])))
                out.append('<div class="cell"><div class="k">{} {}</div><div class="v small">{}</div></div>'.format(esc(t["wk52"]), esc(t["low"]), fmt_num(st["lo"])))
            out.append("</div>\n")
        rows = it.candles[-30:][::-1]
        out.append('<div class="tblwrap"><table><thead><tr><th>{}</th><th class="num">{}{}</th><th class="num">{}</th></tr></thead><tbody>'.format(esc(t["date"]), esc(t["price"]), esc(unit), esc(t["chg"])))
        prev_v = None
        # compute day-over-day from chronological order
        chron = it.candles[-31:]
        chg_map = {}
        for i in range(1, len(chron)):
            a, b = chron[i - 1].get("value"), chron[i].get("value")
            if a and b is not None:
                chg_map[chron[i].get("time")] = (float(b) - float(a)) / float(a) * 100.0
        for cnd in rows:
            tm = cnd.get("time")
            dv = chg_map.get(tm)
            out.append('<tr><td>{}</td><td class="num">{}</td><td class="num {}">{}</td></tr>'.format(esc(tm), fmt_num(cnd.get("value")), pct_class(dv) if dv is not None else "flat", fmt_pct(dv) if dv is not None else "—"))
        out.append("</tbody></table></div>\n")
        out.append('<div class="note">{}</div>\n'.format(esc(t["hist_note"])))

    peers = [p for p in items_by_sector.get(it.sector_ko, []) if p is not it]
    if peers:
        out.append(h2(lang, t["peers"].format(sector=sector)))
        out.append('<div class="peers">')
        for p in peers[:40]:
            out.append('<a href="{}">{} <span class="{}">{}</span></a>'.format(p.href(lang), esc(p.name(lang)), pct_class(p.main["chg"]), fmt_pct(p.main["chg"])))
        if len(peers) > 40:
            out.append('<a href="{}">{}</a>'.format(idx_href, esc(t["all_in_sector"].format(sector=sector))))
        out.append("</div>\n")

    out.append('<p><a class="cta" href="{}">{}</a></p>\n'.format("/ko/" if lang == "ko" else "/", esc(t["see_terminal"])))
    out.append(footer(lang, n_items))
    return "".join(out)


# ----------------------------------------------------------------------------
# commodities index
# ----------------------------------------------------------------------------
def render_index(lang, items, items_by_sector, ref_date):
    t = T[lang]
    p = "/ko" if lang == "ko" else ""
    path = p + "/commodities/"
    alt = ("/" if lang == "ko" else "/ko/") + "commodities/"
    n = len(items)
    title = t["cm_index_title"].format(n=n)
    desc = t["cm_index_desc"].format(n=n, date=ref_date)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": SITE + path, "url": SITE + path, "name": title, "description": desc, "inLanguage": lang, "dateModified": ref_date, "isPartOf": {"@id": SITE + "/#website"}},
        breadcrumb_ld(lang, [(t["az"], None)]), ORG_LD]}
    out = [head(lang, title, desc, path, alt, ld), "<body>\n", topbar(lang, alt), '<div class="wrap">\n', crumbs(lang, [(t["az"], None)])]
    out.append("<h1>{}</h1>\n".format(esc(t["cm_index_h1"])))
    out.append('<p class="lead">{}</p>\n'.format(esc(t["cm_index_intro"].format(n=n, date=ref_date))))
    # sector jump links
    sectors = sorted(items_by_sector.keys(), key=lambda s: -len(items_by_sector[s]))
    out.append('<div class="peers">')
    for s in sectors:
        ex = items_by_sector[s][0]
        out.append('<a href="#s-{}">{} ({})</a>'.format(slugify(ex.sector_en or "other"), esc(ex.sector(lang)), len(items_by_sector[s])))
    out.append("</div>\n")
    for s in sectors:
        lst = items_by_sector[s]
        ex = lst[0]
        out.append('<h2 class="sector-h {}" id="s-{}">{} · {}</h2>\n'.format("ko" if lang == "ko" else "", slugify(ex.sector_en or "other"), esc(ex.sector(lang)), len(lst)))
        out.append('<div class="tblwrap"><table><thead><tr><th>{}</th><th class="num">{}</th><th class="num">{}</th><th class="num">{}</th></tr></thead><tbody>'.format(esc(t["name"]), esc(t["prev"]), esc(t["last"]), esc(t["chg"])))
        for it in sorted(lst, key=lambda x: x.name(lang).lower()):
            q = it.main
            out.append('<tr><td><a href="{}">{}</a>{}</td><td class="num">{}</td><td class="num">{}</td><td class="num {}">{}</td></tr>'.format(
                it.href(lang), esc(it.name(lang)), (' <span style="color:var(--dim);font-size:11px">' + esc(it.unit) + "</span>") if it.unit else "",
                fmt_num(q["prev"]), fmt_num(q["last"]), pct_class(q["chg"]), fmt_pct(q["chg"])))
        out.append("</tbody></table></div>\n")
    out.append(footer(lang, n))
    return "".join(out)


# ----------------------------------------------------------------------------
# daily brief
# ----------------------------------------------------------------------------
def render_daily(lang, items, items_by_sector, cm, stocks, fx, macro, ref_date, built_at):
    t = T[lang]
    p = "/ko" if lang == "ko" else ""
    path = p + "/daily/" + ref_date + ".html"
    alt = ("/" if lang == "ko" else "/ko/") + "daily/" + ref_date + ".html"
    pulse = cm.get("pulse", {})
    movers = [it for it in items if it.main["chg"] is not None]
    gainers = sorted(movers, key=lambda x: -float(x.main["chg"]))[:10]
    losers = sorted(movers, key=lambda x: float(x.main["chg"]))[:10]
    gainers = [g for g in gainers if float(g.main["chg"]) > 0]
    losers = [l for l in losers if float(l.main["chg"]) < 0]
    up = pulse.get("up_count") or sum(1 for m in movers if float(m.main["chg"]) > 0)
    down = pulse.get("down_count") or sum(1 for m in movers if float(m.main["chg"]) < 0)
    flat = pulse.get("flat_count") or (len(movers) - up - down)
    total = pulse.get("total") or len(movers)
    g1 = gainers[0] if gainers else None
    g2 = gainers[1] if len(gainers) > 1 else g1
    l1 = losers[0] if losers else None

    def nm(x):
        return x.name(lang) if x else "—"

    def pc(x):
        return fmt_pct(x.main["chg"]) if x else "—"

    title = t["daily_title"].format(date=ref_date, up=up, down=down)
    desc = t["daily_desc"].format(date=ref_date, up=up, down=down, flat=flat, g1=nm(g1), g1p=pc(g1), l1=nm(l1), l1p=pc(l1))
    lead = t["lead_gain"].format(g1=nm(g1), g1p=pc(g1), g2=nm(g2), g2p=pc(g2), l1=nm(l1), l1p=pc(l1)) if g1 and l1 else ""
    intro = t["daily_intro"].format(date=ref_date, up=up, down=down, flat=flat, total=total, lead=lead)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "@id": SITE + path, "mainEntityOfPage": SITE + path, "headline": t["daily_h1"].format(date=ref_date),
         "description": desc, "inLanguage": lang, "datePublished": ref_date, "dateModified": built_at,
         "author": {"@id": SITE + "/#org"}, "publisher": {"@id": SITE + "/#org"}, "image": SITE + "/og-image.png"},
        breadcrumb_ld(lang, [(t["daily"], p + "/daily/"), (ref_date, None)]), ORG_LD]}
    out = [head(lang, title, desc, path, alt, ld, og_type="article"), "<body>\n", topbar(lang, alt), '<div class="wrap">\n',
           crumbs(lang, [(t["daily"], p + "/daily/"), (ref_date, None)])]
    out.append("<h1>{}</h1>\n".format(esc(t["daily_h1"].format(date=ref_date))))
    out.append('<div class="sub">{}</div>\n'.format(esc(t["asof"].format(date=ref_date))))
    out.append('<p class="lead">{}</p>\n'.format(esc(intro)))

    out.append(h2(lang, t["pulse"]))
    out.append('<div class="grid">')
    out.append('<div class="cell"><div class="k">{}</div><div class="v up">{}</div></div>'.format(esc(t["up"]), up))
    out.append('<div class="cell"><div class="k">{}</div><div class="v down">{}</div></div>'.format(esc(t["down"]), down))
    out.append('<div class="cell"><div class="k">{}</div><div class="v flat">{}</div></div>'.format(esc(t["flat"]), flat))
    out.append('<div class="cell"><div class="k">{}</div><div class="v">{}</div></div>'.format(esc(t["count"]), total))
    out.append("</div>\n")

    out.append('<div class="cols">')
    for lbl, lst in ((t["gainers"], gainers), (t["losers"], losers)):
        out.append("<div>" + h2(lang, lbl))
        out.append('<div class="tblwrap"><table><thead><tr><th>{}</th><th>{}</th><th class="num">{}</th><th class="num">{}</th></tr></thead><tbody>'.format(esc(t["name"]), esc(t["sector"]), esc(t["last"]), esc(t["chg"])))
        for it in lst:
            q = it.main
            out.append('<tr><td><a href="{}">{}</a></td><td style="color:var(--muted)">{}</td><td class="num">{}</td><td class="num {}">{}</td></tr>'.format(it.href(lang), esc(it.name(lang)), esc(it.sector(lang)), fmt_num(q["last"]), pct_class(q["chg"]), fmt_pct(q["chg"])))
        out.append("</tbody></table></div></div>")
    out.append("</div>\n")

    out.append(h2(lang, t["by_sector"]))
    out.append('<div class="tblwrap"><table><thead><tr><th>{}</th><th class="num">{}</th><th class="num">{}</th><th class="num">{}</th><th class="num">{}</th><th class="num">{}</th></tr></thead><tbody>'.format(esc(t["sector"]), esc(t["count"]), esc(t["up"]), esc(t["down"]), esc(t["flat"]), esc(t["avg_chg"])))
    for s in sorted(items_by_sector.keys(), key=lambda s: -len(items_by_sector[s])):
        lst = items_by_sector[s]
        ex = lst[0]
        ch = [float(x.main["chg"]) for x in lst if x.main["chg"] is not None]
        su = sum(1 for c in ch if c > 0)
        sd = sum(1 for c in ch if c < 0)
        avg = (sum(ch) / len(ch)) if ch else 0.0
        out.append('<tr><td><a href="{}/commodities/#s-{}">{}</a></td><td class="num">{}</td><td class="num up">{}</td><td class="num down">{}</td><td class="num flat">{}</td><td class="num {}">{}</td></tr>'.format(p, slugify(ex.sector_en or "other"), esc(ex.sector(lang)), len(lst), su, sd, len(ch) - su - sd, pct_class(avg), fmt_pct(avg)))
    out.append("</tbody></table></div>\n")

    idx = (stocks or {}).get("indices") or []
    if idx:
        out.append(h2(lang, t["indices"]))
        out.append('<div class="tblwrap"><table><thead><tr><th>Index</th><th class="num">{}</th><th class="num">{}</th><th class="num">{}</th></tr></thead><tbody>'.format(esc(t["last"]), esc(t["prev"]), esc(t["chg"])))
        for i in idx:
            if not i.get("found", True) or i.get("price") is None:
                continue
            out.append('<tr><td>{}</td><td class="num">{}</td><td class="num">{}</td><td class="num {}">{}</td></tr>'.format(esc(i.get("name")), fmt_num(i.get("price")), fmt_num(i.get("prev_close")), pct_class(i.get("change_pct")), fmt_pct(i.get("change_pct"))))
        out.append("</tbody></table></div>\n")
        if stocks.get("run_at_kst"):
            out.append('<div class="note">{} KST</div>\n'.format(esc(str(stocks["run_at_kst"])[:16].replace("T", " "))))

    rates = []
    for grp in ("rates", "derived"):
        for k, v in ((fx or {}).get(grp) or {}).items():
            if isinstance(v, dict) and v.get("value") is not None:
                rates.append(v)
    if rates:
        out.append(h2(lang, t["fx"]))
        out.append('<div class="tblwrap"><table><thead><tr><th>Pair</th><th class="num">{}</th><th class="num">{}</th><th class="num">{}</th></tr></thead><tbody>'.format(esc(t["last"]), esc(t["prev"]), esc(t["chg"])))
        for v in rates:
            out.append('<tr><td>{}</td><td class="num">{}</td><td class="num">{}</td><td class="num {}">{}</td></tr>'.format(esc(v.get("name")), fmt_num(v.get("value"), 4 if float(v.get("value")) < 100 else 2), fmt_num(v.get("prev_value"), 4 if float(v.get("prev_value") or 0) < 100 else 2), pct_class(v.get("change_pct")), fmt_pct(v.get("change_pct"))))
        out.append("</tbody></table></div>\n")

    ind = (macro or {}).get("indicators") or []
    if ind:
        out.append(h2(lang, t["macro"]))
        out.append('<div class="tblwrap"><table><thead><tr><th>Indicator</th><th class="num">{}</th><th class="num">{}</th><th>{}</th></tr></thead><tbody>'.format(esc(t["value"]), esc(t["previous"]), esc(t["ref"])))
        for i in ind:
            lbl = i.get("label") if lang == "ko" else (i.get("label_en") or i.get("label"))
            out.append('<tr><td>{}</td><td class="num">{}</td><td class="num">{}</td><td style="color:var(--muted)">{}</td></tr>'.format(esc(lbl), esc(i.get("display") or i.get("value")), esc(i.get("previous")), esc(i.get("ref"))))
        out.append("</tbody></table></div>\n")

    out.append('<p><a class="cta" href="{}">{}</a></p>\n'.format("/ko/" if lang == "ko" else "/", esc(t["see_terminal"])))
    out.append(footer(lang, len(items)))
    return "".join(out)


def render_daily_index(lang, dates, n_items):
    t = T[lang]
    p = "/ko" if lang == "ko" else ""
    path = p + "/daily/"
    alt = ("/" if lang == "ko" else "/ko/") + "daily/"
    title = t["daily_index_title"]
    desc = t["daily_index_desc"]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": SITE + path, "url": SITE + path, "name": title, "description": desc, "inLanguage": lang, "isPartOf": {"@id": SITE + "/#website"}},
        breadcrumb_ld(lang, [(t["daily"], None)]), ORG_LD]}
    out = [head(lang, title, desc, path, alt, ld), "<body>\n", topbar(lang, alt), '<div class="wrap">\n', crumbs(lang, [(t["daily"], None)])]
    out.append("<h1>{}</h1>\n".format(esc(t["daily_index_h1"])))
    out.append('<p class="lead">{}</p>\n'.format(esc(desc)))
    out.append('<ul class="archive" style="list-style:none;padding:0;margin:0">')
    for i, d in enumerate(dates):
        out.append('<li><a href="{}/daily/{}.html">{}</a>{}</li>'.format(p, d, esc(t["daily_h1"].format(date=d)), ' <span style="color:var(--orange);font-size:11px">' + esc(t["latest"]) + "</span>" if i == 0 else ""))
    out.append("</ul>\n")
    out.append(footer(lang, n_items))
    return "".join(out)


# ----------------------------------------------------------------------------
# Korean copy of the terminal (index.html -> ko/index.html)
# ----------------------------------------------------------------------------
KO_TITLE = "CHINANEWS — 중국 원자재·증시·환율 실시간 터미널 | 희토류·반도체·6N 구리 공급"
KO_BANNER = """
<!-- supply-banner -->
<style>
  .sup-wrap{background:var(--bg-1);border-bottom:1px solid var(--line);padding:10px 14px 12px}
  .sup-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
  @media(max-width:900px){.sup-grid{grid-template-columns:1fr}}
  .sup-card{background:var(--panel);border:1px solid var(--line-2);border-top:2px solid var(--orange);padding:11px 13px;display:flex;flex-direction:column;min-height:200px}
  .sup-card .panel-title{margin-bottom:6px}
  .sup-card .panel-title a{color:var(--orange)}
  .sup-card p{font-size:12.5px;color:var(--text);line-height:1.55;margin:0 0 7px}
  .sup-card ul{margin:0 0 8px;padding-left:16px;font-size:11.5px;color:var(--muted)}.sup-card li{margin:2px 0}
  .sup-card .lp{font-size:11px;color:var(--muted);border-top:1px solid var(--line-grid);padding-top:6px;margin-top:auto;font-family:"JetBrains Mono",monospace}
  .sup-card .lp b{color:var(--text-bright);font-weight:600}
  .sup-card .acts{display:flex;gap:8px;align-items:center;margin-top:8px}
  .sup-btn{display:inline-block;padding:4px 11px;border:1px solid var(--orange);border-radius:2px;color:var(--orange);font-weight:700;font-size:12px;background:rgba(232,192,120,.06)}
  .sup-btn:hover{background:var(--orange);color:#000}
  .sup-lnk{font-size:12px;color:var(--muted)}.sup-lnk:hover{color:var(--text-bright)}
  .sup-more{margin-top:8px;text-align:center}
  .sup-more button{background:var(--bg-2);border:1px solid var(--line-2);border-radius:2px;color:var(--text);font-size:12px;padding:5px 14px;cursor:pointer;font-family:inherit}
  .sup-more button:hover{border-color:var(--orange);color:var(--orange)}
  .sup-mini{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:8px;margin-top:8px}
  .sup-mini a{display:block;background:var(--panel);border:1px solid var(--line-2);padding:8px 10px;font-size:12px;color:var(--text)}
  .sup-mini a b{display:block;color:var(--orange);font-size:12.5px;margin-bottom:2px}
  .sup-mini a span{color:var(--muted);font-size:11px}
  .sup-mini a:hover{border-color:var(--orange)}
  .sup-mini[hidden]{display:none}
</style>
<div class="sup-wrap" id="supply-banner">
  <div class="sup-grid">
    <div class="sup-card">
      <div class="panel-title"><a href="/ko/supply/rare-earths.html">중국 희토류 공급</a> <span class="badge-live">SUPPLY</span></div>
      <p>네오디뮴·프라세오디뮴·디스프로슘·테르븀·이트륨·란탄·세륨 등 란탄족 전 범위 — 내몽골·간저우 생산자의 산화물 3N~5N, 금속, 자석용 합금. 수출허가 대행 포함.</p>
      <ul><li>17개 원소 · 산화물·금속·PrNd/DyFe 합금</li><li>자석·형광체·촉매·세라믹 등급</li><li>COA(ICP) · 샘플 100g부터</li></ul>
      <div class="lp" data-items="산화네오디뮴=산화네오디뮴|산화디스프로슘=산화디스프로슘|산화프라세오디뮴=산화프라세오디뮴">현물가 불러오는 중…</div>
      <div class="acts"><a class="sup-btn" href="/ko/supply/rare-earths.html">규격·상세 →</a></div>
    </div>
    <div class="sup-card">
      <div class="panel-title"><a href="/ko/supply/semiconductors.html">중국 반도체 조달</a> <span class="badge-live">SUPPLY</span></div>
      <p>MCU, 전력소자(MOSFET·IGBT·SiC/GaN), 메모리, 아날로그/PMIC, 센서, LED를 중국 정식 생산자·공인 대리점에서 조달. 서구 품번 대체품 검색, 샘플 검증, 수출통제 심사.</p>
      <ul><li>수요 기반 조달 — 단종·오픈마켓 재고 없음</li><li>기존 BOM 품번 대체품 검색 서비스</li><li>생산자 보증 · 고장분석 지원</li></ul>
      <div class="lp" data-items="폴리실리콘=폴리실리콘|게르마늄=게르마늄|금속규소(공업규소)=금속규소">현물가 불러오는 중…</div>
      <div class="acts"><a class="sup-btn" href="/ko/supply/semiconductors.html">규격·상세 →</a></div>
    </div>
    <div class="sup-card">
      <div class="panel-title"><a href="/ko/supply/high-purity-copper.html">고순도 구리 5N / 6N</a> <span class="badge-live">SUPPLY</span></div>
      <p>스퍼터링 타깃·본딩와이어·초전도 안정화재·연구용 전해·존정련 구리 99.999%, 99.9999% — 잉곳·봉·과립 — GDMS 전원소 성적서 첨부. 무산소동 C10100, A급 전기동도 공급.</p>
      <ul><li>6N은 10개 원소 ICP 합산이 아닌 GDMS(70개 원소 이상)로 검증</li><li>잉곳 1~5kg · 봉 ø10~50mm · 과립 2~6mm</li><li>일일 전기동 가격 + 프리미엄으로 견적</li></ul>
      <div class="lp" data-items="구리=구리">현물가 불러오는 중…</div>
      <div class="acts"><a class="sup-btn" href="/ko/supply/high-purity-copper.html">규격·상세 →</a></div>
    </div>
  </div>
  <div class="sup-more"><button type="button" id="sup-more-btn" data-more="더보기 — 취급 품목 7개 ▾" data-less="접기 ▴">더보기 — 취급 품목 7개 ▾</button></div>
  <div class="sup-mini" id="sup-more-list" hidden>
    <a href="/ko/supply/yttrium.html"><b>이트륨 금속 · 산화이트륨 5N</b><span>반도체 챔버 코팅, YSZ, YAG, Al–Y 합금</span></a>
    <a href="/ko/supply/gallium.html"><b>갈륨 4N~7N · 산화갈륨</b><span>GaN/GaAs 에피, LED, 전력소자 — 수출허가 대행</span></a>
    <a href="/ko/supply/terbium.html"><b>테르븀 산화물 · 금속</b><span>NdFeB 보자력(GBD), 형광체, 테르페놀</span></a>
    <a href="/ko/supply/tungsten.html"><b>텅스텐 — APT·분말·탄화물</b><span>초경, 타깃, 가공재</span></a>
    <a href="/ko/supply/germanium.html"><b>게르마늄 잉곳 · GeO₂ · GeCl₄</b><span>SiGe, 광섬유, 적외선 광학, III-V 태양전지</span></a>
    <a href="/ko/supply/hafnium.html"><b>하프늄 스펀지 · 크리스탈바 · HfO₂</b><span>초합금, 원자력, high-k 절연막</span></a>
    <a href="/ko/supply/semiconductor-materials.html"><b>반도체 소재</b><span>SiC 분말·CVD-SiC 부품, HF, 형석, 리튬 화학품</span></a>
    <a href="/ko/supply/" style="border-color:var(--orange)"><b>전체 품목 →</b><span>공급 허브 · 견적 요청 폼</span></a>
  </div>
</div>
<script>(function(){
  var b=document.getElementById('sup-more-btn'),l=document.getElementById('sup-more-list');
  if(b&&l) b.addEventListener('click',function(){ l.hidden=!l.hidden; b.textContent=l.hidden?b.getAttribute('data-more'):b.getAttribute('data-less'); });
  fetch('/data/commodities.json?t='+Date.now()).then(function(r){return r.json();}).then(function(d){
    var m={}; (d.all_items||[]).forEach(function(x){ if(!(x.display_name in m)) m[x.display_name]=x; });
    (d.featured||[]).forEach(function(x){ if(x.display_name&&!(x.display_name in m)) m[x.display_name]=x; });
    document.querySelectorAll('.sup-card .lp[data-items]').forEach(function(el){
      var en=(window.CN_LANG==='en'), parts=[];
      el.getAttribute('data-items').split('|').forEach(function(pair){
        var k=pair.split('=')[0], lbl=pair.split('=')[1]||k, it=m[k]; if(!it||it.price_today==null) return;
        var p=Number(it.change_pct)||0, col=p>0?'var(--up)':(p<0?'var(--down)':'var(--muted)');
        parts.push(lbl+' <b>'+Number(it.price_today).toLocaleString('en-US')+'</b> <span style="color:'+col+'">'+(p>0?'+':'')+p.toFixed(2)+'%</span>');
      });
      if(parts.length) el.innerHTML=(d.ref_date||'')+' · CNY &nbsp; '+parts.join(' &nbsp;·&nbsp; ');
    });
  }).catch(function(){});
})();</script>
<!-- /supply-banner -->
"""
KO_DESC = ("중국·글로벌 원자재 현물가의 일일 변동을 한눈에 — 중국 증시(CSI300·항셍), 코스피, 위안·원 환율, 금리·부동산, "
           "기술적 차트, 실시간 뉴스, 수입원가 계산기. 매일 갱신되는 라이브 마켓 터미널. chinanews.kr")


def render_ko_home(src_html):
    s = src_html
    s = s.replace('<html lang="en">', '<html lang="ko">', 1)
    s = re.sub(r"<title>.*?</title>", "<title>" + esc(KO_TITLE) + "</title>", s, count=1, flags=re.S)
    s = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="' + esc(KO_DESC) + '">', s, count=1)
    s = s.replace('<link rel="canonical" href="https://chinanews.kr/">', '<link rel="canonical" href="https://chinanews.kr/ko/">', 1)
    s = s.replace('<meta property="og:url" content="https://chinanews.kr/">', '<meta property="og:url" content="https://chinanews.kr/ko/">', 1)
    # compact supply banner (top centre) in Korean
    s = re.sub(r"<!-- supply-banner -->.*?<!-- /supply-banner -->", lambda _m: KO_BANNER, s, count=1, flags=re.S)
    s = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="' + esc(KO_TITLE) + '">', s, count=1)
    s = re.sub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="' + esc(KO_DESC) + '">', s, count=1)
    s = s.replace('<meta property="og:url" content="https://chinanews.kr/">', '<meta property="og:url" content="https://chinanews.kr/ko/">', 1)
    s = s.replace('<meta property="og:locale" content="en_US">', '<meta property="og:locale" content="ko_KR">', 1)
    s = s.replace('<meta property="og:locale:alternate" content="ko_KR">', '<meta property="og:locale:alternate" content="en_US">', 1)
    s = re.sub(r'<meta name="twitter:title" content="[^"]*">', '<meta name="twitter:title" content="' + esc(KO_TITLE) + '">', s, count=1)
    s = re.sub(r'<meta name="twitter:description" content="[^"]*">', '<meta name="twitter:description" content="' + esc(KO_DESC) + '">', s, count=1)
    # default language when the visitor has not chosen one
    s = s.replace("localStorage.getItem('chinanews_lang')||'en'; }catch(e){ return 'en'; }", "localStorage.getItem('chinanews_lang')||'ko'; }catch(e){ return 'ko'; }", 1)
    s = s.replace('<span data-lang="en" class="active">EN</span><span data-lang="ko">KR</span>', '<span data-lang="en">EN</span><span data-lang="ko" class="active">KR</span>', 1)
    # relative assets -> absolute (page lives under /ko/)
    s = re.sub(r"""(['"])data/""", r"\1/data/", s)
    s = s.replace('href="manifest.json"', 'href="/manifest.json"').replace('href="icon.svg"', 'href="/icon.svg"')
    s = s.replace("'<a href=\"'+it.link+'\"", "'<a href=\"'+((/^(https?:|\\/)/.test(it.link||''))?it.link:'/'+it.link)+'\"")
    # nav/footer links that point at EN pages -> KO pages
    s = s.replace('href="/commodities/"', 'href="/ko/commodities/"').replace('href="/daily/"', 'href="/ko/daily/"').replace('href="/supply/"', 'href="/ko/supply/"')
    s = s.replace('>Supply / RFQ<', '>공급·견적<')
    s = s.replace('<a class="tb-tab" href="/ko/commodities/">A–Z</a>', '<a class="tb-tab" href="/ko/commodities/">원자재 목록</a>')
    s = s.replace('<a class="tb-tab" href="/ko/daily/">Daily</a>', '<a class="tb-tab" href="/ko/daily/">일일 시황</a>')
    s = s.replace('>Commodities A–Z</a>', '>원자재 전체 목록</a>').replace('>Daily Brief</a>', '>일일 시황</a>')
    s = s.replace('<a href="/press/abridge-sic-cvd-20260615.html" style="color:var(--orange);margin-right:14px">Press</a>', '<a href="/press/abridge-sic-cvd-20260615.html" style="color:var(--orange);margin-right:14px">보도자료</a>')
    s = s.replace('<a class="tb-tab" href="/ko/" hreflang="ko">한국어</a>', '<a class="tb-tab" href="/" hreflang="en">English</a>')
    s = s.replace('<a href="/ko/" hreflang="ko">한국어</a>', '<a href="/" hreflang="en">English</a>')
    s = s.replace('id="seo-footer" lang="en"', 'id="seo-footer" lang="ko"')
    s = re.sub(r'<p class="seo-about" data-lang="en">.*?</p>\s*', "", s, count=1, flags=re.S)
    s = s.replace('<p class="seo-about" data-lang="ko" hidden>', '<p class="seo-about" data-lang="ko">', 1)
    return s


# ----------------------------------------------------------------------------
# buyer-facing supply / RFQ pages (content in tools/supply_content.py)
# ----------------------------------------------------------------------------
SUP = {
    "en": {"nav": "Supply / RFQ", "crumb": "Supply", "rfq": "Request a quote", "live": "Live China prices (terminal)",
           "faq": "Frequently asked questions", "compliance": "Compliance & quality", "about": "About the supplier",
           "related": "Other products we supply", "index_title": "Rare Earths, Gallium, Germanium, Tungsten, High-Purity Copper & Semiconductors from China — Supply & RFQ | CHINANEWS",
           "index_desc": "BRIDGE GROUP sources strategic materials and semiconductors from licensed Chinese producers: rare earth oxides and metals, yttrium, terbium, gallium, germanium, tungsten, hafnium, 6N copper, SiC and semiconductor components. Request a quote.",
           "index_h1": "Supply from China — Strategic Materials & Semiconductors",
           "index_intro": "We are a Korean trading group with producer relationships across China's rare-earth, minor-metal and semiconductor supply chains. Pick a product line below for specifications, live China prices and an RFQ form — or send one enquiry covering several items.",
           "f_company": "Company", "f_name": "Contact name", "f_email": "Email", "f_phone": "Phone / WhatsApp / WeChat", "f_country": "Country",
           "f_product": "Product", "f_qty": "Quantity & frequency", "f_spec": "Specification / purity / form", "f_msg": "Message (application, target price, delivery terms)",
           "f_send": "Send RFQ", "f_sending": "Sending…", "f_ok": "✓ RFQ received — we reply within one business day", "f_fail": "Failed — please email koreagwangju@gmail.com",
           "f_note": "Replies go out from BRIDGE GROUP (Gwangju, Korea). No brokers' fees are charged to buyers; quotations are producer-backed.",
           "price_cols": ["Item", "Last (CNY)", "Change", "History"], "see": "chart →"},
    "ko": {"nav": "공급·견적", "crumb": "공급", "rfq": "견적 요청", "live": "중국 현물가 (터미널 연동)",
           "faq": "자주 묻는 질문", "compliance": "컴플라이언스·품질", "about": "공급사 소개",
           "related": "다른 취급 품목", "index_title": "중국 희토류·갈륨·게르마늄·텅스텐·고순도 구리·반도체 공급 — 견적 문의 | CHINANEWS",
           "index_desc": "BRIDGE GROUP은 허가받은 중국 생산자로부터 전략소재와 반도체를 조달합니다: 희토류 산화물·금속, 이트륨, 테르븀, 갈륨, 게르마늄, 텅스텐, 하프늄, 6N 구리, SiC, 반도체 부품. 견적 문의.",
           "index_h1": "중국 공급 — 전략소재·반도체",
           "index_intro": "중국 희토류·희소금속·반도체 공급망의 생산자와 직접 거래하는 한국 무역그룹입니다. 아래 품목을 고르면 규격, 중국 현물가, 견적 요청 폼을 볼 수 있습니다. 여러 품목을 한 번에 문의하셔도 됩니다.",
           "f_company": "회사명", "f_name": "담당자", "f_email": "이메일", "f_phone": "전화 / 카카오톡 / 위챗", "f_country": "국가",
           "f_product": "품목", "f_qty": "수량·주기", "f_spec": "규격 / 순도 / 형태", "f_msg": "문의 내용 (용도, 목표가, 납품 조건)",
           "f_send": "견적 요청 보내기", "f_sending": "전송 중…", "f_ok": "✓ 접수됐습니다 — 1영업일 내 회신드립니다", "f_fail": "전송 실패 — koreagwangju@gmail.com 으로 보내주세요",
           "f_note": "회신은 BRIDGE GROUP(광주)에서 드립니다. 바이어에게 중개수수료를 청구하지 않으며, 견적은 생산자 확인을 거칩니다.",
           "price_cols": ["품목", "당일가 (CNY)", "등락", "추이"], "see": "차트 →"},
}
WEB3FORMS_KEY = None


def _web3forms_key(root):
    global WEB3FORMS_KEY
    if WEB3FORMS_KEY is None:
        try:
            with open(os.path.join(root, "index.html"), "r", encoding="utf-8") as f:
                m = re.search(r'name="access_key"\s+value="([0-9a-f-]{36})"', f.read())
            WEB3FORMS_KEY = m.group(1) if m else ""
        except Exception:
            WEB3FORMS_KEY = ""
    return WEB3FORMS_KEY


def supply_href(lang, slug=None):
    return ("/ko" if lang == "ko" else "") + "/supply/" + ((slug + ".html") if slug else "")


def rfq_form(lang, key, subject, product):
    t = SUP[lang]
    fid = "rfq"
    return (
        '<div id="rfq" class="rfqbox"><h2 class="{ko}">{h}</h2>'
        '<form id="{fid}-form" autocomplete="on">'
        '<input type="hidden" name="access_key" value="{key}"><input type="hidden" name="subject" value="{subj}">'
        '<input type="hidden" name="from_name" value="chinanews.kr supply page"><input type="checkbox" name="botcheck" class="hidden" style="display:none" tabindex="-1" autocomplete="off">'
        '<div class="fgrid">'
        '<label>{c}<input type="text" name="company" required></label>'
        '<label>{n}<input type="text" name="name" required></label>'
        '<label>{e}<input type="email" name="email" required></label>'
        '<label>{p}<input type="text" name="phone"></label>'
        '<label>{co}<input type="text" name="country"></label>'
        '<label>{pr}<input type="text" name="product" value="{prod}"></label>'
        '<label>{q}<input type="text" name="quantity" placeholder="e.g. 500 kg / month"></label>'
        '<label>{s}<input type="text" name="specification" placeholder="99.99% · oxide · D50 5 µm"></label>'
        '<label class="full">{m}<textarea name="message" rows="4"></textarea></label>'
        '</div><button type="submit" class="cta" id="{fid}-btn">{send}</button><p class="note">{note}</p></form></div>\n'
        '<script>(function(){{var f=document.getElementById("{fid}-form"),b=document.getElementById("{fid}-btn");if(!f)return;'
        'f.addEventListener("submit",async function(e){{e.preventDefault();b.textContent="{sending}";b.disabled=true;'
        'var j=Object.fromEntries(new FormData(f).entries());try{{var r=await fetch("https://api.web3forms.com/submit",{{method:"POST",headers:{{"Content-Type":"application/json","Accept":"application/json"}},body:JSON.stringify(j)}});'
        'var d=await r.json();if(d.success){{b.textContent="{ok}";b.style.background="#16a34a";b.style.color="#fff";b.style.borderColor="#16a34a";f.reset();}}'
        'else{{b.textContent="{fail}";b.disabled=false;}}}}catch(x){{b.textContent="{fail}";b.disabled=false;}}}});}})();</script>\n'
    ).format(ko="ko" if lang == "ko" else "", h=esc(t["rfq"]), fid=fid, key=esc(key), subj=esc(subject), c=esc(t["f_company"]), n=esc(t["f_name"]),
             e=esc(t["f_email"]), p=esc(t["f_phone"]), co=esc(t["f_country"]), pr=esc(t["f_product"]), prod=esc(product), q=esc(t["f_qty"]),
             s=esc(t["f_spec"]), m=esc(t["f_msg"]), send=esc(t["f_send"]), note=esc(t["f_note"]), sending=esc(t["f_sending"]), ok=esc(t["f_ok"]), fail=esc(t["f_fail"]))


SUPPLY_CSS = """
.kicker{font-size:11px;letter-spacing:2px;text-transform:uppercase;color:var(--orange);font-weight:700;margin-bottom:6px}
.rfqbox{background:var(--panel);border:1px solid var(--orange);border-radius:4px;padding:16px 18px 18px;margin-top:26px}
.rfqbox h2{margin-top:0;border:none}
.fgrid{display:grid;grid-template-columns:1fr 1fr;gap:10px 14px}.fgrid label{display:flex;flex-direction:column;font-size:12px;color:var(--muted);gap:4px}.fgrid .full{grid-column:1/-1}
.fgrid input,.fgrid textarea{background:var(--bg-2);border:1px solid var(--line-2);color:var(--text);padding:8px 10px;font:inherit;font-size:13.5px;border-radius:3px}
.fgrid input:focus,.fgrid textarea:focus{outline:none;border-color:var(--orange)}
@media(max-width:640px){.fgrid{grid-template-columns:1fr}}
button.cta{background:var(--orange);color:#000;border:1px solid var(--orange);cursor:pointer;font-family:inherit;font-size:14px;padding:10px 18px;margin-top:14px}
.faq dt{font-weight:700;color:var(--bright);margin-top:12px}.faq dd{margin:4px 0 0;color:var(--text)}
.comp li{margin:6px 0}
.ctabar{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin:14px 0 4px}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px;margin-top:10px}
.card{background:var(--panel);border:1px solid var(--line-2);border-radius:4px;padding:14px 16px}.card h3{margin:0 0 6px;font-size:15px}.card p{margin:0;font-size:12.5px;color:var(--muted)}.card a.more{display:inline-block;margin-top:8px;font-size:12.5px;font-weight:700}
.rfqcta{background:var(--bg-2);border:1px solid var(--orange);border-radius:4px;padding:12px 14px;margin:16px 0;font-size:13.5px}
"""


def _live_price_rows(lang, keys, by_ko):
    t = SUP[lang]
    rows = []
    for k in keys:
        it = by_ko.get(k)
        if not it:
            continue
        q = it.main
        rows.append('<tr><td><a href="{}">{}</a>{}</td><td class="num">{}</td><td class="num {}">{}</td><td><a href="{}">{}</a></td></tr>'.format(
            it.href(lang), esc(it.name(lang)), (' <span style="color:var(--dim);font-size:11px">' + esc(it.unit) + "</span>") if it.unit else "",
            fmt_num(q["last"]), pct_class(q["chg"]), fmt_pct(q["chg"]), it.href(lang), esc(t["see"])))
    return rows


def render_supply(lang, page, pages, by_ko, ref_date, n_items, key):
    import supply_content as SC
    t = SUP[lang]
    c = page[lang]
    slug = page["slug"]
    path = supply_href(lang, slug)
    alt = supply_href("ko" if lang == "en" else "en", slug)
    faq_ld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in c["faq"]]}
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": SITE + path, "url": SITE + path, "name": c["title"], "description": c["desc"], "inLanguage": lang,
         "dateModified": ref_date, "isPartOf": {"@id": SITE + "/#website"}, "publisher": {"@id": SITE + "/#org"}, "about": {"@type": "Product", "name": c["h1"]}},
        breadcrumb_ld(lang, [(t["crumb"], supply_href(lang)), (c["h1"], None)]), faq_ld, ORG_LD]}
    out = [head(lang, c["title"], c["desc"], path, alt, ld).replace("</style>", SUPPLY_CSS + "</style>"), "<body>\n", topbar(lang, alt), '<div class="wrap">\n',
           crumbs(lang, [(t["crumb"], supply_href(lang)), (c["h1"], None)])]
    out.append('<div class="kicker">{}</div><h1>{}</h1>\n'.format(esc(c["kicker"]), esc(c["h1"])))
    for para in c["intro"]:
        out.append('<p class="lead">{}</p>\n'.format(esc(para)))
    out.append('<div class="ctabar"><a class="cta" href="#rfq">{}</a><span class="note">{}</span></div>\n'.format(esc(t["rfq"]), esc(SC.COMPANY[lang])))

    # product table
    th = c["table_head"]
    out.append('<div class="tblwrap"><table><thead><tr>{}</tr></thead><tbody>'.format("".join("<th>{}</th>".format(esc(h)) for h in th)))
    live_keys = []
    for r in page["rows"]:
        name = r[0] if lang == "en" else r[1]
        forms = r[2] if lang == "en" else r[3]
        uses = r[5] if lang == "en" else r[6]
        out.append("<tr><td><b>{}</b></td><td>{}</td><td>{}</td><td>{}</td></tr>".format(esc(name), esc(forms), esc(r[4]), esc(uses)))
        live_keys.extend(r[7])
    out.append("</tbody></table></div>\n")

    prices = _live_price_rows(lang, live_keys, by_ko)
    if prices:
        out.append(h2(lang, t["live"]))
        out.append('<div class="tblwrap"><table><thead><tr>{}</tr></thead><tbody>{}</tbody></table></div>\n'.format(
            "".join('<th{}>{}</th>'.format(' class="num"' if i in (1, 2) else "", esc(h)) for i, h in enumerate(t["price_cols"])), "".join(prices)))
        out.append('<div class="note">{}</div>\n'.format(esc(T[lang]["asof"].format(date=ref_date))))

    out.append(h2(lang, t["faq"]))
    out.append('<dl class="faq">' + "".join("<dt>{}</dt><dd>{}</dd>".format(esc(q), esc(a)) for q, a in c["faq"]) + "</dl>\n")

    out.append(h2(lang, t["compliance"]))
    out.append('<ul class="comp">' + "".join("<li>{}</li>".format(esc(x)) for x in SC.COMPLIANCE[lang]) + "</ul>\n")
    out.append(h2(lang, t["about"]))
    out.append("<p>{}</p>\n".format(esc(SC.COMPANY[lang])))

    out.append(rfq_form(lang, key, "[chinanews.kr] RFQ: " + page["en"]["h1"], c["h1"]))

    out.append(h2(lang, t["related"]))
    out.append('<div class="peers">' + "".join('<a href="{}">{}</a>'.format(supply_href(lang, p["slug"]), esc(p[lang]["h1"])) for p in pages if p["slug"] != slug) + "</div>\n")
    out.append(footer(lang, n_items))
    return "".join(out)


def render_supply_index(lang, pages, n_items, key, ref_date):
    import supply_content as SC
    t = SUP[lang]
    path = supply_href(lang)
    alt = supply_href("ko" if lang == "en" else "en")
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": SITE + path, "url": SITE + path, "name": t["index_title"], "description": t["index_desc"], "inLanguage": lang, "dateModified": ref_date, "isPartOf": {"@id": SITE + "/#website"}},
        {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": p[lang]["h1"], "url": SITE + supply_href(lang, p["slug"])} for i, p in enumerate(pages)]},
        breadcrumb_ld(lang, [(t["crumb"], None)]), ORG_LD]}
    out = [head(lang, t["index_title"], t["index_desc"], path, alt, ld).replace("</style>", SUPPLY_CSS + "</style>"), "<body>\n", topbar(lang, alt), '<div class="wrap">\n', crumbs(lang, [(t["crumb"], None)])]
    out.append('<div class="kicker">{}</div><h1>{}</h1>\n'.format(esc(t["nav"]), esc(t["index_h1"])))
    out.append('<p class="lead">{}</p>\n'.format(esc(t["index_intro"])))
    out.append('<div class="cards">')
    for p in pages:
        out.append('<div class="card"><h3><a href="{}">{}</a></h3><p>{}</p><a class="more" href="{}">{} →</a></div>'.format(
            supply_href(lang, p["slug"]), esc(p[lang]["h1"]), esc(p[lang]["desc"]), supply_href(lang, p["slug"]), esc(t["rfq"])))
    out.append("</div>\n")
    out.append(h2(lang, t["compliance"]))
    out.append('<ul class="comp">' + "".join("<li>{}</li>".format(esc(x)) for x in SC.COMPLIANCE[lang]) + "</ul>\n")
    out.append(h2(lang, t["about"]))
    out.append("<p>{}</p>\n".format(esc(SC.COMPANY[lang])))
    out.append(rfq_form(lang, key, "[chinanews.kr] RFQ: general", ""))
    out.append(footer(lang, n_items))
    return "".join(out)


# ----------------------------------------------------------------------------
# about page (entity page for search + answer engines)
# ----------------------------------------------------------------------------
ABOUT = {
    "en": {
        "title": "About BRIDGE GROUP — ABridge · Ecobridge · DealBridge | CHINANEWS",
        "desc": "BRIDGE GROUP is a Korean trading group in Gwangju supplying rare earths, gallium, germanium, terbium, tungsten, hafnium, yttrium, 5N/6N copper, semiconductor materials and Chinese semiconductors direct from licensed Chinese producers, and operating the chinanews.kr China markets terminal.",
        "h1": "About BRIDGE GROUP",
        "paras": [
            "BRIDGE GROUP is the umbrella for three Korean trading companies based in Gwangju, South Korea: ABridge Co., Ltd. (strategic materials, semiconductor equipment and agricultural commodities), Ecobridge (petrochemicals, PE resins, PBAT/PLA biodegradable materials and industrial films) and DealBridge (semiconductor and critical-mineral brokerage). The group operates chinanews.kr, a bilingual China markets terminal.",
            "ABridge holds a state-trading rice import quota under Korea's Korea Agro-Fisheries & Food Trade Corporation (aT) and, in June 2026, became the first Korean company to export SiC focus-ring CVD furnace systems directly to a Chinese semiconductor equipment manufacturer (Heilongjiang Zhilian Semiconductor).",
            "Our supply business buys from refineries, fabs and authorised distributors in China and sells to manufacturers, research institutes and traders in Korea and abroad. Every enquiry is classified under Korea's strategic-items rules and screened against U.S., UN and EU sanctions lists before quotation; materials ship with producer certificates and samples are available for independent assay.",
        ],
        "facts_h": "Key facts",
        "facts": [("Legal entities", "ABridge Co., Ltd. (㈜에이브릿지) · Ecobridge (㈜에코브릿지) · DealBridge"), ("Headquarters", "21, Bunam-gil 26beon-gil, Buk-gu, Gwangju, South Korea"), ("Telephone", "+82-1661-0400"), ("Sales enquiries", "koreagwangju@gmail.com · RFQ forms on every supply page"), ("Languages", "Korean, English, Chinese"), ("Websites", "chinanews.kr · abridge.co.kr · ecobridge.biz · dealbridge.asia")],
        "lines_h": "What we supply",
        "press_h": "Press",
        "press": "ABridge secures 4-line SiC-CVD furnace system supply contract to China (15 June 2026)",
    },
    "ko": {
        "title": "BRIDGE GROUP 소개 — 에이브릿지 · 에코브릿지 · 딜브릿지 | CHINANEWS",
        "desc": "BRIDGE GROUP은 광주광역시의 무역그룹으로 허가받은 중국 생산자로부터 희토류·갈륨·게르마늄·테르븀·텅스텐·하프늄·이트륨·5N/6N 구리·반도체 소재·중국산 반도체를 직접 공급하고, 중국 시장 터미널 chinanews.kr를 운영합니다.",
        "h1": "BRIDGE GROUP 소개",
        "paras": [
            "BRIDGE GROUP은 광주광역시에 본사를 둔 세 무역법인의 통합 브랜드입니다: ㈜에이브릿지(전략소재·반도체 장비·농산물), ㈜에코브릿지(석유화학·PE 수지·PBAT/PLA 생분해 소재·산업용 필름), 딜브릿지(반도체·핵심광물 중개). 그룹은 한·영 중국 시장 터미널 chinanews.kr를 운영합니다.",
            "㈜에이브릿지는 한국농수산식품유통공사(aT) 쌀 국영무역 수입 자격을 보유하며, 2026년 6월 한국 기업 최초로 SiC 포커스링 CVD 장비 시스템을 중국 반도체 장비사(흑룡강성 지련반도체)에 직접 수출했습니다.",
            "공급 사업은 중국의 정련소·팹·공인 대리점에서 매입해 국내외 제조사·연구기관·무역상에 판매합니다. 모든 문의는 견적 전에 전략물자 규정으로 판정하고 미국·UN·EU 제재 목록을 조회하며, 소재는 생산자 성적서와 함께 출하하고 제3자 분석용 샘플을 제공합니다.",
        ],
        "facts_h": "기본 정보",
        "facts": [("법인", "㈜에이브릿지 · ㈜에코브릿지 · 딜브릿지"), ("본사", "광주광역시 북구 부남길26번길 21"), ("전화", "1661-0400"), ("견적 문의", "koreagwangju@gmail.com · 각 공급 페이지의 견적 요청 폼"), ("언어", "한국어, 영어, 중국어"), ("웹사이트", "chinanews.kr · abridge.co.kr · ecobridge.biz · dealbridge.asia")],
        "lines_h": "취급 품목",
        "press_h": "보도자료",
        "press": "㈜에이브릿지, 中 지련반도체와 SiC-CVD 장비 1·2차 공급계약 체결 (2026년 6월 15일)",
    },
}


def render_about(lang, pages, n_items):
    t = ABOUT[lang]
    path = "/ko/about.html" if lang == "ko" else "/about.html"
    alt = "/about.html" if lang == "ko" else "/ko/about.html"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "AboutPage", "@id": SITE + path, "url": SITE + path, "name": t["title"], "description": t["desc"], "inLanguage": lang, "isPartOf": {"@id": SITE + "/#website"}, "mainEntity": {"@id": SITE + "/#org"}},
        breadcrumb_ld(lang, [(t["h1"], None)]), ORG_LD]}
    out = [head(lang, t["title"], t["desc"], path, alt, ld).replace("</style>", SUPPLY_CSS + "</style>"), "<body>\n", topbar(lang, alt), '<div class="wrap">\n', crumbs(lang, [(t["h1"], None)])]
    out.append("<h1>{}</h1>\n".format(esc(t["h1"])))
    for para in t["paras"]:
        out.append('<p class="lead">{}</p>\n'.format(esc(para)))
    out.append(h2(lang, t["facts_h"]))
    out.append('<div class="tblwrap"><table><tbody>' + "".join("<tr><td style=\"color:var(--muted);width:30%\">{}</td><td>{}</td></tr>".format(esc(k), esc(v)) for k, v in t["facts"]) + "</tbody></table></div>\n")
    out.append(h2(lang, t["lines_h"]))
    out.append('<div class="peers">' + "".join('<a href="{}">{}</a>'.format(supply_href(lang, p["slug"]), esc(p[lang]["h1"])) for p in pages) + "</div>\n")
    out.append(h2(lang, t["press_h"]))
    out.append('<p><a href="/press/abridge-sic-cvd-20260615.html">{}</a></p>\n'.format(esc(t["press"])))
    out.append(rfq_form(lang, _web3forms_key(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "[chinanews.kr] RFQ: about page", ""))
    out.append(footer(lang, n_items))
    return "".join(out)


def render_feed(root, dates, cm):
    """RSS 2.0 of daily briefs (EN + KO items) for news/answer-engine crawlers."""
    import email.utils
    items = []
    for d in dates[:30]:
        for lang, pfx, title in (("en", "", "China Commodities Daily Brief — "), ("ko", "/ko", "중국 원자재 일일 시황 — ")):
            url = SITE + pfx + "/daily/" + d + ".html"
            pub = email.utils.format_datetime(dt.datetime.strptime(d, "%Y-%m-%d").replace(hour=21, tzinfo=KST))
            items.append("<item><title>{t}{d}</title><link>{u}</link><guid isPermaLink=\"true\">{u}</guid><pubDate>{p}</pubDate><description>{desc}</description></item>".format(
                t=esc(title), d=d, u=url, p=pub, desc=esc(T[lang]["daily_index_desc"])))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel>'
            '<title>CHINANEWS — China Commodities Daily Brief</title><link>{s}/daily/</link>'
            '<description>Daily China spot-market brief: advance/decline counts, top movers, sector breakdown, indices, FX. By BRIDGE GROUP.</description>'
            '<language>en</language><atom:link href="{s}/feed.xml" rel="self" type="application/rss+xml"/>{items}</channel></rss>\n').format(s=SITE, items="".join(items))


# ----------------------------------------------------------------------------
# sitemap
# ----------------------------------------------------------------------------
def render_sitemap(entries):
    out = ['<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n']
    for path, lastmod, freq, prio, alt in entries:
        out.append("  <url>\n    <loc>{}{}</loc>\n".format(SITE, esc(path)))
        if lastmod:
            out.append("    <lastmod>{}</lastmod>\n".format(lastmod))
        out.append("    <changefreq>{}</changefreq>\n    <priority>{}</priority>\n".format(freq, prio))
        if alt:
            en, ko = alt
            out.append('    <xhtml:link rel="alternate" hreflang="en" href="{}{}"/>\n'.format(SITE, esc(en)))
            out.append('    <xhtml:link rel="alternate" hreflang="ko" href="{}{}"/>\n'.format(SITE, esc(ko)))
            out.append('    <xhtml:link rel="alternate" hreflang="x-default" href="{}{}"/>\n'.format(SITE, esc(en)))
        out.append("  </url>\n")
    out.append("</urlset>\n")
    return "".join(out)


# ----------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    data = os.path.join(root, "data")

    cm = load(os.path.join(data, "commodities.json"))
    if not cm or not cm.get("all_items"):
        print("build_pages: commodities.json missing or empty — nothing built", file=sys.stderr)
        return 1
    i18n = load(os.path.join(data, "commodity_i18n.json"), {})
    chart_map = load(os.path.join(data, "chart_map.json"), {})
    stocks = load(os.path.join(data, "stocks_latest.json"), {})
    fx = load(os.path.join(data, "fx_latest.json"), {})
    macro = load(os.path.join(data, "macro_latest.json"), {})
    ref_date = cm.get("ref_date") or dt.datetime.now(KST).strftime("%Y-%m-%d")
    built_at = dt.datetime.now(KST).strftime("%Y-%m-%dT%H:%M:%S+09:00")
    today = dt.datetime.now(KST).strftime("%Y-%m-%d")

    items = build_items(cm, i18n, chart_map, os.path.join(data, "commodity_charts"))
    by_sector = {}
    for it in items:
        by_sector.setdefault(it.sector_ko, []).append(it)
    n = len(items)

    written = 0
    entries = []

    # commodity pages
    for it in items:
        for lang in ("en", "ko"):
            path = os.path.join(root, it.href(lang).lstrip("/"))
            if write_if_changed(path, render_commodity(lang, it, by_sector, ref_date, n)):
                written += 1
        entries.append((it.href("en"), ref_date, "daily", "0.7", (it.href("en"), it.href("ko"))))
        entries.append((it.href("ko"), ref_date, "daily", "0.7", (it.href("en"), it.href("ko"))))

    # commodity index
    for lang in ("en", "ko"):
        p = "/ko" if lang == "ko" else ""
        if write_if_changed(os.path.join(root, p.lstrip("/"), "commodities", "index.html"), render_index(lang, items, by_sector, ref_date)):
            written += 1
        entries.append((p + "/commodities/", ref_date, "daily", "0.8", ("/commodities/", "/ko/commodities/")))

    # daily brief for ref_date (+ archive)
    for lang in ("en", "ko"):
        p = "/ko" if lang == "ko" else ""
        if write_if_changed(os.path.join(root, p.lstrip("/"), "daily", ref_date + ".html"), render_daily(lang, items, by_sector, cm, stocks, fx, macro, ref_date, built_at)):
            written += 1
    dates = set()
    for lang_dir in ("daily", os.path.join("ko", "daily")):
        d = os.path.join(root, lang_dir)
        if os.path.isdir(d):
            for fn in os.listdir(d):
                m = re.match(r"^(\d{4}-\d{2}-\d{2})\.html$", fn)
                if m:
                    dates.add(m.group(1))
    dates = sorted(dates, reverse=True)
    for d in dates:
        entries.append(("/daily/" + d + ".html", d, "monthly", "0.6", ("/daily/" + d + ".html", "/ko/daily/" + d + ".html")))
        entries.append(("/ko/daily/" + d + ".html", d, "monthly", "0.6", ("/daily/" + d + ".html", "/ko/daily/" + d + ".html")))
    for lang in ("en", "ko"):
        p = "/ko" if lang == "ko" else ""
        if write_if_changed(os.path.join(root, p.lstrip("/"), "daily", "index.html"), render_daily_index(lang, dates, n)):
            written += 1
        entries.append((p + "/daily/", dates[0] if dates else today, "daily", "0.6", ("/daily/", "/ko/daily/")))

    # buyer-facing supply / RFQ pages
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import supply_content as SC
        order = ["rare-earths", "yttrium", "gallium", "terbium", "tungsten", "germanium", "hafnium", "high-purity-copper", "semiconductor-materials", "semiconductors"]
        pages = sorted(SC.PAGES, key=lambda p: order.index(p["slug"]) if p["slug"] in order else 99)
        by_ko = {it.ko: it for it in items}
        key = _web3forms_key(root)
        for lang in ("en", "ko"):
            for p in pages:
                if write_if_changed(os.path.join(root, supply_href(lang, p["slug"]).lstrip("/")), render_supply(lang, p, pages, by_ko, ref_date, n, key)):
                    written += 1
            if write_if_changed(os.path.join(root, supply_href(lang).lstrip("/"), "index.html"), render_supply_index(lang, pages, n, key, ref_date)):
                written += 1
        sup_entries = [("/supply/", today, "weekly", "0.9", ("/supply/", "/ko/supply/")), ("/ko/supply/", today, "weekly", "0.9", ("/supply/", "/ko/supply/"))]
        for p in pages:
            en_p, ko_p = supply_href("en", p["slug"]), supply_href("ko", p["slug"])
            sup_entries.append((en_p, ref_date, "weekly", "0.9", (en_p, ko_p)))
            sup_entries.append((ko_p, ref_date, "weekly", "0.9", (en_p, ko_p)))
        entries = sup_entries + entries
    except Exception as e:
        print("build_pages: supply/landing pages skipped:", e, file=sys.stderr)

    # Korean terminal copy (terminal/index.html -> ko/terminal/index.html)
    try:
        with open(os.path.join(root, "index.html"), "r", encoding="utf-8") as f:
            src = f.read()
        if write_if_changed(os.path.join(root, "ko", "index.html"), render_ko_home(src)):
            written += 1
    except Exception as e:
        print("build_pages: ko/index.html skipped:", e, file=sys.stderr)

    # about pages + RSS feed
    try:
        for lang in ("en", "ko"):
            if write_if_changed(os.path.join(root, "ko" if lang == "ko" else "", "about.html"), render_about(lang, pages, n)):
                written += 1
        entries.insert(0, ("/about.html", today, "monthly", "0.8", ("/about.html", "/ko/about.html")))
        entries.insert(1, ("/ko/about.html", today, "monthly", "0.8", ("/about.html", "/ko/about.html")))
        if write_if_changed(os.path.join(root, "feed.xml"), render_feed(root, dates, cm)):
            written += 1
    except Exception as e:
        print("build_pages: about/feed skipped:", e, file=sys.stderr)

    # static pages
    static = [("/", today, "daily", "1.0", ("/", "/ko/")), ("/ko/", today, "daily", "1.0", ("/", "/ko/")),
              ("/press/abridge-sic-cvd-20260615.html", "2026-06-15", "monthly", "0.7", None),
              ]
    entries = static + entries
    if write_if_changed(os.path.join(root, "sitemap.xml"), render_sitemap(entries)):
        written += 1

    print("build_pages: {} commodities, {} daily briefs, {} sitemap urls, {} files written (ref_date {})".format(n, len(dates), len(entries), written, ref_date))
    return 0


if __name__ == "__main__":
    sys.exit(main())
