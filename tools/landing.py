# -*- coding: utf-8 -*-
"""
Home page (sales landing) for chinanews.kr — EN at /, KO at /ko/.
Rendered by build_pages.py; prices come from data/*.json at build time.

Order of the hero cards is fixed by the owner: rare earths, semiconductors, 5N/6N copper.
"""

HERO_ORDER = ["rare-earths", "semiconductors", "high-purity-copper"]
MORE_ORDER = ["yttrium", "gallium", "terbium", "tungsten", "germanium", "hafnium", "semiconductor-materials"]

L = {
    "en": {
        "title": "Rare Earths, Semiconductors & 5N/6N High-Purity Copper from China — Producer-Direct Supply | CHINANEWS",
        "desc": "BRIDGE GROUP supplies rare earth oxides and metals, Chinese semiconductors and 5N/6N high-purity copper direct from licensed Chinese producers to buyers in Korea and worldwide. Live China prices, COA, samples, export-licence handling. Request a quote.",
        "h1": "Rare Earths · Semiconductors · High-Purity Copper from China",
        "sub": "Producer-direct supply from China's rare-earth, semiconductor and refined-metal supply chains — with certificates, samples and export-control screening on every enquiry.",
        "cta": "Request a quote",
        "cta2": "See live China prices",
        "more": "More products we supply",
        "more_btn": "Show 7 more product lines",
        "less_btn": "Show fewer",
        "detail": "Details & specs →",
        "rfq": "Request a quote →",
        "live_h": "Live China spot prices — strategic materials",
        "live_note": "China domestic spot quotations from our terminal, updated daily. Export prices quoted per enquiry.",
        "why_h": "Why buyers work with us",
        "why": [
            ("Producer-direct, not broker-to-broker", "We buy from the refinery, fab or authorised distributor and quote with the producer's certificate in hand. No stacked margins, no unverified stock."),
            ("Proven China execution", "In June 2026 ABridge became the first Korean company to export SiC focus-ring CVD furnace systems directly to a Chinese semiconductor equipment maker."),
            ("Compliance on every enquiry", "Strategic-items self-classification (YESTRADE) and buyer screening against U.S. CSL, UN and EU lists before any quotation. We decline restricted requests."),
            ("Certificates & samples first", "COA with ICP-MS/GDMS impurity profiles; 100 g–1 kg samples for independent assay before volume orders. Semiconductor lots are sample-verified."),
        ],
        "how_h": "How it works",
        "how": [
            ("1 · Send an RFQ", "Product, purity/spec, quantity, destination. One enquiry can cover several items."),
            ("2 · Quote & samples", "Producer-backed FOB/CIF quotation within one business day; samples and certificates on request."),
            ("3 · Contract & shipment", "Licence handling, third-party inspection, shipment to Busan/Incheon or your port."),
        ],
        "idx_h": "Markets now",
        "idx_link": "Open the live terminal — 405 commodities, indices, FX →",
        "terminal": "Terminal",
        "about": "BRIDGE GROUP (ABridge Co., Ltd. · Ecobridge) is a trading group based in Gwangju, South Korea, holding a state-trading rice quota under Korea's aT and supplying strategic materials, semiconductors and petrochemicals between China and Korea.",
        "nav": ["Rare earths", "Semiconductors", "6N copper", "All products", "Terminal", "Press"],
    },
    "ko": {
        "title": "중국 희토류 공급 · 중국 반도체 조달 · 고순도 구리 5N/6N — 생산자 직거래 | CHINANEWS",
        "desc": "BRIDGE GROUP은 허가받은 중국 생산자로부터 희토류 산화물·금속, 중국산 반도체, 고순도 구리 5N/6N을 국내외 바이어에게 직접 공급합니다. 중국 현물가 매일 갱신, 성적서·샘플, 수출허가 대행. 견적 문의.",
        "h1": "중국 희토류 공급 · 중국 반도체 조달 · 고순도 구리 5N/6N",
        "sub": "중국 희토류·반도체·정련금속 공급망의 생산자와 직거래합니다. 모든 문의에 성적서·샘플·수출통제 심사가 따라갑니다.",
        "cta": "견적 요청",
        "cta2": "중국 현물가 보기",
        "more": "그 외 취급 품목",
        "more_btn": "더보기 — 7개 품목",
        "less_btn": "접기",
        "detail": "규격·상세 →",
        "rfq": "견적 요청 →",
        "live_h": "전략소재 중국 현물가 — 실시간",
        "live_note": "터미널의 중국 내수 현물 호가, 매일 갱신. 수출 가격은 문의별 견적.",
        "why_h": "바이어가 저희와 거래하는 이유",
        "why": [
            ("브로커가 아닌 생산자 직거래", "정련소·팹·공인 대리점에서 직접 매입하고 생산자 성적서를 들고 견적합니다. 마진이 겹치지 않고, 출처 불명 재고가 없습니다."),
            ("검증된 중국 실행력", "㈜에이브릿지는 2026년 6월 한국 기업 최초로 SiC 포커스링 CVD 장비를 중국 반도체 장비사에 직접 수출했습니다."),
            ("모든 문의에 컴플라이언스", "견적 전 전략물자 자가판정(YESTRADE)과 미국 CSL·UN·EU 제재 대상 조회. 제한 대상 요청은 거절합니다."),
            ("성적서와 샘플이 먼저", "ICP-MS/GDMS 불순물 프로파일이 담긴 COA, 본 주문 전 100g~1kg 샘플로 제3자 분석. 반도체 로트는 샘플 검증 후 출하."),
        ],
        "how_h": "진행 절차",
        "how": [
            ("1 · 견적 요청", "품목, 순도/규격, 수량, 납품지를 보내주세요. 여러 품목을 한 번에 문의해도 됩니다."),
            ("2 · 견적·샘플", "1영업일 내 생산자 확인을 거친 FOB/CIF 견적, 요청 시 샘플과 성적서."),
            ("3 · 계약·선적", "수출허가 처리, 제3자 검사, 부산·인천 또는 지정 항구까지 선적."),
        ],
        "idx_h": "지금 시장",
        "idx_link": "실시간 터미널 열기 — 원자재 405종·지수·환율 →",
        "terminal": "터미널",
        "about": "BRIDGE GROUP(㈜에이브릿지 · ㈜에코브릿지)은 광주광역시에 본사를 둔 무역그룹으로, aT 쌀 국영무역 자격을 보유하고 한·중 간 전략소재·반도체·석유화학 제품을 공급합니다.",
        "nav": ["희토류", "반도체", "6N 구리", "전체 품목", "터미널", "보도자료"],
    },
}

