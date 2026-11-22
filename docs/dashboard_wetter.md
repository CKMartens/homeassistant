# Dashboard „Wetter“ (`dashboard-wetter`)

Eigenes Dashboard mit einer Ansicht „Klima“ (`/dashboard-wetter/wetter`, Subview, kiosk-mode). Nicht zu verwechseln mit der Seite Wetter im Test Dashboard bzw. „Dashboard“ (siehe [test_dashboard.md](test_dashboard.md)).

Stand: [dashboards/dashboard_wetter.json](../dashboards/dashboard_wetter.json).

## Inhalt

| Bereich | Karten |
|---|---|
| Messwerte | WS2350 Außentemperatur und Luftfeuchte (Sensor-Karten), OpenWeatherMap aktuell und stündlich (`custom:weather-chart-card`) |
| Warnungen und Radar | Unwetterwarnung DWD (`custom:meteoalarm-card`), Windy Regen, Schnee (nur bei `snowy`), Gewitter (nur bei `lightning`/`lightning-rainy`) |
| Regen, Wind, Pegel | WS2350 Regenmengen, Solarstrahlung, Taupunkt, Wind (10-min-Mittel), Pegel Itz Coburg und Schenkenau |

## Unwetterwarnung: Meteoalarm → DWD (2026-11-22)

Spook meldete `binary_sensor.meteoalarm` als unbekannte Entität. Die Meteoalarm-Integration ist in HA nicht (mehr) eingerichtet, es gibt keinen Config-Entry `meteoalarm`. Wann sie wegfiel, ist nicht belegt. Eingerichtet ist dagegen **DWD Unwetterwarnungen** (`dwd_weather_warnings`, Warncell 809473170, Gemeinde Untersiemau) mit:

- `sensor.gemeinde_untersiemau_aktuelle_warnstufe`
- `sensor.gemeinde_untersiemau_vorwarnstufe`

Die meteoalarm-card kann DWD direkt, die Karte lautet jetzt:

```yaml
type: custom:meteoalarm-card
integration: dwd
entities:
  - entity: sensor.gemeinde_untersiemau_aktuelle_warnstufe
  - entity: sensor.gemeinde_untersiemau_vorwarnstufe
```

Meteoalarm (EUMETNET) muss dafür nicht wieder eingerichtet werden; für Deutschland liefert es ohnehin die DWD-Warnungen, nur gröber (Landkreis statt Gemeinde).

## Windy-Karten auf Untersiemau (2026-11-22)

Die drei Windy-Karten (Regen, Schnee, Gewitter) zeigten auf das Rheinland (lat ≈ 51.05, lon ≈ 7.06–7.12). Jetzt stehen Kartenmitte und Detailpunkt auf Untersiemau, `lat=50.195&lon=10.970&detailLat=50.195&detailLon=10.970`, wie im „Dashboard“.
