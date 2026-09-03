# -*- coding: utf-8 -*-
"""
Buyer-facing supply / RFQ landing pages for chinanews.kr (EN + KO).

Each page: slug, title, meta description, h1, intro paragraphs, product table
(name / forms / purity / applications), optional live-price hooks (Korean
display_name keys that exist in data/commodities.json), FAQ, keywords.
Rendered by build_pages.py -> /supply/<slug>.html and /ko/supply/<slug>.html.

Rule: no price-source attribution anywhere. Compliance wording is mandatory.
"""

COMPANY = {
    "en": "BRIDGE GROUP (ABridge Co., Ltd. · Ecobridge) — Gwangju, South Korea. Licensed trading company; state-trading rice quota holder under Korea's aT; Korea's first direct exporter of SiC focus-ring CVD furnace systems to China (June 2026).",
    "ko": "BRIDGE GROUP(㈜에이브릿지 · ㈜에코브릿지) — 광주광역시. aT 쌀 국영무역 자격 보유 무역법인, 2026년 6월 한국 기업 최초로 SiC 포커스링 CVD 장비를 중국에 직접 수출.",
}

COMPLIANCE = {
    "en": [
        "Every enquiry is screened before quotation: strategic-items self-classification (Korea YESTRADE) and buyer screening against the U.S. Consolidated Screening List and UN/EU sanctions lists. We do not quote sanctioned parties, military end-users or embargoed destinations.",
        "Materials ship with mill/producer certificates of analysis (ICP-MS/GDMS as applicable). Samples are available for independent third-party assay before volume orders.",
        "Semiconductor finished goods are sourced on a demand basis from authorised Chinese producers and distributors only — no EOL brokerage, no unverified stock. Sample lots are verified before shipment.",
    ],
    "ko": [
        "모든 문의는 견적 전에 심사합니다: 전략물자 자가판정(YESTRADE)과 미국 통합제재목록(CSL)·UN·EU 제재 대상 조회. 제재 대상, 군 최종사용자, 금수 지역에는 견적하지 않습니다.",
        "소재는 생산자 성적서(COA, 필요 시 ICP-MS/GDMS)와 함께 출하하며, 본 주문 전 제3자 분석용 샘플을 제공합니다.",
        "반도체 완성품은 중국 정식 생산자·공인 대리점에서만 수요 기반으로 조달합니다. 단종(EOL) 브로커링이나 출처 불명 재고는 취급하지 않으며, 샘플 로트를 검증한 뒤 출하합니다.",
    ],
}

# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
PAGES = [
    {
        "slug": "rare-earths",
        "en": {
            "title": "Rare Earth Oxides, Metals & Alloys from China — Supply & RFQ | CHINANEWS",
            "desc": "Source rare earth oxides, metals and alloys from China: neodymium, praseodymium, dysprosium, terbium, yttrium, lanthanum, cerium and more. Live China prices, purity grades 3N–5N, COA, samples. Request a quote.",
            "h1": "Rare Earths from China — Oxides, Metals & Alloys",
            "kicker": "Supply · RFQ",
            "intro": [
                "We supply rare earth oxides, metals and master alloys sourced from producers in China's main rare-earth regions (Inner Mongolia, Jiangxi/Ganzhou, Sichuan), for magnet makers, phosphor and ceramic producers, catalyst formulators and research buyers in Korea and overseas.",
                "Prices below are live China domestic spot quotations from our terminal, updated daily. Export pricing (FOB/CIF, USD) is quoted per enquiry and depends on purity, form, quantity and licence status.",
            ],
            "table_head": ["Element", "Typical forms", "Purity", "Main uses"],
            "faq": [
                ("What is the minimum order?", "Oxides and metals from 25 kg (drum) for most elements; magnet-grade PrNd alloy and Dy/Tb from 100 kg. Sample lots of 100 g–1 kg are available."),
                ("Do you provide certificates?", "Yes — producer COA with REO purity and impurity profile (ICP). Third-party assay (SGS, CTI) can be arranged at cost."),
                ("Are rare earths export-controlled?", "Some rare-earth products fall under China's export-licence regime and Korea's strategic-items rules. We confirm licence status before quoting and only ship with proper documentation."),
                ("Which Incoterms do you quote?", "FOB China port, CIF Busan/Incheon, or DAP for Korean buyers. Other destinations on request."),
            ],
        },
        "ko": {
            "title": "중국 희토류 산화물·금속·합금 공급 — 견적 문의 | CHINANEWS",
            "desc": "네오디뮴·프라세오디뮴·디스프로슘·테르븀·이트륨·란탄·세륨 등 중국산 희토류 산화물·금속·합금 공급. 중국 현물가 매일 갱신, 순도 3N~5N, 성적서·샘플 제공. 견적 문의.",
            "h1": "중국 희토류 공급 — 산화물·금속·합금",
            "kicker": "공급 · 견적",
            "intro": [
                "내몽골·장시(간저우)·쓰촨 등 중국 주요 희토류 산지의 생산자로부터 희토류 산화물·금속·마스터합금을 조달해 국내외 자석·형광체·세라믹·촉매 제조사와 연구기관에 공급합니다.",
                "아래 가격은 터미널의 중국 내수 현물가로 매일 갱신됩니다. 수출 가격(FOB/CIF, USD)은 순도·형태·수량·허가 상태에 따라 문의별로 견적합니다.",
            ],
            "table_head": ["원소", "취급 형태", "순도", "주요 용도"],
            "faq": [
                ("최소 주문량은 얼마인가요?", "대부분의 산화물·금속은 25kg(드럼)부터, 자석용 PrNd 합금과 Dy·Tb는 100kg부터입니다. 100g~1kg 샘플을 제공합니다."),
                ("성적서를 제공하나요?", "네. REO 순도와 불순물 프로파일(ICP)이 기재된 생산자 COA를 제공하며, 요청 시 SGS·CTI 등 제3자 분석을 실비로 진행합니다."),
                ("희토류는 수출통제 품목인가요?", "일부 희토류 제품은 중국의 수출허가제와 한국의 전략물자 규정 적용 대상입니다. 견적 전에 허가 상태를 확인하고 정식 서류로만 출하합니다."),
                ("인코텀즈는요?", "중국항 FOB, 부산·인천 CIF, 국내 바이어는 DAP 가능합니다. 그 외 지역은 문의해 주세요."),
            ],
        },
        # rows: (en_name, ko_name, forms_en, forms_ko, purity, uses_en, uses_ko, [live price keys])
        "rows": [
            ("Neodymium (Nd)", "네오디뮴", "Nd₂O₃ oxide · Nd metal · PrNd alloy", "산화물 Nd₂O₃ · 금속 · PrNd 합금", "99.5–99.99%", "NdFeB permanent magnets (EV motors, wind turbines), lasers", "NdFeB 영구자석(EV 모터·풍력), 레이저", ["산화네오디뮴", "금속네오디뮴", "프라세오디뮴네오디뮴합금", "프라세오디뮴네오디뮴산화물"]),
            ("Praseodymium (Pr)", "프라세오디뮴", "Pr₆O₁₁ oxide · Pr metal", "산화물 Pr₆O₁₁ · 금속", "99.5–99.99%", "Magnets, pigments, aircraft alloys", "자석, 안료, 항공 합금", ["산화프라세오디뮴"]),
            ("Dysprosium (Dy)", "디스프로슘", "Dy₂O₃ oxide · Dy metal · DyFe alloy", "산화물 Dy₂O₃ · 금속 · DyFe 합금", "99.5–99.99%", "High-temperature NdFeB magnets, nuclear control rods", "고온용 NdFeB 자석, 원자로 제어봉", ["산화디스프로슘", "금속디스프로슘", "디스프로슘철합금"]),
            ("Terbium (Tb)", "테르븀", "Tb₄O₇ oxide · Tb metal", "산화물 Tb₄O₇ · 금속", "99.9–99.99%", "Magnet coercivity additive, green phosphors, magnetostrictive alloys", "자석 보자력 첨가제, 녹색 형광체, 자기변형 합금", []),
            ("Yttrium (Y)", "이트륨", "Y₂O₃ oxide 4N–5N · Y metal", "산화물 Y₂O₃ 4N~5N · 금속", "99.99–99.999%", "YSZ ceramics, phosphors, YAG lasers, semiconductor coatings (Y₂O₃ plasma-resistant)", "YSZ 세라믹, 형광체, YAG 레이저, 반도체 내플라즈마 코팅", []),
            ("Lanthanum (La)", "란탄", "La₂O₃ oxide · La metal · La carbonate", "산화물 La₂O₃ · 금속 · 탄산란탄", "99–99.99%", "FCC catalysts, optical glass, NiMH batteries", "FCC 촉매, 광학유리, NiMH 전지", []),
            ("Cerium (Ce)", "세륨", "CeO₂ oxide · Ce carbonate · Ce metal", "산화물 CeO₂ · 탄산세륨 · 금속", "99–99.99%", "Glass polishing, auto catalysts, UV absorbers", "유리 연마, 자동차 촉매, UV 흡수제", []),
            ("Samarium (Sm)", "사마륨", "Sm₂O₃ oxide · Sm metal", "산화물 Sm₂O₃ · 금속", "99.5–99.99%", "SmCo magnets, neutron absorbers", "SmCo 자석, 중성자 흡수재", []),
            ("Gadolinium (Gd)", "가돌리늄", "Gd₂O₃ oxide · Gd metal", "산화물 Gd₂O₃ · 금속", "99.9–99.99%", "MRI contrast, scintillators, magnet additive", "MRI 조영제, 섬광체, 자석 첨가제", []),
            ("Europium (Eu)", "유로퓸", "Eu₂O₃ oxide", "산화물 Eu₂O₃", "99.99%", "Red phosphors, anti-counterfeit inks", "적색 형광체, 위조방지 잉크", []),
            ("Holmium (Ho)", "홀뮴", "Ho₂O₃ oxide · Ho metal", "산화물 Ho₂O₃ · 금속", "99.9–99.99%", "Magnet flux concentrators, medical lasers", "자속 집중기, 의료 레이저", []),
            ("Erbium (Er)", "에르븀", "Er₂O₃ oxide · Er metal", "산화물 Er₂O₃ · 금속", "99.9–99.99%", "Fibre-optic amplifiers, glass colourant", "광섬유 증폭기, 유리 착색", []),
            ("Ytterbium (Yb)", "이터븀", "Yb₂O₃ oxide · Yb metal", "산화물 Yb₂O₃ · 금속", "99.9–99.99%", "Fibre lasers, stainless steel additive", "파이버 레이저, 스테인리스 첨가제", []),
            ("Thulium (Tm) · Lutetium (Lu)", "툴륨 · 루테튬", "Oxides · metals", "산화물 · 금속", "99.9–99.99%", "Medical imaging, PET scintillators, research", "의료 영상, PET 섬광체, 연구용", []),
            ("Scandium (Sc)", "스칸듐", "Sc₂O₃ oxide · Al-Sc master alloy", "산화물 Sc₂O₃ · Al-Sc 마스터합금", "99.9–99.999%", "Aluminium-scandium alloys (aerospace), SOFC electrolytes", "알루미늄-스칸듐 합금(항공), SOFC 전해질", []),
        ],
    },
    {
        "slug": "hafnium",
        "en": {
            "title": "Hafnium Sponge, Crystal Bar & Hafnium Oxide from China — Supply & RFQ | CHINANEWS",
            "desc": "Hafnium supply from China: hafnium sponge, crystal bar, HfO₂ oxide, HfCl₄ and Hf–Zr products for nuclear, aerospace superalloys and semiconductor high-k gate dielectrics. Purity up to 99.99%, low-Zr grades. Request a quote.",
            "h1": "Hafnium from China — Sponge, Crystal Bar, Oxide",
            "kicker": "Supply · RFQ",
            "intro": [
                "Hafnium is a strategic metal produced as a co-product of nuclear-grade zirconium refining. We source hafnium sponge, crystal bar, hafnium oxide (HfO₂) and hafnium tetrachloride (HfCl₄) from Chinese producers for superalloy, plasma-cutting, nuclear and semiconductor buyers.",
                "Low-zirconium grades (Zr < 0.5% / < 1%) and semiconductor-grade HfO₂ (4N+) are available on request with full impurity certificates.",
            ],
            "table_head": ["Product", "Specification", "Purity", "Main uses"],
            "faq": [
                ("Is hafnium export-controlled?", "Hafnium metal and certain compounds are listed under nuclear-related dual-use controls in most jurisdictions. We verify end-use and licence requirements before quoting; shipments carry end-user statements where required."),
                ("What zirconium content can you supply?", "Standard hafnium sponge is Zr ≤ 1–3%. Low-Zr crystal bar (Zr ≤ 0.5%) and nuclear-grade (Zr < 0.2%) are quoted case by case."),
                ("Typical lead time?", "Sponge and oxide: 3–6 weeks ex-works after confirmation. Crystal bar and custom compounds: 6–10 weeks."),
            ],
        },
        "ko": {
            "title": "중국 하프늄 공급 — 스펀지·크리스탈바·산화하프늄 견적 | CHINANEWS",
            "desc": "중국산 하프늄 공급: 하프늄 스펀지, 크리스탈바, 산화하프늄(HfO₂), 염화하프늄(HfCl₄). 원자력·항공 초합금·반도체 high-k 게이트 절연막용. 순도 최대 99.99%, 저지르코늄 등급. 견적 문의.",
            "h1": "중국 하프늄 공급 — 스펀지·크리스탈바·산화물",
            "kicker": "공급 · 견적",
            "intro": [
                "하프늄은 원자력급 지르코늄 정련의 부산물로 생산되는 전략금속입니다. 중국 생산자로부터 하프늄 스펀지·크리스탈바·산화하프늄(HfO₂)·염화하프늄(HfCl₄)을 조달해 초합금·플라즈마 절단·원자력·반도체 수요처에 공급합니다.",
                "저지르코늄 등급(Zr < 0.5% / < 1%)과 반도체용 HfO₂(4N 이상)는 전체 불순물 성적서와 함께 요청 시 공급합니다.",
            ],
            "table_head": ["제품", "규격", "순도", "주요 용도"],
            "faq": [
                ("하프늄은 수출통제 품목인가요?", "하프늄 금속과 일부 화합물은 대부분 국가에서 원자력 관련 이중용도 품목으로 통제됩니다. 견적 전에 최종용도와 허가 요건을 확인하고, 필요 시 최종사용자 서약서와 함께 출하합니다."),
                ("지르코늄 함량은 어느 수준까지 되나요?", "표준 스펀지는 Zr 1~3% 이하입니다. 저Zr 크리스탈바(Zr 0.5% 이하), 원자력급(Zr 0.2% 미만)은 건별 견적입니다."),
                ("납기는요?", "스펀지·산화물은 확정 후 3~6주(공장 출하 기준), 크리스탈바·맞춤 화합물은 6~10주입니다."),
            ],
        },
        "rows": [
            ("Hafnium sponge", "하프늄 스펀지", "Hf ≥ 99.5% (Zr ≤ 3%) · 3–25 mm", "Hf 99.5% 이상(Zr 3% 이하) · 3~25mm", "99.5–99.9%", "Superalloy (Ni-based) additive, plasma-cutting electrodes", "니켈계 초합금 첨가제, 플라즈마 절단 전극", []),
            ("Hafnium crystal bar", "하프늄 크리스탈바", "Iodide process · Zr ≤ 0.5%", "요오드법 · Zr 0.5% 이하", "99.9–99.99%", "Nuclear control rods, sputtering targets, research", "원자로 제어봉, 스퍼터링 타깃, 연구용", []),
            ("Hafnium oxide (HfO₂)", "산화하프늄", "Powder · D50 1–10 µm · semiconductor grade available", "분말 · D50 1~10µm · 반도체 등급 가능", "99.9–99.99%", "High-k gate dielectric (ALD precursor feed), optical coatings, ceramics", "high-k 게이트 절연막(ALD 전구체 원료), 광학 코팅, 세라믹", []),
            ("Hafnium tetrachloride (HfCl₄)", "염화하프늄", "Anhydrous · Zr ≤ 0.1%", "무수 · Zr 0.1% 이하", "99.9%+", "ALD/CVD precursor synthesis, organometallics", "ALD/CVD 전구체 합성, 유기금속", []),
            ("Hafnium carbide (HfC) · Hafnium wire/foil", "탄화하프늄 · 하프늄 선재/박판", "Powder · ø0.5–3 mm wire · 0.05–1 mm foil", "분말 · 선재 ø0.5~3mm · 박판 0.05~1mm", "99.5%+", "Ultra-high-temperature ceramics, aerospace, electrodes", "초고온 세라믹, 항공우주, 전극", []),
        ],
    },
    {
        "slug": "yttrium",
        "en": {
            "title": "Yttrium Metal & Yttrium Oxide (Y₂O₃) 5N from China — Supply & RFQ | CHINANEWS",
            "desc": "Yttrium metal (ingot, sponge, sputtering-target grade 3N–4N) and high-purity yttrium oxide Y₂O₃ 4N–5N from China for semiconductor chamber coatings, YSZ ceramics, phosphors, YAG and Al–Y / Mg–Y alloys. COA, samples. Request a quote.",
            "h1": "Yttrium Metal & Yttrium Oxide (Y₂O₃) from China",
            "kicker": "Supply · RFQ",
            "intro": [
                "Yttrium oxide is the workhorse material for plasma-resistant coatings inside semiconductor etch and deposition chambers, for yttria-stabilised zirconia (YSZ) ceramics, and for phosphors and YAG laser crystals. We supply 4N and 5N Y₂O₃ from Chinese producers with ICP impurity certificates.",
                "For semiconductor coating customers we can supply spray-grade granulated Y₂O₃ (spherical, 10–50 µm) and Y₂O₃-based composite powders (YOF, Y-Al) to specification.",
            ],
            "table_head": ["Product", "Specification", "Purity", "Main uses"],
            "faq": [
                ("What does 5N mean in practice?", "Y₂O₃/TREO ≥ 99.999% with total non-rare-earth impurities typically below 50 ppm; certificates list each element by ICP-MS."),
                ("Minimum order?", "5N: 25 kg; 4N: 50 kg. 500 g samples available."),
                ("Can you match a customer spec sheet?", "Yes — send your particle-size (D10/D50/D90), loss-on-ignition and impurity limits with the RFQ and we will quote against it."),
            ],
        },
        "ko": {
            "title": "중국 이트륨 금속·산화이트륨(Y₂O₃) 5N 공급 — 견적 문의 | CHINANEWS",
            "desc": "이트륨 금속(잉곳·스펀지·타깃용 3N~4N)과 고순도 산화이트륨 Y₂O₃ 4N~5N 중국산 공급. 반도체 챔버 코팅, YSZ 세라믹, 형광체, YAG, Al–Y/Mg–Y 합금용. 성적서·샘플. 견적 문의.",
            "h1": "중국 이트륨 금속·산화이트륨(Y₂O₃) 공급",
            "kicker": "공급 · 견적",
            "intro": [
                "산화이트륨은 반도체 식각·증착 챔버 내부의 내플라즈마 코팅, 이트리아 안정화 지르코니아(YSZ) 세라믹, 형광체와 YAG 레이저 결정의 핵심 소재입니다. 중국 생산자로부터 4N·5N Y₂O₃를 ICP 불순물 성적서와 함께 공급합니다.",
                "반도체 코팅 고객에게는 용사용 조립 분말(구형, 10~50µm)과 Y₂O₃계 복합 분말(YOF, Y-Al)을 규격에 맞춰 공급할 수 있습니다.",
            ],
            "table_head": ["제품", "규격", "순도", "주요 용도"],
            "faq": [
                ("5N은 실제로 어떤 의미인가요?", "Y₂O₃/TREO 99.999% 이상, 비희토류 불순물 합계가 보통 50ppm 미만이며, 성적서에 ICP-MS 원소별 수치가 기재됩니다."),
                ("최소 주문량은요?", "5N은 25kg, 4N은 50kg부터입니다. 500g 샘플을 제공합니다."),
                ("고객 규격서에 맞출 수 있나요?", "네. 입도(D10/D50/D90), 강열감량, 불순물 한도를 문의에 첨부해 주시면 그 기준으로 견적합니다."),
            ],
        },
        "rows": [
            ("Yttrium metal", "이트륨 금속", "Ingot 1–10 kg · sponge · distilled lump · sputtering-target blank", "잉곳 1~10kg · 스펀지 · 증류 덩어리 · 스퍼터링 타깃 소재", "99.9–99.99% (3N–4N)", "Al–Y / Mg–Y master alloys, Y-based sputtering targets, YIG/YAG crystal feed, research", "Al–Y/Mg–Y 마스터합금, Y계 스퍼터링 타깃, YIG/YAG 결정 원료, 연구용", []),
            ("Yttrium–aluminium / yttrium–magnesium master alloy", "이트륨-알루미늄 / 이트륨-마그네슘 마스터합금", "Al-10Y · Mg-30Y ingot", "Al-10Y · Mg-30Y 잉곳", "Y content ±0.5%", "Aerospace Al alloys, WE43 magnesium alloys", "항공용 Al 합금, WE43 마그네슘 합금", []),
            ("Y₂O₃ 5N", "산화이트륨 5N", "99.999% · D50 3–8 µm · LOI ≤ 1%", "99.999% · D50 3~8µm · 강열감량 1% 이하", "99.999%", "Semiconductor chamber coatings, optical ceramics, single crystals", "반도체 챔버 코팅, 광학 세라믹, 단결정", []),
            ("Y₂O₃ 4N", "산화이트륨 4N", "99.99% · D50 1–10 µm", "99.99% · D50 1~10µm", "99.99%", "YSZ, phosphors, YAG, glass additive", "YSZ, 형광체, YAG, 유리 첨가제", []),
            ("Y₂O₃ spray granules", "용사용 Y₂O₃ 조립분", "Spherical 10–50 µm · flowability ≥ 25 s/50 g", "구형 10~50µm · 유동도 25s/50g 이상", "99.9–99.99%", "Plasma-spray / APS coatings on etch chamber parts", "식각 챔버 부품 플라즈마 용사(APS) 코팅", []),
            ("YSZ (8 mol% Y₂O₃)", "이트리아 안정화 지르코니아", "Powder · 3YSZ / 8YSZ", "분말 · 3YSZ / 8YSZ", "99.9%", "SOFC electrolytes, thermal barrier coatings, dental ceramics", "SOFC 전해질, 열차폐 코팅, 치과 세라믹", []),
        ],
    },
    {
        "slug": "high-purity-copper",
        "en": {
            "title": "6N High-Purity Copper (99.9999%) from China — Supply & RFQ | CHINANEWS",
            "desc": "High-purity copper 5N–6N (99.999–99.9999%) ingots, rods, granules and sputtering-target blanks from China for semiconductor interconnects, superconducting cable and research. GDMS certificates. Also LME-grade cathode. Request a quote.",
            "h1": "High-Purity Copper 5N / 6N — Ingot, Rod, Granule",
            "kicker": "Supply · RFQ",
            "intro": [
                "We supply electrolytically refined and zone-refined high-purity copper (5N 99.999% and 6N 99.9999%) from Chinese producers for semiconductor sputtering targets and bonding wire, superconducting cable stabilisers, cryogenic and research applications — alongside standard Grade A cathode and OFC rod for industrial buyers.",
                "6N lots ship with GDMS full-element certificates (typically ≥ 70 elements) and RRR values on request. Live China copper prices are shown below; high-purity grades are quoted as a premium over the daily cathode price.",
            ],
            "table_head": ["Product", "Specification", "Purity", "Main uses"],
            "faq": [
                ("How do you verify 6N purity?", "By GDMS (glow-discharge mass spectrometry) covering the full periodic table, not a 10-element ICP sum. Buyers may nominate an independent lab; we will not quote against certificates that exclude key impurities (Ag, S, O, As, Sb, Bi)."),
                ("Do you supply OFC / C10100?", "Yes — OFE/C10100 rod, bar and plate from Chinese mills, with oxygen ≤ 5 ppm certificates."),
                ("Minimum order?", "6N: 10 kg; 5N: 25 kg; cathode/OFC: 1 t. Samples 100–500 g."),
            ],
        },
        "ko": {
            "title": "중국 6N 고순도 구리(99.9999%) 공급 — 견적 문의 | CHINANEWS",
            "desc": "고순도 구리 5N~6N(99.999~99.9999%) 잉곳·봉·과립·스퍼터링 타깃 소재 중국산 공급. 반도체 배선, 초전도 케이블, 연구용. GDMS 성적서. LME급 전기동도 취급. 견적 문의.",
            "h1": "고순도 구리 5N / 6N — 잉곳·봉·과립",
            "kicker": "공급 · 견적",
            "intro": [
                "전해정련·존정련한 고순도 구리(5N 99.999%, 6N 99.9999%)를 중국 생산자로부터 조달해 반도체 스퍼터링 타깃·본딩와이어, 초전도 케이블 안정화재, 극저온·연구용으로 공급합니다. 산업용 바이어에게는 A급 전기동과 OFC 봉재도 함께 공급합니다.",
                "6N 로트는 GDMS 전원소 성적서(보통 70개 원소 이상)와 함께 출하하며, 요청 시 RRR 값을 제공합니다. 아래는 중국 구리 현물가이며, 고순도 등급은 일일 전기동 가격에 프리미엄을 더해 견적합니다.",
            ],
            "table_head": ["제품", "규격", "순도", "주요 용도"],
            "faq": [
                ("6N 순도는 어떻게 검증하나요?", "10개 원소만 합산하는 ICP가 아니라 주기율표 전 원소를 보는 GDMS(글로방전 질량분석)로 검증합니다. 바이어가 독립 분석기관을 지정할 수 있으며, 핵심 불순물(Ag·S·O·As·Sb·Bi)이 빠진 성적서로는 견적하지 않습니다."),
                ("OFC / C10100도 되나요?", "네. 중국 제강사의 OFE/C10100 봉·바·판재를 산소 5ppm 이하 성적서와 함께 공급합니다."),
                ("최소 주문량은요?", "6N 10kg, 5N 25kg, 전기동·OFC 1톤부터입니다. 샘플은 100~500g."),
            ],
        },
        "rows": [
            ("6N copper (99.9999%)", "6N 구리", "Ingot 1–5 kg · rod ø10–50 mm · granule 2–6 mm · GDMS cert", "잉곳 1~5kg · 봉 ø10~50mm · 과립 2~6mm · GDMS 성적서", "99.9999%", "Sputtering targets, bonding wire, superconductor stabiliser, research", "스퍼터링 타깃, 본딩와이어, 초전도 안정화재, 연구용", ["구리"]),
            ("5N copper (99.999%)", "5N 구리", "Ingot · rod · plate · GDMS/ICP cert", "잉곳 · 봉 · 판 · GDMS/ICP 성적서", "99.999%", "Targets, electronic alloys, evaporation material", "타깃, 전자용 합금, 증착재", []),
            ("OFE copper C10100 / C10200", "무산소동 C10100 / C10200", "Rod · bar · plate · O ≤ 5 / 10 ppm", "봉 · 바 · 판 · 산소 5/10ppm 이하", "99.99%", "Vacuum electronics, accelerator cavities, busbars", "진공 전자, 가속기 공동, 부스바", []),
            ("Grade A cathode", "A급 전기동", "LME/SHFE registered brands · 1 t bundles", "LME/SHFE 등록 브랜드 · 1톤 번들", "99.99%", "Wire rod, industrial", "선재, 산업용", []),
        ],
    },
    {
        "slug": "semiconductor-materials",
        "en": {
            "title": "Semiconductor Materials from China — SiC, Germanium, Silicon, Hafnium, Fluorides | Supply & RFQ",
            "desc": "Source semiconductor process materials from China: SiC powder and CVD-SiC focus rings, germanium ingot/dioxide, polysilicon and silicon metal, hafnium oxide, hydrofluoric acid, fluorite, yttrium oxide. Live prices, COA, samples. Request a quote.",
            "h1": "Semiconductor Materials from China",
            "kicker": "Supply · RFQ",
            "intro": [
                "BRIDGE GROUP supplies process materials and consumables to semiconductor, solar and compound-semiconductor manufacturers: silicon carbide (SiC) powder and CVD-SiC parts, germanium, polysilicon and industrial silicon, hafnium and yttrium compounds, and electronic-grade fluorochemicals — sourced from Chinese producers and shipped with certificates.",
                "In June 2026 ABridge became the first Korean company to export SiC focus-ring CVD furnace systems directly to a Chinese semiconductor equipment maker; the same network supplies the materials below.",
            ],
            "table_head": ["Material", "Forms", "Grade", "Process use"],
            "faq": [
                ("Do you supply CVD-SiC parts, not just powder?", "Yes — CVD-SiC focus rings, edge rings and susceptor coatings for 8- and 12-inch etch/epi tools, made to drawing."),
                ("Electronic-grade chemicals?", "HF (49%, UP/EL grade), NH₄F/BOE and fluorite feedstock for fluorochemical makers. Sulfuric and nitric on request."),
                ("Export controls?", "Most materials on this page are not controlled, but some equipment and high-spec compounds are. Each RFQ is classified before quotation."),
            ],
        },
        "ko": {
            "title": "중국 반도체 소재 공급 — SiC·게르마늄·실리콘·하프늄·불화물 | 견적 문의",
            "desc": "중국산 반도체 공정 소재 조달: SiC 분말·CVD-SiC 포커스링, 게르마늄 잉곳·이산화게르마늄, 폴리실리콘·금속규소, 산화하프늄, 불화수소산, 형석, 산화이트륨. 현물가 매일 갱신, 성적서·샘플. 견적 문의.",
            "h1": "중국 반도체 소재 공급",
            "kicker": "공급 · 견적",
            "intro": [
                "BRIDGE GROUP은 반도체·태양광·화합물반도체 제조사에 공정 소재와 소모품을 공급합니다: 탄화규소(SiC) 분말과 CVD-SiC 부품, 게르마늄, 폴리실리콘과 공업용 규소, 하프늄·이트륨 화합물, 전자급 불소화학품을 중국 생산자로부터 조달해 성적서와 함께 출하합니다.",
                "㈜에이브릿지는 2026년 6월 한국 기업 최초로 SiC 포커스링 CVD 장비를 중국 반도체 장비사에 직접 수출했으며, 같은 네트워크로 아래 소재를 공급합니다.",
            ],
            "table_head": ["소재", "형태", "등급", "공정 용도"],
            "faq": [
                ("분말만이 아니라 CVD-SiC 부품도 되나요?", "네. 8·12인치 식각/에피 장비용 CVD-SiC 포커스링·엣지링·서셉터 코팅을 도면대로 제작 공급합니다."),
                ("전자급 케미컬은요?", "HF(49%, UP/EL급), NH₄F/BOE, 불소화학 원료용 형석을 공급합니다. 황산·질산은 문의해 주세요."),
                ("수출통제는요?", "이 페이지의 소재 대부분은 비통제 품목이지만 일부 장비·고사양 화합물은 통제 대상입니다. 모든 문의는 견적 전에 판정합니다."),
            ],
        },
        "rows": [
            ("Silicon carbide (SiC)", "탄화규소(SiC)", "Powder (α/β, 0.5–50 µm) · CVD-SiC focus/edge rings · SiC-coated graphite", "분말(α/β, 0.5~50µm) · CVD-SiC 포커스/엣지링 · SiC 코팅 흑연", "99.9–99.9995%", "Etch chamber consumables, epi susceptors, SiC crystal growth feed", "식각 챔버 소모품, 에피 서셉터, SiC 결정성장 원료", []),
            ("Germanium", "게르마늄", "Zone-refined ingot · GeO₂ 5N · Ge tetrachloride", "존정련 잉곳 · GeO₂ 5N · 사염화게르마늄", "99.999%+", "IR optics, SiGe epitaxy, fibre-optic dopant, solar (III-V substrate)", "적외선 광학, SiGe 에피, 광섬유 도펀트, III-V 태양전지 기판", ["게르마늄"]),
            ("Polysilicon · Silicon metal", "폴리실리콘 · 금속규소", "Electronic/solar-grade chunk · 553/441/2202 industrial silicon", "전자/태양광급 청크 · 553/441/2202 공업규소", "99.5% – 9N", "Wafer feedstock, silicones, aluminium alloys", "웨이퍼 원료, 실리콘 화합물, 알루미늄 합금", ["폴리실리콘", "금속규소(공업규소)"]),
            ("Hafnium oxide (HfO₂)", "산화하프늄", "Powder 4N · HfCl₄ precursor feed", "분말 4N · HfCl₄ 전구체 원료", "99.99%", "High-k gate dielectric (ALD)", "high-k 게이트 절연막(ALD)", []),
            ("Yttrium oxide (Y₂O₃)", "산화이트륨", "5N powder · spray granules", "5N 분말 · 용사용 조립분", "99.99–99.999%", "Plasma-resistant chamber coatings", "내플라즈마 챔버 코팅", []),
            ("Hydrofluoric acid · Fluorite", "불화수소산 · 형석", "HF 49% UP/EL · acid-grade fluorspar 97% CaF₂", "HF 49% UP/EL급 · 산급 형석 CaF₂ 97%", "EL grade / 97%", "Wet etch/clean, BOE, fluorochemical feedstock", "습식 식각·세정, BOE, 불소화학 원료", ["불화 수소산", "형석"]),
            ("Lithium & battery chemicals", "리튬·배터리 화학품", "Li₂CO₃ battery grade · LiPF₆ · LFP", "탄산리튬 배터리급 · 육불화인산리튬 · LFP", "99.5%+", "Cathode / electrolyte production", "양극재·전해액 생산", ["탄산리튬", "육불화인산리튬", "인산 철 리튬"]),
        ],
    },
    {
        "slug": "semiconductors",
        "en": {
            "title": "Chinese Semiconductors — MCU, Power Devices, Memory, Analog | Sourcing & RFQ | CHINANEWS",
            "desc": "Source finished semiconductors from authorised Chinese producers: MCUs, power discretes (MOSFET, IGBT, SiC/GaN), memory (DRAM, NAND, NOR), analog/PMIC, sensors, LEDs. Demand-based sourcing, verified samples, export-control screening. Request a quote.",
            "h1": "Chinese Semiconductors — Demand-Based Sourcing",
            "kicker": "Sourcing · RFQ",
            "intro": [
                "We source finished semiconductor components from authorised Chinese fabless designers, IDMs and their franchised distributors for OEMs and EMS providers in Korea and abroad. Typical requests: cost-down alternatives to Western/Japanese parts, second sources for supply-constrained lines, and China-made devices for products sold into China.",
                "We do not broker end-of-life or open-market stock. Every lot is traced to the producer or an authorised channel, sample-verified (marking, X-ray/decap where warranted, electrical test on request) and screened for export-control status before quotation.",
            ],
            "table_head": ["Category", "Typical devices", "Representative Chinese producers", "Applications"],
            "faq": [
                ("Can you cross-reference a Western part number?", "Yes — send the part number, quantity and application; we return pin-compatible or functional Chinese alternatives with datasheets and sample availability."),
                ("MOQ and lead time?", "Distributor stock: reels/trays from 1 reel, 1–2 weeks. Production orders: producer MOQ, 6–12 weeks."),
                ("How do you handle export controls?", "Advanced logic, high-end FPGAs/GPUs and certain RF parts are controlled or restricted. We classify each RFQ under Korean strategic-items rules and screen the buyer; restricted requests are declined."),
                ("Warranty and RMA?", "Producer warranty passes through; failure-analysis support is arranged with the producer for production customers."),
            ],
        },
        "ko": {
            "title": "중국산 반도체 조달 — MCU·전력반도체·메모리·아날로그 | 견적 문의 | CHINANEWS",
            "desc": "중국 정식 생산자·공인 대리점에서 반도체 완성품 조달: MCU, 전력 소자(MOSFET·IGBT·SiC/GaN), 메모리(DRAM·NAND·NOR), 아날로그/PMIC, 센서, LED. 수요 기반 조달, 샘플 검증, 수출통제 심사. 견적 문의.",
            "h1": "중국산 반도체 — 수요 기반 조달",
            "kicker": "조달 · 견적",
            "intro": [
                "중국 팹리스·IDM과 그 공인 대리점으로부터 반도체 완성품을 조달해 국내외 OEM·EMS에 공급합니다. 주요 수요: 서구·일본 부품의 원가절감 대체품, 공급이 막힌 라인의 세컨드 소스, 중국 판매용 제품에 들어갈 중국산 소자.",
                "단종(EOL)·오픈마켓 재고는 취급하지 않습니다. 모든 로트는 생산자 또는 공인 채널까지 추적하고, 샘플을 검증(마킹, 필요 시 X-ray/디캡, 요청 시 전기 시험)하며, 견적 전에 수출통제 여부를 심사합니다.",
            ],
            "table_head": ["분류", "대표 소자", "주요 중국 생산자", "적용 분야"],
            "faq": [
                ("서구 부품 품번으로 대체품을 찾아주나요?", "네. 품번·수량·용도를 보내주시면 핀 호환 또는 기능 호환 중국산 대체품을 데이터시트·샘플 가능 여부와 함께 회신합니다."),
                ("MOQ와 납기는요?", "대리점 재고는 릴/트레이 1릴부터 1~2주, 생산 주문은 생산자 MOQ 기준 6~12주입니다."),
                ("수출통제는 어떻게 처리하나요?", "첨단 로직, 고급 FPGA/GPU, 일부 RF 부품은 통제·제한 대상입니다. 모든 문의를 전략물자 규정으로 판정하고 바이어를 심사하며, 제한 대상 요청은 거절합니다."),
                ("보증과 RMA는요?", "생산자 보증이 그대로 적용되며, 양산 고객에게는 생산자와 연계한 고장분석을 지원합니다."),
            ],
        },
        "rows": [
            ("Microcontrollers (MCU)", "마이크로컨트롤러(MCU)", "ARM Cortex-M0/M3/M4, RISC-V, 8051 · 8–32 bit", "ARM Cortex-M0/M3/M4, RISC-V, 8051 · 8~32비트", "GigaDevice, WCH, HDSC (Xiaohua), Geehy, MindMotion, Nations", "Consumer, appliances, motor control, IoT", "가전, 모터 제어, IoT", []),
            ("Power discretes", "전력 소자", "Si MOSFET, IGBT modules, SiC MOSFET/diode, GaN HEMT", "Si MOSFET, IGBT 모듈, SiC MOSFET/다이오드, GaN HEMT", "BYD Semi, StarPower, CR Micro, Silan, Innoscience, BASiC", "EV/charging, solar inverters, industrial drives, power supplies", "EV·충전, 태양광 인버터, 산업 드라이브, 전원", []),
            ("Memory", "메모리", "DRAM (DDR4/LPDDR4X), NAND (SLC/TLC), NOR flash, SRAM", "DRAM(DDR4/LPDDR4X), NAND(SLC/TLC), NOR 플래시, SRAM", "CXMT, YMTC, GigaDevice, Longsys, Biwin", "Embedded, storage, automotive (non-controlled grades)", "임베디드, 스토리지, 차량용(비통제 등급)", []),
            ("Analog & power management", "아날로그·전원관리", "PMIC, LDO, DC-DC, op-amps, gate drivers, ADC", "PMIC, LDO, DC-DC, 연산증폭기, 게이트 드라이버, ADC", "SG Micro, 3PEAK, Silergy, Chipsea, Awinic", "Mobile, industrial, automotive", "모바일, 산업, 차량용", []),
            ("Sensors & interface", "센서·인터페이스", "MEMS mics, pressure/IMU, Hall, touch, USB/CAN/RS-485 transceivers", "MEMS 마이크, 압력/IMU, 홀, 터치, USB/CAN/RS-485 트랜시버", "Goertek, MEMSensing, Novosense, Chipanalog", "Consumer, automotive, industrial", "가전, 차량, 산업", []),
            ("Optoelectronics", "광전자", "LED chips/packages, laser diodes, photodiodes, display drivers", "LED 칩/패키지, 레이저 다이오드, 포토다이오드, 디스플레이 드라이버", "Sanan, HC Semitek, Nationstar, Chipone", "Lighting, display, sensing", "조명, 디스플레이, 센싱", []),
        ],
    },
    {
        "slug": "gallium",
        "en": {
            "title": "Gallium Metal 4N–7N & Gallium Oxide from China — Supply & RFQ | CHINANEWS",
            "desc": "Source gallium from China: gallium metal 99.99–99.99999% (4N–7N), gallium oxide Ga₂O₃, GaAs/GaN feedstock, GaCl₃. For GaN/GaAs epitaxy, LEDs, power devices, solar and alloys. Export-licence handling. Request a quote.",
            "h1": "Gallium from China — Metal 4N–7N, Oxide, Compounds",
            "kicker": "Supply · RFQ",
            "intro": [
                "China produces the large majority of the world's primary gallium as a by-product of alumina refining. We supply gallium metal from 4N (99.99%) industrial grade to 7N (99.99999%) semiconductor grade, plus gallium oxide, gallium trichloride and GaAs/GaN feedstock, from licensed Chinese producers to compound-semiconductor, LED, power-device and research buyers.",
                "Gallium exports from China require an export licence; we handle the application with the producer and quote lead times that include licence processing.",
            ],
            "table_head": ["Product", "Specification", "Purity", "Main uses"],
            "faq": [
                ("How long does the export licence take?", "Typically 30–45 days from complete end-user documentation. Licensed producers hold quotas; small semiconductor-grade lots are usually faster than tonnage industrial lots."),
                ("Packaging?", "Gallium metal in PE bottles (100 g–1 kg) or PTFE-lined drums; shipped solid (melting point 29.8 °C) with temperature-controlled logistics in summer."),
                ("Minimum order?", "7N: 1 kg; 6N: 5 kg; 4N: 25 kg. 100 g samples available."),
            ],
        },
        "ko": {
            "title": "중국 갈륨 금속 4N~7N·산화갈륨 공급 — 견적 문의 | CHINANEWS",
            "desc": "중국산 갈륨 조달: 갈륨 금속 99.99~99.99999%(4N~7N), 산화갈륨 Ga₂O₃, GaAs/GaN 원료, 염화갈륨. GaN/GaAs 에피, LED, 전력소자, 태양광, 합금용. 수출허가 대행. 견적 문의.",
            "h1": "중국 갈륨 공급 — 금속 4N~7N·산화물·화합물",
            "kicker": "공급 · 견적",
            "intro": [
                "중국은 알루미나 정련 부산물로 세계 1차 갈륨의 대부분을 생산합니다. 허가받은 중국 생산자로부터 4N(99.99%) 공업급부터 7N(99.99999%) 반도체급 갈륨 금속과 산화갈륨·염화갈륨·GaAs/GaN 원료를 조달해 화합물반도체·LED·전력소자·연구 수요처에 공급합니다.",
                "중국의 갈륨 수출은 허가 대상입니다. 생산자와 함께 허가 신청을 진행하며, 허가 소요 기간을 포함해 납기를 견적합니다.",
            ],
            "table_head": ["제품", "규격", "순도", "주요 용도"],
            "faq": [
                ("수출허가는 얼마나 걸리나요?", "최종사용자 서류가 갖춰진 뒤 보통 30~45일입니다. 허가 생산자는 쿼터를 보유하며, 소량 반도체급이 톤 단위 공업급보다 빠릅니다."),
                ("포장은요?", "PE 병(100g~1kg) 또는 PTFE 라이닝 드럼. 고체 상태(융점 29.8℃)로 출하하며 여름철은 온도관리 물류를 씁니다."),
                ("최소 주문량은요?", "7N 1kg, 6N 5kg, 4N 25kg부터. 100g 샘플 제공."),
            ],
        },
        "rows": [
            ("Gallium metal 7N", "갈륨 금속 7N", "99.99999% · GDMS cert · PE bottle", "99.99999% · GDMS 성적서 · PE 병", "7N", "GaN/GaAs MOCVD & MBE sources, LED/laser epitaxy, RF/power devices", "GaN/GaAs MOCVD·MBE 소스, LED/레이저 에피, RF/전력소자", []),
            ("Gallium metal 6N", "갈륨 금속 6N", "99.9999% · ICP/GDMS cert", "99.9999% · ICP/GDMS 성적서", "6N", "Compound-semiconductor crystal growth, CIGS solar", "화합물반도체 결정성장, CIGS 태양전지", []),
            ("Gallium metal 4N", "갈륨 금속 4N", "99.99% · industrial", "99.99% · 공업급", "4N", "Alloys (Galinstan), NdFeB magnet additive, catalysts, research", "합금(갈린스탄), NdFeB 첨가제, 촉매, 연구용", []),
            ("Gallium oxide (Ga₂O₃)", "산화갈륨", "β-Ga₂O₃ powder 4N–5N", "β-Ga₂O₃ 분말 4N~5N", "99.99–99.999%", "Ga₂O₃ ultra-wide-bandgap substrates, phosphors, catalysts", "Ga₂O₃ 초광대역 기판, 형광체, 촉매", []),
            ("Gallium trichloride (GaCl₃) · Gallium nitrate", "염화갈륨 · 질산갈륨", "Anhydrous GaCl₃ 4N · Ga(NO₃)₃ solution", "무수 GaCl₃ 4N · 질산갈륨 용액", "99.99%", "HVPE GaN, precursors, radiopharma (Ga-68 generator feed)", "HVPE GaN, 전구체, 방사성의약(Ga-68) 원료", []),
            ("GaAs / GaN polycrystalline feedstock", "GaAs / GaN 다결정 원료", "Poly GaAs 6N · GaN powder", "다결정 GaAs 6N · GaN 분말", "6N", "Single-crystal growth, substrates", "단결정 성장, 기판", []),
        ],
    },
    {
        "slug": "terbium",
        "en": {
            "title": "Terbium Oxide (Tb₄O₇) & Terbium Metal from China — Supply & RFQ | CHINANEWS",
            "desc": "Source terbium from China: terbium oxide Tb₄O₇ 99.9–99.999%, terbium metal, Tb–Fe / Tb–Dy–Fe (Terfenol) alloys. For NdFeB magnet coercivity, green phosphors, magnetostrictive actuators. COA, samples, export-licence handling. Request a quote.",
            "h1": "Terbium from China — Oxide, Metal, Alloys",
            "kicker": "Supply · RFQ",
            "intro": [
                "Terbium is the scarcest of the magnet rare earths and the key additive for raising the coercivity of NdFeB magnets used in EV traction motors and wind turbines. We supply terbium oxide, terbium metal and terbium master alloys from producers in Jiangxi and Guangdong (ionic-clay heavy rare earths) to magnet, phosphor and actuator manufacturers.",
                "Terbium products are subject to China's rare-earth export-licence regime; we manage licensing with the producer and ship with full REO/impurity certificates.",
            ],
            "table_head": ["Product", "Specification", "Purity", "Main uses"],
            "faq": [
                ("Tb vs Dy for magnets?", "Both raise coercivity; Tb is roughly twice as effective per kg but costs several times more. Grain-boundary diffusion (GBD) processes use Tb metal or Tb–H powders in small quantities — we supply GBD-grade material."),
                ("Minimum order?", "Oxide: 10 kg; metal: 5 kg; alloys: 25 kg. Samples 100 g."),
                ("Lead time?", "Stock oxide 2–3 weeks plus licence (30–45 days); metal and alloys 6–8 weeks."),
            ],
        },
        "ko": {
            "title": "중국 테르븀 산화물(Tb₄O₇)·금속 공급 — 견적 문의 | CHINANEWS",
            "desc": "중국산 테르븀 조달: 산화테르븀 Tb₄O₇ 99.9~99.999%, 테르븀 금속, Tb–Fe / Tb–Dy–Fe(테르페놀) 합금. NdFeB 자석 보자력, 녹색 형광체, 자기변형 액추에이터용. 성적서·샘플·수출허가 대행. 견적 문의.",
            "h1": "중국 테르븀 공급 — 산화물·금속·합금",
            "kicker": "공급 · 견적",
            "intro": [
                "테르븀은 자석용 희토류 중 가장 희소하며, EV 구동모터와 풍력터빈용 NdFeB 자석의 보자력을 높이는 핵심 첨가제입니다. 장시·광둥(이온흡착형 중희토) 생산자로부터 산화테르븀·테르븀 금속·마스터합금을 조달해 자석·형광체·액추에이터 제조사에 공급합니다.",
                "테르븀 제품은 중국 희토류 수출허가 대상입니다. 생산자와 함께 허가를 진행하고 REO·불순물 성적서와 함께 출하합니다.",
            ],
            "table_head": ["제품", "규격", "순도", "주요 용도"],
            "faq": [
                ("자석에는 Tb와 Dy 중 뭐가 낫나요?", "둘 다 보자력을 높입니다. Tb는 kg당 효과가 약 2배지만 가격은 수 배입니다. 입계확산(GBD) 공정은 소량의 Tb 금속이나 Tb–H 분말을 쓰며, GBD 등급을 공급합니다."),
                ("최소 주문량은요?", "산화물 10kg, 금속 5kg, 합금 25kg부터. 샘플 100g."),
                ("납기는요?", "재고 산화물 2~3주 + 허가(30~45일), 금속·합금 6~8주."),
            ],
        },
        "rows": [
            ("Terbium oxide (Tb₄O₇)", "산화테르븀", "Powder · TREO ≥ 99% · Tb₄O₇/TREO 99.9–99.999%", "분말 · TREO 99% 이상 · Tb₄O₇/TREO 99.9~99.999%", "3N–5N", "Magnet additive, green phosphors, Faraday rotator glass (TGG)", "자석 첨가제, 녹색 형광체, 패러데이 회전자 유리(TGG)", []),
            ("Terbium metal", "테르븀 금속", "Ingot / lump / distilled · GBD grade", "잉곳 · 덩어리 · 증류 · GBD 등급", "99.9–99.99%", "Grain-boundary diffusion for NdFeB, Terfenol-D, research", "NdFeB 입계확산, 테르페놀-D, 연구용", []),
            ("Tb–Fe / Tb–Dy–Fe alloys", "Tb–Fe / Tb–Dy–Fe 합금", "Tb-Fe 80/20 · Terfenol-D rods", "Tb-Fe 80/20 · 테르페놀-D 봉", "Alloy spec", "Magnetostrictive actuators, sonar transducers", "자기변형 액추에이터, 소나 트랜스듀서", []),
            ("Terbium fluoride / chloride", "불화테르븀 · 염화테르븀", "TbF₃ 4N · TbCl₃ · hydride powder", "TbF₃ 4N · TbCl₃ · 수소화물 분말", "99.99%", "Metal reduction feed, GBD coatings, optical", "금속 환원 원료, GBD 코팅, 광학", []),
        ],
    },
    {
        "slug": "tungsten",
        "en": {
            "title": "Tungsten from China — APT, Tungsten Oxide, Powder, Carbide | Supply & RFQ | CHINANEWS",
            "desc": "Source tungsten products from China: ammonium paratungstate (APT), tungsten trioxide, tungsten metal powder, tungsten carbide powder, ferrotungsten, tungsten wire/rod/plate and sputtering targets. Live China APT and concentrate prices. Request a quote.",
            "h1": "Tungsten from China — APT, Oxide, Powder, Carbide",
            "kicker": "Supply · RFQ",
            "intro": [
                "China supplies over 80% of the world's tungsten. We source the full chain — tungsten concentrate, APT, tungsten oxides, tungsten metal and carbide powders, ferrotungsten and mill products — from producers in Jiangxi, Hunan and Fujian for hard-metal tool makers, steel mills, electronics and semiconductor buyers.",
                "Live China prices for tungsten concentrate and APT are shown below. Tungsten exports from China are licensed; we handle the licence with the producer.",
            ],
            "table_head": ["Product", "Specification", "Grade", "Main uses"],
            "faq": [
                ("Which carbide grades?", "WC powder from 0.4 µm (nano/ultrafine) to 10 µm coarse, with or without Co/Cr₃C₂/VC additions; cast tungsten carbide for hardfacing."),
                ("Semiconductor tungsten?", "High-purity W powder (4N–5N) and sputtering targets for W-plug/interconnect deposition; WF₆ on request."),
                ("Minimum order?", "APT/oxide: 1 t; powders: 100 kg; mill products: per drawing."),
            ],
        },
        "ko": {
            "title": "중국 텅스텐 공급 — APT·산화텅스텐·분말·탄화텅스텐 | 견적 문의 | CHINANEWS",
            "desc": "중국산 텅스텐 제품 조달: 파라텅스텐산암모늄(APT), 삼산화텅스텐, 텅스텐 금속분말, 탄화텅스텐 분말, 페로텅스텐, 텅스텐 선재·봉·판, 스퍼터링 타깃. 중국 APT·정광 현물가 매일 갱신. 견적 문의.",
            "h1": "중국 텅스텐 공급 — APT·산화물·분말·탄화물",
            "kicker": "공급 · 견적",
            "intro": [
                "중국은 세계 텅스텐의 80% 이상을 공급합니다. 장시·후난·푸젠 생산자로부터 정광, APT, 산화텅스텐, 텅스텐 금속·탄화물 분말, 페로텅스텐, 가공재까지 전 체인을 조달해 초경공구·제강·전자·반도체 수요처에 공급합니다.",
                "아래는 텅스텐 정광과 APT의 중국 현물가입니다. 중국의 텅스텐 수출은 허가 대상이며 생산자와 함께 허가를 진행합니다.",
            ],
            "table_head": ["제품", "규격", "등급", "주요 용도"],
            "faq": [
                ("탄화텅스텐 등급은요?", "0.4µm(나노/초미립)부터 10µm 조립까지 WC 분말, Co/Cr₃C₂/VC 첨가 여부 선택 가능, 하드페이싱용 주조 탄화텅스텐."),
                ("반도체용 텅스텐은요?", "W 플러그·배선 증착용 고순도 W 분말(4N~5N)과 스퍼터링 타깃, 요청 시 WF₆."),
                ("최소 주문량은요?", "APT·산화물 1톤, 분말 100kg, 가공재는 도면 기준."),
            ],
        },
        "rows": [
            ("Tungsten concentrate", "텅스텐 정광", "Wolframite / scheelite · WO₃ ≥ 65%", "흑중석 · 회중석 · WO₃ 65% 이상", "65% WO₃", "APT feedstock", "APT 원료", ["텅스텐 정광"]),
            ("Ammonium paratungstate (APT)", "파라텅스텐산암모늄(APT)", "WO₃ ≥ 88.5% · GB/T 10116 grade 0", "WO₃ 88.5% 이상 · GB/T 10116 0급", "APT-0", "Tungsten oxide/powder production", "산화텅스텐·분말 생산", ["암모늄 파라텅스테이트"]),
            ("Tungsten oxide (WO₃ · blue/yellow)", "산화텅스텐(청색/황색)", "Powder · FSSS 10–30 µm", "분말 · FSSS 10~30µm", "99.95%", "Reduction to W powder, catalysts, electrochromics", "W 분말 환원, 촉매, 전기변색", []),
            ("Tungsten metal powder", "텅스텐 금속분말", "FSSS 0.6–30 µm · 4N–5N available", "FSSS 0.6~30µm · 4N~5N 가능", "99.95–99.999%", "Hard metal, heavy alloys, semiconductor targets, additive manufacturing", "초경, 중합금, 반도체 타깃, 적층제조", []),
            ("Tungsten carbide powder", "탄화텅스텐 분말", "WC 0.4–10 µm · total C 6.13% · cast WC", "WC 0.4~10µm · 총탄소 6.13% · 주조 WC", "99.9%", "Cutting tools, wear parts, hardfacing", "절삭공구, 내마모 부품, 하드페이싱", []),
            ("Ferrotungsten (FeW)", "페로텅스텐", "W 75–80% · lumps 10–50 mm", "W 75~80% · 괴 10~50mm", "FeW80", "Tool and high-speed steel", "공구강·고속도강", []),
            ("Tungsten wire / rod / plate / crucibles", "텅스텐 선재·봉·판·도가니", "Per ASTM B760 / drawing", "ASTM B760 · 도면 기준", "99.95%", "Lighting, furnaces, sapphire growth, semiconductor heaters", "조명, 로, 사파이어 성장, 반도체 히터", []),
        ],
    },
    {
        "slug": "germanium",
        "en": {
            "title": "Germanium Ingot, Germanium Dioxide & GeCl₄ from China — Supply & RFQ | CHINANEWS",
            "desc": "Source germanium from China: zone-refined germanium ingot 5N–6N, germanium dioxide GeO₂ 5N, germanium tetrachloride, Ge wafers and IR optical blanks. For SiGe epitaxy, fibre optics, infrared optics, III-V solar substrates. Live China price. Request a quote.",
            "h1": "Germanium from China — Ingot, Dioxide, Tetrachloride",
            "kicker": "Supply · RFQ",
            "intro": [
                "China is the largest producer of primary germanium, recovered from zinc refining and coal fly ash in Yunnan and Inner Mongolia. We supply zone-refined germanium ingot, germanium dioxide, germanium tetrachloride and germanium optical blanks from licensed Chinese producers to fibre-optic, infrared-optics, semiconductor and solar buyers.",
                "Live China germanium prices are shown below. Germanium products are subject to China's export-licence regime; we manage licensing with the producer.",
            ],
            "table_head": ["Product", "Specification", "Purity", "Main uses"],
            "faq": [
                ("Resistivity of your ingot?", "Zone-refined ingot ≥ 50 Ω·cm (intrinsic grade); 6N lots ≥ 47 Ω·cm certified by four-point probe and GDMS."),
                ("Do you supply Ge wafers?", "Yes — 2–6 inch Ge substrates (n/p type, orientation to spec) for III-V solar cells and photonics, made to order."),
                ("Minimum order?", "Ingot: 5 kg; GeO₂: 10 kg; GeCl₄: 25 kg. Samples 100 g."),
            ],
        },
        "ko": {
            "title": "중국 게르마늄 잉곳·이산화게르마늄·GeCl₄ 공급 — 견적 문의 | CHINANEWS",
            "desc": "중국산 게르마늄 조달: 존정련 게르마늄 잉곳 5N~6N, 이산화게르마늄 GeO₂ 5N, 사염화게르마늄, Ge 웨이퍼·적외선 광학 블랭크. SiGe 에피, 광섬유, 적외선 광학, III-V 태양전지 기판용. 중국 현물가 매일 갱신. 견적 문의.",
            "h1": "중국 게르마늄 공급 — 잉곳·이산화물·사염화물",
            "kicker": "공급 · 견적",
            "intro": [
                "중국은 윈난·내몽골의 아연 정련과 석탄 비산재에서 회수하는 1차 게르마늄의 최대 생산국입니다. 허가받은 중국 생산자로부터 존정련 잉곳, 이산화게르마늄, 사염화게르마늄, 광학 블랭크를 조달해 광섬유·적외선 광학·반도체·태양광 수요처에 공급합니다.",
                "아래는 게르마늄의 중국 현물가입니다. 게르마늄 제품은 중국 수출허가 대상이며 생산자와 함께 허가를 진행합니다.",
            ],
            "table_head": ["제품", "규격", "순도", "주요 용도"],
            "faq": [
                ("잉곳 비저항은요?", "존정련 잉곳 50Ω·cm 이상(진성급), 6N 로트는 47Ω·cm 이상을 4탐침·GDMS로 인증합니다."),
                ("Ge 웨이퍼도 되나요?", "네. III-V 태양전지·포토닉스용 2~6인치 Ge 기판(n/p형, 방위 지정)을 주문 제작합니다."),
                ("최소 주문량은요?", "잉곳 5kg, GeO₂ 10kg, GeCl₄ 25kg부터. 샘플 100g."),
            ],
        },
        "rows": [
            ("Germanium ingot (zone-refined)", "게르마늄 잉곳(존정련)", "≥ 50 Ω·cm · 5N–6N · GDMS", "50Ω·cm 이상 · 5N~6N · GDMS", "99.999–99.9999%", "Ge/SiGe epitaxy, IR optics, detectors", "Ge/SiGe 에피, 적외선 광학, 검출기", ["게르마늄"]),
            ("Germanium dioxide (GeO₂)", "이산화게르마늄", "Electronic grade 5N · hexagonal", "전자급 5N · 육방정", "99.999%", "Fibre-optic preform dopant, PET catalyst, phosphors", "광섬유 프리폼 도펀트, PET 촉매, 형광체", []),
            ("Germanium tetrachloride (GeCl₄)", "사염화게르마늄", "Optical-fibre grade · H ≤ 1 ppm", "광섬유급 · H 1ppm 이하", "99.9999%", "Optical fibre core doping (MCVD/OVD)", "광섬유 코어 도핑(MCVD/OVD)", []),
            ("Germanium wafers & optical blanks", "게르마늄 웨이퍼·광학 블랭크", "2–6 inch substrates · IR lens/window blanks", "2~6인치 기판 · 적외선 렌즈/윈도 블랭크", "Single crystal", "III-V multi-junction solar, thermal imaging optics", "III-V 다중접합 태양전지, 열영상 광학", []),
        ],
    },
]

# Commodity display_name -> supply page slug (adds an RFQ call-to-action on those commodity pages)
COMMODITY_TO_SUPPLY = {
    "산화네오디뮴": "rare-earths", "금속네오디뮴": "rare-earths", "산화프라세오디뮴": "rare-earths",
    "프라세오디뮴네오디뮴산화물": "rare-earths", "프라세오디뮴네오디뮴합금": "rare-earths",
    "산화디스프로슘": "rare-earths", "금속디스프로슘": "rare-earths", "디스프로슘철합금": "rare-earths",
    "게르마늄": "germanium", "텅스텐 정광": "tungsten", "암모늄 파라텅스테이트": "tungsten", "폴리실리콘": "semiconductor-materials",
    "금속규소(공업규소)": "semiconductor-materials", "불화 수소산": "semiconductor-materials", "형석": "semiconductor-materials",
    "탄산리튬": "semiconductor-materials", "육불화인산리튬": "semiconductor-materials", "인산 철 리튬": "semiconductor-materials",
    "구리": "high-purity-copper",
}
