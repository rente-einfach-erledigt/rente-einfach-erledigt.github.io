# SEO und GEO – Plan und Stand

Der SEO/GEO-Agent pflegt diese Datei (neueste Einträge oben in den Abschnitten).
Ziel: Menschen, die bei Google oder in KI-Antworten (ChatGPT, Perplexity, Google KI-Übersicht)
nach dem Altersvorsorgedepot fragen, landen auf rente-einfach-erledigt.github.io und rechnen ihre Förderung aus.

## Regeln für Artikel
- Alle Regeln aus marke.md gelten (informieren, nie beraten, „bis zu“, keine Rendite, Pflicht-Hinweis, Vorsprung bis 31.12.2026).
- Ein Artikel = eine Suchfrage. Die Antwort steht in den ersten 2 Sätzen (für KI-Zitate).
- 700–1.300 Wörter, kurze Absätze, Zwischenüberschriften als Fragen, eine Tabelle oder Liste mit Zahlen.
- Jede Zahl mit Quelle (Link am Ende), Stand-Datum sichtbar. Quellen-Reihenfolge laut marke.md: zuerst Helvetia, dann OVB, dann offizielle Stellen, Fachpresse nur ergänzend.
- Mindestens 2 Links auf den Rechner (/#rechner) und 1 Link auf einen anderen Artikel, sobald es welche gibt.
- Vorlage: vorlagen/artikel.html. Seite liegt unter docs/ratgeber/<slug>.html.
- JSON-LD: Article + FAQPage (3–5 Fragen aus dem Artikel). Seite in docs/sitemap.xml, docs/llms.txt und docs/ratgeber/index.html eintragen.

## Themen-Warteschlange (oben = als Nächstes)
1. riester-wechseln-altersvorsorgedepot – „Riester ins Altersvorsorgedepot wechseln: geht das ohne Verlust?“
2. altersvorsorgedepot-kinderzulage – „Kinderzulage im Altersvorsorgedepot: bis zu 300 € pro Kind“
3. altersvorsorgedepot-foerderung-zurueckzahlen – „Muss ich die Förderung im Altersvorsorgedepot zurückzahlen?“ (neu 19.10.: ING-FAQ „Kann ich die Förderung verlieren?“, Presse „540 Euro Staatszuschuss zurück?“)
4. altersvorsorgedepot-jetzt-abschliessen – „Altersvorsorgedepot schon 2026 abschließen: geht das?“
5. altersvorsorgedepot-selbststaendige – „Altersvorsorgedepot für Selbstständige: erstmals gefördert“
6. altersvorsorgedepot-kosten – „Was kostet das Altersvorsorgedepot? Der 1-%-Kostendeckel erklärt“
7. altersvorsorgedepot-standarddepot – „Staatliches Standarddepot: Was ist das und kommt es?“ (neu 19.10.: Start verzögert sich laut BMF, Presse 12.10.)
8. altersvorsorgedepot-vs-etf-sparplan – „Altersvorsorgedepot oder normaler ETF-Sparplan?“
9. altersvorsorgedepot-auszahlung – „Wann und wie wird das Altersvorsorgedepot ausgezahlt?“

## Wartet auf Freigabe
- 2026-10-19 – altersvorsorgedepot-rechner – „Altersvorsorgedepot Rechner: So viel Förderung bekommst du“ (Zweig artikel/altersvorsorgedepot-rechner, enthält auch /ratgeber/, Sitemap, llms.txt, Footer-Link)

## Veröffentlicht
(noch keine)

## GEO-Beobachtungen
- 2026-10-19 – Google „Altersvorsorgedepot Rechner“: oben stehen Raisin, steuerschroeder.de, HanseMerkur, zendepot, extraETF, Finanztip, covago – fast nur Anbieter/Portale mit eigenem Rechner; unsere Seite taucht noch nicht auf.
- 2026-10-19 – Infoseiten (ING, finanzfacts) nutzen Fragen als Zwischenüberschriften („Kann ich die Förderung verlieren?“, „Wird die Förderung automatisch gutgeschrieben?“); finanzfacts zeigt ein sichtbares Prüfdatum – passt zu unserem Stand-Datum.
- 2026-10-19 – Laut finanzfacts (Stand 17.10.) war am 06.10. noch kein Altersvorsorgedepot vom BZSt zertifiziert; finanzen.net (05.10.) schreibt, vor 01.01.2027 könne kein Anbieter verkaufen. Felix hat am 19.10. bestätigt: Über die OVB/Helvetia-Strecke ist das Depot jetzt abschließbar, die Förderung gibt es ab Januar 2027. Formulierung bleibt: „Depot jetzt eröffnen, Förderung ab 2027“.
