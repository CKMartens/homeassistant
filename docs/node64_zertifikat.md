# Zertifikat von Node64 in HA beziehen

Stand: 2026-11-22, live: Package + Skript eingespielt, erstes Zertifikat bis 2027-02-20 abgeholt. HTTPS in HA aktiv seit 2026-11-22 08:28 (UI, bestätigt).

## Idee

Node64 auf **kronos** (10.10.0.11, UI auf Port 8080) ist die zentrale Stelle für Let's Encrypt im Heimnetz. Es holt das Wildcard-Zertifikat `*.home.martens-heimnetz.de` (Node64-Zertifikat-ID **2**) per DNS-01 über Hetzner DNS und erneuert es selbst. Alle anderen Systeme holen es nur noch ab:

```
GET /api/certs/2/bundle?format=fullchain|key|pem|zip
Authorization: Bearer node64_...
If-None-Match: <ETag vom letzten Abruf>   -> 304, solange unverändert
```

- ETag = Fingerabdruck des Zertifikats, Header `X-Cert-Not-After` = Ablauf
- Abrufe mit privatem Schlüssel (`key`, `pem`, `zip`) stehen im Node64-Audit
- 404 unbekannte ID, 409 noch nicht ausgestellt, 422 unbekanntes Format

In HA übernimmt das `scripts/node64/cert_pull.py` (liegt in HA unter `/config/node64/cert_pull.py`), gestartet von `shell_command.node64_zertifikat_abholen` aus [packages/node64_zertifikat.yaml](../packages/node64_zertifikat.yaml).

## Ablauf des Skripts

1. Liest `node64_url`, `node64_cert_id`, `node64_api_key` aus `/config/secrets.yaml`.
2. Holt `fullchain` mit dem gespeicherten ETag (`/config/node64/state.json`). Fehlt eine der Dateien in `/config/ssl`, ohne ETag.
3. **304**: nichts tun. **200**: `key` holen, ETag muss zum fullchain passen (sonst ein zweiter Versuch, falls Node64 genau dazwischen erneuert hat).
4. Prüft, dass der Schlüssel zum Zertifikat passt und es nicht abgelaufen ist. Sonst wird nichts ersetzt.
5. Schreibt atomar (Temp-Datei im selben Ordner, fsync, `os.replace`) nach `/config/ssl/privkey.pem` (0600) und `/config/ssl/fullchain.pem` (0644), die alten Dateien bleiben als `.bak`.
6. Gibt eine JSON-Zeile aus (`status` = `updated` / `unchanged` / `error`, `not_after`, `days_left`, `fingerprint`, `message`), Exit-Code immer 0.

## Automation

`automation.system_zertifikat_von_node64_abholen` läuft täglich 09:30 und nach jedem HA-Start:

- **updated**: Push aufs Pixel 9 mit Knopf „Jetzt neu starten“ (prüft erst die Konfiguration, dann `homeassistant.restart`) und eine HA-Benachrichtigung. HA lädt Zertifikate nur beim Start, darum kein automatischer Neustart.
- **unchanged**: still.
- **error**: Push + HA-Benachrichtigung mit der Meldung des Skripts.
- Läuft das Zertifikat in weniger als 21 Tagen ab, kommt zusätzlich eine Warnung. Normal erneuert Node64 rund 30 Tage vorher, die Warnung fängt also eine hängende Erneuerung ab.

09:30 statt nachts, damit ein Neustart nie mit den Morgen-Automationen (Vorklimatisierung, Karl) kollidiert und der Push nicht nachts kommt.

## Einbau

1. In Node64 unter Einstellungen > API-Keys einen Key für HA anlegen (erledigt 2026-11-22). Den Key nur in `secrets.yaml` eintragen, nie in Chat oder Repo.
2. `scripts/node64/cert_pull.py` nach `/config/node64/cert_pull.py` kopieren (Studio Code Server).
3. `packages/node64_zertifikat.yaml` nach `/config/packages/` kopieren.
4. `secrets.yaml` ergänzen:
   ```yaml
   node64_url: https://kronos.home.martens-heimnetz.de:8080
   node64_cert_id: 2
   node64_api_key: node64_...
   ```
   Lieber `https://` mit Namen als `http://10.10.0.11:8080`, sonst geht der API-Key im Klartext durchs LAN. Voraussetzung: das Zertifikat der Node64-UI ist gültig (ist dasselbe Wildcard-Zertifikat).
