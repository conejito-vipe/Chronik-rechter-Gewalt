"""Opferperspektive (Brandenburg): verlinkt Fälle auf die aktuelle Einzelseite der Chronik, ersetzt Platzhaltertexte durch
den Chroniktext (Straßennamen entfernt) und ergänzt belegte Fälle, die noch fehlen (z. B. Propaganda).
Daten: opferperspektive.de (WordPress-Schnittstelle + Chronikliste, Abruf 27.11.2026), Koordinaten bis 2021 aus Tatort Rechts.
Aufruf: python3 op_link.py op.json tatortrechts.json docs [--write]"""
import json, sys, re, collections, datetime
from shapely.geometry import shape, Point
from shapely.strtree import STRtree
OPF, TRF, DOCS = sys.argv[1], sys.argv[2], sys.argv[3]
O = json.load(open(OPF, encoding='utf-8'))
TR = [x for x in json.load(open(TRF, encoding='utf-8'))['incidents'] if x['chron'] == 'Opferperspektive']
F = json.load(open(f'{DOCS}/faelle.json', encoding='utf-8'))
G = json.load(open(f'{DOCS}/gemeinden.geojson', encoding='utf-8'))['features']
geoms = [shape(f['geometry']) for f in G]; tree = STRtree(geoms); props = [f['properties'] for f in G]
src = open(DOCS + '/../tools/tatortrechts_import.py', encoding='utf-8').read()
ns = {'re': re}; exec(src[src.index('OK_WORDS'):src.index('old = collections')], ns)
mask, kat = ns['mask'], ns['kat']
lsrc = open(DOCS + '/../tools/link_sources.py', encoding='utf-8').read()
exec(lsrc[lsrc.index('GRP = {'):lsrc.index('idx = collections')], ns); fits = ns['fits']
MON = {m: i + 1 for i, m in enumerate(['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'])}
def pdate(t):
    m = re.match(r'(\d+)\.\s*(\w+)\s+(\d{4})', t or '')
    return '%s-%02d-%02d' % (m.group(3), MON.get(m.group(2), 0), int(m.group(1))) if m and m.group(2) in MON else None
slug = lambda u: u.rstrip('/').split('/')[-1]
posts = {p['id']: p for p in O['posts']}
bylist = collections.defaultdict(list)
for l in O['liste']:
    bylist[(pdate(l['datum']), (l['h3'] or '').strip())].append(l)
bb = {}
for p in props:
    if p['land'] == 'Brandenburg': bb.setdefault(p['name'].split(',')[0].strip().lower(), p['ags'])
def ags_name(o):
    o = (o or '').strip().lower()
    return bb.get(o) or bb.get(re.split(r'\s*[\(/,]|\s+-\s+', o)[0].strip())
trgeo = {slug(x['url']): x['geo'] for x in TR}
def ags_geo(g):
    pt = Point(*g)
    for i in tree.query(pt):
        if geoms[i].contains(pt): return props[i]['ags']
for p in O['posts']:
    l = posts and None
    meta = [m for m in O['liste'] if m['key'] == str(p['id'])]
    if not meta: meta = bylist.get((p['date'], p['city'].strip()), [])
    p['stadt'] = meta[0]['stadt'] if len(meta) == 1 and meta[0]['stadt'] else p['city']
    g = trgeo.get(slug(p['link']))
    p['ags'] = (ags_geo(g) if g else None) or ags_name(p['stadt']) or ags_name(p['city'])
    p['kat'] = kat({'title': '', 'desc': p['text']})
byslug = {slug(p['link']): p for p in O['posts']}
idx = collections.defaultdict(list)
for p in O['posts']:
    if p['ags']: idx[(p['date'], p['ags'])].append(p)
GEN = 'https://www.opferperspektive.de/category/chronologie-rechter-angriffe'
PLACE = re.compile(r'^Vorfall in .* am \d{4}-\d{2}-\d{2}, eingeordnet als')
QOP = 'Opferperspektive e.V. – Chronologie rechter Angriffe (Brandenburg)'
st = collections.Counter(); usedp = set()
for r in F:
    us = (r['urls'] or '').split(); p = None
    nu = []
    for u in us:
        if '/rechte-angriffe/chronologie-rechter-angriffe/' in u and slug(u) in byslug:
            p = byslug[slug(u)]; u = p['link']; st['Link aktualisiert'] += 1
        nu.append(u)
    us = list(dict.fromkeys(nu))
    if p is None and r['state'] == 'Brandenburg' and us and all(u == GEN for u in us):
        c = [q for q in idx.get((r['date'], r['ags']), []) if fits(q['kat'], r['kategorie']) and q['id'] not in usedp]
        if len(c) == 1:
            p = c[0]; us = [p['link']]; st['neu verlinkt'] += 1
        else: st['ohne eindeutige Einzelseite'] += 1
    if p is not None:
        usedp.add(p['id'])
        if PLACE.match(r['beschreibung'] or '') and p['text']:
            r['beschreibung'] = mask(p['text']); st['Platzhaltertext ersetzt'] += 1
    r['urls'] = ' '.join(us)
have = {(r['date'], r['ags']) for r in F}
nxt = max(int(r['id'][4:]) for r in F) + 1
new = []
for p in sorted(O['posts'], key=lambda p: (p['date'], p['id'])):
    if p['id'] in usedp: continue
    if not p['ags']: st['neu: Gemeinde unklar'] += 1; continue
    if (p['date'], p['ags']) in have: st['neu: Tag/Gemeinde schon belegt'] += 1; continue
    g = next(q for q in props if q['ags'] == p['ags'])
    new.append({'id': 'CRG-%05d' % nxt, 'date': p['date'], 'state': 'Brandenburg', 'ags': p['ags'], 'gemeinde': g['name'], 'ort': g['name'],
                'kategorie': p['kat'], 'beschreibung': mask(p['text']), 'quelle': QOP, 'quellentyp': 'Beratungsstelle/NGO', 'drucksache': '', 'urls': p['link']})
    have.add((p['date'], p['ags'])); nxt += 1
st['neu ergänzt'] = len(new)
print(dict(st)); print('neue Kategorien', collections.Counter(r['kategorie'] for r in new).most_common()); print('neue Jahre', sorted(collections.Counter(r['date'][:4] for r in new).items()))
if '--write' in sys.argv:
    F.extend(new); F.sort(key=lambda r: (r['date'], r['id']))
    json.dump(F, open(f'{DOCS}/faelle.json', 'w', encoding='utf-8'), ensure_ascii=False); print('geschrieben', len(F))
