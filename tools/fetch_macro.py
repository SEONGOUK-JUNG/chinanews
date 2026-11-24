"""Refresh both macro panels from dated Trading Economics observations.

python fetch_macro.py --data-dir ../data
Requires requests and beautifulsoup4. No forecast or inferred reference month.
All sources must validate before either output is replaced.
"""
import argparse
import calendar
import datetime as dt
import json
import math
import os
from pathlib import Path
import re
import requests
from bs4 import BeautifulSoup

BASE = 'https://tradingeconomics.com/china/'
KST = dt.timezone(dt.timedelta(hours=9))
MONTHS = {m: i for i, m in enumerate(calendar.month_abbr) if m}
MACRO = ['manufacturing-pmi', 'non-manufacturing-pmi', 'services-pmi',
         'gdp-growth-annual', 'inflation-cpi', 'producer-prices-change',
         'unemployment-rate', 'interest-rate', 'cash-reserve-ratio',
         'balance-of-trade', 'retail-sales', 'currency', 'stock-market']
RATES = ['loan-prime-rate-5y', 'government-bond-yield', 'interbank-rate',
         'money-supply-m2', 'loan-growth', 'housing-index']

def number(text):
    value = float(text.strip().replace(',', '').replace('%', '').replace('−', '-'))
    if not math.isfinite(value):
        raise ValueError('non-finite observation')
    return value

def month_ref(text, today):
    m = re.fullmatch(r'([A-Za-z]{3})/(\d{2})', text.strip())
    if not m or m[1] not in MONTHS:
        raise ValueError('Unrecognized reference: ' + text)
    date = dt.date(2000 + int(m[2]), MONTHS[m[1]], 1)
    if date > today or (today - date).days > 150:
        raise ValueError('Stale/future reference: ' + text)
    return date.isoformat()[:7]

def parse_sources(summary, m2, bond, today):
    observations = {}
    for row in BeautifulSoup(summary, 'html.parser').select('tr'):
        cells = row.find_all('td', recursive=False)
        if len(cells) != 7:
            continue
        a = cells[0].find('a', href=True)
        if not a or not a['href'].startswith('/china/'):
            continue
        key = a['href'].split('/')[-1]
        if key not in set(MACRO + RATES):
            continue
        observations[key] = dict(value=number(cells[1].get_text()),
                                 previous=number(cells[2].get_text()),
                                 ref=month_ref(cells[6].get_text(), today),
                                 source_url=BASE + key)

    # M2 summary table is a stock in CNY billion, NOT its YoY rate.
    releases = []
    for row in BeautifulSoup(m2, 'html.parser').select('tr[data-category="Money Supply M2"]'):
        actual, previous, reference = (row.select_one('#' + x) for x in ('actual', 'previous', 'reference'))
        if actual is None or not actual.get_text(strip=True):
            continue  # Future calendar rows contain forecasts, not observations.
        released = dt.date.fromisoformat(row.find('td').get_text(strip=True))
        if released > today:
            continue
        month = MONTHS[reference.get_text(strip=True)]
        year = released.year - (month > released.month)
        ref = dt.date(year, month, 1)
        if (today - ref).days > 100:
            continue
        if '%' not in actual.get_text() or '%' not in previous.get_text():
            raise ValueError('M2 calendar must report percentage growth')
        releases.append((released, dict(value=number(actual.get_text()), previous=number(previous.get_text()),
                                       ref=ref.isoformat()[:7], source_url=BASE + 'money-supply-m2')))
    if not releases:
        raise ValueError('No recent actual M2 growth release')
    observations['money-supply-m2'] = max(releases, key=lambda x: x[0])[1]

    row = BeautifulSoup(bond, 'html.parser').select_one('tr[data-symbol="GCNY10YR:GOV"]')
    if row is None:
        raise ValueError('Missing 10Y bond quote')
    source_date = row.select_one('#date').get_text(strip=True)
    m = re.fullmatch(r'([A-Za-z]{3})/(\d{1,2})', source_date)
    if not m:
        raise ValueError('Unknown bond date: ' + source_date)
    date = dt.date(today.year, MONTHS[m[1]], int(m[2]))
    if date > today:
        date = date.replace(year=date.year - 1)
    if (today - date).days > 10:
        raise ValueError('Stale bond quote')
    observations['government-bond-yield'] = dict(value=number(row.select_one('#p').get_text()),
        previous=None, ref=date.isoformat(), source_url=BASE + 'government-bond-yield')
    missing = set(MACRO + RATES) - observations.keys()
    if missing:
        raise ValueError('Missing indicators: ' + ', '.join(sorted(missing)))
    return observations

def build_document(old, keys, observations, now):
    if len(old['indicators']) != len(keys):
        raise ValueError('Unexpected panel schema')
    doc = dict(old)
    doc.update(as_of=now.date().isoformat(), updated_at_kst=now.isoformat(timespec='seconds'),
               note='Daily source check; each card shows its observation period. Latest published actuals only.')
    doc['indicators'] = []
    for original, key in zip(old['indicators'], keys):
        item = dict(original)
        item.update(observations[key])
        item['ref_en'] = item['ref']
        item['hint'] = '발표치 · 기준기간 확인'
        item['hint_en'] = 'published actual · reference period shown'
        value = item['value']
        if key == 'gdp-growth-annual':
            year, month = map(int, item['ref'].split('-'))
            item['ref'] = item['ref_en'] = f'{year} Q{(month - 1) // 3 + 1}'
        if key == 'manufacturing-pmi':
            item.update(label='RatingDog 제조업 PMI', label_en='RatingDog Manufacturing PMI')
        if key == 'services-pmi':
            item.update(label='RatingDog 서비스 PMI', label_en='RatingDog Services PMI')
        if key == 'balance-of-trade':
            item['display'] = f'${value:,.1f}B'
        elif key == 'stock-market':
            item['display'] = f'{value:,.0f}'
        elif key == 'currency':
            item['display'] = f'{value:.2f}'
        elif key.endswith('-pmi'):
            item['display'] = f'{value:.1f}'
        else:
            item['display'] = f'{value:.2f}%'
        doc['indicators'].append(item)
    return doc

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-dir', type=Path, default=Path(__file__).resolve().parent.parent / 'data')
    parser.add_argument('--fixture-dir', type=Path, help='Offline parser verification only')
    args = parser.parse_args()
    pages = []
    for slug, fixture in [('indicators', 'te_indicators.html'), ('money-supply-m2', 'te_m2.html'),
                          ('government-bond-yield', 'te_bond.html')]:
        if args.fixture_dir:
            pages.append((args.fixture_dir / fixture).read_text(encoding='utf-8-sig'))
        else:
            response = requests.get(BASE + slug, timeout=45, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
            pages.append(response.content.decode('utf-8-sig', errors='replace'))
    now = dt.datetime.now(KST)
    observations = parse_sources(*pages, now.date())
    outputs = {}
    for name, keys in [('macro_latest.json', MACRO), ('rates_property_latest.json', RATES)]:
        path = args.data_dir / name
        old = json.loads(path.read_text(encoding='utf-8-sig'))
        outputs[path] = build_document(old, keys, observations, now)
    for path, doc in outputs.items():
        temp = path.with_suffix('.json.tmp')
        temp.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        os.replace(temp, path)
        print(f'{path.name}: {len(doc["indicators"])} observations; checked {doc["as_of"]}')

if __name__ == '__main__':
    main()
