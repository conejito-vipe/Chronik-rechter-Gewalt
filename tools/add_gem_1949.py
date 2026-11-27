"""Ergänzt docs/wahl_gem.json um die Bundestagswahlen 1949–1969 (Gemeinden nach AGS, Zweitstimmen/Parteistimmen).
Quelle: GERDA-Datei (vote_type=party), Anteile = Stimmen / gültige Stimmen je Gemeinde.
1949–1969 sind CDU und CSU in der Datei zusammengefasst (cdu_csu); sie werden als CDU geführt, CSU entfällt für diese Jahre.
Aufruf: python3 add_gem_1949.py RAW.csv docs/wahl_gem.json"""
import csv, json, sys, collections
RAW, OUT = sys.argv[1], sys.argv[2]
YEARS = ['1949', '1953', '1957', '1961', '1965', '1969']
# Datei-Spalte -> Schlüssel in wahl_gem.json
MAP = {'spd': 'spd', 'cdu_csu': 'cdu', 'fdp': 'fdp', 'kpd': 'kpd', 'npd': 'npd', 'drp': 'drp', 'dp': 'dp', 'gb_bhe': 'gb_bhe', 'bp': 'bp'}
LAB = {'dp': 'DP', 'drp': 'DRP', 'gb_bhe': 'GB/BHE', 'kpd': 'KPD', 'bp': 'BP'}
J = json.load(open(OUT, encoding='utf-8'))
idx = {a: i for i, a in enumerate(J['ags'])}
for k, v in LAB.items():
    J['parteien'].setdefault(k, v)
if 'drp' not in J['rechts']:
    J['rechts'] = sorted(set(J['rechts']) | {'drp'})
rows = [x for x in csv.DictReader(open(RAW, encoding='utf-8-sig')) if x['vote_type'] == 'party' and x['year'] in YEARS]
acc = {y: {k: [None] * len(J['ags']) for k in MAP.values()} for y in YEARS}
used = collections.Counter(); tot = collections.defaultdict(lambda: collections.Counter()); V = collections.Counter()
for x in rows:
    y = x['year']
    try:
        v = float(x['votes_valid'])
    except (ValueError, TypeError):
        continue
    if v <= 0:
        continue
    V[y] += v
    for col, key in MAP.items():
        try:
            tot[y][key] += float(x[col])
        except (ValueError, TypeError):
            pass
    if x['ags'] not in idx:
        continue
    i = idx[x['ags']]
    used[y] += 1
    for col, key in MAP.items():
        try:
            acc[y][key][i] = round(float(x[col]) / v * 100, 1)
        except (ValueError, TypeError):
            pass
for y in YEARS:
    J['jahre'][y] = {k: a for k, a in acc[y].items() if any(val is not None for val in a)}
J['jahre'] = dict(sorted(J['jahre'].items(), key=lambda kv: int(kv[0])))
J['hinweis_1949'] = ('1949–1969: CDU inklusive CSU (in der Quelle zusammengefasst), daher kein eigener CSU-Wert. '
                     '1949 eine Stimme. Gemeinden nach AGS-Stand des jeweiligen Jahres; nicht zuordenbare fehlen.')
J['quelle'] += ' | 1949–1969: GERDA Gemeindedaten (Parteistimmen), Anteile je gültige Stimmen.'
json.dump(J, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('gemeinden je Jahr', dict(used))
for y in YEARS:
    print(y, {k: round(100 * tot[y][k] / V[y], 1) for k in ['spd', 'cdu', 'fdp', 'npd', 'drp', 'gb_bhe', 'dp'] if V[y]})
