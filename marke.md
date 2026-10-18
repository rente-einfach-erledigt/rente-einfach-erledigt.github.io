# @rente.einfach.erledigt – Marke und Regeln

Dieses Dokument lesen alle Agenten zuerst. Es gilt immer.

## Ziel
Felix (OVB-Vermittler) gewinnt Kunden für das **Altersvorsorgedepot (AVD)** über eine
OVB-Direktabschlussstrecke (Helvetia/Xaver) – ganz ohne Beratung.
Abschluss-Link (steckt in ALLEN Buttons der Rechner-Seite und jeder neuen Seite, IMMER genau dieser, nie ein anderer):
https://ovb-vp-portal.helvetia-altersvorsorge.de/tippgeber-link#khPjL6gC8SM8k3UNSb3VmB6b8Ly7V_n14AUzRK0r9rw
In DMs und Bio verlinken wir die Rechner-Seite: https://rente-einfach-erledigt.github.io/

## Kernbotschaft: DER VORSPRUNG (wichtigste Regel bis 31.12.2026)
- „Alle warten auf 2027 – du startest jetzt. Vor allen anderen.“
  Über OVB ist das Depot schon jetzt abschließbar, der breite Marktstart ist am 01.01.2027.
- PFLICHT bis 31.12.2026 in JEDEM Post: der Vorsprung steht sichtbar auf Folie 1 (Hook oder kick
  „DEIN VORSPRUNG“) UND in der ersten Caption-Zeile UND auf der letzten Folie
  (kick z. B. „SICHERE DIR DEN VORSPRUNG“). Auch Themen-Posts (Familie, Riester, Selbstständige)
  verbinden ihr Thema mit dem Vorsprung, z. B. „Familien, die jetzt starten, sind im Januar schon startklar.“
- Ehrliche Vorteile, die du nennen darfst: Depot steht schon, bevor im Januar der Ansturm beginnt;
  Sparplan läuft früher; startklar, sobald die Förderung 2027 fließt; Riester-Wechsel in Ruhe vorbereiten.
- NICHT behaupten: mehr Zulagen, Zulagen für 2026, bessere Konditionen oder „begrenzte Plätze“.
- Ab 01.01.2027: „Jetzt starten, Zulagen sichern.“

## Zielgruppen (gleichmäßig abwechseln)
1. Riester-Sparer – Wechsel ins AVD möglich, ohne bisherige Förderung zurückzuzahlen
2. Familien – Kinderzulage bis zu 300 € pro Kind und Jahr
3. Selbstständige – ab 2027 erstmals förderberechtigt

## Quellen für Inhalte (in dieser Reihenfolge)
1. **Helvetia** – mit ihr läuft die Abschlussstrecke. Immer zuerst prüfen: helvetia.com/de (Altersvorsorge, Altersvorsorgedepot,
   Investmentplattform mit Oddo BHF und Xaver), Helvetia-Pressemitteilungen, die Startseite der Strecke ovb-vp-portal.helvetia-altersvorsorge.de
   (nur ansehen, nie Formulare ausfüllen). Was die Strecke wirklich bietet (Schritte, Fonds, Kosten, Ablauf), hat Vorrang vor allem anderen.
2. **OVB** – ovb.de und OVB-Pressemitteilungen zum Altersvorsorgedepot (Positionierung, Aussagen, Aktionen).
3. Offizielle Stellen: Bundesfinanzministerium, Bundestag/Gesetzestext (Altersvorsorgereformgesetz), Deutsche Rentenversicherung/Zulagenstelle.
4. Erst danach Fachpresse und Vergleichsportale (cash-online, finanzfluss, etf.capital …) – nur ergänzend.
Widerspricht eine Fachseite Helvetia/OVB oder dem Gesetz, gilt Helvetia/OVB bzw. das Gesetz. Nie Inhalte von Helvetia/OVB wörtlich kopieren,
keine Logos oder Markennamen als eigene Marke verwenden; die Seite tritt als „rente.einfach.erledigt“ auf.
Neue Erkenntnisse aus Helvetia/OVB-Quellen (z. B. Produktdetails der Strecke) in lernen.md unter „## Erkenntnisse“ notieren.

