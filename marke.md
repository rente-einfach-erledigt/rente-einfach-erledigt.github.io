# @rente.einfach.erledigt – Marke und Regeln

Dieses Dokument lesen alle Agenten zuerst. Es gilt immer.

## Ziel
Felix (OVB-Vermittler) gewinnt Kunden für das **Altersvorsorgedepot (AVD)** über eine
OVB-Direktabschlussstrecke (Helvetia/Xaver) – ganz ohne Beratung.
Abschluss-Link (in jede DM, in die Bio): https://ovb.helvetia-altersvorsorge.de/get-started

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

## Fakten (vor jeder Woche per Websuche prüfen)
- Grundzulage bis zu 540 € pro Jahr
- Kinderzulage bis zu 300 € pro Kind und Jahr
- Berufseinsteigerbonus einmalig 200 € (Altersgrenze vor Nutzung prüfen)
- Kostendeckel Standarddepot: max. 1 % Effektivkosten pro Jahr
- Anlage in Fonds/ETFs, keine Beitragsgarantie
- Riester-Verträge können weiterlaufen oder ins AVD gewechselt werden

## Regeln (Pflicht)
- Informieren, nie beraten. Keine Empfehlung „du solltest …“.
- Zulagen immer mit „bis zu“.
- Keine Renditeversprechen, keine Zinsbeispiele.
- Jede Caption endet mit: „Keine Anlageberatung. Keine Beitragsgarantie, der Wert kann schwanken.“
- Nie „kündige Riester“. Kündigen kann Förderung kosten – nur so erwähnen.
- Keine Zulagen für 2026 versprechen.
- Keine falsche Dringlichkeit, keine Fake-Countdowns.
- Faceless: nur Grafiken, Text, ggf. KI-Stimme. Kein Gesicht.

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

## Ablauf
1. Sonntag: Wochen-Agent recherchiert, schreibt 7 Posts, rendert Bilder, pusht sie hierher,
   lädt sie zu iHatePosting (upload_media per raw.githubusercontent-URL), legt Entwürfe an
   und trägt alles in die Freigabe-Seite ein.
2. Felix tippt auf der Freigabe-Seite ✓ oder ✗.
3. Täglich: Posting-Agent plant freigegebene Entwürfe zum geplanten Termin ein, löscht abgelehnte.
4. Freitag: Auswertungs-Agent schreibt Erkenntnisse in `lernen.md`.

## Adressen
- Freigabe-Seite (Artefakt mit Datenbank, Sammlung `posts`): https://claude.ai/artifact/ND7MXo9UfG9widVMYUCmnh
- Bilder öffentlich: https://raw.githubusercontent.com/zhwolffelix-code/rente-einfach-erledigt-content/main/posts/<id>/folie_N.png
- iHatePosting: Konto von Felix, Zeitzone Europe/Berlin

## Datenmodell Freigabe-Seite (`posts/<id>`, id = `JJJJ-MM-TT-thema`)
datum (JJJJ-MM-TT), uhrzeit (HH:MM), thema, zielgruppe, wort, kanaele [..], format, caption,
bilder [/_blob/... Asset-URLs der Freigabe-Seite], status, ihpPostId, hinweis, erstelltAm
status: offen → freigegeben | abgelehnt (Felix) → geplant → gepostet | fehler (Agenten)
