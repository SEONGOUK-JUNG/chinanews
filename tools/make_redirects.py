# -*- coding: utf-8 -*-
"""버려진 주소를 제자리로 넘겨 준다.

정적 사이트라 서버에서 301 을 줄 수 없으므로, 같은 자리에 넘김 페이지를 둔다.
  - <link rel="canonical"> 로 "진짜 주소는 이쪽" 이라고 알린다(구글이 중복을 합쳐 준다)
  - <meta http-equiv="refresh"> 로 사람은 곧바로 옮겨 간다
넘김 페이지는 사이트맵에 넣지 않는다(빌더가 목록에서 만들기 때문에 저절로 빠진다).

실행: python tools/make_redirects.py
"""
import io, json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://chinanews.kr"

PAGE = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<link rel="canonical" href="{target_abs}">
<meta name="robots" content="noindex, follow">
<meta http-equiv="refresh" content="0; url={target}">
<style>body{{margin:0;padding:48px 24px;background:#0f1115;color:#c9d1d9;font:15px/1.7 system-ui,sans-serif;text-align:center}}
a{{color:#58a6ff}}</style>
</head>
<body>
<p>{moved}</p>
<p><a href="{target}">{go}</a></p>
<script>location.replace({target_js});</script>
</body>
</html>
"""

TEXT = {
    "en": {"title": "Moved — CHINANEWS", "moved": "This page has moved.", "go": "Continue"},
    "ko": {"title": "주소가 바뀌었습니다 — CHINANEWS", "moved": "이 페이지는 자리를 옮겼습니다.", "go": "이어서 보기"},
}


def write(path, body):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    old = None
    if os.path.exists(path):
        with io.open(path, encoding="utf-8") as f:
            old = f.read()
    if old == body:
        return False
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(body)
    return True


def redirect(rel_path, target, lang):
    t = TEXT[lang]
    body = PAGE.format(
        lang=lang, title=t["title"], moved=t["moved"], go=t["go"],
        target=target, target_abs=SITE + target, target_js=json.dumps(target),
    )
    return write(os.path.join(ROOT, rel_path.lstrip("/")), body)


def main():
    # 1) 사이트맵에 없는 품목 파일 = 예전 꼬리표 주소 → 꼬리표를 뗀 자리로 넘긴다
    with io.open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8") as f:
        sm = f.read()
    listed = set(re.findall(r"<loc>[^<]*?(/(?:ko/)?commodity/[^<]+)</loc>", sm))
    made = 0
    for lang, prefix in (("en", ""), ("ko", "/ko")):
        folder = os.path.join(ROOT, prefix.lstrip("/"), "commodity")
        if not os.path.isdir(folder):
            continue
        for fn in sorted(os.listdir(folder)):
            if not fn.endswith(".html"):
                continue
            rel = "{}/commodity/{}".format(prefix, fn)
            if rel in listed:
                continue
            base = re.sub(r"-[0-9a-f]{6}\.html$", ".html", fn)
            target = "{}/commodity/{}".format(prefix, base)
            if base == fn or target not in listed:
                print("  넘길 곳을 못 찾음:", rel)
                continue
            if redirect(rel, target, lang):
                made += 1
                print("  {} → {}".format(rel, target))

    # 2) 지워진 옛 한국어 첫 화면 → 지금의 한국어 첫 화면
    if redirect("/index-ko-legacy.html", "/ko/", "ko"):
        made += 1
        print("  /index-ko-legacy.html → /ko/")

    print("넘김 페이지 {}개".format(made))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
