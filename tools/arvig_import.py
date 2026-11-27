import json, sys, re, collections, pyreadr
from shapely.geometry import shape, Point
from shapely.strtree import STRtree
ARV, DOCS = sys.argv[1], sys.argv[2]
df = pyreadr.read_r(ARV)['arvig']
F = json.load(open(DOCS + '/faelle.json'))
G = json.load(open(DOCS + '/gemeinden.geojson'))['features']
geoms = [shape(f['geometry']) for f in G]
tree = STRtree(geoms)
props = [f['properties'] for f in G]
byags = {p['ags']: p for p in props}
print('type urls', type(F[0]['urls']).__name__)
seen = {(r['date'], r['ags']) for r in F}
CAT = {'arson': 'Brandanschlag', 'assault': 'Körperverletzung', 'miscellaneous attack': 'Angriffe auf Unterkünfte',
       'suspicion': 'Verdachtsfall', 'other': 'Sonstige'}
def cat(c):
    parts = [p.strip() for p in c.split('&') if p.strip() != 'demonstration']
    if not parts: return None
    pr = ['arson', 'assault', 'miscellaneous attack', 'suspicion', 'other']
    parts.sort(key=lambda p: pr.index(p) if p in pr else 9)
    return CAT.get(parts[0])
new, skip = [], collections.Counter()
nxt = max(int(r['id'][4:]) for r in F) + 1
for row in df.itertuples():
    k = cat(row.category_en)
    if not k: skip['demo'] += 1; continue
    desc = (row.description if isinstance(row.description, str) else '').strip()
    if k == 'Angriffe auf Unterkünfte':
        t = desc.lower()
        if re.search(r'unterkunft|heim|container|notunterkunft|turnhalle|wohnung|haus der|aufnahme', t): pass
        elif re.search(r'bedroh|beleidig|beschimpf', t): k = 'Bedrohung'
        elif re.search(r'schmier|hakenkreuz|graffiti|beschädig|sprüh', t): k = 'Sachbeschädigung'
        else: k = 'Angriffe auf Geflüchtete'
    date = str(row.date)[:10]
    ags = None
    try:
        pt = Point(float(row.longitude), float(row.latitude))
        for i in tree.query(pt):
            if geoms[i].contains(pt): ags = props[i]['ags']; break
    except Exception: pass
    if not ags:
        cid = str(row.community_id).split('.')[0].zfill(12)
        a = cid[:5] + cid[9:]
        if a in byags: ags = a
    if not ags: skip['noags'] += 1; continue
    if (date, ags) in seen: skip['dup'] += 1; continue
    seen.add((date, ags))
    p = byags[ags]
    src = row.source if isinstance(row.source, str) else ''
    urls = [u for u in src.split() if u.startswith('http')]
    new.append({'id': 'CRG-%05d' % nxt, 'date': date, 'state': row.state, 'ags': ags, 'gemeinde': p['name'],
                'ort': p['name'], 'kategorie': k, 'beschreibung': desc,
                'quelle': 'Mut gegen rechte Gewalt / ARVIG', 'quellentyp': 'Stiftung/Liste', 'drucksache': '',
                'urls': ' '.join(urls or ['https://github.com/davben/arvig']) if isinstance(F[0]['urls'], str) else urls})
    nxt += 1
print('neu', len(new), dict(skip))
print(collections.Counter(r['date'][:4] for r in new), collections.Counter(r['kategorie'] for r in new))
print('src sample', df['source'].head(3).tolist())
if len(sys.argv) > 3:
    F.extend(new); F.sort(key=lambda r: (r['date'], r['id']))
    json.dump(F, open(DOCS + '/faelle.json', 'w'), ensure_ascii=False)
    print('geschrieben', len(F))
