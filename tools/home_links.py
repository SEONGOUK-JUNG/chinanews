# -*- coding: utf-8 -*-
"""첫 화면에서 품목 페이지로 가는 길을 만든다.

구글이 품목 페이지 131개를 "발견했지만 가 보지 않은" 까닭은 그 페이지들이 목록 한 곳에서만
이어져 있었기 때문이다. 첫 화면에 분야 아홉 개와 주요 품목 서른 개를 걸어 두면
검색 로봇이 첫 화면에서 두 걸음 안에 모든 품목에 닿는다.

실행: python tools/home_links.py   (build_pages.py 를 돌린 뒤)
"""
import io, json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK_A = "<!-- home-commodity-links:start -->"
MARK_B = "<!-- home-commodity-links:end -->"
TOP_N = 30

CSS = (
    "<style>"
    ".hcl{margin:26px 0 8px;padding:18px 20px;border:1px solid var(--line,#232a33);border-radius:12px;background:var(--panel,#131820)}"
    ".hcl h2{margin:0 0 4px;font-size:15px;letter-spacing:.2px}"
    ".hcl p{margin:0 0 12px;font-size:12px;color:var(--dim,#7d8794)}"
    ".hcl .row{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:12px}"
    ".hcl .row a{font-size:12px;padding:5px 10px;border:1px solid var(--line,#232a33);border-radius:999px;"
    "color:var(--fg,#c9d1d9);text-decoration:none}"
    ".hcl .row a:hover{border-color:#58a6ff;color:#58a6ff}"
    ".hcl .row.sect a{background:rgba(88,166,255,.08);border-color:rgba(88,166,255,.35)}"
    "</style>"
)


def sector_list():
    d = os.path.join(ROOT, "commodities")
    out = []
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".html") or fn == "index.html":
            continue
        path = os.path.join(d, fn)
        with io.open(path, encoding="utf-8") as f:
            head = f.read(4000)
        m = re.search(r"<h1>([^<]+)</h1>", head)
        name = m.group(1).strip() if m else fn[:-5]
        n = 0
        with io.open(path, encoding="utf-8") as f:
            n = f.read().count('<td><a href="/commodity/')
        out.append((fn[:-5], name, n))
    out.sort(key=lambda x: -x[2])
    return out


def top_commodities(lang_prefix=""):
    """사이트맵에 오른 품목 가운데 이름이 짧고 널리 찾는 것부터 고른다(차트가 있는 것 우선)."""
    idx = os.path.join(ROOT, lang_prefix.lstrip("/"), "commodities", "index.html")
    with io.open(idx, encoding="utf-8") as f:
        html = f.read()
    pairs = re.findall(r'<td><a href="(' + (lang_prefix or "") + r'/commodity/[^"]+)">([^<]+)</a>', html)
    seen, out = set(), []
    for href, name in pairs:
        if href in seen:
            continue
        seen.add(href)
        out.append((href, name))
    return out


def block(lang_prefix, sectors, picks):
    if lang_prefix:
        h2 = "원자재 바로 가기"
        lead = "분야를 고르거나 품목 이름을 눌러 오늘 가격과 흐름을 보세요."
        allname = "전체 {}개 보기"
    else:
        h2 = "Browse commodities"
        lead = "Pick a sector, or open a commodity for today's price and its chart."
        allname = "All {} commodities"
    total = sum(n for _, _, n in sectors)
    news_ko = ('<p style="margin:-6px 0 12px"><a href="/press/yttrium-oxide-supply-20260917.html" '
               'style="color:#E8C078;text-decoration:none">새 소식 · 산화이트륨 5N(Y₂O₃ 99.999%) 국내 공급 개시 →</a></p>')
    news_en = ('<p style="margin:-6px 0 12px"><a href="/press/yttrium-oxide-supply-20260917.html" '
               'style="color:#E8C078;text-decoration:none">New · Yttrium oxide 5N (Y₂O₃ 99.999%) now supplied to Korea →</a></p>')
    out = [MARK_A, CSS, '<section class="hcl">',
           "<h2>{}</h2>".format(h2), "<p>{}</p>".format(lead),
           news_ko if lang_prefix else news_en,
           '<div class="row sect">']
    for slug, name, n in sectors:
        out.append('<a href="{}/commodities/{}.html">{} <span style="opacity:.6">{}</span></a>'.format(
            lang_prefix, slug, name, n))
    out.append('<a href="{}/commodities/">{}</a>'.format(lang_prefix, allname.format(total)))
    out.append("</div>")
    out.append('<div class="row">')
    for href, name in picks:
        out.append('<a href="{}">{}</a>'.format(href, name))
    out.append("</div></section>")
    out.append(MARK_B)
    return "".join(out)


def put(path, body):
    with io.open(path, encoding="utf-8") as f:
        s = f.read()
    if MARK_A in s:
        s = re.sub(re.escape(MARK_A) + r"[\s\S]*?" + re.escape(MARK_B), body, s, count=1)
    else:
        i = s.rfind("<footer")
        if i < 0:
            print("  꼬리말을 못 찾음:", path)
            return False
        s = s[:i] + body + s[i:]
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(s)
    return True


def main():
    sectors = sector_list()
    print("분야 {}개".format(len(sectors)))
    for prefix, page in (("", "index.html"), ("/ko", os.path.join("ko", "index.html"))):
        picks = top_commodities(prefix)[:TOP_N]
        body = block(prefix, sectors, picks)
        if put(os.path.join(ROOT, page), body):
            print("  {} · 분야 {}개 + 품목 {}개 링크".format(page, len(sectors), len(picks)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
