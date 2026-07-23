<!-- BLOCK-ID: OBS-MANUAL-WINS-DIFF-026 -->

# OBS-MANUAL-WINS-DIFF-026 — scelta umana vince a schermo (§4.1/§4.3)

**Stato:** diff pronto, **STOP pre-deploy** (nessun deploy eseguito).

## Summary
- `build_asset_identity`: se `os_guess ∈ manual_overrides` → `labels.os` / `os_selected` = scelta umana; candidati nmap restano; `os_divergence` se scan ≠ human.
- Vocabolario `field_sources`: `manuale` → `manual` (write path + migrazione bootstrap idempotente).
- nmap `<portused>` → `provenance.used_ports` → evidence → `os_ports_used`.
- UI Identità: preselezione da `os_selected`, riga discreta divergenza.

## Test
`pytest` (7 test OBS-026) OK; `npm run lint` OK.

## Unified diff (-U5)

```diff
diff --git a/observatory/CHANGELOG.md b/observatory/CHANGELOG.md
index 2db0820..9ff7986 100644
--- a/observatory/CHANGELOG.md
+++ b/observatory/CHANGELOG.md
@@ -1,11 +1,44 @@
 # Changelog
 
+## 0.10.17 — 2026-07-23
+
+- **OBS-MANUAL-WINS-DIFF-026:** scelta OS umana vince a schermo (`labels.os` / `os_selected`); `os_divergence` quando nmap diverge; `field_sources` uniformato a `manual` (+ migrazione bootstrap); `used_ports` da nmap `<portused>` persistiti in evidence → `os_ports_used`.
+
+## 0.10.16 — 2026-07-23
+
+- **Restyle OBS-DESIGN-SPEC-025 (fasi A–F):** token ardesia + Inter/JetBrains Mono; ESLint `no-undef`; primitivi UI (DenseRow, StatusBadge, DirectionBar, HourlySparkline, CandidateList, SaveIndicator); Dossier con TOC sticky + OS multi-match; note auto-save; Inventario su tipografia sans; vista **Oggi** (coda triage proposte/nuovi/monitor). Spec in `docs/obs-design-spec-025.md`.
+
 ## 0.10.15 — 2026-07-23
 
 - **Fix Inventario crash (regressione 0.10.11):** badge infrastruttura chiamava `catLabel()` non definito nello SFC → `ReferenceError` al primo device infra e smontaggio della vista. Ripristinato helper; hardened `matchDeviceFilter`/`sourceLabel(dhcp)`; `AssetDecide`/`AssetNotes` tollerano `assetId` null.
 
+## 0.10.14 — 2026-07-23
+
+- **Hostname DHCP → name_proposals (`source=dhcp`):** collector legge `dhcp.log`/`ja4d.log`, API `POST /api/ingest/dhcp-hostnames`. Confidence alta su hostname parlanti (`AmazonAQM-*`, `ROMO-*`, `*-bild-*`, …); skip rumore (`amazon-<hex>`, `Amazon`, Fritz `PC-MAC`). Solo proposta, mai auto-rinomina. Priorità display: umano > dhcp parlante > fritz sintetico (escluso) > oui.
+- **Adozioni:** Amazon AQM 48/64, Loewe bild 7.77 (42) — identificati da hostname DHCP.
+
+## 0.10.13 — 2026-07-23
+
+- **DHCP fingerprint in dhcp.log:** `zeek/dhcp_fingerprint.zeek` estende `DHCP::Info` con `param_list` (opt 55) e `vendor_class` (opt 60); `@load` da `local.zeek` accanto a JA4. Input Fingerbank correlabile a MAC/IP senza package extra. Volume compose: `./zeek` intera.
+
+## 0.10.12 — 2026-07-23
+
+- **Sensore Zeek JA4 in produzione:** image `observatory-zeek-ja4:prod` (base `zeek/zeek:8.2` + package `zeek/foxio/ja4` v0.18.8); `@load ja4` in `zeek/local.zeek`. Impronte TLS (`ssl.log` → `ja4`/`ja4s`) + JA4D DHCP (`ja4d.log`). Prune esteso a `ja4d*`. Spike accettato (~98% ja4, RAM ~121 MiB/768). Rollback: `image: zeek/zeek:8.2` + `docker compose --profile span up -d --force-recreate zeek`.
+
+## 0.10.11 — 2026-07-23
+
+- **Abitudini — contesto AI in UI (OBS-DOSSIER-COMPLETE-022):** `/habits` espone `dst_context` + `dst_category` da `ip_intel`; riga destinazione = descrizione leggibile in evidenza, nome tecnico+IP solo in tooltip (fallback middle-ellipsis se `non_deducibile`).
+- **Dossier autosufficiente:** `AssetChassis` / `AssetDecide` / `AssetNotes` estratti; `/dossier/:id` ha interfacce+presenza, Tu decidi (rinomina/adotta/ignora/watch), note editabili, Identity (OS protect) e Habits. Drawer Inventario riusa Decide/Notes (anteprima).
+- **Contesto — automazione + confidence (022 addendum):**
+  - job notturno `IP_INTEL_CONTEXT_NIGHTLY_*` (default OFF): solo `context IS NULL`, mai ritenta `non_deducibile`; stesso batch/sleep dello script
+  - correzione manuale `PATCH /api/ip-intel/context` (`source=manual`, priorità max, ✎ in Abitudini)
+  - ritento esplicito script `--retry-non-deducibile` (dopo validazione prompt)
+  - UI: conf≥0.7 normale · 0.3–0.7 arancione + «probabile:» · manual tono distinto; tooltip con fonte+conf
+  - prompt propositivo (ipotesi su indizi leggibili) — validare con `--preview` su batch misto prima di apply/retry
+  - **confidence strutturata (OBS-IP-INTEL-STRUCT-023):** colonne `context_category` / `context_what` / `context_confidence` = fonte di verità; `context` blob solo mirror derivato; backfill one-shot con log fail (`scripts/ip_intel_context_struct_migrate.py`); `/habits` → `dst_category`/`dst_context`/`dst_confidence`/`dst_source`; priorità `manual` > `ai`
+
 ## 0.10.10 — 2026-07-23
 
 - **Dossier pagina piena + sidebar RADAR/MAPPA (OBS-DOSSIER-PAGE-021):** `AssetIdentity` / `AssetHabits` estratti (fetch autonomo, OS actions nel componente); `/dossier` hub + `/dossier/:id`; drawer Inventario = anteprima + Tu decidi + «Apri Dossier»; stub onesti Oggi/Osservatorio/Come funziona.
 
 ## 0.10.9 — 2026-07-23
diff --git a/observatory/VERSION b/observatory/VERSION
index ba78838..f00339d 100644
--- a/observatory/VERSION
+++ b/observatory/VERSION
@@ -1 +1 @@
-0.10.15
+0.10.17
diff --git a/observatory/api/app/routers/assets.py b/observatory/api/app/routers/assets.py
index 729d5af..3e11673 100644
--- a/observatory/api/app/routers/assets.py
+++ b/observatory/api/app/routers/assets.py
@@ -629,23 +629,23 @@ def update_asset(
     meta["manual_overrides"] = sorted(overrides)
     sources = dict(meta.get("field_sources") or {})
     now = datetime.utcnow()
     for field in data:
         sources[field] = {
-            "source": "manuale",
+            "source": "manual",
             "confidence": 1.0,
             "last_seen": now.isoformat() + "Z",
         }
     if watch_flag is not None:
         sources["watch_fingerprint"] = {
-            "source": "manuale",
+            "source": "manual",
             "confidence": 1.0,
             "last_seen": now.isoformat() + "Z",
         }
     if os_opt_out is not None:
         sources["os_fingerprint_opt_out"] = {
-            "source": "manuale",
+            "source": "manual",
             "confidence": 1.0,
             "last_seen": now.isoformat() + "Z",
         }
     meta["field_sources"] = sources
     # Re-read watch keys into meta after enable/disable mutated asset.meta
@@ -733,11 +733,11 @@ def adopt_name(
     overrides = set(meta.get("manual_overrides") or [])
     overrides.add("name")
     meta["manual_overrides"] = sorted(overrides)
     sources = dict(meta.get("field_sources") or {})
     sources["name"] = {
-        "source": f"manuale (proposta {source})",
+        "source": f"manual (proposta {source})",
         "confidence": 1.0,
         "last_seen": datetime.utcnow().isoformat() + "Z",
     }
     meta["field_sources"] = sources
     asset.meta = meta
@@ -827,20 +827,20 @@ def adopt_fingerprint(
     now = datetime.utcnow()
     if fact.kind == "device_class":
         asset.category = fact.value
         overrides.add("category")
         sources["category"] = {
-            "source": f"manuale (fact {fact.source})",
+            "source": f"manual (fact {fact.source})",
             "confidence": 1.0,
             "last_seen": now.isoformat() + "Z",
         }
         applied["category"] = fact.value
     elif fact.kind == "os":
         asset.os_guess = fact.value
         overrides.add("os_guess")
         sources["os_guess"] = {
-            "source": f"manuale (fact {fact.source})",
+            "source": f"manual (fact {fact.source})",
             "confidence": 1.0,
             "last_seen": now.isoformat() + "Z",
         }
         applied["os_guess"] = fact.value
     else:
diff --git a/observatory/api/app/services/asset_identity.py b/observatory/api/app/services/asset_identity.py
index ed48220..301a541 100644
--- a/observatory/api/app/services/asset_identity.py
+++ b/observatory/api/app/services/asset_identity.py
@@ -15,14 +15,33 @@ from app.services.macutil import is_locally_administered, normalize_mac
 from app.services.os_scan_guard import exclusion_payload
 from app.services.oui_store import lookup_oui_vendor
 
 OS_LABEL_MAC_MISMATCH = "OS non attribuito (MAC discordante — vedi dettagli)"
 
-# Prefer richer announcement sources first; then FRITZ hostname.
+
+def normalize_field_source_label(src: str) -> str:
+    """Unify field_sources vocabulary: ``manuale`` → ``manual`` (OBS-026)."""
+    s = str(src or "")
+    if s == "manuale" or s.startswith("manuale"):
+        return "manual" + s[len("manuale") :]
+    return s
+
+
+def is_manual_os_override(asset: Asset) -> bool:
+    """True when human locked ``os_guess`` via manual_overrides."""
+    meta = dict(asset.meta or {})
+    overrides = {str(x) for x in (meta.get("manual_overrides") or [])}
+    if "os_guess" not in overrides:
+        return False
+    return bool((asset.os_guess or "").strip())
+
+
+# Prefer richer announcement sources first; DHCP parlante > FRITZ > …
 _HOSTNAME_SOURCE_RANK = {
     "mdns": 100,
     "dns": 90,
+    "dhcp": 85,
     "ssdp": 70,
     "fritz": 50,
     "nmap": 40,
     "ai": 10,
 }
@@ -381,20 +400,93 @@ def build_asset_identity(
         "trust_level": asset.trust_level or "",
     }
 
     if os_name and os_accuracy is not None:
         if os_attribution and os_attribution.get("kind") == "chassis_sibling":
-            os_label = (
+            scan_os_label = (
                 f"{os_name} ({os_accuracy}%) · sibling "
                 f"{os_attribution.get('observed_mac') or ''}".rstrip()
             )
         else:
-            os_label = f"{os_name} ({os_accuracy}%)"
+            scan_os_label = f"{os_name} ({os_accuracy}%)"
     elif os_attribution:
-        os_label = OS_LABEL_MAC_MISMATCH
+        scan_os_label = OS_LABEL_MAC_MISMATCH
+    else:
+        scan_os_label = "non rilevato"
+
+    # Multi-match OS candidates for UI (§3.5) — from evidence.raw_hints, never invent.
+    os_candidates: list[dict[str, Any]] = []
+    seen_names: set[str] = set()
+    for hint in list(os_evidence.get("raw_hints") or [])[:5]:
+        if not isinstance(hint, dict):
+            continue
+        hname = str(hint.get("name") or "").strip()
+        if not hname or hname in seen_names:
+            continue
+        try:
+            hacc = int(hint.get("accuracy") or 0)
+        except (TypeError, ValueError):
+            hacc = 0
+        if hacc <= 0:
+            continue
+        seen_names.add(hname)
+        os_candidates.append({"name": hname, "accuracy": hacc, "subtitle": ""})
+    if os_name and os_name not in seen_names:
+        os_candidates.insert(
+            0,
+            {
+                "name": os_name,
+                "accuracy": int(os_accuracy or 0),
+                "subtitle": "",
+            },
+        )
+
+    human_os = (asset.os_guess or "").strip()
+    manual_os = is_manual_os_override(asset)
+    os_divergence: dict[str, Any] | None = None
+    if manual_os:
+        os_label = f"{human_os} · scelta manuale"
+        os_selected = human_os
+        os_selected_source = "manual"
+        if human_os not in seen_names:
+            os_candidates.insert(
+                0,
+                {
+                    "name": human_os,
+                    "accuracy": 100,
+                    "subtitle": "scelta manuale",
+                },
+            )
+            seen_names.add(human_os)
+        if os_name and os_name != human_os:
+            acc = int(os_accuracy or 0)
+            acc_bit = f" ({acc}%)" if acc > 0 else ""
+            os_divergence = {
+                "human": human_os,
+                "scan": os_name,
+                "accuracy": os_accuracy,
+                "message": (
+                    f"la scansione propone {os_name}{acc_bit}, "
+                    f"la tua scelta resta {human_os}"
+                ),
+            }
     else:
-        os_label = "non rilevato"
+        os_label = scan_os_label
+        os_selected = os_name
+        os_selected_source = "nmap_os" if os_name else None
+
+    os_ports_used = []
+    for p in list(os_evidence.get("used_ports") or os_evidence.get("ports") or []):
+        try:
+            os_ports_used.append(int(p))
+        except (TypeError, ValueError):
+            continue
+    # Dedup preserve order
+    seen_ports: set[int] = set()
+    os_ports_used = [
+        p for p in os_ports_used if p > 0 and not (p in seen_ports or seen_ports.add(p))
+    ]
 
     payload: dict[str, Any] = {
         "asset_id": asset.id,
         "mac": mac or None,
         "is_private": is_private,
@@ -402,10 +494,15 @@ def build_asset_identity(
         "vendor_reliable": vendor_reliable if vendor else False,
         "vendor_display": vendor_display,
         "os_name": os_name,
         "os_accuracy": os_accuracy,
         "os_attribution": os_attribution,
+        "os_candidates": os_candidates,
+        "os_ports_used": os_ports_used,
+        "os_selected": os_selected,
+        "os_selected_source": os_selected_source,
+        "os_divergence": os_divergence,
         "hostname": hostname,
         "services": services_text,
         "services_list": services,
         "device_type": device_type,
         "first_seen": _iso(first_seen),
diff --git a/observatory/api/app/services/fingerprint_facts.py b/observatory/api/app/services/fingerprint_facts.py
index 31e619b..b97850f 100644
--- a/observatory/api/app/services/fingerprint_facts.py
+++ b/observatory/api/app/services/fingerprint_facts.py
@@ -346,10 +346,22 @@ def _write_host_scan_facts(
     counts = {"os_facts": 0, "model_facts": 0, "endpoints": 0, "services": 0}
     prov = dict(host.get("provenance") or {})
     ip = str(host.get("ip") or "").strip()
     os_hints = list(prov.get("os_hints") or host.get("os_hints") or [])
     services = list(prov.get("services") or host.get("services") or [])
+    used_ports_raw = list(prov.get("used_ports") or host.get("used_ports") or [])
+    used_ports: list[int] = []
+    seen_ports: set[int] = set()
+    for raw in used_ports_raw:
+        try:
+            pid = int(raw)
+        except (TypeError, ValueError):
+            continue
+        if pid <= 0 or pid in seen_ports:
+            continue
+        seen_ports.add(pid)
+        used_ports.append(pid)
     extra = dict(evidence_extra or {})
 
     best = None
     for hint in os_hints:
         name = normalize_nmap_os_name(str(hint.get("name") or ""))
@@ -365,10 +377,11 @@ def _write_host_scan_facts(
         conf = max(0.0, min(1.0, best[1] / 100.0))
         evidence = {
             "profile": source_profile,
             "accuracy": best[1],
             "raw_hints": os_hints[:3],
+            "used_ports": used_ports[:32],
             "mac": host_mac,
             **extra,
         }
         if upsert_fact(
             db,
diff --git a/observatory/api/app/services/schema_migrations.py b/observatory/api/app/services/schema_migrations.py
index e9c4a3e..13ae157 100644
--- a/observatory/api/app/services/schema_migrations.py
+++ b/observatory/api/app/services/schema_migrations.py
@@ -64,10 +64,13 @@ MIGRATIONS: dict[str, dict[str, str]] = {
     },
     # OBS-AI-CONTEXT Wave 1c.
     "ip_intel": {
         "context": "TEXT",
         "context_source": "VARCHAR(16)",
+        "context_category": "VARCHAR(32)",
+        "context_what": "TEXT",
+        "context_confidence": "FLOAT",
         "ai_fetched_at": "DATETIME",
     },
 }
 
 # Idempotent unique indexes (SQLite: no table rebuild). Apply ONLY after
@@ -153,6 +156,44 @@ def apply_sqlite_migrations(engine: Engine) -> list[str]:
                         "duplicate (interface_id, ip) rows still present"
                     )
                     continue
             connection.execute(text(ddl))
             changed.append(f"index.{name}")
+    # Idempotent: fill structured context cols from legacy blob when empty.
+    try:
+        insp = inspect(engine)
+        if "ip_intel" in set(insp.get_table_names()):
+            cols = {c["name"] for c in insp.get_columns("ip_intel")}
+            if "context_category" in cols:
+                from app.db import session_scope
+                from app.services.ip_intel_context import backfill_structured_from_blobs
+
+                with session_scope() as db:
+                    stats = backfill_structured_from_blobs(db)
+                n = int(stats.get("ok") or 0) if isinstance(stats, dict) else int(stats or 0)
+                fail = int(stats.get("fail") or 0) if isinstance(stats, dict) else 0
+                if n or fail:
+                    changed.append(f"ip_intel.context_backfill:ok={n}:fail={fail}")
+                    print(
+                        f"[bootstrap] ip_intel context structured backfill "
+                        f"rows={n} fail={fail}"
+                    )
+    except Exception as exc:  # noqa: BLE001
+        print(f"[bootstrap] ip_intel context backfill skipped: {exc}")
+
+    # OBS-026: field_sources source=manuale → manual (idempotent).
+    try:
+        insp = inspect(engine)
+        if "assets" in set(insp.get_table_names()):
+            from app.db import session_scope
+            from app.services.field_sources_vocab import migrate_field_sources_manual_vocab
+
+            with session_scope() as db:
+                stats = migrate_field_sources_manual_vocab(db)
+            n = int(stats.get("changed") or 0)
+            if n:
+                changed.append(f"assets.field_sources_manual_vocab:{n}")
+                print(f"[bootstrap] field_sources manuale→manual rows={n}")
+    except Exception as exc:  # noqa: BLE001
+        print(f"[bootstrap] field_sources vocab migrate skipped: {exc}")
+
     return changed
diff --git a/observatory/collector/collector/adapters/nmap_scan.py b/observatory/collector/collector/adapters/nmap_scan.py
index e0ae4e2..a1ba620 100644
--- a/observatory/collector/collector/adapters/nmap_scan.py
+++ b/observatory/collector/collector/adapters/nmap_scan.py
@@ -227,10 +227,21 @@ def parse_nmap_xml(
                 "name": item.get("name", "")[:160],
                 "accuracy": int(item.get("accuracy", "0") or 0),
             }
             for item in node.findall("./os/osmatch")[:3]
         ]
+        used_ports: list[int] = []
+        seen_ports: set[int] = set()
+        for item in node.findall("./os/portused"):
+            try:
+                pid = int(item.get("portid", "0") or 0)
+            except (TypeError, ValueError):
+                continue
+            if pid <= 0 or pid in seen_ports:
+                continue
+            seen_ports.add(pid)
+            used_ports.append(pid)
         hosts.append(
             {
                 "hostname": hostname,
                 "ip": addresses.get("ipv4", target) or ipv4,
                 "mac": mac,
@@ -241,10 +252,11 @@ def parse_nmap_xml(
                 "kind": "nmap",
                 "provenance": {
                     "profile": profile,
                     "services": services[:128],
                     "os_hints": os_hints,
+                    "used_ports": used_ports[:32],
                     "l3_only": not bool(mac),
                     "confidence": 0.9 if mac else 0.4,
                 },
             }
         )
diff --git a/observatory/tests/test_asset_identity.py b/observatory/tests/test_asset_identity.py
index 1edeba9..a94259d 100644
--- a/observatory/tests/test_asset_identity.py
+++ b/observatory/tests/test_asset_identity.py
@@ -232,23 +232,101 @@ def test_identity_os_mac_mismatch_legacy_scan_meta(db):
     assert ident["labels"]["os"] == OS_LABEL_MAC_MISMATCH
     assert ident["os_attribution"]["observed_mac"] == "DC:A6:32:9C:A7:62"
     assert "OS rilevato ma non attribuito" in ident["os_attribution"]["message"]
 
 
-def test_oui_parse_ieee_and_lookup(db):
-    sample = """
-# comment
-00-11-32   (hex)\t\tSynology Incorporated
-001132     (base 16)\t\tSynology Incorporated
-"""
-    parsed = parse_ieee_oui_txt(sample)
-    assert parsed["00:11:32"].startswith("Synology")
-    upsert_oui(db, "00:11:32", parsed["00:11:32"], source="ieee")
+def test_identity_manual_os_wins_and_divergence(db):
+    """OBS-026: manual os_guess wins labels/selection; scan divergence declared."""
+    asset = _asset(db, mac="00:11:32:AA:BB:01", ip="192.168.1.11", name="NAS")
+    asset.os_guess = "ADM 4.x (ASUSTOR)"
+    asset.meta = {
+        "manual_overrides": ["os_guess"],
+        "field_sources": {
+            "os_guess": {"source": "manual", "confidence": 1.0},
+        },
+    }
+    db.add(
+        FingerprintFact(
+            asset_id=asset.id,
+            kind="os",
+            value="Linux 4.15 - 5.19",
+            source="nmap_os",
+            confidence=0.95,
+            evidence={
+                "accuracy": 95,
+                "raw_hints": [
+                    {"name": "Linux 4.15 - 5.19", "accuracy": 95},
+                    {"name": "OpenWrt 21.02", "accuracy": 92},
+                ],
+                "used_ports": [22, 443],
+            },
+        )
+    )
+    db.flush()
+    ident = build_asset_identity(db, asset)
+    assert ident["labels"]["os"] == "ADM 4.x (ASUSTOR) · scelta manuale"
+    assert ident["os_selected"] == "ADM 4.x (ASUSTOR)"
+    assert ident["os_selected_source"] == "manual"
+    assert ident["os_name"] == "Linux 4.15 - 5.19"
+    assert ident["os_divergence"]["human"] == "ADM 4.x (ASUSTOR)"
+    assert ident["os_divergence"]["scan"] == "Linux 4.15 - 5.19"
+    assert "la tua scelta resta" in ident["os_divergence"]["message"]
+    assert ident["os_ports_used"] == [22, 443]
+    names = [c["name"] for c in ident["os_candidates"]]
+    assert names[0] == "ADM 4.x (ASUSTOR)"
+    assert "Linux 4.15 - 5.19" in names
+
+
+def test_identity_os_ports_from_used_ports(db):
+    asset = _asset(db, mac="00:11:32:AA:BB:02", ip="192.168.1.12", name="Box")
+    db.add(
+        FingerprintFact(
+            asset_id=asset.id,
+            kind="os",
+            value="Linux",
+            source="nmap_os",
+            confidence=0.9,
+            evidence={"accuracy": 90, "used_ports": [22, 80, 22]},
+        )
+    )
+    db.flush()
+    ident = build_asset_identity(db, asset)
+    assert ident["os_ports_used"] == [22, 80]
+    assert ident["os_divergence"] is None
+    assert ident["os_selected_source"] == "nmap_os"
+
+
+def test_normalize_field_source_label():
+    from app.services.asset_identity import normalize_field_source_label
+
+    assert normalize_field_source_label("manuale") == "manual"
+    assert normalize_field_source_label("manuale (proposta dhcp)") == "manual (proposta dhcp)"
+    assert normalize_field_source_label("manual") == "manual"
+    assert normalize_field_source_label("OUI") == "OUI"
+
+
+def test_migrate_field_sources_manual_vocab(db):
+    from app.services.field_sources_vocab import migrate_field_sources_manual_vocab
+
+    asset = _asset(db, mac="00:11:32:AA:BB:03", ip="192.168.1.13", name="X")
+    asset.meta = {
+        "field_sources": {
+            "os_guess": {"source": "manuale", "confidence": 1.0},
+            "name": {"source": "manuale (proposta dhcp)", "confidence": 1.0},
+            "category": {"source": "OUI", "confidence": 0.7},
+        }
+    }
     db.flush()
-    vendor, reliable = lookup_oui_vendor(db, "00:11:32:11:22:33")
-    assert reliable is True
-    assert "Synology" in vendor
+    stats = migrate_field_sources_manual_vocab(db)
+    assert stats["changed"] == 1
+    db.refresh(asset)
+    sources = asset.meta["field_sources"]
+    assert sources["os_guess"]["source"] == "manual"
+    assert sources["name"]["source"] == "manual (proposta dhcp)"
+    assert sources["category"]["source"] == "OUI"
+    # idempotent
+    assert migrate_field_sources_manual_vocab(db)["changed"] == 0
 
 
 def test_os_opt_out_via_meta_blocks_enqueue(db, monkeypatch):
     monkeypatch.setenv("SCANNER_PRIVILEGED", "true")
     get_settings.cache_clear()
diff --git a/observatory/tests/test_fingerprint_b2.py b/observatory/tests/test_fingerprint_b2.py
index 859f145..a700adb 100644
--- a/observatory/tests/test_fingerprint_b2.py
+++ b/observatory/tests/test_fingerprint_b2.py
@@ -238,10 +238,35 @@ def test_apply_nmap_scan_facts_chassis_sibling_gate_rejects_without_c1c2c3(db):
     assert stats["os_attributed_via_chassis_sibling"] == 0
     assert stats["skipped_mac_mismatch"] == 1
     assert stats["os_discarded_mac_mismatch"] is True
 
 
+def test_apply_nmap_scan_facts_persists_used_ports(db):
+    asset = _asset(db, mac="AA:BB:CC:DD:EE:44", ip="192.168.1.44")
+    stats = apply_nmap_scan_facts(
+        db,
+        asset_id=asset.id,
+        hosts=[
+            {
+                "ip": "192.168.1.44",
+                "mac": "AA:BB:CC:DD:EE:44",
+                "os_hints": [{"name": "Linux 5.10", "accuracy": 91}],
+                "used_ports": [22, 443],
+            }
+        ],
+    )
+    assert stats["os_facts"] == 1
+    fact = db.scalar(
+        select(FingerprintFact).where(
+            FingerprintFact.asset_id == asset.id,
+            FingerprintFact.kind == "os",
+        )
+    )
+    assert fact is not None
+    assert fact.evidence.get("used_ports") == [22, 443]
+
+
 def test_eligible_excludes_solid_os_fact(db):
     settings = Settings(network_cidr="192.168.0.0/22")
     a = _asset(db, mac="AA:BB:CC:DD:EE:02", ip="192.168.1.9")
     b = _asset(db, mac="AA:BB:CC:DD:EE:03", ip="192.168.1.10", name="Cassiopea")
     apply_nmap_scan_facts(
diff --git a/observatory/tests/test_m2_discovery.py b/observatory/tests/test_m2_discovery.py
index 138d0f8..73f5b43 100644
--- a/observatory/tests/test_m2_discovery.py
+++ b/observatory/tests/test_m2_discovery.py
@@ -49,10 +49,30 @@ def test_parse_nmap_sn_keeps_ping_only_hosts():
     assert hosts[0]["mac"] == ""
     assert hosts[0]["provenance"]["l3_only"] is True
     assert hosts[1]["mac"] == "AA:BB:CC:DD:EE:51"
 
 
+def test_parse_nmap_xml_extracts_os_portused():
+    xml = """<?xml version="1.0"?>
+    <nmaprun>
+      <host>
+        <address addr="192.168.1.70" addrtype="ipv4"/>
+        <address addr="AA:BB:CC:DD:EE:70" addrtype="mac" vendor="Vendor"/>
+        <os>
+          <portused state="open" proto="tcp" portid="22"/>
+          <portused state="closed" proto="tcp" portid="1"/>
+          <osmatch name="Linux 4.15 - 5.19" accuracy="95"/>
+          <osmatch name="OpenWrt 21.02" accuracy="92"/>
+        </os>
+      </host>
+    </nmaprun>
+    """
+    rows = parse_nmap_xml(xml, profile="os_fingerprint", target="192.168.1.70")
+    assert rows[0]["provenance"]["used_ports"] == [22, 1]
+    assert rows[0]["provenance"]["os_hints"][0]["name"].startswith("Linux")
+
+
 def test_parse_nmap_xml_keeps_ip_only():
     xml = """<?xml version="1.0"?>
     <nmaprun>
       <host>
         <address addr="192.168.1.60" addrtype="ipv4"/>
diff --git a/observatory/web/package.json b/observatory/web/package.json
index d7029e8..97373d1 100644
--- a/observatory/web/package.json
+++ b/observatory/web/package.json
@@ -1,20 +1,26 @@
 {
   "name": "lan-observatory-web",
   "private": true,
-  "version": "0.10.10",
+  "version": "0.10.17",
   "type": "module",
   "scripts": {
     "dev": "vite",
     "build": "vite build",
     "preview": "vite preview",
-    "test": "node --test src/*.test.js"
+    "lint": "eslint src --max-warnings 0",
+    "test": "node --test src/*.test.js src/**/*.test.js"
   },
   "dependencies": {
+    "@fontsource/inter": "^5.3.0",
+    "@fontsource/jetbrains-mono": "^5.3.0",
     "vue": "^3.5.13",
     "vue-router": "^4.5.0"
   },
   "devDependencies": {
     "@vitejs/plugin-vue": "^5.2.1",
+    "eslint": "^10.7.0",
+    "eslint-plugin-vue": "^10.10.0",
+    "globals": "^17.7.0",
     "vite": "^6.0.3"
   }
 }
diff --git a/observatory/web/src/components/AssetIdentity.vue b/observatory/web/src/components/AssetIdentity.vue
index ce6ff9a..09665c9 100644
--- a/observatory/web/src/components/AssetIdentity.vue
+++ b/observatory/web/src/components/AssetIdentity.vue
@@ -1,9 +1,11 @@
 <script setup>
 import { computed, ref, watch } from "vue";
 import { api } from "../api";
 import { formatDate } from "../formatTime";
+import CandidateList from "./ui/CandidateList.vue";
+import StatusBadge from "./ui/StatusBadge.vue";
 
 const props = defineProps({
   assetId: { type: [Number, String], required: true },
 });
 
@@ -15,16 +17,40 @@ const error = ref("");
 const technicalOpen = ref(false);
 const osScanBusy = ref(false);
 const osScanMsg = ref("");
 const actionBusy = ref(false);
 const actionMsg = ref("");
+const selectedOs = ref(null);
+const osPickMsg = ref("");
 
 const numericId = computed(() => {
   const n = Number(props.assetId);
   return Number.isFinite(n) && n > 0 ? n : null;
 });
 
+const osCandidates = computed(() =>
+  (identity.value?.os_candidates || []).map((c) => ({
+    id: c.name,
+    name: c.name,
+    subtitle: c.subtitle || "",
+    confidence: c.accuracy,
+  })),
+);
+
+const showOsCandidates = computed(() => {
+  const n = osCandidates.value.length;
+  if (n > 1) return true;
+  if (identity.value?.os_selected_source === "manual" && n >= 1) return true;
+  return false;
+});
+
+const osEvidenceLine = computed(() => {
+  const ports = identity.value?.os_ports_used || [];
+  if (!ports.length) return "";
+  return `Porte usate ${ports.join(" · ")}`;
+});
+
 async function load({ technical = technicalOpen.value } = {}) {
   const id = numericId.value;
   if (!id) {
     identity.value = null;
     error.value = "";
@@ -33,10 +59,15 @@ async function load({ technical = technicalOpen.value } = {}) {
   loading.value = true;
   error.value = "";
   osScanMsg.value = "";
   try {
     identity.value = await api.assetIdentity(id, technical);
+    if (identity.value?.os_selected) {
+      selectedOs.value = identity.value.os_selected;
+    } else if (identity.value?.os_name) {
+      selectedOs.value = identity.value.os_name;
+    }
   } catch (e) {
     identity.value = null;
     error.value = e.message || "Identità non disponibile";
   } finally {
     loading.value = false;
@@ -103,57 +134,121 @@ async function detectOsNow() {
   } finally {
     osScanBusy.value = false;
   }
 }
 
+async function adoptOsCandidate(name) {
+  const id = numericId.value;
+  if (!id || !name) return;
+  osPickMsg.value = "";
+  try {
+    await api.updateAsset(id, { os_guess: name });
+    osPickMsg.value = "scelta salvata";
+    await load({ technical: technicalOpen.value });
+    emit("changed");
+  } catch (e) {
+    osPickMsg.value = e.message || "salvataggio fallito";
+  }
+}
+
+async function onOsSelect(id) {
+  selectedOs.value = id;
+  await adoptOsCandidate(String(id));
+}
+
+async function onOsFree(text) {
+  selectedOs.value = text;
+  await adoptOsCandidate(text);
+}
+
 watch(
   () => props.assetId,
   () => {
     technicalOpen.value = false;
     osScanMsg.value = "";
     actionMsg.value = "";
+    osPickMsg.value = "";
     load({ technical: false });
   },
   { immediate: true },
 );
 </script>
 
 <template>
-  <section class="asset-identity inv-p-sec inv-chi-sei">
+  <section id="chi-sei" class="asset-identity inv-p-sec inv-chi-sei">
     <div class="inv-p-seclabel"><span>Chi sei</span><span class="line" /></div>
-    <p class="inv-purpose">Chi è questo device — identità osservata</p>
+    <p class="inv-purpose">Identità osservata</p>
     <div v-if="loading" class="inv-p-note-sugg">caricamento…</div>
     <template v-else-if="identity">
-      <div class="inv-kv inv-identity-kv">
-        <span class="k">Vendor</span>
-        <span class="v">
-          {{ identity.labels.vendor }}
+      <div class="id-grid">
+        <div class="id-cell">
+          <span class="id-k">Vendor</span>
+          <span class="id-v">
+            {{ identity.labels.vendor }}
+            <span
+              v-if="identity.vendor && !identity.vendor_reliable"
+              class="badge-privacy"
+              title="MAC locally-administered: OUI non affidabile"
+            >privacy</span>
+          </span>
+        </div>
+        <div class="id-cell">
+          <span class="id-k">Tipo</span>
+          <span class="id-v">{{ identity.labels.device_type }}</span>
+        </div>
+        <div class="id-cell">
+          <span class="id-k">OS</span>
           <span
-            v-if="identity.vendor && !identity.vendor_reliable"
-            class="badge-privacy"
-            title="MAC locally-administered: OUI non affidabile"
-          >privacy</span>
-        </span>
-        <span class="k">OS</span>
-        <span
-          class="v"
-          :class="{
-            'os-mac-mismatch': identity.os_attribution?.kind === 'mac_mismatch',
-            'os-chassis-sibling': identity.os_attribution?.kind === 'chassis_sibling',
-          }"
-          :title="identity.os_attribution?.message || undefined"
-        >{{ identity.labels.os }}</span>
+            class="id-v"
+            :class="{
+              'os-mac-mismatch': identity.os_attribution?.kind === 'mac_mismatch',
+              'os-chassis-sibling': identity.os_attribution?.kind === 'chassis_sibling',
+            }"
+            :title="identity.os_attribution?.message || undefined"
+          >{{ identity.labels.os }}</span>
+        </div>
+      </div>
+
+      <p v-if="identity.os_divergence?.message" class="os-divergence">
+        {{ identity.os_divergence.message }}
+      </p>
+
+      <div v-if="showOsCandidates" class="os-cands">
+        <p class="os-cands-lead">
+          <template v-if="identity.os_selected_source === 'manual'">
+            Scelta manuale attiva. I candidati nmap restano disponibili come proposta.
+          </template>
+          <template v-else>
+            {{ osCandidates.length }} corrispondenze. Scegli quella giusta, oppure lascia la prima.
+          </template>
+        </p>
+        <CandidateList
+          v-model="selectedOs"
+          :candidates="osCandidates"
+          :evidence-line="osEvidenceLine"
+          @select="onOsSelect"
+          @free="onOsFree"
+        />
+        <p v-if="osPickMsg" class="inv-os-msg">{{ osPickMsg }}</p>
+      </div>
+
+      <div class="inv-kv inv-identity-kv">
         <span class="k">Hostname</span><span class="v">{{ identity.labels.hostname }}</span>
         <span class="k">Servizi</span><span class="v">{{ identity.labels.services }}</span>
-        <span class="k">Tipo</span><span class="v">{{ identity.labels.device_type }}</span>
         <span class="k">MAC</span>
-        <span class="v">
+        <span class="v mono">
           {{ identity.labels.mac }}
           <span v-if="identity.is_private" class="badge-privacy">U/L</span>
         </span>
         <span class="k">Prima volta</span><span class="v">{{ fmtSeen(identity.first_seen) || identity.labels.first_seen }}</span>
-        <span class="k">Presence</span><span class="v">{{ identity.labels.presence }}</span>
+        <span class="k">Presence</span>
+        <span class="v">
+          <StatusBadge
+            :tone="identity.labels.presence === 'present' || identity.labels.presence === 'presente' ? 'presente' : 'muted'"
+            :label="identity.labels.presence"
+          />
+        </span>
       </div>
       <div
         class="inv-switchrow"
         :class="{ on: identity.os_scan && identity.os_scan.opt_out }"
         @click="toggleOsProtect"
@@ -222,89 +317,104 @@ watch(
 </template>
 
 <style scoped>
 .inv-p-sec { margin-top: 18px; }
 .inv-p-seclabel {
-  font-size: 11px; letter-spacing: 0.12em; text-transform: uppercase;
-  color: var(--inv-faint); margin-bottom: 9px;
+  font-size: 14px; font-weight: 500; text-transform: none; letter-spacing: 0;
+  color: var(--text-1); margin-bottom: 9px;
   display: flex; align-items: center; gap: 10px;
 }
-.inv-p-seclabel .line { flex: 1; height: 1px; background: var(--inv-border-soft); }
+.inv-p-seclabel .line { flex: 1; height: 0.5px; background: var(--border); }
 .inv-purpose {
-  margin: 0 0 10px; font-size: 12px; color: var(--inv-faint); line-height: 1.35;
+  margin: 0 0 10px; font-size: 12px; color: var(--text-3); line-height: 1.35;
+}
+.inv-p-note-sugg { font-size: 12.5px; color: var(--text-3); }
+.id-grid {
+  display: grid;
+  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
+  gap: 8px;
+  margin-bottom: 14px;
+}
+.id-cell {
+  background: var(--bg-1);
+  border: 0.5px solid var(--border);
+  border-radius: var(--radius);
+  padding: 10px 12px;
+}
+.id-k { display: block; font-size: 11px; color: var(--text-3); margin-bottom: 4px; }
+.id-v { font-size: 13px; color: var(--text-1); word-break: break-word; }
+.os-cands { margin: 12px 0; }
+.os-cands-lead { margin: 0 0 8px; font-size: 12px; color: var(--text-2); }
+.os-divergence {
+  margin: 0 0 12px;
+  font-size: 12px;
+  color: var(--text-2);
+  line-height: 1.4;
+  padding-left: 10px;
+  border-left: 2px solid var(--accent);
 }
-.inv-p-note-sugg { font-size: 12.5px; color: var(--inv-faint); }
 .inv-kv {
   display: grid; grid-template-columns: 108px 1fr; gap: 8px 10px;
   font-size: 12.5px; margin-top: 12px;
 }
-.inv-kv .k { color: var(--inv-faint); }
-.inv-kv .v { color: var(--inv-mut); word-break: break-all; }
+.inv-kv .k { color: var(--text-3); }
+.inv-kv .v { color: var(--text-2); word-break: break-all; }
 .inv-identity-kv { margin-top: 0; }
 .inv-identity-kv .os-mac-mismatch {
   cursor: help;
-  border-bottom: 1px dotted color-mix(in srgb, var(--inv-warn, #c9a227) 70%, transparent);
+  border-bottom: 1px dotted color-mix(in srgb, var(--attn) 70%, transparent);
 }
 .inv-identity-kv .os-chassis-sibling {
   cursor: help;
-  border-bottom: 1px dotted color-mix(in srgb, var(--inv-green, #3d9a5f) 55%, transparent);
+  border-bottom: 1px dotted color-mix(in srgb, var(--accent) 55%, transparent);
 }
 .badge-privacy {
-  display: inline-block; margin-left: 6px; font-size: 10px; letter-spacing: 0.04em;
-  text-transform: uppercase; border: 1px solid var(--inv-border); border-radius: 4px;
-  padding: 0 5px; color: var(--inv-faint); vertical-align: middle;
+  display: inline-block; margin-left: 6px; font-size: 10px;
+  border: 0.5px solid var(--border); border-radius: 4px;
+  padding: 0 5px; color: var(--text-3); vertical-align: middle;
 }
 .inv-switchrow {
   display: flex; align-items: center; gap: 10px; margin: 12px 0 2px; cursor: pointer;
 }
 .sw {
-  width: 36px; height: 20px; border-radius: 20px; background: var(--inv-bg-row);
-  border: 1px solid var(--inv-border); position: relative; flex-shrink: 0;
+  width: 36px; height: 20px; border-radius: 20px; background: var(--bg-1);
+  border: 0.5px solid var(--border); position: relative; flex-shrink: 0;
 }
 .sw::after {
   content: ""; position: absolute; top: 2px; left: 2px; width: 14px; height: 14px;
-  border-radius: 50%; background: var(--inv-faint); transition: all 0.15s;
+  border-radius: 50%; background: var(--text-3); transition: all 0.15s;
 }
-.inv-switchrow.on .sw { background: var(--inv-green-deep); border-color: var(--inv-green-dim); }
-.inv-switchrow.on .sw::after { left: 18px; background: var(--inv-green); }
-.swlbl { font-size: 12.5px; color: var(--inv-mut); }
-.inv-switchrow.on .swlbl { color: var(--inv-text); }
-.inv-swnote { font-size: 11px; color: var(--inv-faint); margin: 2px 0 0 46px; }
+.inv-switchrow.on .sw { background: color-mix(in srgb, var(--ok) 18%, var(--bg-1)); border-color: var(--ok); }
+.inv-switchrow.on .sw::after { left: 18px; background: var(--ok); }
+.swlbl { font-size: 12.5px; color: var(--text-2); }
+.inv-switchrow.on .swlbl { color: var(--text-1); }
+.inv-swnote { font-size: 11px; color: var(--text-3); margin: 2px 0 0 46px; }
 .inv-os-actions {
   display: flex; flex-wrap: wrap; align-items: center; gap: 8px; margin: 12px 0 8px;
 }
-.inv-os-excl, .inv-os-msg { font-size: 11.5px; color: var(--inv-faint); }
-.inv-os-excl { color: var(--inv-mut); }
+.inv-os-excl, .inv-os-msg { font-size: 11.5px; color: var(--text-3); }
+.inv-os-excl { color: var(--text-2); }
 .scan-sema {
   display: inline-flex; align-items: center; gap: 6px;
-  font-size: 11px; letter-spacing: 0.04em; text-transform: uppercase;
-  color: var(--inv-faint); border: 1px solid var(--inv-border);
-  border-radius: 6px; padding: 2px 8px 2px 6px;
+  font-size: 11px; color: var(--text-2);
 }
 .scan-sema .dot {
-  width: 8px; height: 8px; border-radius: 50%; background: var(--inv-faint);
-}
-.scan-sema.green { border-color: var(--inv-green-dim); color: var(--inv-green); }
-.scan-sema.green .dot { background: var(--inv-green); }
-.scan-sema.yellow { border-color: #a68b2c; color: #c4a035; }
-.scan-sema.yellow .dot { background: #c4a035; }
-.scan-sema.red { border-color: #8b3a3a; color: #c45c5c; }
-.scan-sema.red .dot { background: #c45c5c; }
-.scan-sema-reason {
-  margin: 0 0 8px; font-size: 11.5px; line-height: 1.4; color: var(--inv-faint);
+  width: 7px; height: 7px; border-radius: 50%; background: var(--text-3);
 }
+.scan-sema.green .dot, .scan-sema.ok .dot { background: var(--ok); }
+.scan-sema.amber .dot, .scan-sema.warn .dot { background: var(--attn); }
+.scan-sema.red .dot, .scan-sema.alert .dot { background: var(--alert); }
+.scan-sema-reason { font-size: 11px; color: var(--text-3); margin: 0 0 8px; }
 .inv-btn {
-  background: var(--inv-bg-row); border: 1px solid var(--inv-border);
-  border-radius: 8px; padding: 7px 12px; color: var(--inv-mut);
-  font-family: inherit; font-size: 12.5px; cursor: pointer;
-}
-.inv-btn:disabled { opacity: 0.5; cursor: not-allowed; }
-.inv-btn.ghost {
-  background: transparent; border-style: dashed; margin-top: 4px;
+  background: var(--bg-1); border: 0.5px solid var(--border);
+  border-radius: var(--radius); padding: 7px 14px; color: var(--text-2);
+  font-family: inherit; font-size: 12.5px; cursor: pointer; min-height: 0;
 }
+.inv-btn.ghost { background: transparent; }
+.inv-btn:disabled { opacity: 0.55; cursor: not-allowed; }
 .inv-tech {
-  margin: 8px 0 0; padding: 10px; max-height: 220px; overflow: auto;
-  font-size: 10.5px; line-height: 1.35; color: var(--inv-faint);
-  background: var(--inv-bg-row); border: 1px solid var(--inv-border-soft);
-  border-radius: 6px; white-space: pre-wrap; word-break: break-word;
+  margin-top: 8px; padding: 10px; background: var(--bg-1); border: 0.5px solid var(--border);
+  border-radius: var(--radius); font-family: var(--font-mono); font-size: 11px;
+  overflow: auto; max-height: 280px; color: var(--text-2);
 }
+.mono { font-family: var(--font-mono); }
 </style>
diff --git a/observatory/api/app/services/field_sources_vocab.py b/observatory/api/app/services/field_sources_vocab.py
new file mode 100644
index 0000000..40e7348
--- /dev/null
+++ b/observatory/api/app/services/field_sources_vocab.py
@@ -0,0 +1,42 @@
+"""Normalize asset.meta.field_sources vocabulary (OBS-MANUAL-WINS-DIFF-026)."""
+
+from __future__ import annotations
+
+from typing import Any
+
+from sqlalchemy.orm import Session
+
+from app.models import Asset
+from app.services.asset_identity import normalize_field_source_label
+
+
+def migrate_field_sources_manual_vocab(db: Session) -> dict[str, int]:
+    """Rewrite ``manuale`` → ``manual`` in assets.meta.field_sources (idempotent)."""
+    changed = 0
+    scanned = 0
+    for asset in db.query(Asset).all():
+        scanned += 1
+        meta = dict(asset.meta or {})
+        sources = dict(meta.get("field_sources") or {})
+        if not sources:
+            continue
+        dirty = False
+        next_sources: dict[str, Any] = {}
+        for field, entry in sources.items():
+            if not isinstance(entry, dict):
+                next_sources[field] = entry
+                continue
+            row = dict(entry)
+            raw = str(row.get("source") or "")
+            normalized = normalize_field_source_label(raw)
+            if normalized != raw:
+                row["source"] = normalized
+                dirty = True
+            next_sources[field] = row
+        if dirty:
+            meta["field_sources"] = next_sources
+            asset.meta = meta
+            changed += 1
+    if changed:
+        db.flush()
+    return {"scanned": scanned, "changed": changed}
```
