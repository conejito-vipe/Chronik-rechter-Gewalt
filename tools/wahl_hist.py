import csv, json, sys, collections
SRC, DOCS = sys.argv[1], sys.argv[2]
LAND = {'SH':'Schleswig-Holstein','HH':'Hamburg','NI':'Niedersachsen','HB':'Bremen','NW':'Nordrhein-Westfalen','HE':'Hessen',
 'RP':'Rheinland-Pfalz','BW':'Baden-Württemberg','BY':'Bayern','SL':'Saarland','BE':'Berlin','BB':'Brandenburg',
 'MV':'Mecklenburg-Vorpommern','SN':'Sachsen','ST':'Sachsen-Anhalt','TH':'Thüringen'}
KZ = {'01':'Schleswig-Holstein','02':'Hamburg','03':'Niedersachsen','04':'Bremen','05':'Nordrhein-Westfalen','06':'Hessen','07':'Rheinland-Pfalz','08':'Baden-Württemberg','09':'Bayern','10':'Saarland','11':'Berlin','12':'Brandenburg','13':'Mecklenburg-Vorpommern','14':'Sachsen','15':'Sachsen-Anhalt','16':'Thüringen'}
NORM = {'Die Linke.':'Die Linke','DIE LINKE':'Die Linke','PDS':'Die Linke','B90/Gr':'GRÜNE','DKP/DRP':'DRP'}
META = {'Wahlberechtigte','Wähler','Ungültige','Gültige'}
out = collections.defaultdict(lambda: collections.defaultdict(lambda: {'b':0,'w':0,'g':0,'p':collections.Counter()}))
def add(y, land, party, v):
    for area in (land, 'Deutschland'):
        a = out[y][area]
        if party == 'Wahlberechtigte': a['b'] += v
        elif party == 'Wähler': a['w'] += v
        elif party == 'Gültige': a['g'] += v
        elif party not in META: a['p'][NORM.get(party, party)] += v
# 1949: Wahlkreisdatei
hdr = None
for l in open(SRC + '/tidy_bundestag/data_raw/btw49_kerg.csv', encoding='latin1'):
    f = [x.strip() for x in l.rstrip('\n').split(';')]
    if f[0] == 'Wahlkreis': hdr = f; continue
    if hdr and f[0].isdigit() and int(f[0]) < 900:
        land = LAND[f[2]]
        for i, h in enumerate(hdr):
            if i >= 3 and h and i < len(f) and f[i]:
                add('1949', land, {'Wahlberechtigte':'Wahlberechtigte','Wähler':'Wähler','Gültige':'Gültige','Ungültige':'Ungültige'}.get(h, h), int(f[i]))
# 1953-2017: tidy returns (exakte Dubletten entfernen)
seen = set()
for r in csv.DictReader(open(SRC + '/steffen-stell_btw_data/btw_returns.csv')):
    key = tuple(r.values())
    if key in seen: continue
    seen.add(key)
    if r['state'] == 'Bund' or int(r['district_no']) >= 900: continue
    if r['vote_type'] not in ('Zweitstimmen', ''): continue
    add(r['year'], LAND[r['state']], r['party_name_short'], int(r['votes'] or 0))
# 2025: vorhandene Wahlkreisdaten
w = json.load(open(DOCS + '/wahl.json'))['2025']
for k, wk in w['wk'].items():
    land = KZ.get(str(wk['land']).zfill(2), wk['land'])
    add('2025', land, 'Wahlberechtigte', wk.get('berechtigt') or 0)
    add('2025', land, 'Wähler', wk.get('waehler') or 0)
    g = sum(p['abs'] for p in wk['parteien'].values())
    add('2025', land, 'Gültige', g)
    for p, v in wk['parteien'].items(): add('2025', land, p, v['abs'])
res = {}
for y in sorted(out):
    res[y] = {}
    for area, a in out[y].items():
        s = sum(a['p'].values())
        if abs(s - a['g']) > max(10, a['g'] * 0.002): print('WARN Summe', y, area, s, a['g'])
        keep = {p: v for p, v in a['p'].items() if v / a['g'] >= 0.005}
        rest = s - sum(keep.values())
        if rest > 0: keep['Sonstige'] = keep.get('Sonstige', 0) + rest
        res[y][area] = {'b': a['b'], 'w': a['w'], 'g': a['g'], 'p': dict(sorted(keep.items(), key=lambda x: -x[1]))}
D = res
for y in D: print(y, {p: round(v / D[y]['Deutschland']['g'] * 100, 1) for p, v in list(D[y]['Deutschland']['p'].items())[:8]}, len(D[y]) - 1, 'Länder')
json.dump({'quelle': 'Die Bundeswahlleiterin, Wahlkreisergebnisse (kerg); aufbereitet über github.com/max-alletsee/tidy_bundestag (1949) und github.com/steffen-stell/btw_data (1953–2017); 2025: wahl.json',
           'hinweis': '1949: eine Stimme; 1953–2025: Zweitstimme. Berlin bis 1987 ohne Direktwahl, bis 1987 ohne DDR. PDS und Die Linke zusammengefasst, Grüne inkl. Bündnis 90/Grüne (1990). Parteien unter 0,5 % unter Sonstige. 2021 fehlt.',
           'jahre': D}, open(DOCS + '/wahl_hist.json', 'w'), ensure_ascii=False, separators=(',', ':'))
