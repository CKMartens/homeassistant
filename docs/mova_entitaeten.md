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
