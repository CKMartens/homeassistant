# System – Zigbee2MQTT-Wächter

Stand 2026-10-17, vorbereitet, noch nicht in HA eingespielt.
YAML: [`packages/zigbee2mqtt_waechter.yaml`](../packages/zigbee2mqtt_waechter.yaml)

## Problem

Nach einem HA-/Host-Neustart läuft Zigbee2MQTT manchmal nicht. Auffällig wird das erst, wenn Zigbee-Lichter (z. B. Deckenfluter) oder der Bewegungsmelder im Abstellraum nicht reagieren.

Befund vom 2026-10-17 (Supervisor-Log): um 13:44 ist das Add-on fünfmal innerhalb von rund 20 Sekunden mit Exit-Code 1 beendet worden. Der Watchdog hat jedes Mal sofort neu gestartet und danach aufgegeben, ab dann war `binary_sensor.zigbee2mqtt_bridge_connection_state` bis zum manuellen Start um 17:25 `off`. Der Watchdog hilft also nur bei einzelnen Abstürzen, nicht wenn Z2M beim Hochfahren mehrfach schnell hintereinander scheitert. Vermutete Ursache (nicht belegt, das Add-on-Log davon ist weg): Der Netzwerk-Koordinator `tcp://10.10.0.39:6638` oder das Netz war in dem Moment noch nicht erreichbar; um 15:26 gab es zusätzlich DNS-Fehler im Supervisor.

## Lösung

Eine Automation prüft die Bridge und startet das Add-on mit Abstand neu, statt sofort hintereinander wie der Watchdog.

| Zweck | Wert |
|---|---|
| Automation | `automation.system_zigbee2mqtt_wachter` (id `system_zigbee2mqtt_waechter`) |
| Bridge-Status | `binary_sensor.zigbee2mqtt_bridge_connection_state` (`on` = online) |
| Add-on | `45df7312_zigbee2mqtt`, Neustart per `hassio.app_restart` |
| Meldung | `notify.mobile_app_pixel_9` (Carsten), bei Fehlschlag zusätzlich HA-Benachrichtigung `zigbee2mqtt_waechter` |

## Ablauf

| Auslöser | Was passiert |
|---|---|
| HA-Start | 3 min warten, dann prüfen |
| Bridge seit 3 min `off` / `unavailable` / `unknown` | prüfen |
| alle 30 min | prüfen (Sicherheitsnetz, falls ein Durchlauf erfolglos war) |

Prüfen heißt: Ist die Bridge `on`, passiert nichts. Sonst bis zu 3 Neustarts, nach jedem bis zu 3 min auf „online“ warten, dazwischen 2 min Pause. Klappt es, kommt eine kurze Info aufs Pixel 9. Klappt es nicht, kommt eine Warnung mit hoher Priorität und eine Benachrichtigung in HA; die wird beim nächsten Erfolg automatisch entfernt.

`mode: single`: Läuft gerade ein Durchlauf, werden weitere Auslöser still verworfen.

## Stolperfallen

- Ist der Koordinator (10.10.0.39) selbst weg, helfen Neustarts nicht. Dann meldet die Automation alle 30 min, bis er wieder da ist.
- Fällt Mosquitto aus, wird der Bridge-Sensor `unavailable`, und die Automation startet Z2M neu, obwohl der Broker das Problem ist. Das schadet nicht, löst es aber auch nicht.
- Beim gewollten Stoppen von Z2M (Wartung) die Automation vorher ausschalten, sonst startet sie das Add-on nach 3 min wieder.
