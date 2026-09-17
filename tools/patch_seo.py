# -*- coding: utf-8 -*-
"""build_pages.py 에 검색 색인 문제 두 가지를 고쳐 넣는다. 한 번만 실행한다.

 1) 주소 고정 — 예전에는 이름이 겹치면 md5(한글이름) 을 꼬리표로 붙였다.
    한글 이름이 조금만 달라져도 꼬리표가 바뀌어 같은 품목이 주소 여러 개로 갈라졌고,
    구글은 그것을 중복으로 보고 색인에서 걸렀다. 이제 data/slug_map.json 에 적어 두고 계속 쓴다.
 3) 분야별 목록 — 405개를 한 페이지에 늘어놓으면 검색 로봇이 끝까지 가지 않는다.
    분야마다 목록 페이지를 따로 만들어 첫 화면 → 분야 → 품목 세 걸음 안에 닿게 한다.
"""
import io, os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "tools", "build_pages.py")

NL = chr(10)
BS_N = chr(92) + "n"          # 생성될 소스 안에 들어갈 \n 두 글자

src = io.open(P, encoding="utf-8").read()
if "slug_map.json" in src:
    print("이미 반영되어 있습니다.")
    raise SystemExit(0)

# ---------------------------------------------------------------- 1) 주소 고정
old_slug = NL.join([
    "    # slugs (stable, unique)",
    "    used = {}",
    "    for ko in order:",
    "        it = items[ko]",
    "        if it.chart_id:",
    "            base = slugify(it.chart_id)",
    "        elif it.en:",
    "            base = slugify(it.en)",
    "        else:",
    '            base = ""',
    "        if not base:",
    '            base = "k-" + hashlib.md5(ko.encode("utf-8")).hexdigest()[:8]',
    "        slug = base",
    "        if slug in used:",
    '            slug = base + "-" + hashlib.md5(ko.encode("utf-8")).hexdigest()[:6]',
    "        used[slug] = ko",
    "        it.slug = slug",
])
assert src.count(old_slug) == 1, "주소 짓는 부분을 못 찾음"

new_slug = NL.join([
    "    # slugs — 한 번 정한 주소는 영원히 그대로 둔다(data/slug_map.json).",
    "    data_dir = os.path.dirname(charts_dir)",
    '    slug_map_path = os.path.join(data_dir, "slug_map.json")',
    "    slug_map = load(slug_map_path, {}) or {}",
    "    taken = {}",
    "    for _k, _v in slug_map.items():",
    "        taken[_v] = _k",
    "    added = 0",
    "    for ko in order:",
    "        it = items[ko]",
    "        # 바뀌지 않는 이름표: 차트 아이디 > 영문 이름 > 한글 이름",
    '        key = (it.chart_id or "").strip() or (it.en or "").strip() or ko',
    "        if key in slug_map:",
    "            it.slug = slug_map[key]",
    "            continue",
    "        if it.chart_id:",
    "            base = slugify(it.chart_id)",
    "        elif it.en:",
    "            base = slugify(it.en)",
    "        else:",
    '            base = ""',
    "        if not base:",
    '            base = "k-" + hashlib.md5(key.encode("utf-8")).hexdigest()[:8]',
    "        slug, seq = base, 2",
    "        while slug in taken and taken[slug] != key:",
    '            slug = "{}-{}".format(base, seq)',
    "            seq += 1",
    "        slug_map[key] = slug",
    "        taken[slug] = key",
    "        it.slug = slug",
    "        added += 1",
    "    if added:",
    "        write_if_changed(slug_map_path, json.dumps(slug_map, ensure_ascii=False, indent=1, sort_keys=True) + chr(10))",
    '        print("build_pages: 새 주소 {}개를 slug_map.json 에 적었습니다".format(added))',
])
src = src.replace(old_slug, new_slug, 1)

# ------------------------------------------------------- 3) 분야별 목록 페이지
anchor = NL.join([
    "# ----------------------------------------------------------------------------",
    "# daily brief",
    "# ----------------------------------------------------------------------------",
])
assert src.count(anchor) == 1, "일일 브리핑 표시를 못 찾음"

