# homeassistant

Konfiguration und Doku für Home Assistant „Casa Martens“: Blueprints, Automationen, Skripte und Helper, die in HA eingespielt sind (oder dafür vorbereitet wurden), als Backup und zur Versionierung.

- `blueprints/automation/`: eigene Blueprints
- `packages/`: YAML je Thema, nutzbar als HA-Package oder zum Kopieren in die UI (Hinweise im Kopfkommentar jeder Datei)
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
| Mova Saugroboter | [Package](packages/mova_reinigung.yaml) · [Entitäten](docs/mova_entitaeten.md) | `automation.haushalt_mova_reinigung_bei_abwesenheit` + `script.haushalt_mova_reinigung_starten`: reinigt nach Kalender „Haushalt“, wenn alle weg sind, höchstens einmal pro Tag. | live seit 2026-10-07 |
| LED Deko Zweig | [Package](packages/deko_zweig.yaml) · [Doku](docs/deko_zweig.md) | Zeitsteuerung per Broadlink-IR (An + Prog8), abhängig von Anwesenheit und Werktag. | vorbereitet, noch nicht eingespielt |
| Radio BOB! auf den Echos | [Package](packages/radio_bob.yaml) · [Doku](docs/radio_bob.md) | `script.radio_bob_abspielen` / `script.radio_bob_stopp` starten bzw. pausieren den per `input_select` gewählten Radio-BOB-Sender (TuneIn) auf Echo Wohnzimmer, Bad oder Büro, mit Lautstärke-Regler. Dashboard-Karte in der Doku. | vorbereitet, noch nicht eingespielt |

## Pflege

Jede Änderung im Repo trägt diese README mit nach: neue oder geänderte Blueprints, Automationen, Skripte und Helper mit kurzer Beschreibung und Status.
