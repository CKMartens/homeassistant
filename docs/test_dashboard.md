# Test Dashboard (`test-dashboard`)

Umbau am 2026-10-21: Menüleiste wie im „Dashboard“ (DBuit sidebar-card + kiosk-mode), Startseite mit NeonPlan 3D, Farben aus der NeonPlan-3D-Karte.

## Seiten (Menüleiste)

| Seite | Pfad | Inhalt |
|---|---|---|
| Home | `/test-dashboard/home` | NeonPlan-3D-Karte (Höhe 720), Badges Carsten/Elke |
| Karl | `/test-dashboard/karl` | Saugroboter Karl (Mova Z60): nur die Dreame-Karte (volle Breite), dazu Start-Skript und Automatik-Schalter. Die Mova-Kacheln (Wasser, Fehler, Steuerung) sind entfernt, weil die Karte sie schon enthält |
| Balkonkraftwerk | `/test-dashboard/bkw` | Solakon ONE: Leistung, Akku, Prognose, Verläufe (mini-graph-card), Nulleinspeisung und Speicher |
| Wetter | `/test-dashboard/wetter` | WS2350 groß, DWD-Vorhersage Itzgrund-Herreth (täglich/stündlich), NINA/Wetter/Pollen, Windrose (Ausgabe `kph`, `kmh` erzeugt einen Konfigurationsfehler), Windy-Regenradar (Untersiemau) |
| Autos | `/test-dashboard/autos` | Zuhause/Ladekabel (`binary_sensor.auto_*`), Vehicle Status Cards MG und Capri, Fahrtenbuch Capri |
| Sicherheit | `/test-dashboard/sicherheit` | Fenster/Türen/Kellertür/Hausalarm, Alarmo Haus und Keller, Kameras Terrasse und Flur |
| Räume (alt) | `/test-dashboard/uebersicht` | bisherige Übersicht; Raum-, Aquarium-, Garten-Ansichten sind jetzt Unterseiten (`subview`). **Nur im Test Dashboard, beim Livestellen raus.** |

Die alten Ansichten `neonplan3d`, `robi`, `bkw`, `auto`, `cameras` sind in den neuen Seiten aufgegangen. Navigationslinks in den alten Ansichten zeigen auf die neuen Pfade.

## Farben (NeonPlan 3D)

| Rolle | Wert |
|---|---|
| Hintergrund | `#070b14` |
| Karte/Panel | `#0d1628` (Verlauf `#16223a`) |
| Akzent | `#37e0ff` |
| Text / gedämpft | `#e6eefc` / `#a9b8d4` |
| Linie | `rgba(120,190,255,0.22)` |
| ok / Warnung / Alarm / warm | `#4dff80` / `#ffcc40` / `#ff4d40` / `#ffb547` |

- button-card-Vorlagen `neon_tile` und `neon_weather` im Dashboard.
- Standardkarten bekommen die Farben per `card_mod` (läuft über UIX).
- Alle Ansichten setzen `theme: Neonplan3D`. Das Theme liegt in [themes/neonplan3d.yaml](../themes/neonplan3d.yaml) und ist seit 2026-10-21 unter `/config/themes/` eingespielt (geladen mit `frontend.reload_themes`).

## Umsetzung und Rückweg

- Änderung per ha-mcp `python_transform`: [dashboards/test_dashboard_umbau.py](../dashboards/test_dashboard_umbau.py).
- Stand vorher gesichert als ha-mcp-Backup `dashboard.test-dashboard.20261021_071525.yaml` (Rückweg: `ha_manage_backup` scope `edits`, action `restore`).
- Beim Livestellen: Menüpunkt und Ansicht „Räume (alt)“ weglassen.
- Später geplant: Daten, Aquarium, Grill & Räuchern als weitere Menüpunkte.
