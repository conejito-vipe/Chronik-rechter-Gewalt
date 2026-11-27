"""Baut docs/wahl_gem.json: Zweitstimmen-Anteile je Gemeinde (1990–2025) aus der GERDA-Datei federal_muni_harm_25.csv.
Quelle: GERDA (Heddesheimer, Hilbig, Sichart & Wiedemann), CC BY 4.0, https://www.german-elections.com ; Gemeinden auf Stand 2025.
Die Datei enthält Zweitstimmen (geprüft: Bundesergebnisse 2017 und 2025 stimmen mit der Bundeswahlleiterin überein)."""
import csv, json, sys, collections
SRC, OUT = sys.argv[1], sys.argv[2]
LAB = {'cdu':'CDU','csu':'CSU','spd':'SPD','gruene':'GRÜNE','fdp':'FDP','linke_pds':'Die Linke','afd':'AfD','npd':'NPD','rep':'REP',
 'die_rechte':'DIE RECHTE','dvu':'DVU','iii_weg':'Der III. Weg','dkp':'DKP','kpd':'KPD','bsw':'BSW','freie_wahler':'FREIE WÄHLER',
 'piraten':'PIRATEN','die_partei':'Die PARTEI','volt':'Volt','bp':'BP','zentrum':'Zentrum','werteunion':'WerteUnion',
 'bundnis_deutschland':'BÜNDNIS DEUTSCHLAND','dsu':'DSU','ddd':'DDD','fap':'FAP','tierschutz':'Tierschutzpartei','gartenpartei':'Die Gartenpartei'}
RECHTE = {'afd','npd','rep','die_rechte','dvu','iii_weg','fap','werteunion','bundnis_deutschland','dsu','ddd'}
rows = list(csv.DictReader(open(SRC, encoding='utf-8-sig')))
years = sorted({x['election_year'] for x in rows})
# Parteien: national >= 0,5 % in mindestens einem Jahr oder rechts
tot = collections.defaultdict(lambda: collections.Counter()); V = collections.Counter()
for x in rows:
    try: v = float(x['valid_votes'])
    except: continue
    V[x['election_year']] += v
    for c in LAB:
        try: tot[x['election_year']][c] += float(x[c]) * v
        except: pass
keep = [c for c in LAB if c in RECHTE or any(tot[y][c] / V[y] >= 0.005 for y in years if V[y])]
ags_list = sorted({x['ags'] for x in rows})
idx = {a: i for i, a in enumerate(ags_list)}
J = {'quelle': 'GERDA: federal_muni_harm_25 (Zweitstimmen, Gemeindegrenzen 2025), CC BY 4.0. Heddesheimer, Hilbig, Sichart & Wiedemann, german-elections.com',
     'ags': ags_list, 'parteien': {c: LAB[c] for c in keep}, 'rechts': sorted(RECHTE & set(keep)), 'jahre': {}}
for y in years:
    d = {}
    for c in keep:
        arr = [None] * len(ags_list)
        any_val = False
        for x in rows:
            if x['election_year'] != y: continue
            try: s = float(x[c]) * 100
            except: continue
            arr[idx[x['ags']]] = round(s, 1); any_val = True
        if any_val: d[c] = arr
    J['jahre'][y] = d
json.dump(J, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('jahre', years, 'parteien', len(keep), 'gemeinden', len(ags_list))
