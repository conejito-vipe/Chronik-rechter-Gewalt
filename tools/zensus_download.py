#!/usr/bin/env python3
"""Lädt Tabellen der Zensusdatenbank 2022 per Web-Service als CSV.

Start per Doppelklick auf zensus_download.bat (Windows) bzw. zensus_download.command (Mac).
Das Programm fragt nach dem API-Token. Der Token wird beim Tippen nicht angezeigt
und nirgends gespeichert.
"""
import getpass
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://ergebnisse.zensus2022.de/api/rest/2020/data/tablefile"
TABELLEN = ["1000A-1019", "2000S-1003"]  # Staatsangehörigkeit, Bildung


def hole(tabelle, token):
    body = urllib.parse.urlencode({
        "name": tabelle,
        "area": "all",
        "format": "csv",
        "language": "de",
    }).encode()
    req = urllib.request.Request(BASE, data=body, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    req.add_header("username", token)
    req.add_header("password", "")
    with urllib.request.urlopen(req, timeout=900) as r:
        return r.read()


def main():
    ordner = os.path.dirname(os.path.abspath(__file__))
    token = os.environ.get("ZENSUS_TOKEN") or getpass.getpass(
        "API-Token einfügen (Eingabe bleibt unsichtbar) und Enter drücken: "
    ).strip()
    if not token:
        print("Kein Token eingegeben.")
        return 1
    for t in TABELLEN:
        print("Lade", t, "... (kann einige Minuten dauern)")
        try:
            data = hole(t, token)
        except urllib.error.HTTPError as e:
            print("  Fehler", e.code, e.reason)
            if e.code in (401, 403):
                print("  Der Token ist falsch oder abgelaufen. Neuen Token in der Zensusdatenbank erzeugen.")
            return 1
        except Exception as e:  # Netzwerk, Zeitüberschreitung u. a.
            print("  Fehler:", e)
            return 1
        ziel = os.path.join(ordner, t + ".csv")
        with open(ziel, "wb") as f:
            f.write(data)
        print("  gespeichert:", ziel, "(" + str(len(data)) + " Bytes)")
    print("Fertig. Bitte beide CSV-Dateien im Chat hochladen.")
    return 0


if __name__ == "__main__":
    code = main()
    input("\nEnter drücken zum Schließen ...")
    sys.exit(code)
