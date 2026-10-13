# -*- coding: utf-8 -*-
"""품목 페이지 색인 정책 (2026-10-14 도입).

배경: 2026-09-24~10-08 구글 9월 스팸 업데이트 뒤(9/27) 노출이 2주 2,440 → 75 로 무너짐.
틀에 숫자만 바뀌는 품목 페이지 약 800개가 '대량 자동 생성 콘텐츠'로 읽혔을 가능성이 커서,
구글에 보여 줄 품목 페이지를 질 좋은 소수로 줄인다. 페이지 자체는 그대로 두고(방문자·내부 링크 유지)
나머지는 <meta name="robots" content="noindex,follow"> + 사이트맵 제외.

색인 유지 조건 (하나라도 해당하면 유지):
  1) KEEP_SLUGS — 서치 콘솔 2026-07-11~10-10 노출 합계(한·영) 20회 이상 품목
  2) 차트 이력이 MIN_CANDLES 개 이상 쌓인 품목 (chart_map 품목)
  3) 공급(견적) 페이지와 연결된 전략소재 (supply_content.COMMODITY_TO_SUPPLY)
"""

MIN_CANDLES = 10

KEEP_SLUGS = {
    "lithium-carbonate", "propylene-oxide", "hrc", "polysilicon", "pp", "benzene", "coal", "refined-naphthalene",
    "ethylene-glycol", "pta", "polybutadiene-rubber", "silicone-dmc", "lldpe", "toluene", "yellow-phosphorus", "bromine",
    "polyester-yarn", "sulfur", "praseodymium-neodymium-alloy", "nitrile-rubber", "steel-billet", "butadiene", "wire-rod",
    "iron-ore", "methanol", "mdi", "fluorite", "diethylene-glycol", "caustic-soda", "dioctyl-phthalate", "dysprosium-metal",
    "phenol", "acrylic-acid", "silicon-metal", "isobutyraldehyde", "tdi", "acetylacetone", "natural-rubber", "pvc",
    "neodymium-oxide", "phthalic-anhydride", "white-sugar", "dysprosium-oxide", "naphtha", "soybean", "sulfuric-acid", "tin",
    "polyester", "bisphenol-a", "zinc", "aniline", "paraxylene", "corn", "stainless-steel-sheet", "dimethylformamide",
    "propylene-glycol", "epichlorohydrin", "dipropylene-glycol", "dimethoxymethane", "ferrosilicon", "sbr", "caprolactam",
    "lpg", "sodium-bromide", "butyl-acrylate",
}


def indexable(it, supply_map=None):
    if it.slug in KEEP_SLUGS:
        return True
    if len(it.candles or []) >= MIN_CANDLES:
        return True
    if supply_map and it.ko in supply_map:
        return True
    return False
