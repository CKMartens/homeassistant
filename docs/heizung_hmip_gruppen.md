# Heizung: HmIP-Wandthermostat + HmIP-eTRV-2 als Heizungsgruppe

Stand 2026-10-15, live in Schlafzimmer und Büro.
YAML: [`packages/heizung_hmip_gruppen.yaml`](../packages/heizung_hmip_gruppen.yaml),
Blueprint: [`blueprints/automation/heizplan_flex_plus.yaml`](../blueprints/automation/heizplan_flex_plus.yaml) (ab v1.4-plus)

Dieses Muster ist die Vorlage für alle Räume, die auf Homematic-IP-Heizkörperthermostate umgestellt werden.

## Aufbau

| Ebene | Wer macht was |
|---|---|
| OpenCCU-Heizungsgruppe (WTH-2 + eTRV-2 + HmIP-Drehgriffkontakte) | Sollwert am Wandthermostat → Ventil, Boost, Fensterabsenkung, Regelung auf die Raumtemperatur des WTH-2, Entkalkung. Läuft funkdirekt, auch ohne HA. |
| HA: Heizplan Flex Plus | Zeitplan (Komfort/ECO), Abwesenheit, Heizsaison. Steuert **nur die Gruppen-Entität**, nie eTRV oder WTH einzeln. |

Eine Einstellung am Wandthermostat gilt bis zum nächsten Programmlauf von Flex Plus
(Zeitplanwechsel, Anwesenheitswechsel, Heizsaison an, HA-Neustart).

## Räume

| Raum | Gruppe (HA) | Geräte | Automation |
|---|---|---|---|
| Schlafzimmer | `climate.heizgruppe_schlafzimmer_int0000007` | HmIP-WTH-2, HmIP-eTRV-2, 2 Drehgriffkontakte | `automation.heizplan_schlafzimmer` |
| Büro | `climate.heizgruppe_buro_int0000006` | HmIP-WTH-2, HmIP-eTRV-2, 1 Drehgriffkontakt | `automation.heizplan_buro` |

## Einstellungen in der OpenCCU (je Gruppe)

| Parameter | Wert |
|---|---|
| Betriebsart | Manu (setzt Flex Plus ab v1.4 selbst) |
| Boost-Dauer | 10 min |
| Fensterkontakte | in der Gruppe (HmIP-Drehgriffkontakte) |
| Fenster-auf-Temperatur | 12 °C |
| Wochenprogramm | ungenutzt |

## Einstellungen in Flex Plus

- `climate_entity`: nur die Gruppen-Entität
- `window_activ: false` (Fenster macht die Gruppe)
- `descale_activ: false` (Entkalkung macht das eTRV-2)

## Checkliste für den nächsten Raum

1. Backup HA + OpenCCU.
2. eTRV-2 (und ggf. WTH-2) an der OpenCCU anlernen, Raum zuordnen.
3. Altes Gerät ablernen. **Danach HA einmal neu starten** (siehe Stolperfallen).
4. In HA nach Verweisen auf alte Entitäten suchen (Automationen, CCA, Fensterüberwachung, Dashboards) und ersetzen.
5. OpenCCU: Heizungsgruppe anlegen (Einstellungen siehe oben).
6. In HA erscheint die Gruppe als `climate.heizgruppe_<raum>_int000000x`.
7. Flex Plus des Raums auf die Gruppe umstellen, `window_activ`/`descale_activ` aus, Beschreibung anpassen.
8. Automation einmal ausführen, Trace prüfen: Gruppe auf `heat` (Manu) mit Planwert.
9. Praxistest: Drehrad, Boost, Fenster auf/zu.

## Stolperfallen

- **`hvac_mode` in `set_temperature` wird von Homematic(IP) Local ignoriert.** Die Gruppe blieb auf Auto mit Werks-Wochenprogramm. Behoben in Flex Plus v1.4-plus durch ein eigenes `climate.set_hvac_mode: heat` (nur für Thermostate, die nicht schon auf `heat` stehen).
- **Nach dem Ablernen eines Geräts hingen Entitäten fest.** Am 14.10. gegen 20:10 (Ablernen des alten HM-TC-IT-WM-W-EU) meldete HA `Platform homematicip_local does not generate unique IDs … already exists`. Danach waren Gruppe, eTRV, Badsensor und mehrere Sensoren eingefroren bzw. `unavailable`. Ein Reload der Integration half nicht, erst ein **HA-Neustart**.
- **BidCos und HmIP lassen sich nicht verknüpfen.** Der alte Funk-Wandthermostat (HM-TC-IT-WM-W-EU) kann kein HmIP-eTRV-2 steuern, deshalb wurde er durch einen HmIP-WTH-2 ersetzt.

## Geplant

- Bad: eTRV-2 + neuer WTH-2.
- Küche + Ess-/Wohnbereich (ein Raum mit Raumteiler): eine Gruppe mit 2× eTRV-2 und **einem** WTH-2 am Raumteiler, ein Flex Plus für den ganzen Raum, HmIP-STHD in der Küche nur als Kontrollfühler.
