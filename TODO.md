# Offene Punkte / Open items

🇩🇪 [Deutsch](#-deutsch) · 🇺🇸 [English](#-english)

Stand / as of: 26.11.2026

---

## 🇩🇪 Deutsch

### Morgen (Browser-Abruf)
- [ ] Amadeu Antonio Stiftung, Chronik (https://www.amadeu-antonio-stiftung.de/chronik/) per Browser abrufen. Zuerst 2015 bis Februar 2017, danach den Rest. Detailseiten lesen, nur Faktenangaben und Quellenlinks übernehmen.
- [ ] Abgleich mit den 3.307 vorhandenen Fällen (Datum, Gemeinde, Textähnlichkeit). Dubletten markieren, nicht übernehmen.
- [ ] Todesopfer-Liste (https://www.amadeu-antonio-stiftung.de/todesopfer-rechter-gewalt/) vollständig gegenprüfen. Aktuell 247 Einträge aus Seitenabruf. Beim Münchner Anschlag 2016 fehlt vermutlich eine Person (9 statt 10). Auf weitere Lücken prüfen.
- [ ] Nutzungserlaubnis der Stiftung einholen (keine Lizenz auf der Seite, „© Amadeu Antonio Stiftung“).

### Daten
- [ ] Arbeitslose (Bundesagentur für Arbeit): freie Daten gibt es nur auf Kreisebene, Gemeindeebene ist kostenpflichtig (Arbeitslosenquoten, AkG). Entscheiden: Kreisebene anzeigen oder Gemeindedaten kaufen. Bis dahin zeigt die Karte Erwerbslose (Zensus 2022, Tab. 2000S-1001).
- [ ] Straftaten allgemein: PKS gibt es nur für Bund, Länder, Kreise und größere Städte. Quellen suchen (LKA, Regionalstatistik), Entwicklung der letzten 20 Jahre (2006 bis 2025).
- [ ] Entwicklung seit 2006: Einwohner und Bevölkerungsstruktur je Gemeinde für 2006 (Regionalstatistik, Fortschreibung). Gebietsstandsänderungen beachten.
- [ ] Wahlergebnisse: Bundestagswahl 2021, 2017, 2013, 2009 sowie Landtags- und Kommunalwahlen auf Gemeindeebene. Aktuell nur Bundestagswahl 2025 als Näherung über den Wahlkreis. Gemeindeergebnisse bei den Landesämtern oder der Bundeswahlleiterin suchen.
- [ ] Zensus Bildung (Tab. 2000S-1003): nur 1.578 Gemeinden verfügbar. Prüfen, ob eine andere Tabelle mehr Gemeinden abdeckt.
- [ ] Zensus-Gebietsstand 15.05.2022 gegen Gemeindestand 31.12.2025: 37 AGS ohne Zuordnung (Gemeindefusionen) nachziehen.
- [ ] Länderebene: Deutsche und Ausländer aus Tab. 1000A-1019 im Länder-Tooltip anzeigen.
- [ ] Klären: „Daten vor und nach dem Zeitraum“. Welche Quellen sind gemeint (andere Chroniken, amtliche Zahlen vor 2015 und nach Februar 2017)?
- [ ] 2016-Überzählung gegenüber der Sekundärquelle (ca. 144 %) klären. Quelle der Vergleichszahl prüfen.
- [ ] 33 Einträge ohne Quellen-URL und 3 ohne Quellennamen nachrecherchieren. 125 mögliche Dubletten prüfen (`daten/dubletten_pruefliste.csv`).

### Karte und Qualität
- [ ] Karte im Browser prüfen: Länderbeschriftungen (NRW, Baden-Württemberg, Brandenburg/Berlin), Grenzen (Länder blau, Gemeinden dünn gestrichelt), Todesopfer-Filter, Panel, Tabellen, Ladezeit (Gemeindegeometrie 11 MB), Smartphone-Ansicht.
- [ ] Todesopfer-Einfärbung (lila) überdeckt die Fall-Einfärbung in diesen Gemeinden. Prüfen, ob ein anderes Muster oder ein Ring besser ist.
- [ ] Straßenmaskierung stichprobenartig prüfen. Die Erkennung maskiert zu viel (z. B. „Bahnhof“, „Marktplatz“) und könnte einzelne Adressen übersehen.
- [ ] Hinweis „Punkt ist nicht exakt“ in der Karte sichtbar platzieren (Schutz der Unterkünfte).
- [ ] Öffentliche Seite mit SEO: GitHub Pages aus `docs/` aktivieren, Sitemap, Open-Graph-Bild, strukturierte Daten. Die private Artifact-Seite wird von Suchmaschinen nicht indexiert.

### Recht und Lizenz
- [ ] Lizenz klären: Das Repository enthält GPL v3. Gewünscht ist „frei nutzbar, aber nicht verkaufbar“. GPL erlaubt den Verkauf, passt also nicht. Alternativen für Daten prüfen (z. B. CC BY-NC 4.0). Pflichtangaben der Datenquellen beachten (BKG und Destatis: Datenlizenz Deutschland, Namensnennung 2.0).
- [ ] Die ursprüngliche CSV im Repo (`Chronik rechter Gewalt - Rechte Gewalt.csv`) enthält genaue Koordinaten und Adressen. Entscheiden, ob sie bleibt, ersetzt oder entfernt wird (Schutz der Unterkünfte).
- [ ] Ursprung der Rohdaten dokumentieren.

### Footer
vipecoded with Claude (Anthropic) by conejito-vipe with love ❤️

---

## 🇺🇸 English

### Tomorrow (browser retrieval)
- [ ] Retrieve the Amadeu Antonio Stiftung chronicle (https://www.amadeu-antonio-stiftung.de/chronik/) with a browser. First 2015 to February 2017, then the rest. Read the detail pages; take over only facts and source links.
- [ ] Match against the 3,307 existing cases (date, municipality, text similarity). Mark duplicates, do not import them.
- [ ] Fully re-check the fatalities list (https://www.amadeu-antonio-stiftung.de/todesopfer-rechter-gewalt/). Currently 247 entries from page retrieval. For the 2016 Munich attack one person is probably missing (9 instead of 10). Check for further gaps.
- [ ] Obtain permission from the foundation (no licence on the site, "© Amadeu Antonio Stiftung").

### Data
- [ ] Unemployed persons (Federal Employment Agency): free data only at district level; municipality level is paid. Decide: show district level or buy municipality data. Until then the map shows persons without employment (census 2022, table 2000S-1001).
- [ ] Crime in general: police crime statistics exist only for the federation, states, districts and larger cities. Find sources (state police, Regionalstatistik) and the 20-year trend (2006 to 2025).
- [ ] Development since 2006: population and structure per municipality for 2006 (Regionalstatistik). Mind boundary changes.
- [ ] Election results: federal elections 2021, 2017, 2013, 2009 plus state and local elections at municipality level. Currently only the 2025 federal election as an approximation via the constituency.
- [ ] Census education (table 2000S-1003): only 1,578 municipalities available. Check for another table with wider coverage.
- [ ] Census boundaries 15 May 2022 vs. municipalities 31 Dec 2025: map the 37 unmatched AGS codes (mergers).
- [ ] State level: show Germans and foreigners (table 1000A-1019) in the state tooltip.
- [ ] Clarify: "data before and after the period". Which sources are meant (other chronicles, official figures before 2015 and after February 2017)?
- [ ] Clarify the 2016 overcount against the secondary source (about 144 %). Check the source of the comparison figure.
- [ ] Research 33 entries without a source URL and 3 without a source name. Review 125 possible duplicates (`daten/dubletten_pruefliste.csv`).

### Map and quality
- [ ] Test the map in a browser: state labels (NRW, Baden-Württemberg, Brandenburg/Berlin), borders (states blue, municipalities thin dashed), fatalities filter, panel, tables, load time (11 MB municipality geometry), smartphone view.
- [ ] The fatalities colour (purple) covers the case colouring in those municipalities. Check whether a pattern or ring is better.
- [ ] Spot-check street masking. The detection over-masks (e.g. "Bahnhof", "Marktplatz") and could miss single addresses.
- [ ] Place the note "point is not exact" visibly on the map (protection of accommodations).
- [ ] Public page with SEO: enable GitHub Pages from `docs/`, sitemap, Open Graph image, structured data. The private artifact page is not indexed by search engines.

### Rights and licence
- [ ] Clarify the licence: the repository contains GPL v3. The wish is "freely usable but not sellable". GPL allows selling, so it does not fit. Check alternatives for data (e.g. CC BY-NC 4.0). Observe attribution duties of the data sources (BKG and Destatis: Data licence Germany, attribution 2.0).
- [ ] The original CSV in the repo (`Chronik rechter Gewalt - Rechte Gewalt.csv`) contains exact coordinates and addresses. Decide whether it stays, is replaced or removed (protection of accommodations).
- [ ] Document the origin of the raw data.

### Footer
vipecoded with Claude (Anthropic) by conejito-vipe with love ❤️
