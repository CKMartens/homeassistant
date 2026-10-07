# MG MGS5 EV – Vorklimatisierung an Bürotagen

Stand 2026-10-07, live in HA als `automation.auto_mg_vorklimatisierung_burotage`.
YAML: [`packages/mg_vorklimatisierung.yaml`](../packages/mg_vorklimatisierung.yaml)

Ziel: An Bürotagen vor allem in der kalten Jahreszeit Freikratzen und beschlagene Scheiben vermeiden.

## Rahmenbedingungen

- Bürotage: Termin „Büro“ in `calendar.dienst_carsten`
- Abfahrt = Bürobeginn − 45 min; ein MG-Klimazyklus läuft 10 min
- Laternenparker: unter freiem Himmel, ca. 2 m neben einer Hauswand, nachts **nicht** am Strom → SoC-Sperre < 20 %

## Entitäten

| Zweck | entity_id |
|---|---|
| Klima (Gesamt) | `climate.mg_mgs5_ev_climate` (Presets u. a. `front_windscreen`, bisher ungenutzt) |
| Klima ein/aus | `switch.mg_mgs5_ev_air_conditioning` |
| Modus | `select.mg_mgs5_ev_climate_mode` (Off, Cool, Fan only, Heat/cool, Heat) |
| Zieltemperatur | `number.mg_mgs5_ev_climate_target_temperature` (16–30 °C) |
| Heckscheibe | `switch.mg_mgs5_ev_rear_window_defrost` |
| Lenkradheizung | `switch.mg_mgs5_ev_heated_steering_wheel` |
| Akku | `sensor.mg_mgs5_ev_state_of_charge` |
| Wetter aktuell | `sensor.ws2350_v2_38_outdoor_temperature`, `_dewpoint`, `_humidity` |
| Vorhersage | `weather.forecast_home` (met.no, hourly + daily, Wind in km/h) |
| Nachtwerte | `input_number.mg_nacht_bewolkung`, `_niederschlag`, `_wind` |
| Push | `notify.mobile_app_pixel_9` |

## Stufen

Die Frostschwelle liegt bei +3 °C statt 0 °C: Bei klarem Himmel strahlt die Scheibe nachts ab und wird 2–5 K kälter als die Luft, außerdem misst die Station höher als das Auto steht.

| Stufe | Bedingung | Zyklen | Start | Zieltemperatur |
|---|---|---|---|---|
| 3 – Vereisung | T ≤ −3 °C, **oder** T ≤ 1 °C und Nachtniederschlag ≥ 0,2 mm | 2 | Abfahrt − 20 min | Maximum (30 °C) |
| 2 – Frost | T ≤ 0 °C, **oder** T ≤ 3 °C bei Bewölkung < 50 % und Wind < 11 km/h | 1 | Abfahrt − 10 min | Maximum (30 °C) |
| 1 – Beschlag | T ≤ 10 °C und (Taupunktabstand ≤ 3 K **oder** RH ≥ 85 % **oder** Nachtniederschlag ≥ 0,2 mm) | 1 | Abfahrt − 10 min | 22 °C |
| 0 | sonst | – | – | – |

Je Zyklus: Heat/cool (entfeuchtet gegen Innenbeschlag), Heckscheibenheizung an, Lenkradheizung ab T ≤ 5 °C.
Startet die Klima nicht innerhalb von 3 min, gibt es genau einen Retry, danach einen Push.

## Offen

- Beim ersten echten Lauf im Trace prüfen: Übernimmt der MG Modus und Temperatur, solange die Klima noch aus ist? Geht der AC-Switch nach 10 min auf `off`?
- Preset `front_windscreen` für Stufe 2/3 testen und ggf. einbauen.
- Regen vor 22:00 sieht der Snapshot nicht; das fängt meist der Taupunktabstand am Morgen ab.
