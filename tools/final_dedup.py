import csv
base = 'chronik_clean_v3.csv'
with open(base, newline='', encoding='utf-8') as f:
    rd = csv.DictReader(f); cols = rd.fieldnames; rows = list(rd)
byid = {r['id']: r for r in rows}
manual = {  # Paare mit identischem Vorfall; die spätere Zeile (höhere row_raw) wird entfernt
 'CRG-01429':'Guben 2015-12-27 (doppelt beschrieben)',
 'CRG-02132':'Neunkirchen-Seelscheid 2016-02-20 (Beleidigung, doppelt)',
 'CRG-02139':'Illertissen 2016-02-21 (Sachbeschädigung, doppelt)',
 'CRG-02268':'Stockelsdorf 2016-03-07 (Sachbeschädigung, doppelt)',
 'CRG-02102':'Schöningen 2016-02-16 (abgeschnittener Text, doppelt)',
 'CRG-02614':'Guben 2016-05-31 (Bierflaschen, doppelt)',
 'CRG-01215':'Verl 2015-11-14 (Asylunterkunft, doppelt)',
 'CRG-01557':'Berlin 2016-01-08 (Kennzeichen, doppelt)',
 'CRG-02060':'Gengenbach 2016-02-10 (Kennzeichen, doppelt)',
}
removed = {}
for k, why in manual.items():
    if k not in byid: continue
    removed[k] = (why, 'manuell geprüft')
# verbleibende Kandidaten aus der ersten Liste (Kettenregel), nur wenn Partner noch vorhanden
with open('dubletten_pruefliste.csv', newline='', encoding='utf-8') as f:
    for c in csv.DictReader(f):
        if c['verdict'] != 'wahrscheinlich_dublette': continue
        x, p = c['id'], c['peer_id']
        if x in removed or x not in byid or p not in byid or p in removed: continue
        later, earlier = (x, p) if int(byid[x]['row_raw']) > int(byid[p]['row_raw']) else (p, x)
        removed[later] = (f"Partner {earlier} (Ähnlichkeit {c['similarity']})", 'automatisch, Kettenregel')
clean = [r for r in rows if r['id'] not in removed]
with open('chronik_clean_v4.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(clean)
with open('dubletten_log_v4.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['removed_id','removed_row_raw','date','municipality','grund','methode'])
    for k,(why,m) in removed.items():
        r = byid[k]; w.writerow([k, r['row_raw'], r['date'], r['municipality'], why, m])
print('entfernt gesamt:', len(removed), '| verbleibend:', len(clean))
for k,(why,m) in removed.items(): print(k, byid[k]['municipality'], why, m)
