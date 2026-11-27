"""Ersetzt den Platzhalter in den Todesopfer-Einzelfällen durch Fakten aus der Stiftungsliste
(Alter, Ort, Status). Namen werden bewusst nicht übernommen. Zuordnung über die Einzelseiten-URL."""
import json, sys
DOCS = sys.argv[1] if len(sys.argv) > 1 else 'docs'
F = json.load(open(f'{DOCS}/faelle.json', encoding='utf-8'))
T = json.load(open(f'{DOCS}/todesopfer.json', encoding='utf-8'))
by_url = {t['url']: t for t in T if t.get('url')}
n = 0
for r in F:
    if r['kategorie'] != 'Todesopfer':
        continue
    t = by_url.get(r['urls'])
    if not t:
        continue
    parts = ['Todesopfer rechter Gewalt laut Amadeu Antonio Stiftung.']
    if t.get('alter'):
        parts.append(f"Alter: {t['alter']} Jahre.")
    if t.get('ort'):
        parts.append(f"Ort laut Stiftung: {t['ort']}.")
    parts.append(f"Status laut Stiftung: {t['status'] or 'ohne Angabe'}.")
    r['beschreibung'] = ' '.join(parts)
    n += 1
json.dump(F, open(f'{DOCS}/faelle.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('aktualisiert', n)