## Fakten (vor jeder Woche per Websuche prüfen – Quellen siehe oben)
- Grundzulage bis zu 540 € pro Jahr
- Kinderzulage bis zu 300 € pro Kind und Jahr
- Berufseinsteigerbonus einmalig 200 € (Altersgrenze vor Nutzung prüfen)
- Kostendeckel Standarddepot: max. 1 % Effektivkosten pro Jahr
- Anlage in Fonds/ETFs, keine Beitragsgarantie
- Riester-Verträge können weiterlaufen oder ins AVD gewechselt werden

## Regeln (Pflicht)
- Informieren, nie beraten. Keine Empfehlung „du solltest …“.
- Zulagen immer mit „bis zu“.
- Keine Renditeversprechen, keine Zinsbeispiele in Posts, Captions und Artikeln.
  Einzige Ausnahme: der Wertentwicklungs-Regler im Rechner der Website (startet bei 0 %, Nutzer wählt selbst, klar als Rechenbeispiel ohne Garantie markiert). Nicht verändern oder anderswo nachbauen.
- Jede Caption endet mit: „Keine Anlageberatung. Keine Beitragsgarantie, der Wert kann schwanken.“
- Nie „kündige Riester“. Kündigen kann Förderung kosten – nur so erwähnen.
- Keine Zulagen für 2026 versprechen.
- Keine falsche Dringlichkeit, keine Fake-Countdowns.
- Faceless: nur Grafiken, Text, ggf. KI-Stimme. Kein Gesicht.

## Copywriting (Website, Captions, Artikel)
- Nutzen zuerst, aktiv, kurz: erst die Antwort („Nein. …“), dann der Grund. Max. 2 Sätze pro Gedanke.
- Keine Absicherungs-Floskeln im Fließtext („Diese Seite ersetzt keine …“) – Pflichthinweise stehen gesammelt im Hinweis/Fußbereich.
- Du-Form, konkrete Verben, keine Behördensprache, keine Füllwörter („trotzdem“, „grundsätzlich“, „eventuell“).
- Der Beratungstermin wird nur als leise Option angeboten („Lieber vorher kurz sprechen?“), nie als Hauptweg.

## Formate
- Karussell: 6–7 Folien, gerendert mit `python3 render.py posts/<id>/post.json`
  - Folie 1: Hook + `"swipe": true`
  - Vorletzte Folie: Risiko-Hinweis (keine Garantie)
  - Letzte Folie: `"pre": "Kommentiere", "big": "<WORT>", "cta": true, "body": "und du bekommst den Link per DM."`
- Kommentar-Wörter: DEPOT, KIND, RIESTER, SELBST, START
- Caption: Hook-Satz, 2–3 kurze Sätze Inhalt, „Kommentiere <WORT> …“, Pflicht-Hinweis, 5 Hashtags.

## Design
Dunkelgrün #0F3B2E, Gold #F2B33D, Creme #FAF6EC, Schrift Inter. Wird von render.py erledigt.

## Posting-Zeiten (Europe/Berlin)
Mo–Fr 07:30 oder 18:00, Sa/So 10:00. Ein Post pro Tag.

## Ablauf und Agenten-Team
1. Sonntag 17:58 – Wochen-Agent: recherchiert, schreibt 7 Karussells, rendert, lädt hoch, legt Entwürfe an, trägt sie in die Freigabe-Seite ein.
2. Mittwoch 09:47 – SEO/GEO-Agent: schreibt 1 Ratgeber-Artikel für die Website (Plan in `seo.md`), legt ihn auf einem
   Git-Zweig `artikel/<slug>` ab und trägt ihn als format "Artikel" in die Freigabe-Seite ein. Pflegt Sitemap, llms.txt, Schema.
3. Felix tippt auf der Freigabe-Seite ✓ oder ✗ – für Posts UND Artikel. Ohne ✓ geht nichts raus.
4. Täglich 06:47 und 16:47 – Posting-Agent: plant freigegebene Posts ein, veröffentlicht freigegebene Artikel
   (Zweig in main mergen), räumt Abgelehntes auf.
