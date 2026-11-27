"""Ergänzt die Bundestagswahl 2021 (Bund und Länder, Zweitstimme) in docs/wahl_hist.json.
Quelle: Die Bundeswahlleiterin, Ergebnisse nach Wahlkreisen (Stand 23.02.2024), Datenlizenz Deutschland – Namensnennung 2.0."""
import csv, json, sys
SRC, DOCS = sys.argv[1], sys.argv[2]
LAND_NAMES = {'Berlin','Nordrhein-Westfalen','Baden-Württemberg','Bayern','Sachsen','Hessen','Hamburg','Niedersachsen','Schleswig-Holstein','Thüringen','Rheinland-Pfalz','Brandenburg','Sachsen-Anhalt','Bremen','Mecklenburg-Vorpommern','Saarland'}
NORM = {'DIE LINKE': 'Die Linke', 'Die PARTEI': 'Die PARTEI'}
rows = list(csv.reader(open(SRC, encoding='utf-8-sig'), delimiter=';'))
h = [i for i, r in enumerate(rows) if r and r[0] == 'Wahlart'][0]
out = {}
def area(name):
    return out.setdefault(name, {'b': 0, 'w': 0, 'g': 0, 'p': {}})
for r in rows[h + 1:]:
    if len(r) < 13 or r[2] not in ('Bund', 'Land'):
        continue
    name = 'Deutschland' if r[2] == 'Bund' else r[4]
    if r[2] == 'Land' and name not in LAND_NAMES:
        continue
    g, stimme, n = r[7], r[10], r[11]
    if not n.isdigit():
        continue
    n = int(n); a = area(name)
    if g == 'System-Gruppe':
        if r[8] == 'Wahlberechtigte': a['b'] = n
        elif r[8] == 'Wählende': a['w'] = n
        elif r[8] == 'Gültige' and stimme == '2': a['g'] = n
    elif g == 'Partei' and stimme == '2':
        p = NORM.get(r[8], r[8])
        a['p'][p] = a['p'].get(p, 0) + n
res = {}
for name, a in out.items():
    if not a['g']: continue
    keep = {p: v for p, v in a['p'].items() if v / a['g'] >= 0.005}
    rest = sum(a['p'].values()) - sum(keep.values())
    if rest > 0: keep['Sonstige'] = keep.get('Sonstige', 0) + rest
    res[name] = {'b': a['b'], 'w': a['w'], 'g': a['g'], 'p': dict(sorted(keep.items(), key=lambda x: -x[1]))}
W = json.load(open(f'{DOCS}/wahl_hist.json', encoding='utf-8'))
W['jahre']['2021'] = res
W['hinweis'] = W['hinweis'].replace(' 2021 fehlt.', ' 2021 aus der Bundeswahlleiterin-Datei (Stand 23.02.2024).')
W['quelle'] = W['quelle'] + '; 2021: Die Bundeswahlleiterin, Ergebnisse nach Wahlkreisen, Stand 23.02.2024 (Datenlizenz Deutschland – Namensnennung 2.0). Enthält die Korrektur der Wiederholungswahl Berlin 2024.'
json.dump(W, open(f'{DOCS}/wahl_hist.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
d = res['Deutschland']
print('Bund 2021:', {p: round(v / d['g'] * 100, 1) for p, v in list(d['p'].items())[:8]}, 'Länder:', len(res) - 1, 'Wahlberechtigte', d['b'])
