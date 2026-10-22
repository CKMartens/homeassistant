# Mova – Entitäten-Referenz (per ha-mcp ausgelesen, 2026-10-07)

Gerät in HA: **MOVA Z60 Ultra Roller** (mova.vacuum.r9544a), Integration **dreame_vacuum** (HACS), 228 Entitäten.

| Zweck | entity_id | Werte |
|---|---|---|
| Sauger | `vacuum.z60_ultra_roller_standalone` | docked, … |
| Reinigungsart | `select.z60_ultra_roller_standalone_cleaning_mode` | sweeping, mopping, sweeping_and_mopping, mopping_after_sweeping |
| Saugstärke | `select.z60_ultra_roller_standalone_suction_level` | quiet, standard, strong, turbo |
| Route | `select.z60_ultra_roller_standalone_cleaning_route` | quick, standard, intensive, deep |
| Feuchte | `number.z60_ultra_roller_standalone_wetness_level` | 1–32 (nur im Wischmodus verfügbar, App-Wert 16) |
| Individuelle Reinigung | `switch.z60_ultra_roller_standalone_customized_cleaning` | muss für globale Werte **off** sein |
| Kalender | `calendar.haushalt` | |
| Anwesenheit | `zone.home` | person.carsten_martens (Pixel 9), person.elke_martens (Pixel 9a) |

Räume (Segment-IDs für `dreame_vacuum.vacuum_clean_segment`):
1 Wohnzimmer · 2 Bad · 4 Esszimmer · 5 Flur · 6 Schlafzimmer · 7 Arbeitszimmer · 8 Küche

Nützliche Services: `dreame_vacuum.vacuum_clean_segment` (segments, repeats 1–3, suction_level 0–3, water_volume 1–3), `dreame_vacuum.vacuum_set_custom_cleaning`, `vacuum.start`.

## Karl v2 (seit 2026-10-21)

Der Robi heißt bei uns **Karl**.

**Automatik:** `automation.haushalt_karl_reinigung_bei_abwesenheit` startet Mo–Fr 07–17 Uhr, wenn `zone.home` 10 min auf 0 steht, `input_boolean.karl_automatik` an ist und heute noch nicht gereinigt wurde (Automatik, Dashboard oder Mova-App über `sensor.z60_ultra_roller_standalone_cleaning_history`). Modus aus dem Kalender „Haushalt“. Vorher Ansage per `notify.alexa_media` (type announce) auf `media_player.echo_wohnzimmer`, `echo_schlafzimmer`, `echo_dot_buro`, Echos mit „Bitte nicht stören“ werden ausgelassen: „Entschuldigung, dass ich störe. Das Saugen / Das Saugen und Wischen / Die Intensivreinigung startet in fünf Minuten.“ Kommt in den 5 Minuten jemand heim, bleibt Karl stehen.

**Reinigungsart:** „Saugen“ = `sweeping`; „Saugen & Wischen“ und „Intensiv“ = `mopping_after_sweeping` (erst saugen, dann wischen, wie „Wischen nach dem Saugen“ in der Mova-App; seit 2026-10-22, vorher gleichzeitig).

**Override:** `script.haushalt_mova_reinigung_starten` mit Feldern `modus` (saugen, saugen_wischen, intensiv) und `raeume` (Segment-IDs, leer = überall; Einzelräume über `dreame_vacuum.vacuum_clean_segment`). Jeder Start setzt `input_datetime.mova_letzte_auto_reinigung` auf heute.

**Dashboard** (Test Dashboard, Ansicht `robi`):

```yaml
- type: tile
  entity: script.haushalt_mova_reinigung_starten
  name: Karl starten
  tap_action:
    action: more-info      # Dialog mit Modus und Räumen
- type: tile
  entity: input_boolean.karl_automatik
- type: tile
  entity: vacuum.z60_ultra_roller_standalone
  name: Karl
  features:
    - type: vacuum-commands
      commands: [start_pause, stop, return_home]
```

Stolperfallen: Jinja-Filter `dict2items` gibt es in HA nicht (namespace-Schleife verwenden). Losschicken des Saugers per ha-mcp blockiert auf Argos die Rechteprüfung, Tests startet Carsten über die Kachel.
