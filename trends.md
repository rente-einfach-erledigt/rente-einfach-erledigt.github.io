# Trends – was gerade funktioniert (Trend-Agent pflegt diese Datei)

Wochen-, Video- und Feed-Agent lesen sie vor jeder Planung. Neueste Einträge oben.
Status je Trend: neu → im Test → behalten | verworfen (entscheidet der Auswertungs-Agent anhand der Zahlen).

## Aktive Trends (max. 8)

### T1 – Anlass: Frühstartrente beschlossen (Familien) – Status: neu
- **Was:** Der Bundestag hat am 16.10.2026 die Frühstartrente beschlossen: der Staat zahlt Kindern von 6 bis 18 Jahren 10 € pro Monat in ein kapitalgedecktes Vorsorgedepot; Eltern/Großeltern können bis zu 6.840 € pro Jahr dazulegen.
- **Warum jetzt:** Große Rentennachricht der Woche, Eltern suchen gerade Erklärungen. Belege: [Bundestag, 16.10.2026](https://www.bundestag.de/dokumente/textarchiv/2026/kw42-de-fruehstartrente-1223624), [Ihre Vorsorge (DRV), 16.10.2026](https://www.ihre-vorsorge.de/altersvorsorge/nachrichten/bundestag-beschliesst-fruehstartrente). Bundesrat muss noch zustimmen, Zahlungen laut Ihre Vorsorge ab 2027 geplant – vor jedem Post per Websuche Stand prüfen.
- **Umsetzung:** Video: hook („Neu beschlossen: *10 € im Monat* für dein Kind“) → text (was die Frühstartrente ist, „Bundesrat muss noch zustimmen“) → counter Kinderzulage AVD „bis zu 300 € pro Kind und Jahr“ → persona Familie mit 2 Kindern → cta. Karussell: „Frühstartrente vs. Kinderzulage – was ist was?“ (2 Spalten, persona-Folie).
- **Zielgruppe:** Familien. **Grenzen:** Nicht behaupten, die Frühstartrente laufe über unsere Strecke; keine Zahlungen für 2026; kein „schnell, bevor …“.

### T2 – Anlass: Weltspartag Fr 30.10.2026 (Einsteiger/Familien) – Status: neu
- **Was:** Der Weltspartag fällt 2026 auf Freitag, 30. Oktober – Banken und Medien sprechen über Sparen, guter Aufhänger „Sparschwein früher vs. geförderter Sparplan heute“.
- **Warum jetzt:** Fester Termin in 11 Tagen. Beleg: [ING Wissen „Ihre Finanzen im Oktober 2026“](https://www.ing.de/wissen/oktober-2026/), [Sparkasse Weltspartag](https://www.sparkasse.de/weltspartag.html).
- **Umsetzung:** Beitrag am 30.10. (Karussell 07:30 oder 18:00). Hook: „Weltspartag: Früher gab’s ein Sparschwein. *Ab 2027 legt der Staat bis zu 50 Cent pro Euro drauf.*“ Folien/Szenen: bars („Du zahlst“ vs. „Staat legt drauf“) → persona Azubi mit 50 €/Monat (+ Einsteigerbonus) → Vorsprung → cta.
- **Zielgruppe:** Einsteiger unter 25 (alternativ Familien). **Grenzen:** Keine Zinsbeispiele, Zulagen mit „bis zu“, keine Zulagen für 2026.

### T3 – Format: „Was ist eigentlich …?“ (Text-Setup + Erklärung) – Status: neu
- **Was:** Ein Begriff als Frage in großem Text („WTF is …“-Mechanik), danach in 3–4 schnellen Szenen die Auflösung mit eigenem Ton.
- **Warum jetzt:** Laut [NewEngen Instagram-Trends Oktober 2026 (Stand 01.10.2026)](https://newengen.com/insights/instagram-trends/) wächst „WTF Is…“ (Text-Setup + Gegenbild), ohne Gesicht und mit Originalton auf jedem Kontotyp machbar.
- **Umsetzung:** Video: hook „Was ist eigentlich das *Altersvorsorgedepot*?“ (oder „… die Grundzulage?“, „… der Riester-Wechsel?“) → list (3 Punkte) → counter → cta. Untertitel groß, 18–25 s. Wir schreiben „Was ist eigentlich …“, nicht „WTF“.
- **Zielgruppe:** Einsteiger unter 25, Grundlagen.

### T4 – Format: Mythos-Serie „Ein Irrtum pro Clip“ mit Folgen-Nummer – Status: neu
- **Was:** Pro Video genau ein verbreiteter Irrtum, aufgelöst in einem Satz, als nummerierte Serie („Irrtum 1/5“).
- **Warum jetzt:** NewEngen (01.10.2026) nennt das Schilder-Format „ein Mythos pro Clip“ als aktuellen Trend für Nischen-Mythen ([Quelle](https://newengen.com/insights/instagram-trends/)); [Lightreel Wochenbericht 10.–17.10.2026](https://lightreel.ai/blogs/whats-trending-on-instagram) sieht serielle Episoden mit Nummer + Recap wachsen.
- **Umsetzung:** video.py `myth`-Szene als Herzstück, kick „IRRTUM 1/5“ in der hook-Szene; Reihe z. B. „Riester muss ich kündigen“ → „Selbstständige bekommen keine Förderung“ → „Ich bin zu jung dafür“. Danach counter/persona → cta. Pro Woche max. 1 Folge, Zielgruppe wechselt.
- **Zielgruppe:** je Folge eine (Riester 40+, Selbstständige, Einsteiger). **Grenzen:** nie „kündige Riester“.

### T5 – Format: Problem → Weg → Ergebnis / Vorher-Nachher-Rechnung – Status: neu
- **Was:** Alltagsproblem als Text-Hook, dann der Weg, dann das sichtbare Ergebnis als Zahl bzw. zwei Figuren im Vergleich.
- **Warum jetzt:** [Lightreel 10.–17.10.2026](https://lightreel.ai/blogs/whats-trending-on-instagram) nennt „Problem → Weg → Beweis“ und Vorher/Nachher-Vergleich als aktuelle faceless Mechaniken; Karussells holen laut [Metricool-Instagram-Studie 2026 (OnlineMarketing.de, 06.07.2026)](https://onlinemarketing.de/social-media-marketing/instagram-studie-2026-formate-beste-performance) rund 9× mehr Speicherungen als Einzelbilder, Reels die meisten Shares.
- **Umsetzung:** Hook „Ich spare 100 € im Monat – *und der Staat?*“ → zwei persona-Szenen/-Folien („ohne Förderung“ vs. „mit Zulagen“, bzw. „startet mit 25 vs. 45“) → bars → cta. Als Karussell mit Hinweis „Speichern für später“ auf der vorletzten Folie.
- **Zielgruppe:** Selbstständige oder Riester-Sparer (Facebook 40+). **Grenzen:** nur Beiträge + Zulagen, keine Kursentwicklung.

### Eigene Zahlen (Stand 19.10.2026)
- Noch zu wenig Daten (2 Beiträge je Kanal): Instagram 5 Interaktionen (Start-Post DEPOT, 2 Kommentare), Threads 111 Aufrufe, TikTok 54 Aufrufe, Facebook keine Werte. Noch kein „Eigener Gewinner“.

## Tests dieser und letzter Woche
(Format: Datum – Beitrag-ID – Trend – Kanal – Ergebnis gegenüber Durchschnitt)

## Verworfen (nicht wieder testen)
(noch keine)
