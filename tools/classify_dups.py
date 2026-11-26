import csv, sys, difflib, collections
src, out = sys.argv[1], sys.argv[2]
with open(src, newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
groups = collections.defaultdict(list)
for x in rows:
    groups[(x['date'], x['municipality'])].append(x)
def sim(a, b):
    return difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()
results = []
for x in rows:
    if x['possible_duplicate'] != 'True':
        continue
    peers = [p for p in groups[(x['date'], x['municipality'])] if p['id'] != x['id']]
    best = max(((sim(x['description'], p['description']), p) for p in peers), default=(0, None))
    s, p = best
    same_url = bool(p) and bool(x['source_urls']) and x['source_urls'] == p['source_urls']
    if s >= 0.8:
        verdict = 'wahrscheinlich_dublette'
    elif s >= 0.5 or same_url:
        verdict = 'pruefen'
    else:
        verdict = 'verschiedene_tat'
    results.append({'id': x['id'], 'date': x['date'], 'municipality': x['municipality'],
                    'peer_id': p['id'] if p else '', 'similarity': round(s, 2),
                    'same_url': same_url, 'verdict': verdict,
                    'description': x['description'][:200]})
with open(out, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(results[0].keys()))
    w.writeheader(); w.writerows(results)
print(collections.Counter(r['verdict'] for r in results))