5. Konfiguration prüfen, HA neu starten. Danach die Automation einmal ausführen und prüfen, ob `/config/ssl/fullchain.pem` und `/config/ssl/privkey.pem` da sind (Terminal: `ls -l /config/ssl`, `openssl x509 -in /config/ssl/fullchain.pem -noout -subject -enddate`).
6. Erst dann HTTPS in HA einschalten. **Seit HA 2026.8 nicht mehr per `http:` in der `configuration.yaml`**, die wird ignoriert (Reparatur `yaml_still_present_after_migration`). Stattdessen: Einstellungen > System > Netzwerk > Bereich **SSL/TLS** (ggf. Strg+F5):
   - Zertifikat: `/config/ssl/fullchain.pem`
   - Schlüssel: `/config/ssl/privkey.pem`
   HA übernimmt das als Probelauf mit Zeitlimit; nach erfolgreichem Test von `https://homeassistant.home.martens-heimnetz.de:8123` in der UI bestätigen, sonst fällt es automatisch zurück. Aktive Konfiguration prüfen: WebSocket `{"type": "http/config"}` (`stable` / `pending` / `active_config_type`).
   Danach unter Einstellungen > System > Netzwerk die lokale URL auf `https://homeassistant.home.martens-heimnetz.de:8123` setzen. Der DNS-Eintrag `homeassistant.home.martens-heimnetz.de -> 10.10.0.29` existiert schon in DNS64.
7. Let's-Encrypt-App (`core_letsencrypt`, gestoppt) deinstallieren.

## Was sich mit HTTPS direkt in HA ändert

- `http://…:8123` geht nicht mehr, nur noch `https://homeassistant.home.martens-heimnetz.de:8123`. Aufruf per IP gibt eine Zertifikatswarnung.
- Companion-Apps (Pixel 9, Pixel 9a, Tablet) auf die neue interne URL umstellen.
- Alles, was HA lokal per HTTP anspricht, umstellen: z. B. Node64-Healthchecks auf HA, Neonplan3D, Browser-Lesezeichen. ha-mcp und andere Apps sprechen HA intern über den Supervisor an und sind nicht betroffen.
- Nabu Casa (Fernzugriff, Alexa) läuft weiter, der Cloud-Tunnel nutzt seine eigenen Zertifikate.
- Ist `/config/ssl/fullchain.pem` kaputt oder fehlt, startet die HTTP-Komponente nicht. Darum prüft das Skript vorher und behält `.bak`. Notfall: Probelauf nicht bestätigen (fällt von selbst zurück) bzw. SSL/TLS in der UI wieder leeren.

## Stolperfallen

- `/ssl` ist im HA-Core-Container unter HA OS **read-only** (erster Lauf am 2026-11-22: `Errno 30 Read-only file system`). Nur Apps wie die Let's-Encrypt-App dürfen dort schreiben. Darum liegen die Dateien unter `/config/ssl` (Ordner 0700, Schlüssel 0600). Folge: der Schlüssel ist in den HA-Backups enthalten (Nabu-Casa-Backups sind verschlüsselt) und für Studio Code Server/Samba lesbar.

- Das Wildcard gilt für `*.home.martens-heimnetz.de`, **nicht** für `home.martens-heimnetz.de` selbst und nicht für Namen eine Ebene tiefer.
- Node64 braucht für die Erneuerung einen funktionierenden DNS-Resolver. Am 2026-11-22 schlug ein manueller Erneuerungsversuch fehl, weil kronos `acme-v02.api.letsencrypt.org` über 10.10.0.200 auflösen wollte (Timeout). Das ist ein Homelab-Thema, die Warnung „läuft bald ab“ fängt es in HA auf.
- Die frühere Let's-Encrypt-App scheiterte an „Zone not found“ für `home.martens-heimnetz.de` und an einem TTL-Konflikt im `_acme-challenge`-RRSet mit Node64. Mit nur einem Aussteller (Node64) gibt es diese Konflikte nicht mehr.
