# -*- coding: utf-8 -*-
"""핵심 품목 페이지에 넣는 사람이 쓴 설명 (2026-10-14 도입, 사용자 승인 문안).

목적: 틀에 숫자만 바뀌는 페이지가 아니라 읽을 거리가 있는 페이지로 만든다(9월 스팸 업데이트 대응).
규칙: 널리 알려진 업계 사실만, 특정 기업·출처명(시세 출처) 금지, 근거 없는 수치·최상급 표현 금지.
형식: GUIDES[slug][lang] = [(소제목, HTML 본문), ...]  — build_pages.render_commodity 가 가격 표 아래에 넣는다.
본문 안의 {RFQ} 는 견적 요청 주소로 바뀐다(공급 페이지가 있으면 그 페이지, 없으면 공급 허브).
"""

_PRICE_KO = ('<p>가격은 중국 내수 현물가를 매일 수집해 <b>달러로 환산</b>한 값입니다. 오늘 가격과 등락, 1년 차트, 52주 최고·최저, 일별 가격표는 <b>회원 전용</b>입니다. '
             '수출 가격(FOB/CIF)은 순도·수량·조건에 따라 달라 별도 견적으로 안내합니다. <a href="{RFQ}">견적 요청 →</a></p>')
_PRICE_EN = ('<p>Prices are China domestic spot quotations collected daily and <b>converted to US dollars</b>. Today\'s price and change, the one-year chart, 52-week high/low and the daily price table are <b>for members</b>. '
             'Export prices (FOB/CIF) depend on grade, quantity and terms and are quoted per enquiry. <a href="{RFQ}">Request a quote →</a></p>')

