# -*- coding: utf-8 -*-
"""이트륨 공급 확정분을 공급 페이지에 반영한다. 한 번만 실행한다.

중국 측과 톤당 단가를 협의한 규격:
  산화이트륨 Y₂O₃ 99.999%(5N) · D50 3~4µm · 분말 · HS 2846.90-1000 · 1,000kg 단위
한국 구매자가 실제로 검색하는 말(산화이트륨, 이트리아, Y2O3, 5N, 수입, 단가)을
제목·소개·자주 묻는 질문에 자연스럽게 넣는다.
"""
import io, os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "tools", "supply_content.py")

src = io.open(P, encoding="utf-8").read()
if "2846.90-1000" in src:
    print("이미 반영되어 있습니다.")
    raise SystemExit(0)

pairs = []

# ── 제목·설명: 검색어를 앞쪽에 둔다 ──────────────────────────────────────────
pairs.append((
    '"title": "중국 이트륨 금속·산화이트륨(Y₂O₃) 5N 공급 — 견적 문의 | CHINANEWS"',
    '"title": "산화이트륨 5N(Y₂O₃ 99.999%) 중국 직수입 공급 — 재고 보유·단가 문의 | CHINANEWS"',
))
pairs.append((
    '"desc": "이트륨 금속(잉곳·스펀지·타깃용 3N~4N)과 고순도 산화이트륨 Y₂O₃ 4N~5N 중국산 공급. 반도체 챔버 코팅, YSZ 세라믹, 형광체, YAG, Al–Y/Mg–Y 합금용. 성적서·샘플. 견적 문의."',
    '"desc": "산화이트륨(이트리아) Y₂O₃ 99.999% 5N, D50 3~4µm 분말을 중국 생산자에서 직수입 공급합니다. HS 2846.90-1000, 1톤 단위 단가 협의 완료. 반도체 챔버 코팅·YSZ·형광체·YAG용. ICP 성적서와 샘플 제공, 한국 내 통관·납품."',
))
pairs.append((
    '"h1": "중국 이트륨 금속·산화이트륨(Y₂O₃) 공급"',
    '"h1": "산화이트륨(Y₂O₃) 5N 중국 직수입 공급"',
))

# ── 소개 문단: 공급 가능 사실을 맨 앞에 ─────────────────────────────────────
old_intro_ko = (
    '                "산화이트륨은 반도체 식각·증착 챔버 내부의 내플라즈마 코팅, 이트리아 안정화 지르코니아(YSZ) 세라믹, '
    '형광체와 YAG 레이저 결정의 핵심 소재입니다. 중국 생산자로부터 4N·5N Y₂O₃를 ICP 불순물 성적서와 함께 공급합니다.",'
)
new_intro_ko = (
    '                "<b>지금 공급 가능합니다.</b> 산화이트륨 Y₂O₃ 99.999%(5N), D50 3~4µm 분말을 중국 생산자와 '
    '1톤 단위 단가 협의를 마치고 공급합니다. HS 코드 2846.90-1000, 최소 1,000kg부터 주문받으며 ICP-MS 성적서가 함께 나갑니다.",\n'
    '                "산화이트륨(이트리아)은 반도체 식각·증착 챔버 내부의 내플라즈마 코팅, 이트리아 안정화 지르코니아(YSZ) 세라믹, '
    '형광체와 YAG 레이저 결정의 핵심 소재입니다. 국내 구매 담당자가 중국 생산자와 직접 거래할 때 겪는 '
    '성적서 검증, 통관, 대금 조건을 저희가 대신 처리합니다.",'
)
pairs.append((old_intro_ko, new_intro_ko))

old_intro_en = (
    '                "Yttrium oxide is the workhorse material for plasma-resistant coatings inside semiconductor etch and '
    'deposition chambers, for yttria-stabilised zirconia (YSZ) ceramics, and for phosphors and YAG laser crystals. '
    'We supply 4N and 5N Y₂O₃ from Chinese producers with ICP impurity certificates.",'
)
new_intro_en = (
    '                "<b>Available now.</b> Yttrium oxide Y₂O₃ 99.999% (5N), D50 3–4 µm powder, priced per tonne with our '
    'Chinese producer and offered from 1,000 kg. HS code 2846.90-1000, ICP-MS certificate with every lot.",\n'
    '                "Yttrium oxide is the workhorse material for plasma-resistant coatings inside semiconductor etch and '
    'deposition chambers, for yttria-stabilised zirconia (YSZ) ceramics, and for phosphors and YAG laser crystals. '
    'We supply 4N and 5N Y₂O₃ from Chinese producers with ICP impurity certificates.",'
)
pairs.append((old_intro_en, new_intro_en))

