import sqlite3, struct, json, csv, collections
from shapely import wkb, STRtree
from shapely.geometry import shape, mapping
from shapely.ops import transform
import pyproj
db = sqlite3.connect('vg250/vg250-ew_ebenen_1231/DE_VG250.gpkg')
srid = db.execute("select srs_id from gpkg_geometry_columns where table_name='vg250_gem'").fetchone()[0]
epsg = db.execute("select organization_coordsys_id from gpkg_spatial_ref_sys where srs_id=?", (srid,)).fetchone()[0]
print('SRID', srid, 'EPSG', epsg)
def geom_from_gpkg(blob):
    flags = blob[3]; env_ind = (flags >> 1) & 7
    env_len = [0,32,48,48,64][env_ind]
    return wkb.loads(blob[8+env_len:])
to_wgs = pyproj.Transformer.from_crs(f"EPSG:{epsg}", "EPSG:4326", always_xy=True).transform
gems = []
for ags, gen, ewz, geom in db.execute("select AGS, GEN, EWZ, geom from vg250_gem"):
    g = transform(to_wgs, geom_from_gpkg(geom))
    gems.append({'ags': ags, 'name': gen, 'ewz': ewz, 'geom': g})
print('Gemeinden geladen', len(gems))
tree = STRtree([g['geom'] for g in gems])
rows = list(csv.DictReader(open('chronik_clean_v4.csv', encoding='utf-8')))
assigned = 0; fallback = 0; per = collections.Counter(); out_cases = []
for r in rows:
    from shapely.geometry import Point
    p = Point(float(r['lon']), float(r['lat']))
    idx = tree.query(p, predicate='intersects')
    if len(idx): i = idx[0]; assigned += 1
    else:
        i = tree.nearest(p); fallback += 1
    g = gems[int(i)]
    per[g['ags']] += 1
    out_cases.append({'id': r['id'], 'date': r['date'], 'state': r['state'], 'ags': g['ags'],
        'gemeinde': g['name'], 'ort': r['city_raw'], 'kategorie': r['category'],
        'beschreibung': r['description'], 'quelle': r['source'], 'quellentyp': r['source_type'],
        'drucksache': r['drucksache'], 'urls': r['source_urls']})
print('zugeordnet per Polygon', assigned, '| Fallback nächstes Polygon', fallback)
# Gemeindeflächen vereinfachen und Attribute mitgeben
feats = []
for g in gems:
    if per.get(g['ags'], 0) == 0 and not g['ewz']:
        pass
    s = g['geom'].simplify(0.0015, preserve_topology=True)
    feats.append({'type': 'Feature', 'properties': {'ags': g['ags'], 'name': g['name'], 'ewz': g['ewz'] or 0,
        'faelle': per.get(g['ags'], 0)}, 'geometry': mapping(s)})
gj = json.dumps({'type': 'FeatureCollection', 'features': feats}, ensure_ascii=False, separators=(',', ':'))
open('gemeinden.geojson', 'w', encoding='utf-8').write(gj)
json.dump(out_cases, open('faelle.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
import os
print('gemeinden.geojson MB', round(os.path.getsize('gemeinden.geojson')/1e6, 2), '| faelle.json MB', round(os.path.getsize('faelle.json')/1e6, 2))
print('Gemeinden mit mind. 1 Fall', sum(1 for v in per.values() if v), '| Gemeinden mit EWZ 0', sum(1 for g in gems if not g['ewz']))
