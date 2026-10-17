# Radio BOB! auf den Echos

Sender und Echo im Dashboard auswählen, auf „Abspielen“ tippen, fertig. Package: [packages/radio_bob.yaml](../packages/radio_bob.yaml).

## Bausteine

| Entität | Zweck |
|---|---|
| `input_select.radio_bob_sender` | die 10 Radio-BOB-Sender, exakt mit TuneIn-Namen |
| `input_select.radio_bob_echo` | Wohnzimmer, Bad, Büro |
| `input_number.radio_bob_lautstaerke` | 0.1–1.0, wird vor dem Start gesetzt |
| `script.radio_bob_abspielen` | setzt Lautstärke und startet den Sender (TuneIn) |
| `script.radio_bob_stopp` | pausiert den gewählten Echo |

Die Zuordnung Anzeigename → Echo steht in beiden Skripten unter `variables: echos:` (live geprüft am 2026-10-17):

- Wohnzimmer → `media_player.echo_wohnzimmer`
- Bad → `media_player.echo_dot_bad`
- Büro → `media_player.echo_dot_buro`

Eingespielt am 2026-10-17 über ha-mcp in den UI-Speicher (Helper und Skripte, ohne Neustart). Das Package deshalb nicht zusätzlich nach `/config/packages/` legen, sonst gibt es doppelte IDs.

Getestet am 2026-10-17: Echo Büro, Lautstärke 0.2, TuneIn-Start und Stopp laufen fehlerfrei.

Ist ein Echo `unavailable` oder fehlt die Zuordnung, gibt es eine Benachrichtigung statt eines Fehlers.

## Dashboard-Karte

Einfach als manuelle Karte einfügen (Dashboard bearbeiten → Karte hinzufügen → Manuell):

```yaml
type: vertical-stack
cards:
  - type: entities
    title: Radio BOB!
    show_header_toggle: false
    entities:
      - entity: input_select.radio_bob_sender
        name: Sender
      - entity: input_select.radio_bob_echo
        name: Echo
      - entity: input_number.radio_bob_lautstaerke
        name: Lautstärke
  - type: horizontal-stack
    cards:
      - type: button
        name: Abspielen
        icon: mdi:play
        tap_action:
          action: perform-action
          perform_action: script.radio_bob_abspielen
      - type: button
        name: Stopp
        icon: mdi:stop
        tap_action:
          action: perform-action
          perform_action: script.radio_bob_stopp
```

## Aus Automationen oder per Sprache

Die Felder überschreiben die Dashboard-Auswahl, die Helper bleiben unverändert:

```yaml
- action: script.radio_bob_abspielen
  data:
    sender: "RADIO BOB! Mittelalter Rock"
    echo: Bad
    lautstaerke: 0.3
```

## Stolperfallen

- Der Sendername muss so heißen, wie TuneIn ihn kennt. „RADIO BOB 70er Rock“ hat wirklich kein Ausrufezeichen.
- Mehrere Echos gleichzeitig gehen über eine Alexa-Multiroom-Gruppe; die kann man bei Bedarf als weiteren Eintrag in `echos` und in `input_select.radio_bob_echo` ergänzen.
