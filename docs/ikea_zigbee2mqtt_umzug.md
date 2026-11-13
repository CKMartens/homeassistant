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
| Schreibtischlampe Büro | `light.198837aa_ebdb_4b08_9c60_97a882d688e0_1` (Gerät „Schreibtischlampe“, Dirigera meldete innr RB 278 T) | `light.buro_schreibtisch_1` (Gerät „Büro Schreibtisch 1“, Z2M meldet IKEA TRADFRI E27 opal 1000 lm) | `automation.taster_schreibtischlampe_carsten` (IKEA-Taster an/aus), Gruppe Alarm, Test Dashboard (Ansicht Büro) | 2026-11-13 |
| Deckenlicht Flur | `light.d275ff70_a0f2_4e61_81b6_58d8fc6a3107_1` (Gerät „Flur “) | `light.flur_deckenlicht` (Gerät „Flur Deckenlicht“, IKEA TRADFRI E27 opal 1000 lm) | `automation.licht_flur`, `automation.tester_flur`, `automation.flur_licht_manuell_zurucksetzen`, `automation.flur_homematic_ip_6fach_taster` (Taste 4), `automation.nachtmodus_aktivieren`, Gruppe Alarm, Test Dashboard (Raumkarte Flur, Ansicht Flur) | 2026-11-13 |
| Eingang-Spot (HA „Eingang Bulb 2“, Dirigera intern „Eingang Bulb 1“) | `light.384aaa0c_beec_48fc_aefa_44a15752e2a4_1` (Gerät „Eingang Bulb 2“, innr RS 240 GU10) | `light.flur_bulb_1` (Gerät „Flur Bulb 1“, Innr Smart spot white GU10) | Szenen `scene.licht_eingang` / `scene.licht_eingang_aus`, Gruppe „Licht Eingang“ (`light.licht_eingang`, damit auch 6fach-Taster Taste 3), Gruppe Alarm | 2026-11-13 |

Nebenbei korrigiert: In der Flur-Raumkarte im Test Dashboard stand unter `lights` die Abstellraum-Lampe, jetzt das Flurlicht.

Hinweis: Die Hersteller-Angaben von Dirigera und Z2M passen bei Abstellraum und Büro über Kreuz (IKEA ↔ Innr). Maßgeblich ist, wo die Lampe physisch sitzt und wie sie in Z2M benannt wurde.

Zuordnung über Hersteller/Modell/Firmware geprüft: Die Namen in HA und Dirigera waren bei den beiden Eingang-Lampen vertauscht.

Offen (noch über Dirigera, laufen): Eingang Bulb 1 (`light.f364e4a2_…_1`, Müller Licht), Schreibtischlampe 2 (`light.dd9558df_…_1`, noch über Dirigera) und weitere.
