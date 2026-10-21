# homeassistant

Konfiguration und Doku für Home Assistant „Casa Martens“: Blueprints, Automationen, Skripte und Helper, die in HA eingespielt sind (oder dafür vorbereitet wurden), als Backup und zur Versionierung.

- `blueprints/automation/`: eigene Blueprints
- `packages/`: YAML je Thema, nutzbar als HA-Package oder zum Kopieren in die UI (Hinweise im Kopfkommentar jeder Datei)
- `dashboards/`, `themes/`: Dashboard-Umbauten und Themes
- `docs/`: Beschreibung, Ablauf und Stolperfallen je Thema

## Blueprints

| Blueprint | Beschreibung | Status |
|---|---|---|
| [Heizplan Flex Plus](blueprints/automation/heizplan_flex_plus.yaml) (`v1.4-plus`) | Heizungssteuerung nach Zeitplan-Helfer: Komfort/ECO, Abwesenheit, Fenster, Verkalkungsschutz, nur in der Heizsaison. Ab v1.4 schaltet er Thermostate selbst auf `heat` (nötig für Homematic IP). | live, eine Automation je Raum |

## Automationen und Packages

| Thema | Package / Doku | Inhalt | Status |
|---|---|---|---|
| Heizung HmIP-Gruppen | [Package](packages/heizung_hmip_gruppen.yaml) · [Doku](docs/heizung_hmip_gruppen.md) | `automation.heizplan_schlafzimmer` und `automation.heizplan_buro` (Flex Plus) steuern die OpenCCU-Heizungsgruppen aus HmIP-WTH-2 + HmIP-eTRV-2. Der Wandthermostat regelt mit, Boost 10 min. | live seit 2026-10-15 |
| MG Vorklimatisierung | [Package](packages/mg_vorklimatisierung.yaml) · [Doku](docs/mg_vorklimatisierung.md) | `automation.auto_mg_vorklimatisierung_burotage` klimatisiert den MG MGS5 EV an Bürotagen vor, Stufe aus Wetter und Nachtwerten. Dazu Helper `input_number.mg_nacht_*`. | live seit 2026-10-07 |
| Capri Vorklimatisierung | [Package](packages/capri_vorklimatisierung.yaml) · [Doku](docs/capri_vorklimatisierung.md) | `automation.auto_capri_vorklimatisierung_diensttage` startet Elkes Ford Capri per FordPass an Diensttagen. Nutzt die MG-Nachtwerte. | live seit 2026-10-07 |
| Saugroboter Karl (Mova Z60) | [Package](packages/mova_reinigung.yaml) · [Doku](docs/mova_entitaeten.md) | `automation.haushalt_karl_reinigung_bei_abwesenheit` reinigt nach Kalender „Haushalt“, wenn alle weg sind, mit Ansage 5 min vorher über drei Echos und höchstens einmal pro Tag (auch App-Starts zählen). `script.haushalt_mova_reinigung_starten` als Override mit Modus und Raumauswahl, Schalter `input_boolean.karl_automatik`. Dashboard-Kacheln im Test Dashboard. | v2 live seit 2026-10-21 (v1-Automation deaktiviert) |
| LED Deko Zweig | [Package](packages/deko_zweig.yaml) · [Doku](docs/deko_zweig.md) | Zeitsteuerung per Broadlink-IR (An + Prog8), abhängig von Anwesenheit und Werktag. | vorbereitet, noch nicht eingespielt |
| Radio BOB! auf den Echos | [Package](packages/radio_bob.yaml) · [Doku](docs/radio_bob.md) | `script.radio_bob_abspielen` / `script.radio_bob_stopp` starten bzw. pausieren den per `input_select` gewählten Radio-BOB-Sender (TuneIn) auf Echo Wohnzimmer, Bad oder Büro, mit Lautstärke-Regler. Dashboard-Karte in der Doku. | live seit 2026-10-17 (UI-Speicher) |
| Zigbee2MQTT-Wächter | [Package](packages/zigbee2mqtt_waechter.yaml) · [Doku](docs/zigbee2mqtt_waechter.md) | `automation.system_zigbee2mqtt_wachter` prüft nach dem HA-Start, bei offline-Bridge und alle 30 min, ob Zigbee2MQTT läuft, startet das Add-on bis zu 3x mit Abstand neu und meldet Erfolg oder Fehlschlag aufs Pixel 9. | live seit 2026-10-17 |
| Auto-Stellplätze | [Package](packages/auto_stellplaetze.yaml) · [Doku](docs/auto_stellplaetze.md) | `binary_sensor.auto_capri_zuhause` und `binary_sensor.auto_mg_zuhause` sind an, wenn der Ford Capri bzw. der MG laut GPS-Tracker der Hersteller-Integration in `zone.home` steht; `binary_sensor.auto_capri_eingesteckt` zeigt, ob der Capri am Ladekabel hängt (FordPass). Für die Stellplätze in Neonplan3D, ohne Außensensoren. | live seit 2026-10-18 (UI-Helfer) |
| Bad Licht und Lüfter | [Package](packages/bad_licht_lufter.yaml) · [Doku](docs/bad_licht_lufter.md) | `automation.bad_licht_nach_prasenz` schaltet das Badlicht (HmIP-BS2 Kanal 4) nach dem Präsenzmelder HmIP-SPI, 1 min Nachlauf. `automation.bad_lufter_nach_prasenz_und_feuchte` lässt den Lüfter (Kanal 8) bei Anwesenheit laufen, 10 min nach, und regelt zusätzlich nach Luftfeuchte (HmIP-STHD, Schwellen per `input_number`). Doku mit Anleitung für die Direktverknüpfung in der OpenCCU und zum Ablernen von Geräten. | live seit 2026-10-20 (UI-Speicher) |
| Test Dashboard | [Umbau-Skript](dashboards/test_dashboard_umbau.py) · [Theme](themes/neonplan3d.yaml) · [Doku](docs/test_dashboard.md) | Menüleiste wie im „Dashboard“, Startseite NeonPlan 3D, Seiten Karl, Balkonkraftwerk, Wetter, Autos, Sicherheit in NeonPlan-Farben. Alte Raum-Ansichten als Unterseiten. | live seit 2026-10-21 (Theme-Datei noch einzuspielen) |

## Pflege

Jede Änderung im Repo trägt diese README mit nach: neue oder geänderte Blueprints, Automationen, Skripte und Helper mit kurzer Beschreibung und Status.