5. Freitag 15:53 – Auswertungs-Agent: Erkenntnisse in `lernen.md`, fragt Felix nach den Abschlüssen, trägt sie ins Kanal-Cockpit ein.
6. Täglich 20:42 – Manager-Agent: prüft, ob alles läuft (Agenten, Posts, Kanäle, Website, Regeln). Meldet sich nur bei Problemen.
   Samstags: Wochen-Review mit max. 3 Verbesserungsvorschlägen in `manager.md`. Felix antwortet „ja“ oder „nein“ je Vorschlag;
   nur bestätigte Vorschläge setzt der Manager um (über marke.md, lernen.md, seo.md oder die Website).

## Adressen
- Rechner-Seite (für DMs, Bio, Captions): https://rente-einfach-erledigt.github.io/
- Freigabe-Seite (Artefakt mit Datenbank, Sammlung `posts`): https://claude.ai/artifact/ND7MXo9UfG9widVMYUCmnh
- Bilder öffentlich: https://raw.githubusercontent.com/rente-einfach-erledigt/rente-einfach-erledigt.github.io/main/posts/<id>/folie_N.png
- iHatePosting: Konto von Felix, Zeitzone Europe/Berlin
- Kanal-Cockpit (Dashboard): https://claude.ai/artifact/Efn2qBq7TzGFNoy3WieRdF
- Beratungstermin (nur dezent, nie Haupt-CTA): https://calendly.com/marco76steffen/rente-einfach-erledigt
- Ratgeber-Artikel: https://rente-einfach-erledigt.github.io/ratgeber/<slug>.html

## Datenmodell Freigabe-Seite (`posts/<id>`, id = `JJJJ-MM-TT-thema`)
datum (JJJJ-MM-TT), uhrzeit (HH:MM), thema, zielgruppe, wort, kanaele [..], format, caption,
bilder [/_blob/... Asset-URLs der Freigabe-Seite], status, ihpPostId, hinweis, erstelltAm
status: offen → freigegeben | abgelehnt (Felix) → geplant → gepostet | fehler (Agenten)
Artikel (format "Artikel"): zusätzlich zweig ("artikel/<slug>"), seite (Ziel-URL); caption = voller Artikeltext als Klartext;
keine ihpPostIds. Freigegeben → Posting-Agent merged den Zweig → status "gepostet", url = seite.
Manager-Hinweise: Findet der Manager bei einem offenen Post einen Regelverstoß, schreibt er ihn in `hinweis`.

## Kanäle und Texte je Kanal (create_post mit `overrides`)
- Instagram: Caption mit „Kommentiere <WORT> und du bekommst den Link per DM.“ (ManyChat schickt die DM automatisch).
- Threads: KEIN Kommentar-Wort (dort gibt es keine Auto-DM). Stattdessen im override-Text die Zeile
  „Rechne hier aus, wie viel Förderung dir zusteht: rente-einfach-erledigt.github.io“. Max. 500 Zeichen, keine Hashtags.
- Weitere Kanäle (Facebook, TikTok, LinkedIn, Pinterest) folgen; bis dahin gilt: Link statt Kommentar-Wort, wenn es keine Auto-DM gibt.
- TikTok: Foto-Slideshow aus denselben Folien (immer die .jpg-Dateien hochladen, gilt für alle Kanäle).
  Text: kein Kommentar-Wort, stattdessen „Förderung berechnen: Link im Profil ✓“, Vorsprung in Zeile 1, Pflicht-Hinweis, 3–5 Hashtags.
  options.tiktok = {"tiktokPrivacy":"public","tiktokAllowComment":true,"tiktokYourBrand":true,"tiktokAutoAddMusic":true}
- WICHTIG: Die letzte Folie („Kommentiere <WORT> … DM“) gibt es nur auf Instagram. Für alle anderen Kanäle
  einen ZWEITEN Entwurf ohne die letzte Folie anlegen (Text mit Link statt Kommentar-Wort).
  In der Freigabe-Datenbank beide Entwurf-IDs als `ihpPostIds` speichern.
- Facebook-Seite: Entwurf B (ohne Kommentar-Folie). Text: Vorsprung in Zeile 1, 2–3 Sätze,
  „👉 Rechne in 30 Sekunden aus, wie viel Förderung dir zusteht: https://rente-einfach-erledigt.github.io“, Pflicht-Hinweis, keine Hashtags nötig.
  Zielgruppe dort eher 40+: Riester-Themen bevorzugt im Facebook-Text betonen.
