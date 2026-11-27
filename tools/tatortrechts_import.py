"""Importiert Fälle der Beratungsstellen-Chroniken aus Tatort Rechts (api.tatortrechts.de/incidents, Abruf 27.11.2026).
Übernommen: alle Chroniken außer Opferperspektive (Brandenburg, eigene Quelle) und der Todesopfer-Liste (eigene Quelle).
Gemeinde über die Koordinate des Falls (Punkt in Gemeindepolygon 2025), Straßennamen werden aus der Beschreibung entfernt,
Dubletten (gleiche Gemeinde, gleiches Datum wie ein vorhandener Fall) werden übersprungen.
Aufruf: python3 tatortrechts_import.py tatortrechts.json docs [--write]"""
import json, sys, re, collections
from shapely.geometry import shape, Point
from shapely.strtree import STRtree
SRC, DOCS = sys.argv[1], sys.argv[2]
WRITE = '--write' in sys.argv
I = json.load(open(SRC, encoding='utf-8'))['incidents']
F = json.load(open(f'{DOCS}/faelle.json', encoding='utf-8'))
G = json.load(open(f'{DOCS}/gemeinden.geojson', encoding='utf-8'))['features']
geoms = [shape(f['geometry']) for f in G]; props = [f['properties'] for f in G]; tree = STRtree(geoms)
SKIP_CHRON = {'Opferperspektive', 'Todesopfer rechter Gewalt, Amadeu Antonio Stiftung'}
QUELLE = {'LEUCHTLINIE': 'LEUCHTLINIE – Chronik (Baden-Württemberg)', 'ezra': 'ezra – Chronik (Thüringen)',
          'RAA Sachsen': 'RAA Sachsen – Chronik', 'LOBBI': 'LOBBI – Chronik rechter Gewalt (Mecklenburg-Vorpommern)',
          'ReachOut': 'ReachOut – Chronik (Berlin)', 'Keine Randnotiz': 'Keine Randnotiz – Chronik (Bremen)',
          'Opferberatung Rheinland': 'Opferberatung Rheinland – Chronik (Nordrhein-Westfalen)',
          'm*power': 'm*power – Chronik (Rheinland-Pfalz)', 'Mobile Opferberatung': 'Mobile Opferberatung – Chronik (Sachsen-Anhalt)',
          'München Chronik': 'München-Chronik', 'response.': 'response. – Chronik (Hessen)'}
OK_WORDS = {'bahnhof', 'hauptbahnhof', 'busbahnhof', 'friedhof', 'schulhof', 'innenhof', 'hinterhof', 'hof', 'spielplatz',
            'sportplatz', 'bolzplatz', 'zeltplatz', 'campingplatz', 'arbeitsplatz', 'weg', 'heimweg', 'rückweg', 'nachhauseweg',
            'fußweg', 'radweg', 'gehweg', 'ring', 'platz', 'marktplatz', 'parkplatz', 'ufer', 'damm', 'straße', 'strasse', 'gasse', 'allee',
            'straßen', 'wegs', 'weges', 'platzes', 'hofes', 'hofs', 'bahnhofs', 'bahnhofes', 'friedhofs', 'friedhofes'}
STREET = re.compile(r'((?-i:\b[A-ZÄÖÜ][\w\-äöüß]*er)\s+)?\b[\w\-äöüßÄÖÜ\.]*(straße|strasse|str\.|weg|platz|allee|gasse|ring|damm|chaussee|ufer|hof|hellweg)(n|s|es)?\b(\s*\d+[a-z]?)?', re.I)
PROTECT = re.compile(r'(III\.|Dritte[nr]?)\s+Weg', re.I)
def mask(t):
    t = PROTECT.sub(lambda m: m.group(0).replace(' ', '\u00a0').replace('Weg', 'W\u200beg'), t)
    t = STREET.sub(lambda m: m.group(0) if m.group(0).strip().lower().rstrip('.') in OK_WORDS else '[Straßenname entfernt]', t)
    return t.replace('\u00a0', ' ').replace('W\u200beg', 'Weg')