renderer = NL.join([
    "# ----------------------------------------------------------------------------",
    "# commodities by sector  (/commodities/<sector>.html)",
    "# ----------------------------------------------------------------------------",
    "def sector_slug(ex):",
    '    return slugify(ex.sector_en or "other")',
    "",
    "",
    "def sector_path(lang, sslug):",
    '    return ("/ko" if lang == "ko" else "") + "/commodities/" + sslug + ".html"',
    "",
    "",
    "def render_sector(lang, sslug, lst, items_by_sector, ref_date, total):",
    "    t = T[lang]",
    "    ex = lst[0]",
    "    sector = ex.sector(lang)",
    "    path = sector_path(lang, sslug)",
    '    alt = sector_path("en" if lang == "ko" else "ko", sslug)',
    '    az_path = ("/ko" if lang == "ko" else "") + "/commodities/"',
    '    if lang == "ko":',
    '        title = "{} 원자재 {}개 — 오늘 가격과 등락 | CHINANEWS".format(sector, len(lst))',
    '        desc = "중국 {} 분야 {}개 품목의 현물 가격과 전일 대비 등락. {} 기준.".format(sector, len(lst), ref_date)',
    '        intro = "{} 분야에서 매일 확인하는 {}개 품목입니다. 이름을 누르면 가격 흐름과 차트를 볼 수 있습니다.".format(sector, len(lst))',
    "    else:",
    '        title = "{} — {} China Commodity Prices Today | CHINANEWS".format(sector, len(lst))',
    '        desc = "China {} sector: spot prices and daily change for {} commodities, as of {}.".format(sector, len(lst), ref_date)',
    '        intro = "The {} commodities we track daily in the {} sector. Open any name for its price history and chart.".format(len(lst), sector)',
    '    ld = {"@context": "https://schema.org", "@graph": [',
    '        {"@type": "CollectionPage", "@id": SITE + path, "url": SITE + path, "name": title,',
    '         "description": desc, "inLanguage": lang, "dateModified": ref_date,',
    '         "isPartOf": {"@id": SITE + "/#website"}},',
    '        breadcrumb_ld(lang, [(t["az"], az_path), (sector, None)]), ORG_LD]}',
    '    out = [head(lang, title, desc, path, alt, ld), "<body>" + chr(10), topbar(lang, alt),',
    "           '<div class=\"wrap\">' + chr(10),",
    '           crumbs(lang, [(t["az"], az_path), (sector, None)])]',
    '    out.append("<h1>{}</h1>".format(esc(sector)) + chr(10))',
    "    out.append('<p class=\"lead\">{}</p>'.format(esc(intro)) + chr(10))",
    "    out.append('<div class=\"peers\">')",
    "    for s2 in sorted(items_by_sector.keys(), key=lambda s: -len(items_by_sector[s])):",
    "        e2 = items_by_sector[s2][0]",
    "        s2slug = sector_slug(e2)",
    "        if s2slug == sslug:",
    "            continue",
    "        out.append('<a href=\"{}\">{} ({})</a>'.format(sector_path(lang, s2slug), esc(e2.sector(lang)), len(items_by_sector[s2])))",
    '    out.append("</div>" + chr(10))',
    "    out.append('<div class=\"tblwrap\"><table><thead><tr><th>{}</th><th class=\"num\">{}</th><th class=\"num\">{}</th><th class=\"num\">{}</th></tr></thead><tbody>'.format(",
    '        esc(t["name"]), esc(t["prev"]), esc(t["last"]), esc(t["chg"])))',
    "    for it in sorted(lst, key=lambda x: x.name(lang).lower()):",
    "        q = it.main",
    "        unit = (' <span style=\"color:var(--dim);font-size:11px\">' + esc(it.unit) + '</span>') if it.unit else ''",
    "        out.append('<tr><td><a href=\"{}\">{}</a>{}</td><td class=\"num\">{}</td><td class=\"num\">{}</td><td class=\"num {}\">{}</td></tr>'.format(",
    '            it.href(lang), esc(it.name(lang)), unit, fmt_num(q["prev"]), fmt_num(q["last"]), pct_class(q["chg"]), fmt_pct(q["chg"])))',
    '    out.append("</tbody></table></div>" + chr(10))',
    "    out.append(footer(lang, total))",
    '    return "".join(out)',
    "",
    "",
])
src = src.replace(anchor, renderer + anchor, 1)

# 목록 페이지의 분야 링크를 분야 페이지로 (닻 대신 실제 페이지)
old_jump = "        out.append('<a href=\"#s-{}\">{} ({})</a>'.format(slugify(ex.sector_en or \"other\"), esc(ex.sector(lang)), len(items_by_sector[s])))"
assert src.count(old_jump) == 1, "분야 건너뛰기 줄을 못 찾음"
new_jump = "        out.append('<a href=\"{}\">{} ({})</a>'.format(sector_path(lang, slugify(ex.sector_en or \"other\")), esc(ex.sector(lang)), len(items_by_sector[s])))"
src = src.replace(old_jump, new_jump, 1)

# 빌드 단계에 분야 페이지 추가
old_build = NL.join([
    "    # commodity index",
    '    for lang in ("en", "ko"):',
    '        p = "/ko" if lang == "ko" else ""',
    '        if write_if_changed(os.path.join(root, p.lstrip("/"), "commodities", "index.html"), render_index(lang, items, by_sector, ref_date)):',
    "            written += 1",
    '        entries.append((p + "/commodities/", ref_date, "daily", "0.8", ("/commodities/", "/ko/commodities/")))',
])
assert src.count(old_build) == 1, "목록 빌드 단계를 못 찾음"
new_build = old_build + NL + NL.join([
    "",
    "    # commodity index by sector",
    "    for _s, _lst in by_sector.items():",
    "        _slug = sector_slug(_lst[0])",
    '        for lang in ("en", "ko"):',
    '            _path = os.path.join(root, sector_path(lang, _slug).lstrip("/"))',
    "            if write_if_changed(_path, render_sector(lang, _slug, _lst, by_sector, ref_date, n)):",
    "                written += 1",
    '        entries.append((sector_path("en", _slug), ref_date, "daily", "0.75", (sector_path("en", _slug), sector_path("ko", _slug))))',
    '        entries.append((sector_path("ko", _slug), ref_date, "daily", "0.75", (sector_path("en", _slug), sector_path("ko", _slug))))',
])
src = src.replace(old_build, new_build, 1)

io.open(P, "w", encoding="utf-8").write(src)
print("build_pages.py 에 1) 주소 고정, 3) 분야별 목록 페이지를 넣었습니다.")
