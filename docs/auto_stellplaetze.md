# Auto-Stellplätze (Neonplan3D)

Live seit 2026-10-18 als UI-Template-Helfer (Einstellungen → Helfer, „Auto Capri zuhause“ / „Auto MG zuhause“ / „Auto Capri eingesteckt“). Die Binärsensoren zeigen, ob Elkes Ford Capri bzw. der MG MGS5 EV zu Hause steht und ob der Capri am Kabel hängt. Gedacht für die Stellplätze im Neonplan3D-Grundriss, ohne Sensoren an der Außenwand.

| Entität | an (`on`) wenn | Quellen |
|---|---|---|
| `binary_sensor.auto_capri_zuhause` | einer der Tracker `home` meldet | `device_tracker.fordpass_wf0spbef1tsd01110_tracker` (FordPass), `device_tracker.ford_capri_2025_extended_range_rwd_standort` (ABRP) |
| `binary_sensor.auto_capri_eingesteckt` | `sensor.fordpass_wf0spbef1tsd01110_elvehplug` = `CONNECTED` (sonst `DISCONNECTED`), Device-Class `plug` | FordPass |
| `binary_sensor.auto_mg_zuhause` | einer der Tracker `home` meldet | `device_tracker.mg_mgs5_ev_gps_location` (MG/iSMART), `device_tracker.mg_s5_2025_2025_standard_range_standort` (ABRP) |

## Logik

- `home` heißt: GPS-Position liegt in `zone.home` (CasaMartens, Radius 200 m). Das deckt die Laternenparkplätze in der Straße ab.
- Zwei Quellen je Auto: fällt die Hersteller-Cloud aus, reicht ABRP und umgekehrt.
- Sind beide Tracker `unavailable` oder `unknown`, ist der Sensor `unavailable`, damit Neonplan3D kein leeres Stellplatz-Bild zeigt, nur weil die Cloud hängt.
- Device-Class `presence`: in der UI „Zuhause“ / „Abwesend“.

## Stolperfallen

- Die Auto-Tracker aktualisieren nur, wenn die Cloud neue Daten liefert (meist bei Zündung aus/an). Nach dem Heimkommen kann es ein paar Minuten dauern.
- Wird der Radius von `zone.home` kleiner gestellt, kann ein Auto, das weiter weg in der Straße parkt, als „Abwesend“ gelten.
- Neonplan3D: Stellplatz-Element an `binary_sensor.auto_*_zuhause` binden, Zustand `on` = Auto sichtbar.
