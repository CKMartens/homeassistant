# Wohnbereich – LED Deko Zweig (Elke)

Stand 2026-10-14, offline vorbereitet, noch nicht in HA eingespielt.
YAML: [`packages/deko_zweig.yaml`](../packages/deko_zweig.yaml)

Der Zweig ist nur per IR steuerbar und blinkt nach dem Einschalten. Darum sendet „An“ immer zwei Befehle: `An`, 3 s Pause, `Prog8`.

## Entitäten

| Zweck | entity_id |
|---|---|
| IR-Sender (Broadlink Mini) | `remote.ir_remote_wohnbereich`, Gerät `LED Deko Zweig`, Befehle `An`, `Aus`, `Prog8` |
| Zustand (gemerkt, IR hat keine Rückmeldung) | `input_boolean.wohnbereich_deko_zweig` |
| Einschalten / Ausschalten | `script.wohnbereich_deko_zweig_an`, `script.wohnbereich_deko_zweig_aus` |
| Automation | `automation.wohnbereich_deko_zweig_zeitsteuerung` |
| Werktag/Feiertag | `binary_sensor.workday_sensor` (Workday-Integration, DE) |
| Anwesenheit | `zone.home` (Carsten Pixel 9, Elke Pixel 9a) |

## Regeln

| Wann | Was | Bedingung |
|---|---|---|
| 05:00 | an | Werktag, jemand zuhause |
| 06:00 | an | Wochenende/Feiertag, jemand zuhause |
| jemand kommt heim (`zone.home` von 0 auf ≥ 1) | an | nach der Einschaltzeit des Tages, Zweig laut Helper aus |
| alle weg (`zone.home` < 1 seit 5 min) | aus | – |
| 00:00 | aus | – |

Fehlt `binary_sensor.workday_sensor`, gilt Mo–Fr als Werktag (Feiertage dann wie Werktage).

## Hinweise

- Wird der Zweig mit der Original-Fernbedienung geschaltet, stimmt der Helper nicht mehr. Aus-Befehle gehen deshalb immer raus; beim Heimkommen wird nur eingeschaltet, wenn der Helper „aus“ sagt.
- Die 3 s Pause zwischen `An` und `Prog8` im Skript anpassen, falls der Zweig `Prog8` verschluckt.
