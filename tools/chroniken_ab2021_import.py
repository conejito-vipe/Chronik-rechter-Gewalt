"""Fälle der Beratungsstellen-Chroniken ab Mai 2021 (Abruf der Websites am 27.11.2026):
RAA Sachsen, ReachOut (Berlin), LOBBI (MV), ezra (Thüringen), Mobile Opferberatung (Sachsen-Anhalt), München-Chronik,
Keine Randnotiz (Bremen/Bremerhaven), Hessenschauthin (Hessen, Nachfolge von response.), Opferberatung Rheinland (NRW).
Gemeinde über Koordinate (wenn vorhanden) oder Ortsname im jeweiligen Land; Straßennamen werden entfernt; Kategorie wie beim
Tatort-Rechts-Import; Dubletten (gleicher Tag, gleiche Gemeinde wie ein vorhandener Fall, in Großstädten zusätzlich gleiche
Kategorie) werden ausgelassen. Aufruf: python3 chroniken_ab2021_import.py <ordner mit chronik_*.json> docs [--write]"""
import json, sys, re, glob, os, collections, unicodedata
from shapely.geometry import shape, Point
from shapely.strtree import STRtree
SRC, DOCS = sys.argv[1], sys.argv[2]
START = '2021-05-01'
F = json.load(open(f'{DOCS}/faelle.json', encoding='utf-8'))
G = json.load(open(f'{DOCS}/gemeinden.geojson', encoding='utf-8'))['features']
geoms = [shape(f['geometry']) for f in G]; tree = STRtree(geoms); props = [f['properties'] for f in G]
byags = {p['ags']: p for p in props}
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tatortrechts_import.py'), encoding='utf-8').read()
ns = {'re': re}; exec(src[src.index('OK_WORDS'):src.index('old = collections')], ns)
mask, kat = ns['mask'], ns['kat']
def norm(s):
    s = unicodedata.normalize('NFC', (s or '').lower()).strip()
    s = re.sub(r'^(stadt|landkreis|lk|kreis)\s+', '', s)
    s = re.sub(r'\s*-\s*', '-', s)
    s = re.sub(r',?\s*(stadt|hansestadt|universitätsstadt|kreisstadt|große kreisstadt)$', '', s)
    s = re.sub(r'\s+(an der|a\.d\.|am|in der|i\.)\s+.*$', lambda m: m.group(0), s)
    return s.strip()
IDX = collections.defaultdict(dict)
for p in props:
    n = norm(p['name'].split(',')[0])
    IDX[p['land']].setdefault(n, p['ags'])
    IDX[p['land']].setdefault(re.split(r'\s*[\(/]', n)[0].strip(), p['ags'])
FIRST = collections.defaultdict(collections.Counter)
for p in props: FIRST[p['land']][norm(p['name']).split(' ')[0]] += 1
for p in props:
    w = norm(p['name']).split(' ')[0]
    if FIRST[p['land']][w] == 1: IDX[p['land']].setdefault(w, p['ags'])
def by_name(land, name):
    if not name: return None
    n = norm(name)
    cands = [n, re.split(r'\s*[\(/,]|\s+-\s+|\s*–\s*', n)[0].strip(), n.split('-')[0].strip(), n.split(' ')[0]]
    for c in cands:
        if c and c in IDX[land]: return IDX[land][c]
    return None
def by_geo(lon, lat):
    try:
        pt = Point(float(lon), float(lat))
    except (TypeError, ValueError):
        return None
    for i in tree.query(pt):
        if geoms[i].contains(pt): return props[i]['ags']
SHORT = re.compile(r'\[/?et_pb[^\]]*\]')
def recs():
    for f in sorted(glob.glob(os.path.join(SRC, 'chronik_*.json'))):
        for r in json.load(open(f, encoding='utf-8'))['recs']:
            yield r
QUELLE = {'raa-sachsen': ('RAA Sachsen – Chronik', 'Sachsen'), 'reachout': ('ReachOut – Chronik (Berlin)', 'Berlin'),
          'lobbi': ('LOBBI – Chronologie (Mecklenburg-Vorpommern)', 'Mecklenburg-Vorpommern'), 'ezra': ('ezra – Chronik (Thüringen)', 'Thüringen'),
          'mobile-opferberatung': ('Mobile Opferberatung – Chronik (Sachsen-Anhalt)', 'Sachsen-Anhalt'),
          'muenchen-chronik': ('München-Chronik', 'Bayern'), 'keine-randnotiz': ('Keine Randnotiz – Chronik (Bremen)', 'Bremen'),
          'hessenschauthin': ('Hessenschauthin – Chronik (Hessen)', 'Hessen'),
          'opferberatung-rheinland': ('Opferberatung Rheinland – Chronik (Nordrhein-Westfalen)', 'Nordrhein-Westfalen')}