GUIDES = {
    "lithium-carbonate": {
        "ko": [
            ("탄산리튬이란", "<p>탄산리튬(Li₂CO₃)은 리튬 화합물 중 가장 많이 거래되는 기초 원료입니다. 전기차와 에너지저장장치(ESS)용 <b>배터리 양극재</b>를 만드는 데 가장 많이 쓰이고, 유리·세라믹, 윤활유, 의약품 원료로도 쓰입니다.</p>"
             '<table><thead><tr><th>등급</th><th>순도</th><th>주 용도</th></tr></thead><tbody>'
             '<tr><td>배터리급</td><td>99.5% 이상</td><td>LFP(리튬인산철)·NCM 양극재</td></tr>'
             '<tr><td>공업급</td><td>99.0~99.2% 안팎</td><td>유리·세라믹, 윤활유, 화학 원료</td></tr></tbody></table>'),
            ("중국이 가격을 정하는 이유", "<p>중국은 세계 리튬 화학제품 정제의 약 3분의 2를 맡고 있습니다. 원료는 세 갈래로 들어옵니다.</p><ul>"
             "<li><b>장시성 이춘</b> — 레피도라이트(리튬운모) 광산과 제련소가 모여 있습니다</li>"
             "<li><b>칭하이·티베트</b> — 소금호수 염수에서 리튬을 뽑습니다</li>"
             "<li><b>수입 원료</b> — 호주산 스포듀민 정광, 칠레·아르헨티나산 원료</li></ul>"
             "<p>그래서 중국 내수 현물가가 사실상 세계 기준 가격 역할을 합니다. 2023년부터는 광저우선물거래소에 탄산리튬 선물이 상장돼 현물가와 선물가가 서로 영향을 주고받습니다.</p>"),
            ("가격을 움직이는 요인", "<ol><li><b>전기차·ESS 수요</b> — 특히 LFP 배터리를 많이 쓰는 중국 내수 판매</li>"
             "<li><b>원료 가격</b> — 스포듀민 정광 가격과 염수 생산 원가</li>"
             "<li><b>공급 조절</b> — 이춘 지역 광산의 인허가·환경 점검에 따른 가동 변화</li>"
             "<li><b>재고</b> — 제련소와 배터리 업체의 재고 쌓기·줄이기</li>"
             "<li><b>선물 시장</b> — 광저우 선물가의 급등락이 현물 호가에 바로 반영됩니다</li></ol>"),
            ("이 페이지의 가격", _PRICE_KO),
        ],
        "en": [
            ("What lithium carbonate is", "<p>Lithium carbonate (Li₂CO₃) is the most widely traded lithium compound. Its largest use is in <b>battery cathode materials</b> for electric vehicles and energy storage systems; it is also used in glass and ceramics, lubricating greases and pharmaceuticals.</p>"
             '<table><thead><tr><th>Grade</th><th>Purity</th><th>Main uses</th></tr></thead><tbody>'
             '<tr><td>Battery grade</td><td>≥ 99.5%</td><td>LFP and NCM cathode materials</td></tr>'
             '<tr><td>Industrial grade</td><td>about 99.0–99.2%</td><td>Glass and ceramics, greases, chemicals</td></tr></tbody></table>'),
            ("Why China sets the price", "<p>China refines roughly two-thirds of the world's lithium chemicals. Its feedstock comes from three directions:</p><ul>"
             "<li><b>Yichun, Jiangxi</b> — lepidolite mines and refineries</li>"
             "<li><b>Qinghai and Tibet</b> — lithium extracted from salt-lake brines</li>"
             "<li><b>Imports</b> — spodumene concentrate from Australia and raw material from Chile and Argentina</li></ul>"
             "<p>China's domestic spot price therefore works as the de facto global benchmark. Since 2023 lithium carbonate futures have traded on the Guangzhou Futures Exchange, and spot and futures prices move each other.</p>"),
            ("What moves the price", "<ol><li><b>EV and energy-storage demand</b> — above all domestic sales of LFP batteries in China</li>"
             "<li><b>Feedstock cost</b> — spodumene concentrate prices and brine production costs</li>"
             "<li><b>Supply discipline</b> — permits and environmental inspections at Yichun mines</li>"
             "<li><b>Inventory</b> — restocking and destocking by refiners and battery makers</li>"
             "<li><b>Futures</b> — sharp moves in Guangzhou futures feed straight into spot offers</li></ol>"),
            ("About the price on this page", _PRICE_EN),
        ],
    },
    "polysilicon": {
        "ko": [
            ("폴리실리콘이란", "<p>폴리실리콘은 순도를 아주 높인 다결정 실리콘으로, <b>태양광 웨이퍼</b>와 <b>반도체 웨이퍼</b>의 출발 원료입니다. 같은 이름이지만 쓰임에 따라 요구 순도가 크게 다릅니다.</p>"
             '<table><thead><tr><th>구분</th><th>순도</th><th>용도</th></tr></thead><tbody>'
             '<tr><td>태양광급</td><td>6N~9N 안팎</td><td>단결정 잉곳·웨이퍼 → 태양전지</td></tr>'
             '<tr><td>전자(반도체)급</td><td>11N 안팎</td><td>반도체용 단결정 실리콘 웨이퍼</td></tr></tbody></table>'
             "<p>제조 방식은 지멘스법으로 만드는 막대형(로드)과 유동층 반응으로 만드는 입자형(그래뉼)이 대표적입니다.</p>"),
            ("중국 시장 구조", "<p>세계 폴리실리콘 생산의 대부분이 중국에서 나옵니다. 전기요금이 싼 신장, 내몽골, 쓰촨, 윈난에 대형 공장이 모여 있고, 잉곳·웨이퍼·셀·모듈까지 이어지는 태양광 공급망도 중국에 집중돼 있습니다. "
             "2024년 말에는 광저우선물거래소에 폴리실리콘 선물이 상장됐습니다.</p>"),
            ("가격을 움직이는 요인", "<ol><li><b>태양광 설치 수요</b> — 중국 내수와 해외 설치량</li>"
             "<li><b>공급 과잉</b> — 대규모 증설로 생산능력이 수요를 크게 웃도는 상황과 감산·재편 움직임</li>"
             "<li><b>전력 비용</b> — 생산 원가에서 전기요금 비중이 큽니다</li>"
             "<li><b>웨이퍼·모듈 가격</b> — 하류 가격이 내려가면 원료 가격도 압박을 받습니다</li>"
             "<li><b>무역 규제</b> — 주요국의 태양광 제품 수입 규제</li></ol>"),
            ("이 페이지의 가격", _PRICE_KO),
        ],
        "en": [
            ("What polysilicon is", "<p>Polysilicon is ultra-pure polycrystalline silicon, the starting material for <b>solar wafers</b> and <b>semiconductor wafers</b>. The required purity differs greatly by use.</p>"
             '<table><thead><tr><th>Type</th><th>Purity</th><th>Use</th></tr></thead><tbody>'
             '<tr><td>Solar grade</td><td>about 6N–9N</td><td>Mono ingots and wafers for solar cells</td></tr>'
             '<tr><td>Electronic grade</td><td>about 11N</td><td>Single-crystal silicon wafers for chips</td></tr></tbody></table>'
             "<p>It is made mainly as rods by the Siemens process or as granules in fluidised-bed reactors.</p>"),
            ("China's market", "<p>Most of the world's polysilicon is produced in China, in large plants in Xinjiang, Inner Mongolia, Sichuan and Yunnan where power is cheap. The downstream solar chain — ingots, wafers, cells and modules — is concentrated there too. "
             "Polysilicon futures were listed on the Guangzhou Futures Exchange at the end of 2024.</p>"),
            ("What moves the price", "<ol><li><b>Solar installations</b> — in China and abroad</li>"
             "<li><b>Overcapacity</b> — capacity well above demand after rapid expansion, and moves to cut output and consolidate</li>"
             "<li><b>Power costs</b> — electricity is a large share of production cost</li>"
             "<li><b>Wafer and module prices</b> — falling downstream prices press on feedstock</li>"
             "<li><b>Trade measures</b> — import restrictions on solar products in major markets</li></ol>"),
            ("About the price on this page", _PRICE_EN),
        ],
    },
    "fluorite": {
        "ko": [
            ("형석이란", "<p>형석(플루오라이트, CaF₂)은 <b>불소 화학의 출발 원료</b>입니다. 품위에 따라 쓰임이 나뉩니다.</p>"
             '<table><thead><tr><th>구분</th><th>품위</th><th>주 용도</th></tr></thead><tbody>'
             '<tr><td>산업용(산성) 형석</td><td>CaF₂ 97% 이상</td><td>불산(HF) → 냉매, 불소수지, 2차전지 전해질(LiPF₆), 반도체 식각액</td></tr>'
             '<tr><td>야금용 형석</td><td>CaF₂ 65~90% 안팎</td><td>제철·제강 용제</td></tr></tbody></table>'),
            ("중국 시장 구조", "<p>중국은 세계 최대의 형석 생산국이자 소비국입니다. 저장, 장시, 내몽골, 후난 등에 광산이 많고, 국내 불소화학 수요가 커지면서 몽골 등에서 수입도 늘고 있습니다. "
             "여러 나라가 형석을 전략·핵심 광물로 분류하고 있습니다.</p>"),
            ("가격을 움직이는 요인", "<ol><li><b>불산 수요</b> — 냉매, 불소수지, 2차전지 전해질 생산</li>"
             "<li><b>냉매 생산 할당</b> — 온실가스 감축 의무에 따른 냉매 생산 쿼터</li>"
             "<li><b>광산 안전·환경 점검</b> — 점검 기간에는 공급이 줄어듭니다</li>"
             "<li><b>수입 물량</b> — 몽골 등에서 들어오는 정광</li>"
             "<li><b>계절 요인</b> — 북부 광산의 겨울철 가동 감소</li></ol>"),
            ("이 페이지의 가격", _PRICE_KO),
        ],
        "en": [
            ("What fluorite is", "<p>Fluorite (fluorspar, CaF₂) is <b>the feedstock of fluorine chemistry</b>. Its use depends on grade.</p>"
             '<table><thead><tr><th>Type</th><th>Grade</th><th>Main uses</th></tr></thead><tbody>'
             '<tr><td>Acid grade</td><td>CaF₂ ≥ 97%</td><td>Hydrofluoric acid → refrigerants, fluoropolymers, battery electrolyte (LiPF₆), semiconductor etchants</td></tr>'
             '<tr><td>Metallurgical grade</td><td>CaF₂ about 65–90%</td><td>Flux in iron and steel making</td></tr></tbody></table>'),
            ("China's market", "<p>China is the world's largest producer and consumer of fluorite, with mines in Zhejiang, Jiangxi, Inner Mongolia and Hunan. As domestic fluorochemical demand has grown, imports from Mongolia and elsewhere have risen. "
             "Several countries classify fluorspar as a strategic or critical mineral.</p>"),
            ("What moves the price", "<ol><li><b>Hydrofluoric acid demand</b> — refrigerants, fluoropolymers and battery electrolyte</li>"
             "<li><b>Refrigerant quotas</b> — production quotas under greenhouse-gas commitments</li>"
             "<li><b>Mine safety and environmental inspections</b> — supply drops while they run</li>"
             "<li><b>Imports</b> — concentrate from Mongolia and other sources</li>"
             "<li><b>Seasonality</b> — lower winter output at northern mines</li></ol>"),
            ("About the price on this page", _PRICE_EN),
        ],
    },
    "propylene-oxide": {
        "ko": [
            ("산화프로필렌이란", "<p>산화프로필렌(PO)은 프로필렌에서 만드는 화학 중간체입니다. 대부분 <b>폴리에테르 폴리올</b>로 바뀌어 가구·자동차 시트·단열재에 쓰이는 <b>폴리우레탄 폼</b>이 되고, 일부는 프로필렌글리콜과 각종 계면활성제 원료가 됩니다.</p>"),
            ("중국 시장 구조", "<p>중국은 세계 최대의 PO 생산국입니다. 예전에는 폐수가 많이 나오는 <b>클로로히드린법</b>이 주류였지만, 지금은 과산화수소를 쓰는 <b>HPPO법</b>과 스티렌·MTBE를 함께 만드는 <b>공산화법</b> 설비가 빠르게 늘었습니다. 신규 설비가 계속 들어오면서 공급이 늘어나는 추세입니다.</p>"),
            ("가격을 움직이는 요인", "<ol><li><b>프로필렌 가격</b> — 원료 원가</li>"
             "<li><b>폴리에테르 수요</b> — 가구·자동차·건설 경기</li>"
             "<li><b>신규 설비 가동</b> — 대형 설비가 돌기 시작하면 가격이 눌립니다</li>"
             "<li><b>공법 규제</b> — 클로로히드린법 설비 퇴출 정책</li>"
             "<li><b>공동 생산품 가격</b> — 공산화법 설비는 스티렌·MTBE 수익도 함께 봅니다</li></ol>"),
            ("이 페이지의 가격", _PRICE_KO),
        ],
        "en": [
            ("What propylene oxide is", "<p>Propylene oxide (PO) is a chemical intermediate made from propylene. Most of it becomes <b>polyether polyols</b> and then <b>polyurethane foam</b> for furniture, car seats and insulation; the rest goes into propylene glycol and surfactants.</p>"),
            ("China's market", "<p>China is the world's largest PO producer. The wastewater-heavy <b>chlorohydrin route</b> used to dominate, but capacity using <b>HPPO</b> (hydrogen peroxide) and <b>co-oxidation</b> routes that also make styrene or MTBE has grown quickly. New plants keep adding supply.</p>"),
            ("What moves the price", "<ol><li><b>Propylene price</b> — the feedstock cost</li>"
             "<li><b>Polyether demand</b> — furniture, auto and construction activity</li>"
             "<li><b>New capacity</b> — large start-ups weigh on prices</li>"
             "<li><b>Process rules</b> — the phase-out of chlorohydrin plants</li>"
             "<li><b>Co-product prices</b> — co-oxidation plants also depend on styrene and MTBE margins</li></ol>"),
            ("About the price on this page", _PRICE_EN),
        ],
    },
    "hrc": {
        "ko": [
            ("열연강판이란", "<p>열연강판(HRC, 열연코일)은 슬래브를 높은 온도에서 눌러 편 판재입니다. 강관, 자동차 부품, 기계, 조선, 건설 구조물에 쓰이고, 냉연강판·도금강판의 원판이 되기도 합니다. 철강 판재 가격의 기준 품목으로 많이 봅니다.</p>"),
            ("중국 시장 구조", "<p>중국은 세계 조강 생산의 절반 이상을 맡고 있습니다. 허베이, 장쑤, 산둥 등에 대형 제철소가 모여 있고, 상하이선물거래소에 열연강판 선물이 거래돼 현물가의 기준 역할을 합니다. 내수가 약할 때는 수출이 늘어 다른 나라 철강 가격에도 영향을 줍니다.</p>"),
            ("가격을 움직이는 요인", "<ol><li><b>원료 가격</b> — 철광석과 점결탄(코크스)</li>"
             "<li><b>내수 경기</b> — 부동산·인프라 건설과 제조업</li>"
             "<li><b>생산 조정</b> — 감산 정책, 환경 규제에 따른 가동 제한</li>"
             "<li><b>수출</b> — 수출 물량과 주요국의 반덤핑 관세</li>"
             "<li><b>선물 시장</b> — 상하이 열연 선물의 움직임</li></ol>"),
            ("이 페이지의 가격", _PRICE_KO),
        ],
        "en": [
            ("What hot-rolled coil is", "<p>Hot-rolled coil (HRC) is steel sheet rolled from slab at high temperature. It is used for pipes, auto parts, machinery, shipbuilding and construction, and is the base material for cold-rolled and coated sheet. It is the usual benchmark for flat-steel prices.</p>"),
            ("China's market", "<p>China produces more than half of the world's crude steel, with large mills in Hebei, Jiangsu and Shandong. HRC futures trade on the Shanghai Futures Exchange and act as a reference for spot prices. When domestic demand is weak, exports rise and affect steel prices elsewhere.</p>"),
            ("What moves the price", "<ol><li><b>Raw materials</b> — iron ore and coking coal</li>"
             "<li><b>Domestic demand</b> — property, infrastructure and manufacturing</li>"
             "<li><b>Output controls</b> — production cuts and environmental curbs</li>"
             "<li><b>Exports</b> — export volumes and anti-dumping duties abroad</li>"
             "<li><b>Futures</b> — moves in Shanghai HRC futures</li></ol>"),
            ("About the price on this page", _PRICE_EN),
        ],
    },
    "pp": {
        "ko": [
            ("폴리프로필렌(PP)이란", "<p>폴리프로필렌은 가장 많이 쓰이는 플라스틱 중 하나입니다. 식품 용기·포장 필름, 자동차 범퍼·내장재, 가전 부품, 부직포·섬유 등에 쓰입니다. 용도에 따라 사출용, 필름용, 섬유용 등 여러 등급으로 나뉩니다.</p>"),
            ("중국 시장 구조", "<p>중국은 세계 최대의 PP 생산국이자 소비국입니다. 원료 프로필렌을 얻는 길이 세 가지인 것이 특징입니다.</p><ul>"
             "<li><b>석유 기반</b> — 나프타 분해</li><li><b>프로판 탈수소(PDH)</b> — 수입 프로판 사용</li><li><b>석탄 기반</b> — 석탄을 올레핀으로 바꾸는 공정</li></ul>"
             "<p>최근 몇 년 대규모 증설이 이어졌고, 다롄상품거래소에 PP 선물이 거래됩니다.</p>"),
            ("가격을 움직이는 요인", "<ol><li><b>원료 가격</b> — 원유, 프로판, 석탄</li>"
             "<li><b>증설</b> — 신규 설비 가동에 따른 공급 증가</li>"
             "<li><b>하류 수요</b> — 포장재·자동차·가전 생산</li>"
             "<li><b>재고</b> — 생산자와 유통 재고 수준</li>"
             "<li><b>선물 시장</b> — 다롄 PP 선물의 움직임</li></ol>"),
            ("이 페이지의 가격", _PRICE_KO),
        ],
        "en": [
            ("What polypropylene is", "<p>Polypropylene (PP) is one of the most widely used plastics: food containers and packaging film, car bumpers and interior parts, appliance parts, nonwovens and fibres. It comes in injection, film and fibre grades, among others.</p>"),
            ("China's market", "<p>China is the world's largest producer and consumer of PP. Its propylene feedstock comes from three routes:</p><ul>"
             "<li><b>Oil-based</b> — naphtha cracking</li><li><b>Propane dehydrogenation (PDH)</b> — using imported propane</li><li><b>Coal-based</b> — coal-to-olefins</li></ul>"
             "<p>Large capacity has been added in recent years, and PP futures trade on the Dalian Commodity Exchange.</p>"),
            ("What moves the price", "<ol><li><b>Feedstock</b> — crude oil, propane and coal</li>"
             "<li><b>New capacity</b> — start-ups add supply</li>"
             "<li><b>Downstream demand</b> — packaging, autos and appliances</li>"
             "<li><b>Inventory</b> — producer and trader stocks</li>"
             "<li><b>Futures</b> — moves in Dalian PP futures</li></ol>"),
            ("About the price on this page", _PRICE_EN),
        ],
    },
    "benzene": {
        "ko": [
            ("벤젠이란", "<p>벤젠은 대표적인 방향족 기초유분입니다. 대부분 다른 화학제품의 원료로 쓰입니다.</p><ul>"
             "<li><b>스티렌(SM)</b> → PS·ABS 수지</li><li><b>페놀</b> → 비스페놀A·폴리카보네이트</li>"
             "<li><b>카프로락탐</b> → 나일론</li><li><b>아닐린</b> → MDI(폴리우레탄)</li></ul>"),
            ("중국 시장 구조", "<p>중국은 세계 최대의 벤젠 소비국입니다. 정유·석유화학 공장(개질·납사분해)에서 나오는 석유계 벤젠과, 코크스 공장 부산물을 정제한 벤젠이 함께 쓰입니다. "
             "부족분은 수입하는데, <b>한국은 중국의 주요 벤젠 공급국</b>입니다. 화동 지역 항구 재고가 가격의 중요한 지표입니다.</p>"),
            ("가격을 움직이는 요인", "<ol><li><b>원유 가격</b></li>"
             "<li><b>하류 수익성</b> — 특히 스티렌 마진</li>"
             "<li><b>항구 재고</b> — 화동 지역 재고 증감</li>"
             "<li><b>수입 물량</b> — 한국 등에서 들어오는 물량</li>"
             "<li><b>정유·석화 설비 가동률</b></li></ol>"),
            ("이 페이지의 가격", _PRICE_KO),
        ],
        "en": [
            ("What benzene is", "<p>Benzene is the main aromatic building block, used almost entirely to make other chemicals:</p><ul>"
             "<li><b>Styrene (SM)</b> → PS and ABS resins</li><li><b>Phenol</b> → bisphenol A and polycarbonate</li>"
             "<li><b>Caprolactam</b> → nylon</li><li><b>Aniline</b> → MDI for polyurethane</li></ul>"),
            ("China's market", "<p>China is the world's largest benzene consumer. It uses petroleum benzene from refineries and crackers alongside benzene refined from coke-oven by-products, and imports the shortfall — <b>South Korea is one of China's main benzene suppliers</b>. Port inventories in East China are a key price signal.</p>"),
            ("What moves the price", "<ol><li><b>Crude oil</b></li>"
             "<li><b>Downstream margins</b> — especially styrene</li>"
             "<li><b>Port inventories</b> — stock changes in East China</li>"
             "<li><b>Imports</b> — cargoes from Korea and elsewhere</li>"
             "<li><b>Refinery and cracker run rates</b></li></ol>"),
            ("About the price on this page", _PRICE_EN),
        ],
    },
    "coal": {
        "ko": [
            ("석탄이란", "<p>석탄은 쓰임에 따라 크게 둘로 나뉩니다. 발전소에서 태우는 <b>발전용탄(연료탄)</b>과, 코크스로 만들어 철을 녹이는 데 쓰는 <b>제철용 점결탄</b>입니다. 발전용탄은 보통 발열량(예: 5,500kcal/kg) 기준으로 가격을 매깁니다.</p>"),
            ("중국 시장 구조", "<p>중국은 세계 석탄 생산과 소비의 절반가량을 차지합니다. 산시, 내몽골, 산시(陕西)가 3대 산지이고, 인도네시아·호주·몽골·러시아 등에서 수입도 합니다. 북부 항구(친황다오 등)의 재고와 가격이 시장의 기준으로 쓰입니다.</p>"),
            ("가격을 움직이는 요인", "<ol><li><b>전력 수요</b> — 여름 냉방·겨울 난방 성수기</li>"
             "<li><b>수력 발전량</b> — 강수량이 적으면 석탄 발전이 늘어납니다</li>"
             "<li><b>탄광 안전 점검·증산 정책</b></li>"
             "<li><b>수입 물량</b></li>"
             "<li><b>항구·발전소 재고</b></li></ol>"),
            ("이 페이지의 가격", _PRICE_KO),
        ],
        "en": [
            ("What coal is", "<p>Coal splits into two main markets: <b>thermal coal</b> burned in power plants and <b>coking coal</b> turned into coke for iron making. Thermal coal is usually priced by calorific value (for example 5,500 kcal/kg).</p>"),
            ("China's market", "<p>China accounts for about half of the world's coal production and consumption. Shanxi, Inner Mongolia and Shaanxi are the three main producing regions, and China also imports from Indonesia, Australia, Mongolia and Russia. Inventories and prices at northern ports such as Qinhuangdao serve as the market benchmark.</p>"),
            ("What moves the price", "<ol><li><b>Power demand</b> — summer cooling and winter heating peaks</li>"
             "<li><b>Hydropower output</b> — dry seasons mean more coal-fired generation</li>"
             "<li><b>Mine safety inspections and output policy</b></li>"
             "<li><b>Imports</b></li>"
             "<li><b>Port and power-plant stocks</b></li></ol>"),
            ("About the price on this page", _PRICE_EN),
        ],
    },
    "neodymium-oxide": {
        "ko": [
            ("산화네오디뮴이란", "<p>산화네오디뮴(Nd₂O₃)은 경희토류의 대표 산화물로, 가장 강한 영구자석인 <b>네오디뮴(NdFeB) 자석</b>의 핵심 원료입니다. 이 자석은 전기차 구동모터, 풍력발전기, 가전 모터, 스마트폰 부품, 산업용 로봇에 쓰입니다. 시장에서는 프라세오디뮴과 섞인 <b>PrNd 산화물</b> 형태로도 많이 거래됩니다.</p>"),
            ("중국 시장 구조", "<p>중국은 희토류 채굴의 대부분과 분리·정제의 약 90%를 맡고 있습니다. 내몽골(경희토류), 장시·광둥(중희토류 이온흡착형 광상)이 주요 산지이고 미얀마산 원료도 들여옵니다. "
             "정부가 채굴·제련 총량을 관리하고, 일부 희토류와 관련 기술에는 수출 통제를 적용하고 있습니다.</p>"),
            ("가격을 움직이는 요인", "<ol><li><b>자석 수요</b> — 전기차·풍력·가전 생산</li>"
             "<li><b>생산 총량 관리</b> — 채굴·제련 할당량</li>"
             "<li><b>수출 통제</b> — 허가 절차와 대상 품목 변화</li>"
             "<li><b>원료 수입</b> — 미얀마 등에서 들어오는 원료</li>"
             "<li><b>업계 재편</b> — 대형 희토류 그룹 중심의 생산 조정</li></ol>"),
            ("이 페이지의 가격", _PRICE_KO),
        ],
        "en": [
            ("What neodymium oxide is", "<p>Neodymium oxide (Nd₂O₃) is the key light rare-earth oxide and the core raw material for <b>NdFeB magnets</b>, the strongest permanent magnets. They go into EV traction motors, wind turbines, appliance motors, phone components and industrial robots. It is also widely traded blended with praseodymium as <b>PrNd oxide</b>.</p>"),
            ("China's market", "<p>China accounts for most rare-earth mining and roughly 90% of separation and refining. Inner Mongolia (light rare earths) and Jiangxi and Guangdong (ionic-clay deposits) are the main sources, and feedstock is also imported from Myanmar. "
             "The government sets total mining and smelting quotas and applies export controls to some rare earths and related technologies.</p>"),
            ("What moves the price", "<ol><li><b>Magnet demand</b> — EVs, wind power and appliances</li>"
             "<li><b>Production quotas</b> — mining and smelting allocations</li>"
             "<li><b>Export controls</b> — licensing and changes in covered items</li>"
             "<li><b>Feedstock imports</b> — from Myanmar and elsewhere</li>"
             "<li><b>Industry consolidation</b> — output managed by large rare-earth groups</li></ol>"),
            ("About the price on this page", _PRICE_EN),
        ],
    },
    "ethylene-glycol": {
        "ko": [
            ("에틸렌글리콜(MEG)이란", "<p>모노에틸렌글리콜(MEG)은 <b>폴리에스터</b>의 원료입니다. 대부분 PTA와 반응해 의류용 폴리에스터 섬유와 PET 병 수지가 되고, 일부는 자동차 부동액으로 쓰입니다.</p>"),
            ("중국 시장 구조", "<p>중국은 세계 최대의 MEG 소비국입니다. 석유(에틸렌) 기반 공장, 중국 특유의 <b>석탄 기반 MEG</b> 공장, 그리고 중동 등에서 들어오는 수입 물량이 함께 시장을 이룹니다. "
             "화동 지역(장자강 등) 항구 재고가 가격의 중요한 지표이고, 다롄상품거래소에 MEG 선물이 거래됩니다.</p>"),
            ("가격을 움직이는 요인", "<ol><li><b>폴리에스터 가동률</b> — 섬유·병 수지 공장의 수요</li>"
             "<li><b>항구 재고</b> — 화동 지역 재고 증감</li>"
             "<li><b>원료 가격</b> — 원유(에틸렌)와 석탄</li>"
             "<li><b>수입 물량</b> — 중동·북미산 물량</li>"
             "<li><b>선물 시장</b> — 다롄 MEG 선물의 움직임</li></ol>"),
            ("이 페이지의 가격", _PRICE_KO),
        ],
        "en": [
            ("What ethylene glycol is", "<p>Monoethylene glycol (MEG) is a raw material for <b>polyester</b>. Most of it reacts with PTA to make polyester fibre for clothing and PET bottle resin; some is used in antifreeze.</p>"),
            ("China's market", "<p>China is the world's largest MEG consumer. Supply comes from oil-based (ethylene) plants, China's distinctive <b>coal-based MEG</b> plants and imports from the Middle East and elsewhere. "
             "Port inventories in East China (Zhangjiagang and nearby) are a key price signal, and MEG futures trade on the Dalian Commodity Exchange.</p>"),
            ("What moves the price", "<ol><li><b>Polyester run rates</b> — demand from fibre and bottle-resin plants</li>"
             "<li><b>Port inventories</b> — stock changes in East China</li>"
             "<li><b>Feedstock</b> — crude oil (ethylene) and coal</li>"
             "<li><b>Imports</b> — cargoes from the Middle East and North America</li>"
             "<li><b>Futures</b> — moves in Dalian MEG futures</li></ol>"),
            ("About the price on this page", _PRICE_EN),
        ],
    },
}