# ── 표: 확정 규격을 맨 위 줄로 ──────────────────────────────────────────────
old_row = (
    '            ("Y₂O₃ 5N", "산화이트륨 5N", "99.999% · D50 3–8 µm · LOI ≤ 1%", "99.999% · D50 3~8µm · 강열감량 1% 이하", '
    '"99.999%", "Semiconductor chamber coatings, optical ceramics, single crystals", "반도체 챔버 코팅, 광학 세라믹, 단결정", []),'
)
new_row = (
    '            ("Y₂O₃ 5N — in stock", "산화이트륨 5N — 공급 확정분", '
    '"99.999% · D50 3–4 µm · powder · HS 2846.90-1000 · from 1,000 kg", '
    '"99.999% · D50 3~4µm · 분말 · HS 2846.90-1000 · 1,000kg 단위", '
    '"99.999%", "Semiconductor chamber coatings, optical ceramics, single crystals", "반도체 챔버 코팅, 광학 세라믹, 단결정", []),\n'
    '            ("Y₂O₃ 5N", "산화이트륨 5N", "99.999% · D50 3–8 µm · LOI ≤ 1%", "99.999% · D50 3~8µm · 강열감량 1% 이하", '
    '"99.999%", "Semiconductor chamber coatings, optical ceramics, single crystals", "반도체 챔버 코팅, 광학 세라믹, 단결정", []),'
)
pairs.append((old_row, new_row))

# ── 자주 묻는 질문: 단가·통관·납기 ─────────────────────────────────────────
old_faq_ko = '                ("최소 주문량은요?", "5N은 25kg, 4N은 50kg부터입니다. 500g 샘플을 제공합니다."),'
new_faq_ko = (
    '                ("최소 주문량은요?", "이번 공급 확정분(5N, D50 3~4µm)은 1,000kg 단위입니다. 그 밖의 규격은 5N 25kg, 4N 50kg부터이며 500g 샘플을 제공합니다."),\n'
    '                ("단가는 어떻게 되나요?", "톤당 단가를 중국 생산자와 협의해 두었습니다. 시세와 환율에 따라 움직이므로 문의 주시면 그날 기준으로 알려 드립니다."),\n'
    '                ("HS 코드와 통관은요?", "HS 2846.90-1000으로 수입합니다. 수입 신고와 관세 납부, 국내 운송까지 저희가 맡고 구매처는 국내 거래로 받으시면 됩니다."),\n'
    '                ("납기는 얼마나 걸리나요?", "재고분은 통관까지 약 2~3주, 주문 생산은 규격 확정 후 4~6주를 봅니다."),'
)
pairs.append((old_faq_ko, new_faq_ko))

old_faq_en = '                ("Minimum order?", "5N: 25 kg; 4N: 50 kg. 500 g samples available."),'
new_faq_en = (
    '                ("Minimum order?", "The confirmed 5N lot (D50 3–4 µm) ships from 1,000 kg. Other grades start at 25 kg (5N) and 50 kg (4N), with 500 g samples."),\n'
    '                ("How is it priced?", "Per tonne, agreed with the producer. The number moves with the market and FX, so ask and we quote on the day."),\n'
    '                ("HS code and customs?", "Imported under HS 2846.90-1000. We handle the import declaration, duty and domestic delivery, so Korean buyers purchase on domestic terms."),'
)
pairs.append((old_faq_en, new_faq_en))

for old, new in pairs:
    if src.count(old) != 1:
        print("못 찾음 또는 여러 번:", old[:60], "→", src.count(old))
        raise SystemExit(1)
    src = src.replace(old, new, 1)

io.open(P, "w", encoding="utf-8").write(src)
print("supply_content.py 에 이트륨 공급 확정분을 반영했습니다.")
