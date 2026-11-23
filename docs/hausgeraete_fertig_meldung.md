# Hausgeräte – Fertig-Meldung (Waschmaschine, Trockner)

Waschmaschine und Trockner hängen an Tasmota-Steckdosen (`sensor.waschmaschine_energy_power`,
`sensor.trockner_energy_power`). Die Meldung „fertig“ kommt aus dem Blueprint
[Appliance Notifications](https://github.com/Blackshome/appliance-notifications) von Blackshome
(`Blackshome/appliance-notifications.yaml`), eine UI-Automation je Gerät.

| Automation | Aufgabe |
|---|---|
| `automation.waschmaschine_notification` | Blueprint: Start/Ende erkennen (Ende unter 15 W), Push an Pixel 9 + Pixel 9a, Ansage Echo Wohnzimmer, Status `input_select.waschmaschine_status`, `input_boolean.hausgerate_waschmaschine_fertig` |
| `automation.waschetrockner_notification` | dasselbe für den Trockner (`input_select.trockner_status`, `input_boolean.hausgerate_waschetrockner_fertig`) |
| `automation.hausgerate_nachlaufzeit_abschaltung` | schaltet die Steckdose 15 min nach „fertig“ ab, wenn kein neuer Gang startet |
| `automation.waschmaschine_fertig_meldung_absichern` | neu 2026-11-23, siehe unten ([YAML](../packages/hausgeraete_fertig_meldung.yaml)) |
| `automation.trockner_fertig_meldung_absichern` | neu 2026-11-23, siehe unten |

Push-Meldungen und die Ansage gibt es nur zwischen 08:00 und 19:00 (Blueprint-Eingabe
`include_time`). Endet ein Gang früher, setzt der Blueprint nur den Status zurück.

## Stolperfalle 1: Handy-Geräte-ID nach Neuanmeldung der Companion App

Der Blueprint wählt die Handys per Geräte-ID (`end_notify_device`). Hat sich die Companion
App neu angemeldet (so geschehen beim HTTPS-Umzug am 2026-11-22), zeigt die alte ID ins Leere
und die Meldung an dieses Handy fällt still weg. Betroffen waren Waschmaschine, Trockner und
`automation.batteriestand_erkennung_benachrichtigung` (alte ID `164267a7…`).
Seit 2026-11-23 steht dort das aktuelle Pixel 9 (`bc5a022328b480fe2af27b3b55758509`).

Prüfen: In der Automation „In YAML bearbeiten“, jede ID unter `end_notify_device` muss in
**Einstellungen → Geräte** als Handy auftauchen.

## Stolperfalle 2: HA-Neustart mitten im Gang

Der Blueprint hält vom Start bis zum Ende einen laufenden Durchgang (`mode: single`).
Ein HA-Neustart oder das Speichern der Automation beendet ihn. Ein neuer Durchgang startet erst,
wenn die Leistung wieder über die Schwelle steigt. Endet der Gang während oder kurz nach dem
Neustart, gibt es keine Meldung und der Status bleibt auf „läuft“.

Vorfall 2026-11-23 (Zeiten MEZ):

| Zeit | Was passiert |
|---|---|
| 06:03 | 1. Waschgang startet |
| 06:25 | HA-Neustart, Durchgang weg, startet beim nächsten Leistungsanstieg neu |
| 07:05 | Ende erkannt, aber vor 08:00: keine Push-Meldung (gewollt) |
| 07:13 | 2. Waschgang startet |
| 08:00–08:05 | HA-Neustart für das alexa_media-Update 5.22.1. Der Gang endet genau dann (ab ca. 08:05 unter 15 W). Keine Meldung, Status bleibt „läuft“. |
| 08:30 | Leistung steigt wieder, der Blueprint startet einen neuen Durchgang |

Abhilfe: die zwei Automationen „… – Fertig-Meldung absichern“. Sie laufen nach dem HA-Start
und alle 5 min, greifen aber nur, wenn

- das Gerät noch als laufend markiert ist (`input_boolean.hausgerate_*_fertig` = on),
- der Blueprint gerade keinen Durchgang hat (Attribut `current` = 0) und
- die Leistung unter 15 W liegt.

Steigt sie in den nächsten 10 min nicht wieder über 15 W, melden sie wie der Blueprint
(Pixel 9, Pixel 9a, Echo Wohnzimmer, nur 08:00–19:00) und setzen Status, Laufzeit und das
`input_boolean` zurück. Läuft der Blueprint normal, greifen sie nie.

Diagnose: Trace von `automation.waschmaschine_notification`. `failed_single` heißt „lief schon“,
ein Trace mit `finish: null` ist der aktuell wartende Durchgang. Nach einem Neustart fehlt der
Trace des abgebrochenen Durchgangs.
