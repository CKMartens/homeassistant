# Ford Capri (Elke) – Vorklimatisierung an Diensttagen

Stand 2026-10-07, live in HA als `automation.auto_capri_vorklimatisierung_diensttage`.
YAML: [`packages/capri_vorklimatisierung.yaml`](../packages/capri_vorklimatisierung.yaml)
Schwester-Automation und Stufenlogik: [MG-Vorklimatisierung](mg_vorklimatisierung.md)

## Rahmenbedingungen

- Diensttage: Termin „Dienst“ in `calendar.dienst_elke` (meist 07:00, nie vor 06:00). „Schulung“ wird ignoriert.
- Abfahrt = Dienstbeginn − 60 min (gut 40 min Fahrt, Elke ist gern etwas eher da). Eine andere Abfahrtszeit ergibt sich aus einem anderen Dienstbeginn im Kalender.
- Steht wie der MG draußen; die Wetterstufen nutzen dieselben Nachtwerte (`input_number.mg_nacht_*`, 22:00-Snapshot der MG-Automation).

## Entitäten (FordPass, HACS)

| Zweck | entity_id |
|---|---|
| Fernstart | `switch.fordpass_wf0spbef1tsd01110_ignition` |
| Status / Restlaufzeit | `sensor.fordpass_wf0spbef1tsd01110_remotestartstatus`, `_remotestartcountdown` |
| Temperatur für Fernstart | `select.fordpass_wf0spbef1tsd01110_rcctemperature` (lo, 16_0 … 30_0, hi) |
| Frontscheibe | `switch.fordpass_wf0spbef1tsd01110_rccdefrostfront` |
| Heckscheibe | `switch.fordpass_wf0spbef1tsd01110_rccdefrostrear` |
| Laufzeit verlängern | `button.fordpass_wf0spbef1tsd01110_extendremotestart` (nur verfügbar, solange er läuft) |
| Daten holen | `button.fordpass_wf0spbef1tsd01110_request_refresh` |
| Akku / Stecker | `sensor.fordpass_wf0spbef1tsd01110_soc`, `_elvehplug` |
| Push | `notify.mobile_app_pixel_9a` (Elke) |

Die `sensor.ford_capri_2025_extended_range_rwd_*` kommen aus ABRP und sind nur lesend.

## Ablauf

| Stufe | Temperatur | Frontscheibe | Heckscheibe | Start | Laufzeit |
|---|---|---|---|---|---|
| 3 – Vereisung | hi | an | an | Abfahrt − 30 min | einmal verlängert |
| 2 – Frost | hi | an | an | Abfahrt − 15 min | Standard |
| 1 – Beschlag | 22 °C | aus | an | Abfahrt − 15 min | Standard |
| 0 | – | – | – | – | – |

Geprüft wird bei Dienstbeginn − 95 min. Unter 20 % Akku gibt es keinen Start, außer der Capri hängt am Kabel.
Wird der Start nicht bestätigt: Remote Sync, dann genau ein Retry, danach ein Push an Elke.

## Offen

- Beim ersten echten Lauf im Trace prüfen: Laufzeit des Ford-Fernstarts (angenommen 15 min) und ob die Defrost-Switches vor dem Start übernommen werden.
- Die Automation hängt am 22:00-Snapshot der MG-Automation. Wird die deaktiviert, rechnet sie mit veralteten Nachtwerten.
