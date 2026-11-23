# Ecowitt-Wetterstation über Proxy64 (HTTP → HTTPS)

Stand: 2026-11-23, live seit 06:35 Uhr.

## Problem

Seit 2026-11-22 spricht Home Assistant auf Port 8123 nur noch HTTPS (Zertifikat `*.home.martens-heimnetz.de` von Node64, siehe [node64_zertifikat.md](node64_zertifikat.md)).
Das Gateway der WS2350 (EasyWeather-WIFI5D89 V1.7.6) kann beim „Customized Upload“ nur Plain-HTTP senden. Ergebnis: keine Ecowitt-Daten mehr in HA, alle `sensor.ws2350_v2_38_*` `unavailable`, MG- und Capri-Vorklimatisierung liefen auf den Vorhersage-Fallback.

## Lösung

Proxy64 in Node64 (kronos, 10.10.0.11) nimmt den HTTP-Upload an und reicht ihn per HTTPS an HA weiter. Kein zusätzlicher Proxy nötig.

```
WS2350 --HTTP:80--> Proxy64 (kronos) --HTTPS:8123--> Home Assistant /api/webhook/<id>
```

### 1. DNS64

A-Record `ecowitt.home.martens-heimnetz.de` → `10.10.0.11`.

Proxy64 wählt den Host über den Host-Header aus. Mit der IP von kronos in der App käme `Host: 10.10.0.11` an, und unbekannte Namen beantwortet Proxy64 mit 404. Deshalb ein eigener Name.

### 2. Proxy64-Host

| Feld | Wert |
|---|---|
| Namen | `ecowitt.home.martens-heimnetz.de` |
| Ziel | `https` · `homeassistant.home.martens-heimnetz.de` · `8123` |
| SSL | **nur HTTP** (`cert_id: -1`), **HTTPS erzwingen aus** (sonst Redirect, dem die Station nicht folgt) |
| Zertifikat des Ziels prüfen | an |
| Erweitert → Host-Kopf zum Ziel | `homeassistant.home.martens-heimnetz.de` |
| WebSockets | nicht nötig |

### 3. Home Assistant: Trusted Proxy

Proxy64 setzt immer `X-Forwarded-For`. Ohne Freigabe antwortet HA mit **400 Bad Request**.
Einstellungen → System → Netzwerk → Reverse Proxy: X-Forwarded-For verwenden an, Trusted Proxy `10.10.0.11`.
Danach sieht HA die echte IP der Station (passt auch zum local-only-Webhook der Ecowitt-Integration).

### 4. Ecowitt-App (Customized Upload)

| Feld | Wert |
|---|---|
| Protokoll | Ecowitt |
| Server IP / Hostname | `ecowitt.home.martens-heimnetz.de` (nicht die IP) |
| Port | `80` |
| Pfad | `/api/webhook/<webhook-id>` (unverändert) |
| Intervall | 30 s |

## Test

```
curl -v -X POST "http://ecowitt.home.martens-heimnetz.de/api/webhook/<webhook-id>" -d "test=1"
```

- `200` → alles gut
- `301/308` → „HTTPS erzwingen“ ist an
- `400` → Trusted Proxy in HA fehlt
- `404` → Name in Proxy64 bzw. Host-Header passt nicht

Die Webhook-ID steht im Pfad-Feld der Ecowitt-App (HA zeigt sie nach der Einrichtung nicht mehr an).

## Stolperfallen

- Die App meldete beim Speichern einen **Timeout**, die alten Werte blieben drin. Nach Schließen und Neuöffnen der App ließ sich speichern.
- Das Proxy64-Zugriffslog blieb leer. Kontrolle stattdessen über den Request-Zähler des Hosts (Node64 → Proxy64 → Hosts) bzw. `last_updated` von `sensor.ws2350_v2_38_outdoor_temperature`.
