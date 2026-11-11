# Jalousien – Cover Control Automation (CCA)

Alle RolloTron-Jalousien (Rademacher Homepilot) laufen über den Blueprint
[Cover Control Automation](https://github.com/hvorragend/ha-blueprints) von hvorragend
(`hvorragend/cover_control_automation.yaml`), eine UI-Automation je Jalousie.
Geändert werden nur die Blueprint-Eingaben, nie der Blueprint selbst.

| Automation | Jalousie | Schließen |
|---|---|---|
| `automation.jalousie_terassentur` | `cover.rollotron_terassentur` | 22:00 ([YAML](../packages/jalousie_terassentur.yaml)) |
| `automation.jalousie_essbereich` | `cover.rollotron_wohnzimmer` | 22:00, auf 20 % |
| `automation.jalousie_kuchenfenster` | `cover.rollotron_kuche` | 22:00 |
| `automation.jalousie_burofenster` | `cover.rollotron_buro` | 21:00 |
| `automation.jalousie_schlafzimmer_strassenseite` | `cover.rollotron_schlafzimmer_doppelfenster` | Helligkeit, 17:00–21:30 |
| `automation.jalousie_schlafzimmer_gartenseite` | `cover.rollotron_schlafzimmer_fenster` | Helligkeit, 17:00–21:00 |

Der Zustand jeder Instanz steht als JSON im Helfer `input_text.helfer_jalousie_*`
(`man: 1` = manuelle Übersteuerung aktiv, `ts.man` = Zeitpunkt der Handfahrt).

## Stolperfalle: manuelle Übersteuerung ohne Reset

Fährt jemand die Jalousie per Taster oder Homepilot-App, merkt CCA sich das als
„manuell“. Was danach ignoriert wird, steht in `ignore_after_manual_config`. Wie die
Übersteuerung wieder aufgehoben wird, steht in `reset_override_config`. Der Standard dort
ist **leer, also kein Reset**: Die Sperre bleibt dann für immer stehen.

Vorfall 2026-11-08 bis 2026-11-10: Die Terrassentür-Jalousie wurde am Sonntag, 08.11.,
um 13:16 und 14:41 von Hand bewegt. Danach lief die CCA jeden Abend um 22:00, meldete
im Trace aber `no movement [manual override]`. Grund: Nur diese Instanz hatte
`ignore_closing_after_manual` gesetzt, und es gab keinen Reset.

Fix 2026-11-11:
- `ignore_closing_after_manual` entfernt: Abends wird auch nach einer Handfahrt geschlossen.
- `reset_override_config: [reset_fixed_time]`, `reset_override_time: "00:01:00"`: Die
  Übersteuerung wird jede Nacht aufgehoben, Öffnen am Morgen läuft wieder normal.

Die anderen fünf Instanzen ignorieren nach einer Handfahrt nur Öffnen, Lüften und
Beschatten und schließen abends trotzdem. Laut Blueprint setzt eine Fahrt, die nicht
ignoriert wird (hier das Schließen), die Übersteuerung ebenfalls zurück. Einen
Zeit-Reset haben sie nicht. Bleibt dort eine Jalousie morgens nach einer Handfahrt
trotzdem zu, ebenfalls `reset_fixed_time` 00:01 setzen.

## Diagnose

1. Trace der Automation zum Zeitpunkt der erwarteten Fahrt öffnen.
2. In den Variablen `base_gates.closing.override_ok` (bzw. `opening`) prüfen.
   `false` heißt: manuelle Übersteuerung blockiert.
3. Im Helfer `input_text.helfer_jalousie_*` steht `man` und `ts.man`.
