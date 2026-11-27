"""Ergänzt docs/wahl_gem.json um die Bundestagswahlen 1980, 1983 und 1987 (nur Westdeutschland, Gemeinden nach AGS).
Quelle: GERDA-Datei federal_muni_raw.csv (absolute Stimmen je Partei), Anteile = Stimmen / gültige Zweitstimmen.
Gemeinden ohne Entsprechung im AGS-Stand 2025 werden nicht übernommen. Aufruf: python3 add_gem_1980.py RAW.csv docs/wahl_gem.json"""
import csv, json, sys
RAW, OUT = sys.argv[1], sys.argv[2]
YEARS = ['1980', '1983', '1987']
MAP = {'cdu': 'cdu', 'csu': 'csu', 'spd': 'spd', 'gruene': 'grune', 'fdp': 'fdp', 'afd': 'afd', 'npd': 'npd', 'rep': 'rep',
       'die_rechte': 'die_rechte', 'dvu': 'dvu', 'iii_weg': 'iii_weg', 'dkp': 'dkp', 'kpd': 'kpd', 'dsu': 'dsu', 'ddd': 'ddd', 'fap': 'fap'}
J = json.load(open(OUT, encoding='utf-8'))
idx = {a: i for i, a in enumerate(J['ags'])}
keys = [k for k in MAP if k in J['parteien']]
acc = {y: {k: [None] * len(J['ags']) for k in keys} for y in YEARS}
used = {y: 0 for y in YEARS}
for x in csv.DictReader(open(RAW, encoding='utf-8-sig')):
    y = x['election_year']
    if y not in YEARS or x['ags'] not in idx:
        continue
    try:
        v = float(x['valid_votes'])
    except (ValueError, TypeError):
        continue
    if v <= 0:
        continue
    i = idx[x['ags']]
    used[y] += 1
    for k in keys:
        try:
            acc[y][k][i] = round(float(x[MAP[k]]) / v * 100, 1)
        except (ValueError, TypeError):
            pass
for y in YEARS:
    J['jahre'][y] = {k: a for k, a in acc[y].items() if any(val is not None for val in a)}
J['jahre'] = dict(sorted(J['jahre'].items()))
J['hinweis_1980'] = ('1980, 1983 und 1987 nur Westdeutschland (Berlin West). Gemeinden nach AGS-Stand des jeweiligen Jahres; '
                     'Gemeinden, die seitdem umbenannt, geteilt oder zusammengelegt wurden, fehlen oder sind unzugeordnet.')
J['quelle'] += ' | 1980–1987: GERDA federal_muni_raw (absolute Stimmen, Anteile je gültige Zweitstimmen).'
json.dump(J, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('gemeinden je Jahr', used, 'jahre', list(J['jahre'].keys()))
