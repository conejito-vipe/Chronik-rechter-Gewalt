"""Straftaten aus der Polizeilichen Kriminalstatistik (BKA), Kreisebene: 2025 (Tabelle 01, Fälle und HZ) und 2014 (Grundtabelle Kreise).
Jede Gemeinde erhält die Werte ihres Kreises (die PKS veröffentlicht keine Gemeindewerte). Kreisreformen seit 2014
werden über eine Zuordnung alter auf neue Kreisschlüssel zusammengefasst.
Aufruf: python3 pks_import.py PKS2025.xlsx PKS2014.csv docs [--write]"""
import sys, json, csv, io, collections, openpyxl
X25, C14, DOCS = sys.argv[1:4]
wb = openpyxl.load_workbook(X25, read_only=True); ws = wb.worksheets[0]
k25 = {}
for row in ws.iter_rows(values_only=True):
    if row[1] == 'Straftaten insgesamt' and row[2] and str(row[2]).isdigit():
        k25[str(row[2]).zfill(5)] = {'name': row[3], 'abs': int(row[5]), 'hz': round(float(row[6]), 1)}
txt = open(C14, 'rb').read().decode('latin-1')
k14 = {}
for r in csv.reader(io.StringIO(txt), delimiter=';'):
    if len(r) > 5 and r[1] == 'Straftaten insgesamt' and r[2].strip().isdigit():
        k14[r[2].strip().zfill(5)] = int(float(r[4]))
OLD = {'03152': '03159', '03156': '03159'}  # Göttingen + Osterode am Harz -> Landkreis Göttingen (2016)
m14 = collections.Counter()
for k, v in k14.items(): m14[OLD.get(k, k)] += v
G = json.load(open(f'{DOCS}/gemeinden.geojson', encoding='utf-8'))['features']
S = json.load(open(f'{DOCS}/statistik.json', encoding='utf-8'))
miss25, miss14, n = set(), set(), 0
for f in G:
    a = f['properties']['ags']; k = a[:5]
    e = k25.get(k)
    if not e: miss25.add(k); continue
    s = S.setdefault(a, {})
    s.pop('straftaten_2006', None)
    s['straftaten'] = {'abs': e['abs'], 'je100k': e['hz'], 'kreis': e['name'], 'jahr': 2025, 'ebene': 'Kreis'}
    if k in m14: s['straftaten_2014'] = m14[k]
    else: miss14.add(k)
    n += 1
print('Kreise 2025', len(k25), '2014', len(k14), '| Gemeinden mit Werten', n, '| ohne 2025', sorted(miss25)[:10], '| ohne 2014', sorted(miss14))
print('Summe 2025', sum(v['abs'] for v in k25.values()), 'Summe 2014', sum(k14.values()))
if '--write' in sys.argv:
    json.dump(S, open(f'{DOCS}/statistik.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':')); print('geschrieben')
