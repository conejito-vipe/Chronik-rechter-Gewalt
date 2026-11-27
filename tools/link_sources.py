"""Verlinkt Fälle mit allgemeinem Quellenlink (Opferperspektive-Übersichtsseite, ARVIG-Repository) auf die Einzelseite
des Falls in der Chronik der Beratungsstelle (aus Tatort Rechts). Zuordnung: gleiches Datum und gleiche Gemeinde;
nur wenn genau ein Treffer zur Tatgruppe passt (z. B. Körperverletzung/Übergriff). Entfernt außerdem HTML/CSS-Reste aus dem Quellennamen.
Aufruf: python3 link_sources.py tatortrechts.json docs [--write]"""
import json, sys, re, collections
from shapely.geometry import shape, Point
from shapely.strtree import STRtree
SRC, DOCS = sys.argv[1], sys.argv[2]
I = json.load(open(SRC, encoding='utf-8'))['incidents']
F = json.load(open(f'{DOCS}/faelle.json', encoding='utf-8'))
G = json.load(open(f'{DOCS}/gemeinden.geojson', encoding='utf-8'))['features']
geoms = [shape(f['geometry']) for f in G]; tree = STRtree(geoms); props = [f['properties'] for f in G]
# Kategorie-Regeln aus dem Import wiederverwenden, ohne den Import auszuführen
src = open(__file__.replace('link_sources.py', 'tatortrechts_import.py'), encoding='utf-8').read()
ns = {'re': re}
exec(src[src.index('R = lambda'):src.index('old = collections')], ns)
kat = ns['kat']
GRP = {'Körperverletzung': 'g', 'Tätlicher Übergriff': 'g', 'Angriffe auf Geflüchtete': 'g', 'Bedrohung': 'b',
       'Sachbeschädigung': 's', 'Propaganda': 's', 'Angriffe auf Unterkünfte': 'u', 'Brandanschlag': 'f'}
def fits(a, b):
    if 'Sonstige' in (a, b) or 'Verdachtsfall' in (a, b): return True
    if {a, b} <= {'Angriffe auf Unterkünfte', 'Brandanschlag', 'Sachbeschädigung'}: return True
    return GRP.get(a) == GRP.get(b)
idx = collections.defaultdict(list)
for x in I:
    pt = Point(*x['geo'])
    for i in tree.query(pt):
        if geoms[i].contains(pt): idx[(x['date'], props[i]['ags'])].append(x); break
GENERIC = ('https://www.opferperspektive.de/category/chronologie-rechter-angriffe', 'https://github.com/davben/arvig')
stat = collections.Counter()
for r in F:
    q = r.get('quelle') or ''
    if '{' in q:
        r['quelle'] = re.sub(r'^.*\}\s*,?\s*', '', q).strip() or 'Quelle nicht angegeben'; stat['Quellenname bereinigt'] += 1
    us = (r.get('urls') or '').split()
    if not us or not all(u in GENERIC for u in us): continue
    cand = idx.get((r['date'], r['ags']), [])
    if not cand: stat['kein Treffer'] += 1; continue
    # nur inhaltlich passende Treffer (gleiche Tatgruppe), damit kein fremder Fall verlinkt wird
    cand = [x for x in cand if fits(kat(x), r['kategorie'])]
    if len(cand) != 1: stat['mehrdeutig oder unpassend'] += 1; continue
    x = cand[0]
    r['urls'] = ' '.join(dict.fromkeys([x['url']] + us)); stat['verlinkt'] += 1
    stat['verlinkt: ' + x['chron']] += 1
print(dict(stat))
if '--write' in sys.argv:
    json.dump(F, open(f'{DOCS}/faelle.json', 'w', encoding='utf-8'), ensure_ascii=False); print('geschrieben')