R = lambda p: re.compile(p, re.I)
RULES = [('Brandanschlag', R(r'brand|feuer|molotow|angezündet|zündete|brandsatz|brandstift')),
         ('Körperverletzung', R(r'körperverletz|verletzt|schlug|geschlagen|schlagen|schlägt|getreten|\btrat\b|tritt|prügel|faustschl|messer|stach|zu boden|ins gesicht|krankenhaus')),
         ('Tätlicher Übergriff', R(r'beworfen|geworfen|warf|schüsse|geschossen|schoss|angegriffen|attackiert|bespuckt|spuckte|geschubst|gestoßen|angerempelt|übergriff|gewürgt|griff .* an|angriff')),
         ('Angriffe auf Unterkünfte', R(r'unterkunft|asylheim|flüchtlingsheim|asylbewerberheim|erstaufnahme|heim für geflüchtete')),
         ('Bedrohung', R(r'bedroh|drohte|droh|nötig|beleidig|beschimpf|pöbel|gepöbelt|verfolgt')),
         ('Propaganda', R(r'hakenkreuz|hitlergruß|sieg heil|symbol|kennzeichen|schmier|graffiti|gesprüht|sprühte|aufkleber|plakat|flyer|propaganda|parole|rune')),
         ('Sachbeschädigung', R(r'beschädig|zerstört|eingeworfen|scheibe|zerkratzt|steinwurf|steine|demoliert|stolperstein'))]
FAC = [('brand', 'Brandanschlag'), ('versuchte körperverletzung', 'Bedrohung'), ('körperverletzung', 'Körperverletzung'),
       ('propaganda', 'Propaganda'), ('sachbeschädigung', 'Sachbeschädigung'), ('bedrohung', 'Bedrohung'), ('nötigung', 'Bedrohung')]
def kat(x):
    f = (x.get('fac') or '').lower()
    for k, v in FAC:
        if k in f: return v
    t = (x.get('title') or '') + ' ' + (x.get('desc') or '')
    for k, rx in RULES:
        if rx.search(t): return k
    return 'Sonstige'
old = collections.defaultdict(set)
for r in F: old[(r['date'], r['ags'])].add(r['kategorie'])
EWZ = {q['ags']: q.get('ewz') or 0 for q in props}
nxt = max(int(r['id'][4:]) for r in F) + 1
new, skip, dupkey = [], collections.Counter(), set()
for x in sorted(I, key=lambda x: (x['date'] or '', x['id'])):
    if x['chron'] in SKIP_CHRON: skip['eigene Quelle'] += 1; continue
    if not x['url']: skip['ohne Beleg'] += 1; continue
    pt = Point(*x['geo']); ags = None
    for i in tree.query(pt):
        if geoms[i].contains(pt): ags = i; break
    if ags is None: skip['ohne Gemeinde'] += 1; continue
    p = props[ags]
    k = kat(x); hit = old.get((x['date'], p['ags']))
    # Dublette mit vorhandenem Fall: gleiche Gemeinde und gleiches Datum; in Großstädten zusätzlich gleiche Kategorie
    if hit and (EWZ[p['ags']] < 100000 or k in hit): skip['Dublette'] += 1; continue
    title = (x.get('title') or '').strip(); desc = (x.get('desc') or '').strip()
    text = desc if not title or desc.startswith(title) else f'{title}. {desc}'
    dk = (x['date'], p['ags'], re.sub(r'\W+', '', text.lower())[:120])
    if dk in dupkey: skip['doppelt in Quelle'] += 1; continue
    dupkey.add(dk)
    urls = [x['url']] + [s[1] for s in x['src'] if s[1] and s[1].startswith('http') and s[1] != x['url']]
    new.append({'id': 'CRG-%05d' % nxt, 'date': x['date'], 'state': p['land'], 'ags': p['ags'], 'gemeinde': p['name'],
                'ort': p['name'], 'kategorie': k, 'beschreibung': mask(text), 'quelle': QUELLE.get(x['chron'], x['chron']),
                'quellentyp': 'Beratungsstelle/NGO', 'drucksache': '', 'urls': ' '.join(dict.fromkeys(urls))})
    nxt += 1
print('neu', len(new), dict(skip))
print('Kategorien', collections.Counter(r['kategorie'] for r in new).most_common())
print('Länder', collections.Counter(r['state'] for r in new).most_common())
print('maskiert', sum('[Straßenname entfernt]' in r['beschreibung'] for r in new))
if WRITE:
    F.extend(new); F.sort(key=lambda r: (r['date'], r['id']))
    json.dump(F, open(f'{DOCS}/faelle.json', 'w', encoding='utf-8'), ensure_ascii=False)
    print('geschrieben', len(F))