# short blurbs for the three hero cards (EN, KO) + which live prices to show
HERO = {
    "rare-earths": {
        "en": ("Rare Earths from China", "Neodymium, praseodymium, dysprosium, terbium, yttrium, lanthanum, cerium and the full lanthanide range — oxides 3N–5N, metals and magnet alloys, from Inner Mongolia and Ganzhou producers. Export-licence handling included.",
               ["17 elements · oxides, metals, PrNd/DyFe alloys", "Magnet, phosphor, catalyst and ceramic grades", "COA (ICP) · samples from 100 g"]),
        "ko": ("중국 희토류 공급", "네오디뮴·프라세오디뮴·디스프로슘·테르븀·이트륨·란탄·세륨 등 란탄족 전 범위 — 내몽골·간저우 생산자의 산화물 3N~5N, 금속, 자석용 합금. 수출허가 대행 포함.",
               ["17개 원소 · 산화물·금속·PrNd/DyFe 합금", "자석·형광체·촉매·세라믹 등급", "COA(ICP) · 샘플 100g부터"]),
        "live": ["산화네오디뮴", "산화프라세오디뮴", "산화디스프로슘", "프라세오디뮴네오디뮴합금"],
    },
    "semiconductors": {
        "en": ("Chinese Semiconductors — Sourcing", "MCUs, power devices (MOSFET, IGBT, SiC/GaN), memory, analog/PMIC, sensors and LEDs from authorised Chinese producers and franchised distributors. Cross-references for Western part numbers; sample-verified lots; export-control screening.",
               ["Demand-based sourcing — no EOL or open-market stock", "Cross-reference service for existing BOMs", "Producer warranty · failure-analysis support"]),
        "ko": ("중국 반도체 조달", "MCU, 전력소자(MOSFET·IGBT·SiC/GaN), 메모리, 아날로그/PMIC, 센서, LED를 중국 정식 생산자·공인 대리점에서 조달. 서구 품번 대체품 검색, 샘플 검증, 수출통제 심사.",
               ["수요 기반 조달 — 단종·오픈마켓 재고 없음", "기존 BOM 품번 대체품 검색 서비스", "생산자 보증 · 고장분석 지원"]),
        "live": ["폴리실리콘", "게르마늄", "금속규소(공업규소)"],
    },
    "high-purity-copper": {
        "en": ("High-Purity Copper 5N / 6N — Ingot · Rod · Granule", "Electrolytic and zone-refined copper 99.999% and 99.9999% for sputtering targets, bonding wire, superconductor stabilisers and research — with full-element GDMS certificates. Also OFE C10100 and Grade A cathode.",
               ["6N verified by GDMS (≥ 70 elements), not a 10-element ICP sum", "Ingot 1–5 kg · rod ø10–50 mm · granule 2–6 mm", "Priced as a premium over the daily cathode price"]),
        "ko": ("고순도 구리 5N / 6N — 잉곳·봉·과립", "스퍼터링 타깃·본딩와이어·초전도 안정화재·연구용 전해·존정련 구리 99.999%, 99.9999% — GDMS 전원소 성적서 첨부. 무산소동 C10100, A급 전기동도 공급.",
               ["6N은 10개 원소 ICP 합산이 아닌 GDMS(70개 원소 이상)로 검증", "잉곳 1~5kg · 봉 ø10~50mm · 과립 2~6mm", "일일 전기동 가격 + 프리미엄으로 견적"]),
        "live": ["구리"],
    },
}

# live-price strip on the landing page (Korean display_name keys)
STRIP = ["산화네오디뮴", "산화프라세오디뮴", "산화디스프로슘", "금속네오디뮴", "프라세오디뮴네오디뮴합금", "게르마늄", "텅스텐 정광", "코발트", "탄산리튬", "폴리실리콘", "금속규소(공업규소)", "구리"]
