# Chronik rechter Gewalt

🇩🇪 [Deutsch](#-deutsch) · 🇺🇸 [English](#-english)

---

## 🇩🇪 Deutsch

Durchsuchbare Chronik von Angriffen auf Geflüchtete und ihre Unterkünfte (Januar 2015 bis Februar 2017) mit interaktiver Karte bis auf Gemeindeebene, Vergleichsstatistik und einer Liste der Todesopfer rechter Gewalt.

### Was es gibt
- **Karte** (`docs/index.html`): Deutschland nach Gemeinden eingefärbt, nach Fallzahl oder pro 100.000 Einwohner. Bundesland-Grenzen blau, Gemeindegrenzen dünn gestrichelt. Einfärbungen, Gemeinden, Länder und Todesopfer-Gemeinden sind anklickbar und wirken als Filter.
- **Suche und Einzelfälle**: 3.307 Fälle mit Datum, Gemeinde, Kategorie, Beschreibung und Quellenlinks (öffnen im neuen Tab).
- **Statistik je Gemeinde**, absolut und in Prozent: Einwohner, Männer und Frauen, Deutsche und Ausländer, Erwerbsstatus, beruflicher Abschluss, Bundestagswahl 2025. Weitere Kennzahlen siehe [TODO.md](TODO.md).
- **Todesopfer rechter Gewalt** (1990 bis 2026): Faktenangaben aus der Liste der Amadeu Antonio Stiftung mit Link zur Einzelseite.
- **Daten**: bereinigte und geschützte CSV (`daten/chronik_public.csv`), Dublettenprotokolle, Skripte (`tools/`).

### Schutz der Unterkünfte
Die Karte zeigt Fälle nur auf Gemeindeebene. Der Punkt liegt nicht an der echten Stelle. Straßennamen und ähnliche Adressangaben sind in den Beschreibungen maskiert. So lassen sich Unterkünfte nicht aus der Karte ableiten.

### Verzeichnis
- `docs/` Karte und Daten der Karte (Gemeindegrenzen, Statistik, Wahl, Todesopfer)
- `daten/` Fälle (maskiert), Dublettenprotokolle
- `doku/` Vergleich mit amtlichen Zahlen, Datenquellen, Beschreibungstexte
- `tools/` Aufbereitungsskripte, Zensus-Download
- `TODO.md` offene Punkte · `RELEASE_NOTES.md` Änderungen

### Datenquellen
Siehe [doku/DATENQUELLEN.md](doku/DATENQUELLEN.md). Alle Quellen sind mit Tabelle und Stand angegeben.

### Lizenz
Offen. Das Repository enthält GPL v3, das für Daten nicht passt. Gewünscht ist „frei nutzbar, aber nicht verkaufbar“. Bis zur Klärung gelten die Lizenzen der Quellen (Datenlizenz Deutschland, Namensnennung 2.0 für BKG und Destatis). Die Daten der Amadeu Antonio Stiftung liegen als Faktenangaben mit Link vor. Rechte an deren Texten bleiben bei der Stiftung.

### Grenzen
- Die Chronik erhebt keinen Anspruch auf Vollständigkeit. 54 % der Fälle stammen aus Antworten von Regierungen und Parlamenten.
- Zensus-Werte beziehen sich auf den 15.05.2022 und sind gerundet. Berufsabschlüsse gibt es nur für 1.578 Gemeinden.
- Die Bundestagswahl 2025 ist über den Wahlkreis genähert, nicht je Gemeinde ausgezählt.
- Erwerbslose (Zensus, Befragung) sind nicht die bei der Arbeitsagentur gemeldeten Arbeitslosen.

### Footer
vipecoded with Claude (Anthropic) by conejito-vipe with love ❤️

---

## 🇺🇸 English

Searchable chronicle of attacks on refugees and their accommodation (January 2015 to February 2017) with an interactive map down to municipality level, comparison statistics and a list of fatalities of right-wing violence.

### What is included
- **Map** (`docs/index.html`): Germany coloured by municipality, by case count or per 100,000 inhabitants. State borders blue, municipality borders thin dashed. Colour classes, municipalities, states and fatality municipalities are clickable and work as filters.
- **Search and individual cases**: 3,307 cases with date, municipality, category, description and source links (open in a new tab).
- **Statistics per municipality**, absolute and in percent: population, men and women, Germans and foreigners, employment status, vocational qualification, 2025 federal election. More indicators: see [TODO.md](TODO.md).
- **Fatalities of right-wing violence** (1990 to 2026): facts from the Amadeu Antonio Stiftung list with a link to the detail page.
- **Data**: cleaned and protected CSV (`daten/chronik_public.csv`), duplicate logs, scripts (`tools/`).

### Protection of accommodation
The map shows cases at municipality level only. The point is not at the real location. Street names and similar address details are masked in the descriptions, so accommodation cannot be derived from the map.

### Layout
- `docs/` map and its data (municipality boundaries, statistics, elections, fatalities)
- `daten/` cases (masked), duplicate logs
- `doku/` comparison with official figures, data sources, description texts
- `tools/` preparation scripts, census download
- `TODO.md` open items · `RELEASE_NOTES.md` changes

### Data sources
See [doku/DATENQUELLEN.md](doku/DATENQUELLEN.md). Every source is listed with table and date.

### Licence
Open. The repository contains GPL v3, which does not fit data. The wish is "freely usable but not sellable". Until clarified, the licences of the sources apply (Data licence Germany, attribution 2.0 for BKG and Destatis). Amadeu Antonio Stiftung data is kept as facts with a link. Rights in its texts stay with the foundation.

### Limits
- The chronicle does not claim to be complete. 54 % of the cases come from answers of governments and parliaments.
- Census values refer to 15 May 2022 and are rounded. Vocational qualifications exist for 1,578 municipalities only.
- The 2025 federal election is approximated via the constituency, not counted per municipality.
- Persons without employment (census, survey) are not the unemployed registered with the employment agency.

### Footer
vipecoded with Claude (Anthropic) by conejito-vipe with love ❤️
