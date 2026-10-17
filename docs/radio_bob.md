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

Die Zuordnung Anzeigename → Echo steht in beiden Skripten unter `variables: echos:`. Vor dem Einspielen prüfen:

- `media_player.echo_wohnzimmer` (bestätigt)
- `media_player.echo_bad` (abgeleitet)
- `media_player.echo_buro` (abgeleitet)

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
