# Bad – Licht und Lüfter über Präsenzmelder + Feuchte

Stand 2026-10-20, live in HA (UI-Speicher, vorher Backup „vor Bad Licht/Lüfter 2026-10-20“).

| Automation | entity_id | id |
|---|---|---|
| Bad – Licht nach Präsenz | `automation.bad_licht_nach_prasenz` | `bad_licht_praesenz` |
| Bad – Lüfter nach Präsenz und Feuchte | `automation.bad_lufter_nach_prasenz_und_feuchte` | `bad_lufter_steuerung` |

YAML: [`packages/bad_licht_lufter.yaml`](../packages/bad_licht_lufter.yaml)

## Geräte

| Gerät | Modell | Entität in HA | Rolle |
|---|---|---|---|
| Badezimmer Präsenzmelder | HmIP-SPI (000C2409913F04) | `binary_sensor.badezimmer_badezimmer_prasenzmelder_anwesenheit` (Kanal 1) | Anwesenheit |
| Wandtaster 2fach Badezimmer | HmIP-BS2 (003164098DFFBC) | `switch.homematic_ip_wandtaster_2fach_badezimmer_ch4` | Badezimmerlicht |
| | | `switch.homematic_ip_wandtaster_2fach_badezimmer_ch8` | Badezimmerlüfter |
| Temperatursensor Bad | HmIP-STHD | `sensor.homematic_ip_temperatursensor_bad_klima_bad_rel_luftfeuchte` | Luftfeuchte (ganze %) |

Kanäle des HmIP-BS2: 1 und 2 sind die Tasten, 3 und 7 nur die Statusanzeige (`binary_sensor.…_ch3/_ch7`), 4 und 8 die echten Schaltkanäle, 5/6 und 9/10 die virtuellen Kanäle dazu. Direktverknüpfungen gehen immer auf **Kanal 4 bzw. 8**.

Der tado-Wert `sensor.bad_luftfeuchtigkeit` sitzt im Heizkörperventil und liegt meist 2–3 % unter dem STHD, deshalb nimmt die Automation den STHD.

## Ablauf

| Was | Licht (Kanal 4) | Lüfter (Kanal 8) |
|---|---|---|
| Anwesenheit kommt | an | an |
| Anwesenheit 1 min weg | aus | läuft weiter |
| Anwesenheit 10 min weg | – | aus, wenn Feuchte unter der Aus-Schwelle |
| Feuchte ≥ Ein-Schwelle | – | an (auch ohne Anwesenheit) |
| Feuchte < Aus-Schwelle seit 2 min, niemand seit 10 min | – | aus |
| 45 min niemand im Bad | – | aus (Sicherheitsnetz) |

Schwellen als Regler: `input_number.bad_lufter_feuchte_ein` (Start 72 %) und `input_number.bad_lufter_feuchte_aus` (Start 67 %). Die Helper haben keinen `initial`-Wert, damit Änderungen am Regler einen Neustart überleben. Wer das Package neu einspielt, stellt sie einmal auf 72 / 67.

Warum diese Werte (STHD, 2026-10-17 bis 2026-10-20): Grundfeuchte im Bad 60–66 %, abends bis 69 %, nach dem Duschen Spitzen von 72–78 %. Eine Ein-Schwelle von 70 % würde abends ohne Duschen auslösen. Liegt die Grundfeuchte länger über der Aus-Schwelle, beendet das 45-Minuten-Sicherheitsnetz den Lauf. Die Feuchte-Einschaltung kommt erst wieder, wenn die Feuchte erneut über die Ein-Schwelle steigt.

## Direktverknüpfung in der OpenCCU (Licht)

Vorteil: Das Licht geht auch, wenn HA oder das Netz hängt, und es schaltet funkdirekt ohne Umweg. Den Lüfter lassen wir in HA, weil die Feuchte-Regelung eine Direktverknüpfung nicht kann und sich zwei Steuerungen am selben Kanal gegenseitig ausschalten würden.

1. OpenCCU (raspimatic01) → **Einstellungen → Direktverknüpfungen → Neue Verknüpfung**.
2. **Sender:** „Badezimmer Präsenzmelder“, Kanal **:1** (000C2409913F04:1).
3. **Empfänger:** HmIP-BS2 003164098DFFBC, Kanal **:4** (nicht :3, das ist nur der Status).
4. Name z. B. „Bad Präsenz → Licht“, dann **Erstellen und bearbeiten**.
5. Profil beim Empfänger: das Profil mit Einschaltdauer wählen („Ein für eine bestimmte Zeit“ bzw. „Treppenhauslicht“, je nach OpenCCU-Version) und **Einschaltdauer 1 min**. Jede neue Präsenzmeldung startet die Zeit neu.
6. **Helligkeit:** In den Kanalparametern des SPI (Einstellungen → Geräte → Präsenzmelder → Kanal 1) die Helligkeitsschwelle so setzen, dass immer geschaltet wird. Sonst schaltet der SPI tagsüber nicht, obwohl er Anwesenheit meldet.
7. **Speichern** und dann am SPI die **Systemtaste kurz drücken**. Der SPI läuft auf Batterie und holt sich neue Konfigurationsdaten nur, wenn er wach ist. Solange unter **Servicemeldungen** „Konfigurationsdaten stehen zur Übertragung an“ steht, ist die Verknüpfung noch nicht im Gerät. Das ist der häufigste Grund, warum es „nicht geht“.
8. Testen: Bad betreten, Licht muss sofort angehen; nach Verlassen etwa 1 min plus die Haltezeit des SPI bis aus.
9. Läuft es: `automation.bad_licht_nach_prasenz` in HA **deaktivieren** (nicht löschen).

Weitere Stolperfallen:
- Die Tasten am BS2 sind ab Werk intern mit Kanal 4 und 8 verknüpft. Die bleiben, die neue Verknüpfung kommt dazu.
- Duty Cycle: Direktverknüpfungen zählen kaum, aber Kanal 4 nicht zusätzlich aus HA im Sekundentakt schalten.
- Sender und Empfänger müssen an derselben CCU hängen (beide raspimatic01, passt).

## Aufgeräumt am 2026-10-20

- Alter Bewegungsmelder HmIP-SMI55-2 (00319F29922FDA): von Carsten in der OpenCCU gelöscht und auf Werkseinstellung gesetzt, in HA sauber verschwunden. Kommt eventuell in den Eingang oder den Abstellraum.
- Alter Shelly 1 Bad (`switch.shelly1_500bf8`, durch den BS2 ersetzt): Integrationseintrag in HA gelöscht.
- Dashboards: Im „Test Dashboard“ zeigt die Bad-Raumkarte jetzt Präsenz = SPI, Licht = Kanal 4, dazu Lüfter und Heizung; die Bad-Kachel „Deckenlicht“ zeigt Kanal 4; bei der Keller-Raumkarte ist der fälschlich eingetragene Bad-Shelly als Licht entfernt. Im „Dashboard“ (Ansicht Licht, Grundriss) schaltet das Bad-Symbol jetzt Kanal 4.

## Falls ein Homematic-Gerät abgelernt wird (Vorgehen)

1. OpenCCU → Einstellungen → Geräte → Gerät → **Löschen** (ablernen). Soll er woanders hin, vorher „auf Werkseinstellungen zurücksetzen“ wählen.
2. HA: Das Gerät verschwindet aus Homematic(IP) Local. Bleiben Entitäten hängen („unique ID already exists“), hilft nur ein HA-Neustart.
3. Dashboard-Karten mit den alten Entitäten anpassen.
