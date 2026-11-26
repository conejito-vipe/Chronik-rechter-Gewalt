import csv, re, statistics, collections
rows = list(csv.DictReader(open('chronik_clean_v4.csv', encoding='utf-8')))
cols = list(rows[0].keys())
street = re.compile(r'[\w\-äöüß\.]*(straße|strasse|str\.|weg|platz|allee|gasse|ring|damm|chaussee|ufer|hof|parkplatz|hellweg|heimweg)\b', re.I)
masked = 0
for r in rows:
    new, n = street.subn('[Straßenname entfernt]', r['description'])
    if n: masked += 1
    r['description'] = new
# Koordinaten auf Gemeinde-Ebene: Median je Gemeinde, nicht der Fallort
grp = collections.defaultdict(list)
for r in rows: grp[(r['state'], r['municipality'])].append((float(r['lon']), float(r['lat'])))
for r in rows:
    pts = grp[(r['state'], r['municipality'])]
    r['lon'] = f"{statistics.median(p[0] for p in pts):.4f}"
    r['lat'] = f"{statistics.median(p[1] for p in pts):.4f}"
with open('chronik_public_v1.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
print('Beschreibungen maskiert:', masked, '| Gemeinden:', len(grp))
# Restprüfung: verbliebene Hinweise auf Adressen
left = [r['description'] for r in rows if re.search(r'\b\d{1,3}[a-z]?\b\s*(in|an|vor|bei)?\s*(der|dem)?\s*[A-ZÄÖÜ]', r['description'])]
print('Verdacht Hausnummer:', len(left))
print('Beispiel:', left[:2] if left else '-')
print('source_urls mit Pfad-Adressen (Heuristik):', sum(1 for r in rows if re.search(r'str(a|ß)e|straße|weg/', r['source_urls'], re.I)))
