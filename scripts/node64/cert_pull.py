#!/usr/bin/env python3
"""Zertifikat von Node64 (kronos) abholen und nach /ssl legen.

Aufruf (aus HA per shell_command):
    python3 /config/node64/cert_pull.py

Konfiguration in /config/secrets.yaml:
    node64_url: https://kronos.home.martens-heimnetz.de:8080   # Basis-URL ohne /api
    node64_cert_id: 2
    node64_api_key: node64_xxxxxxxx                            # Settings > API keys

Ablauf:
    1. fullchain mit If-None-Match (gespeichertes ETag) holen
       304 -> nichts zu tun
    2. bei 200 den Schlüssel holen, ETag muss zum fullchain passen
    3. prüfen: Schlüssel passt zum Zertifikat, Zertifikat noch gültig
    4. atomar schreiben (temp-Datei im selben Ordner, fsync, os.replace),
       alte Dateien als .bak behalten, privkey mit 0600
    5. ETag speichern

Ausgabe: immer genau eine JSON-Zeile auf stdout, Exit-Code immer 0, damit
die Automation per response_variable sauber auswerten kann:
    {"status": "updated|unchanged|error", "not_after": "...", "days_left": n,
     "fingerprint": "...", "message": "..."}
"""
import datetime as dt
import json
import os
import ssl
import sys
import tempfile
import urllib.error
import urllib.request

SECRETS = "/config/secrets.yaml"
STATE = "/config/node64/state.json"
SSL_DIR = "/ssl"
FULLCHAIN = os.path.join(SSL_DIR, "fullchain.pem")
PRIVKEY = os.path.join(SSL_DIR, "privkey.pem")
TIMEOUT = 20


def out(status, message="", **extra):
    print(json.dumps({"status": status, "message": message, **extra}))
    sys.exit(0)


def load_secrets():
    import yaml

    class Loader(yaml.SafeLoader):
        pass

    # secrets.yaml darf keine Tags haben, zur Sicherheit unbekannte Tags ignorieren
    Loader.add_multi_constructor("!", lambda loader, suffix, node: None)
    with open(SECRETS, encoding="utf-8") as fh:
        data = yaml.load(fh, Loader=Loader) or {}
    try:
        return (
            str(data["node64_url"]).rstrip("/"),
            int(data["node64_cert_id"]),
            str(data["node64_api_key"]),
        )
    except KeyError as err:
        out("error", f"secrets.yaml: {err.args[0]} fehlt")


def load_state():
    try:
        with open(STATE, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {}


def save_state(state):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    atomic_write(STATE, json.dumps(state, indent=2).encode(), 0o600, backup=False)


def fetch(base, cert_id, key, fmt, etag=None):
    req = urllib.request.Request(
        f"{base}/api/certs/{cert_id}/bundle?format={fmt}",
        headers={"Authorization": f"Bearer {key}", "User-Agent": "ha-node64-cert-pull"},
    )
    if etag:
        req.add_header("If-None-Match", etag)
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as resp:
            return resp.status, resp.headers, resp.read()
    except urllib.error.HTTPError as err:
        if err.code == 304:
            return 304, err.headers, b""
        hints = {401: "API-Key ungültig", 403: "API-Key ohne Recht",
                 404: "Zertifikat-ID unbekannt", 409: "noch nicht ausgestellt",
                 422: "Format unbekannt"}
        out("error", f"Node64 HTTP {err.code} bei format={fmt}: {hints.get(err.code, err.reason)}")
    except (urllib.error.URLError, OSError) as err:
        out("error", f"Node64 nicht erreichbar ({base}): {getattr(err, 'reason', err)}")


def verify(chain_pem, key_pem):
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization

    cert = x509.load_pem_x509_certificate(chain_pem)
    pkey = serialization.load_pem_private_key(key_pem, password=None)
    pub = serialization.PublicFormat.SubjectPublicKeyInfo
    enc = serialization.Encoding.DER
    if cert.public_key().public_bytes(enc, pub) != pkey.public_key().public_bytes(enc, pub):
        out("error", "Schlüssel passt nicht zum Zertifikat, nichts ersetzt")
    not_after = cert.not_valid_after_utc
    now = dt.datetime.now(dt.timezone.utc)
    if not_after <= now:
        out("error", f"geliefertes Zertifikat ist abgelaufen ({not_after.isoformat()}), nichts ersetzt")
    try:
        san = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)
        names = san.value.get_values_for_type(x509.DNSName)
    except x509.ExtensionNotFound:
        names = []
    return {
        "not_after": not_after.isoformat(),
        "days_left": (not_after - now).days,
        "fingerprint": cert.fingerprint(hashes.SHA256()).hex(),
        "names": names,
    }


def atomic_write(path, data, mode, backup=True):
    folder = os.path.dirname(path)
    fd, tmp = tempfile.mkstemp(dir=folder, prefix=".node64-", suffix=".tmp")
    try:
        os.fchmod(fd, mode)
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        if backup and os.path.exists(path):
            bak = path + ".bak"
            with open(path, "rb") as src:
                old = src.read()
            bfd, btmp = tempfile.mkstemp(dir=folder, prefix=".node64-", suffix=".bak")
            os.fchmod(bfd, mode)
            with os.fdopen(bfd, "wb") as fh:
                fh.write(old)
            os.replace(btmp, bak)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def main():
    base, cert_id, key = load_secrets()
    state = load_state()
    have_files = os.path.exists(FULLCHAIN) and os.path.exists(PRIVKEY)
    etag = state.get("etag") if have_files else None

    for _ in range(2):  # zweiter Versuch, falls Node64 genau dazwischen erneuert
        status, headers, chain = fetch(base, cert_id, key, "fullchain", etag)
        if status == 304:
            out("unchanged", "Zertifikat unverändert",
                not_after=headers.get("X-Cert-Not-After") or state.get("not_after"),
                days_left=state_days_left(headers.get("X-Cert-Not-After") or state.get("not_after")),
                fingerprint=state.get("fingerprint"))
        new_etag = headers.get("ETag")
        _, kheaders, key_pem = fetch(base, cert_id, key, "key")
        if not new_etag or kheaders.get("ETag") == new_etag:
            break
    else:
        out("error", "ETag von fullchain und key passt zweimal nicht zusammen, nichts ersetzt")

    info = verify(chain, key_pem)
    # erst Schlüssel, dann Kette: beide sind nach diesem Block konsistent,
    # HA liest sie ohnehin erst beim nächsten Neustart
    atomic_write(PRIVKEY, key_pem, 0o600)
    atomic_write(FULLCHAIN, chain, 0o644)
    state.update({"etag": new_etag, "updated": dt.datetime.now(dt.timezone.utc).isoformat(),
                  "not_after": info["not_after"], "fingerprint": info["fingerprint"]})
    save_state(state)
    out("updated", "neues Zertifikat abgelegt, HA-Neustart nötig", **info)


def state_days_left(not_after):
    if not not_after:
        return None
    try:
        value = dt.datetime.fromisoformat(str(not_after).replace("Z", "+00:00"))
    except ValueError:
        try:
            from email.utils import parsedate_to_datetime
            value = parsedate_to_datetime(not_after)
        except (TypeError, ValueError):
            return None
    if value.tzinfo is None:
        value = value.replace(tzinfo=dt.timezone.utc)
    return (value - dt.datetime.now(dt.timezone.utc)).days


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as err:  # alles Unerwartete als JSON melden
        out("error", f"{type(err).__name__}: {err}")