st = collections.Counter(); out = []
for r in recs():
    s = r['site']; q, land = QUELLE[s]
    date, title, text, ags, urls = r.get('date'), r.get('title') or '', r.get('text') or '', None, [r.get('url')]
    if s == 'opferberatung-rheinland' and not date:
        m = re.match(r'(\d{1,2})\.(?:/\d{1,2}\.)?(\d{1,2})\.(\d{2,4})\s*:?\s*(.*)', r.get('place') or '')
        if m:
            y = m.group(3); y = ('20' + y) if len(y) == 2 else y
            date = '%s-%02d-%02d' % (y, int(m.group(2)), int(m.group(1))); r['place'] = m.group(4)
    if not date or date < START: st['vor Mai 2021 oder ohne Datum'] += 1; continue
    if s == 'keine-randnotiz':
        g = (r.get('geometry') or {}).get('coordinates')
        ags = by_geo(*g) if g else None
        ags = ags or ('04012000' if r['place'] == 'Bremerhaven' else '04011000')
        title, text = r.get('headline') or '', r.get('text_plain') or r.get('summary') or ''
        if r.get('types'): r['_types'] = r['types']
    elif s == 'reachout':
        ags = by_geo(r.get('lon'), r.get('lat')) or '11000000'
        title = ''
    elif s == 'muenchen-chronik':
        if 'category-ba-' in r.get('cls', ''): ags = '09162000'
    elif s == 'hessenschauthin':
        place = title.split(':')[0] if ':' in title else ''
        ags = by_name(land, place) or next((by_name(land, c) for c in r.get('cats', []) if by_name(land, c)), None)
        if text.startswith(title): text = text[len(title):].strip()
        text = re.sub(r'\s*Quelle\s+.*$', '', text)
    elif s == 'mobile-opferberatung':
        m = re.match(r'[\d.]+\s+(.*?)\s*(?:\((.*)\))?$', title)
        place = m.group(1) if m else title
        ags = by_name(land, place) or (by_name(land, m.group(2)) if m and m.group(2) else None)
        text = SHORT.sub(' ', text); text = re.sub(r'\s+', ' ', text).strip()
        text = re.sub(r'^(Anlaufstelle \w+|Mobile Opferberatung)[^.]*?(eigener Bericht|Bericht)\s*', '', text); title = ''
    else:
        ags = by_name(land, r.get('place')) or (by_name(land, r.get('county')) if r.get('county') else None)
    if not ags or ags not in byags: st['Gemeinde nicht zuordenbar'] += 1; continue
    body = text if not title or text.startswith(title) else f'{title}. {text}'
    if not body.strip(): st['ohne Text'] += 1; continue
    x = {'title': '', 'desc': body, 'fac': ''}
    if r.get('_types'):
        t = ' '.join(r['_types']).lower()
        x['fac'] = 'propaganda' if t == 'propaganda' else ('körperverletzung' if 'körperverletzung' in t or 'angriff' in t else ('bedrohung' if 'bedroh' in t or 'beleidig' in t else ('sachbeschädigung' if 'sachbesch' in t else '')))
    if r.get('src_url', '').startswith('http'): urls.append(r['src_url'])
    out.append({'date': date, 'ags': ags, 'kat': kat(x), 'text': mask(body), 'quelle': q, 'urls': ' '.join(u for u in dict.fromkeys(urls) if u), 'site': s})
old = collections.defaultdict(set)
for r in F: old[(r['date'], r['ags'])].add(r['kategorie'])
EWZ = {p['ags']: p.get('ewz') or 0 for p in props}
nxt = max(int(r['id'][4:]) for r in F) + 1; new = []; seen = set()
for o in sorted(out, key=lambda o: (o['date'], o['site'])):
    k = (o['date'], o['ags'], re.sub(r'\W+', '', o['text'].lower())[:100])
    if k in seen: st['doppelt in Quelle'] += 1; continue
    seen.add(k)
    hit = old.get((o['date'], o['ags']))
    if hit and (EWZ[o['ags']] < 100000 or o['kat'] in hit): st['Dublette'] += 1; continue
    p = byags[o['ags']]
    new.append({'id': 'CRG-%05d' % nxt, 'date': o['date'], 'state': p['land'], 'ags': o['ags'], 'gemeinde': p['name'], 'ort': p['name'],
                'kategorie': o['kat'], 'beschreibung': o['text'], 'quelle': o['quelle'], 'quellentyp': 'Beratungsstelle/NGO', 'drucksache': '', 'urls': o['urls']})
    nxt += 1; st['neu: ' + o['site']] += 1
print(json.dumps(dict(st), ensure_ascii=False, indent=0))
print('neu gesamt', len(new), collections.Counter(r['kategorie'] for r in new).most_common())
print('Jahre', sorted(collections.Counter(r['date'][:4] for r in new).items()))
if '--write' in sys.argv:
    F.extend(new); F.sort(key=lambda r: (r['date'], r['id']))
    json.dump(F, open(f'{DOCS}/faelle.json', 'w', encoding='utf-8'), ensure_ascii=False); print('geschrieben', len(F))
