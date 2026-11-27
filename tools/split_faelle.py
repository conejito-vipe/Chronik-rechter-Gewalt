"""Teilt docs/faelle.json in zwei Dateien (faelle-1.json bis 2016, faelle-2.json ab 2017), damit jede unter 16 MB bleibt.
Die Seite lädt beide und fügt sie zusammen. faelle.json bleibt die Hauptdatei für die Werkzeuge."""
import json, sys
D = sys.argv[1] if len(sys.argv) > 1 else 'docs'
F = json.load(open(f'{D}/faelle.json', encoding='utf-8'))
a = [r for r in F if r['date'] < '2017']; b = [r for r in F if r['date'] >= '2017']
for n, part in (('faelle-1.json', a), ('faelle-2.json', b)):
    json.dump(part, open(f'{D}/{n}', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(len(a), len(b))
