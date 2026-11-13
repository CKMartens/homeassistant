# IKEA-Lampen: Umzug von Dirigera nach Zigbee2MQTT

Nach den Stromausfällen am 2026-11-12 sind mehrere IKEA-Bulbs in der IKEA-App bzw. am Dirigera-Hub offline. Sie werden direkt in Zigbee2MQTT neu angelernt. In HA bekommt jede Lampe dadurch ein neues Gerät mit neuer Entität, die alte Dirigera-Entität (`light.<uuid>_1`) wird überall ersetzt und danach entfernt.

## Vorgehen je Lampe

1. Lampe in Z2M anlernen und benennen (`<Raum> Deckenlicht` o. ä.), HA legt `light.<name>` per MQTT-Discovery an. Permit join danach wieder aus.
2. Verwendungen der alten Entität suchen: Automationen, Skripte, Szenen, Helper (v. a. die Licht-Gruppe **Alarm**, die alle Lampen enthält) und Dashboards (Test Dashboard, Raumkarten `custom:room-summary-card` mit `lights` und `entities`).
3. Überall auf die neue Entität umstellen. Die neue Entity-ID behalten (lesbar), nicht auf die alte UUID-ID umbenennen.
4. Neues Gerät in den Bereich legen und Label `beleuchtung` setzen.
5. Prüfen, dass keine Verweise mehr auf die alte Entität bestehen, dann das alte Dirigera-Gerät in HA entfernen. In der IKEA-App ebenfalls löschen, sonst legt Dirigera es wieder an.

Stolperfalle: Die Gruppe **Alarm** ist ein UI-Helfer (Config Entry). Ein Umbenennen der Entität aktualisiert ihre Mitgliederliste nicht, sie muss über die Optionen der Gruppe gepflegt werden.

## Stand

| Lampe | Alt (Dirigera) | Neu (Z2M) | Ersetzt in | Datum |
|---|---|---|---|---|
| Deckenlicht Abstellraum | `light.88009a12_3aa6_4957_a9bb_6152a34dae6d_1` (Gerät „Abstellraum_Deckenlampe“) | `light.abstellraum_deckenlicht` (Gerät „Abstellraum Deckenlicht“, Z2M meldet Innr Smart bulb tunable white E27) | `automation.licht_abstellraum`, Gruppe Alarm, Test Dashboard (Raumkarte Abstellraum) | 2026-11-13 |

Nebenbei korrigiert: In der Flur-Raumkarte im Test Dashboard stand unter `lights` die Abstellraum-Lampe, jetzt das Flurlicht `light.d275ff70_a0f2_4e61_81b6_58d8fc6a3107_1` (wird beim Flur-Umzug ersetzt).

Offen: Flur, Eingang Bulb 1 und weitere.
