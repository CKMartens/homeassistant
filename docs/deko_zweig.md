# Wohnbereich – LED Deko Zweig (Elke)

Stand 2026-10-21: Umbau auf Steckdose offline vorbereitet. Die IR-Version (Stand 2026-10-14) läuft seitdem in HA.
YAML: [`packages/deko_zweig.yaml`](../packages/deko_zweig.yaml)

Der Zweig blinkt nach dem Einschalten. Ein und aus geht über die Steckdose, danach kommt per IR `Prog8`, damit er ruhig leuchtet.

## Entitäten

| Zweck | entity_id |
|---|---|
| Steckdose (Ein/Aus, Zustand) | `switch.wohnbereich_steckdose_deko` |
| IR-Sender (Broadlink Mini) | `remote.ir_remote_wohnbereich`, Gerät `LED Deko Zweig`, Befehl `Prog8` (`An`/`Aus` angelernt, aber ungenutzt) |
| Einschalten / Ausschalten | `script.wohnbereich_deko_zweig_an`, `script.wohnbereich_deko_zweig_aus` |
| Automation | `automation.wohnbereich_deko_zweig_zeitsteuerung` |
| Werktag/Feiertag | `binary_sensor.workday_sensor` (Workday-Integration, DE) |
| Anwesenheit | `zone.home` (Carsten Pixel 9, Elke Pixel 9a) |

## Regeln

| Wann | Was | Bedingung |
|---|---|---|
| Steckdose geht an (Automation, App, Taster, nach Stromausfall) | nach 3 s IR `Prog8` | – |
| 05:00 | an | Werktag, jemand zuhause |
| 06:00 | an | Wochenende/Feiertag, jemand zuhause |
| jemand kommt heim (`zone.home` von 0 auf ≥ 1) | an | nach der Einschaltzeit des Tages, Steckdose aus |
| alle weg (`zone.home` < 1 seit 5 min) | aus | – |
| 00:00 | aus | – |

Fehlt `binary_sensor.workday_sensor`, gilt Mo–Fr als Werktag (Feiertage dann wie Werktage).

## Hinweise

- Der frühere Helper `input_boolean.wohnbereich_deko_zweig` entfällt; den Zustand liefert die Steckdose.
- Verschluckt der Zweig `Prog8`, weil er nach dem Einschalten noch nicht bereit ist, im Trigger `steckdose_an` das `for:` von 3 s erhöhen.
