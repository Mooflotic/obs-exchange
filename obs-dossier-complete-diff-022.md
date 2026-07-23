<!-- BLOCK-ID: OBS-DOSSIER-COMPLETE-DIFF-022 -->

# OBS-DOSSIER-COMPLETE-DIFF-022 — Contesto destinazioni + Dossier autosufficiente

**VERSION:** bump **0.10.11** (pending deploy) · live resta `0.10.10`  
**STOP pre-deploy**  
**Nota:** `git add -N` sui file nuovi così compaiono in `git diff -U5`.

## Cosa

### Parte 1 — Contesto AI in Abitudini
1. **API:** `enrich_destination_names` riempie `dst_category` + `dst_context` da `ip_intel.context` (skip `non_deducibile`); `/habits` le espone per destinazione.
2. **UI:** `formatHabitsDestPrimary` — descrizione leggibile in evidenza; nome tecnico + IP solo in tooltip; fallback middle-ellipsis se manca contesto.

### Parte 2 — Dossier autosufficiente
1. **Estratti:** `AssetChassis.vue` (interfacce + presenza + first/last seen), `AssetDecide.vue` (Tu decidi + proposte + watch), `AssetNotes.vue` (notes editabili).
2. **`/dossier/:id`:** Chassis → Identity (OS protect) → Decide → Notes → Habits `wide`.
3. **Drawer Inventario:** riusa `AssetDecide` + `AssetNotes` (anteprima); CTA «Apri Dossier».

## Test
- `pytest tests/test_ip_intel.py` — 12 passed (incluso `test_habits_dst_context_from_ip_intel`)
- `node --test src/habitsUi.test.js` — 11 passed

## Diff (`git diff -U5`, include intent-to-add)

```diff
diff --git a/observatory/CHANGELOG.md b/observatory/CHANGELOG.md
index c04df7b..0759968 100644
--- a/observatory/CHANGELOG.md
+++ b/observatory/CHANGELOG.md
@@ -1,7 +1,12 @@
 # Changelog
 
+## 0.10.11 — pending deploy (STOP)
+
+- **Abitudini — contesto AI in UI (OBS-DOSSIER-COMPLETE-022):** `/habits` espone `dst_context` + `dst_category` da `ip_intel`; riga destinazione = descrizione leggibile in evidenza, nome tecnico+IP solo in tooltip (fallback middle-ellipsis se `non_deducibile`).
+- **Dossier autosufficiente:** `AssetChassis` / `AssetDecide` / `AssetNotes` estratti; `/dossier/:id` ha interfacce+presenza, Tu decidi (rinomina/adotta/ignora/watch), note editabili, Identity (OS protect) e Habits. Drawer Inventario riusa Decide/Notes (anteprima).
+
 ## 0.10.10 — 2026-07-23
 
 - **Dossier pagina piena + sidebar RADAR/MAPPA (OBS-DOSSIER-PAGE-021):** `AssetIdentity` / `AssetHabits` estratti (fetch autonomo, OS actions nel componente); `/dossier` hub + `/dossier/:id`; drawer Inventario = anteprima + Tu decidi + «Apri Dossier»; stub onesti Oggi/Osservatorio/Come funziona.
 
 ## 0.10.9 — 2026-07-23
diff --git a/observatory/VERSION b/observatory/VERSION
index ddf1d4a..223df19 100644
--- a/observatory/VERSION
+++ b/observatory/VERSION
@@ -1 +1 @@
-0.10.10
+0.10.11
diff --git a/observatory/api/app/services/habits.py b/observatory/api/app/services/habits.py
index 65fe4a3..ca145f9 100644
--- a/observatory/api/app/services/habits.py
+++ b/observatory/api/app/services/habits.py
@@ -436,10 +436,12 @@ def asset_habits(
 
     destinations = [
         {
             "dst_ip": (row["dst_ip"] or "").strip(),
             "dst_name": None,
+            "dst_category": None,
+            "dst_context": None,
             "bytes": int(row["bytes_total"] or 0),
             "bytes_out": _nullable_sum(row["bytes_out_sum"]),
             "bytes_in": _nullable_sum(row["bytes_in_sum"]),
             "samples": int(row["samples"] or 0),
             "samples_with_direction": int(row["samples_with_dir"] or 0),
diff --git a/observatory/api/app/services/ip_intel.py b/observatory/api/app/services/ip_intel.py
index 5027794..ebb9172 100644
--- a/observatory/api/app/services/ip_intel.py
+++ b/observatory/api/app/services/ip_intel.py
@@ -1,9 +1,6 @@
-"""Observed public IP → hostname (DNS / TLS SNI). Wave 1b naming.
-
-No AI context here — later wave adds columns on the same table.
-"""
+"""Observed public IP → hostname (DNS / TLS SNI) + optional AI context."""
 
 from __future__ import annotations
 
 import ipaddress
 from datetime import datetime, timedelta, timezone
@@ -148,10 +145,33 @@ def names_for_ips(db: Session, ips: Iterable[str]) -> dict[str, str]:
         return {}
     rows = db.scalars(select(IpIntel).where(IpIntel.ip.in_(wanted))).all()
     return {row.ip: row.name for row in rows if (row.name or "").strip()}
 
 
+def parse_stored_context(blob: str | None) -> tuple[Optional[str], Optional[str]]:
+    """Parse ip_intel.context → (category, what_it_is)."""
+    import re
+
+    text = (blob or "").strip()
+    if not text:
+        return None, None
+    m = re.match(r"^\[([^\]]+)\]\s*(.*?)\s*(?:\(conf=[0-9.]+\))?\s*$", text)
+    if not m:
+        return None, text
+    cat = (m.group(1) or "").strip() or None
+    what = (m.group(2) or "").strip() or None
+    return cat, what
+
+
+def intel_rows_for_ips(db: Session, ips: Iterable[str]) -> dict[str, IpIntel]:
+    wanted = sorted({(ip or "").strip() for ip in ips if is_public_ip(ip or "")})
+    if not wanted:
+        return {}
+    rows = db.scalars(select(IpIntel).where(IpIntel.ip.in_(wanted))).all()
+    return {row.ip: row for row in rows}
+
+
 def special_destination_label(ip: str, network_cidr: str | None = None) -> Optional[str]:
     """Label broadcast / multicast / reserved without DB lookup.
 
     Broadcast LAN is derived from ``network_cidr`` (not hardcoded).
     Returns None if the address should use normal naming (asset / ip_intel).
@@ -226,27 +246,40 @@ def enrich_destination_names(
     db: Session,
     destinations: list[dict[str, Any]],
     *,
     network_cidr: str | None = None,
 ) -> None:
-    """Fill dst_name in-place: specials → ip_intel (public) → asset (private)."""
+    """Fill dst_name / dst_category / dst_context in-place.
+
+    specials → ip_intel (public) → asset (private).
+    Context only when category is present and ≠ non_deducibile.
+    """
     if not destinations:
         return
     if network_cidr is None:
         from app.config import get_settings
 
         network_cidr = get_settings().network_cidr
     ips = [str(d.get("dst_ip") or "") for d in destinations]
-    public_names = names_for_ips(db, ips)
+    intel_by_ip = intel_rows_for_ips(db, ips)
     local_names = local_asset_names_for_ips(db, ips)
     for dest in destinations:
         ip = str(dest.get("dst_ip") or "").strip()
+        dest.setdefault("dst_name", None)
+        dest["dst_category"] = None
+        dest["dst_context"] = None
         if not ip:
             continue
         special = special_destination_label(ip, network_cidr)
         if special:
             dest["dst_name"] = special
             continue
         if is_public_ip(ip):
-            dest["dst_name"] = public_names.get(ip)
+            row = intel_by_ip.get(ip)
+            if row and (row.name or "").strip():
+                dest["dst_name"] = row.name.strip()
+            cat, what = parse_stored_context(getattr(row, "context", None) if row else None)
+            if cat and cat != "non_deducibile" and what:
+                dest["dst_category"] = cat
+                dest["dst_context"] = what
         else:
             dest["dst_name"] = local_names.get(ip)
diff --git a/observatory/tests/test_ip_intel.py b/observatory/tests/test_ip_intel.py
index 6317549..28310a4 100644
--- a/observatory/tests/test_ip_intel.py
+++ b/observatory/tests/test_ip_intel.py
@@ -303,10 +303,70 @@ def test_habits_dst_name_from_ip_intel(db):
     habits = asset_habits(db, asset.id, days=7, now=now + timedelta(hours=1))
     assert habits is not None
     by_ip = {d["dst_ip"]: d for d in habits["destinations"]}
     assert by_ip["93.184.216.34"]["dst_name"] == "www.example.com"
     assert by_ip["192.168.1.1"]["dst_name"] == "FritzBox"
+    assert by_ip["93.184.216.34"].get("dst_context") in (None, "")
+    assert by_ip["93.184.216.34"].get("dst_category") in (None, "")
+
+
+def test_habits_dst_context_from_ip_intel(db):
+    from app.models import IpIntel
+    from app.services.ip_intel_context import format_context_blob
+
+    now = datetime(2026, 7, 23, 12, 0, 0)
+    asset = upsert_observation_asset(
+        db,
+        mac="aa:bb:cc:dd:ee:02",
+        ip="192.168.1.51",
+        seen_at=now - timedelta(days=1),
+        source="test",
+    )
+    db.flush()
+    for iface in asset.interfaces:
+        for addr in iface.addresses:
+            addr.first_seen = now - timedelta(days=1)
+            addr.is_current = True
+    db.add(
+        FlowObservation(
+            dedup_key=str(uuid.uuid4()),
+            sensor_id="zeek-span",
+            src_ip="192.168.1.51",
+            dst_ip="93.184.216.34",
+            dst_port=443,
+            proto="tcp",
+            bytes=100,
+            bytes_out=40,
+            bytes_in=60,
+            observed_at=now,
+        )
+    )
+    upsert_ip_intel(
+        db,
+        ip="93.184.216.34",
+        name="a345.minerva.devices.a2z.com",
+        source="ssl",
+        confidence=0.95,
+        seen_at=now,
+    )
+    row = db.get(IpIntel, "93.184.216.34")
+    assert row is not None
+    row.context = format_context_blob(
+        {
+            "category": "iot",
+            "what_it_is": "Amazon Minerva IoT device service",
+            "confidence": 0.75,
+        }
+    )
+    row.context_source = "ai"
+    db.commit()
+
+    habits = asset_habits(db, asset.id, days=7, now=now + timedelta(hours=1))
+    dest = {d["dst_ip"]: d for d in habits["destinations"]}["93.184.216.34"]
+    assert dest["dst_name"] == "a345.minerva.devices.a2z.com"
+    assert dest["dst_category"] == "iot"
+    assert dest["dst_context"] == "Amazon Minerva IoT device service"
 
 
 def test_enrich_destination_names_public_only_table(db):
     dests = [
         {"dst_ip": "8.8.8.8", "dst_name": None},
diff --git a/observatory/web/package.json b/observatory/web/package.json
index d7029e8..84ad0d2 100644
--- a/observatory/web/package.json
+++ b/observatory/web/package.json
@@ -1,9 +1,9 @@
 {
   "name": "lan-observatory-web",
   "private": true,
-  "version": "0.10.10",
+  "version": "0.10.11",
   "type": "module",
   "scripts": {
     "dev": "vite",
     "build": "vite build",
     "preview": "vite preview",
diff --git a/observatory/web/src/components/AssetChassis.vue b/observatory/web/src/components/AssetChassis.vue
new file mode 100644
index 0000000..b572b44
--- /dev/null
+++ b/observatory/web/src/components/AssetChassis.vue
@@ -0,0 +1,137 @@
+<script setup>
+import { computed, ref, watch } from "vue";
+import { api } from "../api";
+import { composeDevices } from "../inventoryDevices";
+import { formatDate } from "../formatTime";
+
+const props = defineProps({
+  assetId: { type: [Number, String], required: true },
+});
+
+const loading = ref(false);
+const device = ref(null);
+const asset = ref(null);
+
+const numericId = computed(() => {
+  const n = Number(props.assetId);
+  return Number.isFinite(n) && n > 0 ? n : null;
+});
+
+const ifaces = computed(() => device.value?.ifaces || []);
+const firstSeen = computed(
+  () => device.value?.first_seen || asset.value?.first_seen || null,
+);
+const lastSeen = computed(
+  () => device.value?.last_seen || asset.value?.last_seen || null,
+);
+const presence = computed(() => {
+  if (device.value) return device.value.stale ? "non presente" : "presente";
+  return asset.value?.presence_state || "—";
+});
+const status = computed(() => asset.value?.status || device.value?.status || "—");
+
+function fmtSeen(iso) {
+  return formatDate(iso) || "—";
+}
+
+async function loadAll() {
+  const id = numericId.value;
+  if (!id) {
+    device.value = null;
+    asset.value = null;
+    return;
+  }
+  loading.value = true;
+  try {
+    const [row, chassis, assets] = await Promise.all([
+      api.asset(id),
+      api.chassis(),
+      api.assets({ include_historical: "true" }),
+    ]);
+    asset.value = row;
+    const devices = composeDevices(assets, chassis);
+    device.value =
+      devices.find(
+        (d) =>
+          d.primaryId === id ||
+          (d.members || []).some((m) => m.id === id) ||
+          d.key === `asset:${id}`,
+      ) || null;
+  } catch {
+    asset.value = null;
+    device.value = null;
+  } finally {
+    loading.value = false;
+  }
+}
+
+watch(
+  () => props.assetId,
+  () => loadAll(),
+  { immediate: true },
+);
+</script>
+
+<template>
+  <section class="asset-chassis inv-p-sec">
+    <div class="inv-p-seclabel"><span>Interfacce e presenza</span><span class="line" /></div>
+    <div v-if="loading" class="inv-p-note-sugg">caricamento…</div>
+    <template v-else>
+      <div class="inv-kv">
+        <span class="k">Presenza</span>
+        <span class="v">{{ presence }}</span>
+        <span class="k">Stato</span>
+        <span class="v">{{ status }}</span>
+        <span class="k">Prima volta</span>
+        <span class="v">{{ fmtSeen(firstSeen) }}</span>
+        <span class="k">Ultima volta</span>
+        <span class="v">{{ fmtSeen(lastSeen) }}</span>
+        <span class="k">Porta switch</span>
+        <span class="v">{{ device?.port || asset?.port_label || asset?.port || "—" }}</span>
+      </div>
+
+      <div class="inv-p-seclabel" style="margin-top: 14px">
+        <span>Interfacce · {{ ifaces.length || 1 }}</span><span class="line" />
+      </div>
+      <div v-if="!ifaces.length" class="inv-p-note-sugg">
+        {{ asset?.macs?.[0] || "—" }} · {{ asset?.ips?.[0] || "nessun IP" }}
+      </div>
+      <div v-for="(i, idx) in ifaces" :key="idx" class="inv-iface">
+        <div>
+          <span class="imac mono">{{ i.mac || "—" }}</span>
+          <span class="iname">{{ i.name || "iface" }} · {{ i.kind || "—" }}</span>
+        </div>
+        <div class="iip mono">
+          <template v-if="i.ip">{{ i.ip }}</template>
+          <span v-else class="none">— no IP</span>
+        </div>
+      </div>
+    </template>
+  </section>
+</template>
+
+<style scoped>
+.inv-p-sec { margin-top: 18px; }
+.inv-p-seclabel {
+  font-size: 11px; letter-spacing: 0.12em; text-transform: uppercase;
+  color: var(--inv-faint); margin-bottom: 9px;
+  display: flex; align-items: center; gap: 10px;
+}
+.inv-p-seclabel .line { flex: 1; height: 1px; background: var(--inv-border-soft); }
+.inv-p-note-sugg { font-size: 12.5px; color: var(--inv-faint); }
+.inv-kv {
+  display: grid; grid-template-columns: 108px 1fr; gap: 8px 10px;
+  font-size: 12.5px;
+}
+.inv-kv .k { color: var(--inv-faint); }
+.inv-kv .v { color: var(--inv-mut); word-break: break-all; }
+.inv-iface {
+  display: grid; grid-template-columns: 1fr auto; gap: 10px;
+  padding: 6px 0; border-bottom: 1px dashed var(--inv-border-soft); font-size: 12.5px;
+}
+.inv-iface .imac { color: var(--inv-mut); }
+.inv-iface .iname { color: var(--inv-faint); margin-left: 8px; }
+.inv-iface .iip { color: var(--inv-mut); text-align: right; }
+.inv-iface .none { color: var(--inv-faint); }
+.mono { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
+</style>
diff --git a/observatory/web/src/components/AssetDecide.vue b/observatory/web/src/components/AssetDecide.vue
new file mode 100644
index 0000000..2b8f698
--- /dev/null
+++ b/observatory/web/src/components/AssetDecide.vue
@@ -0,0 +1,306 @@
+<script setup>
+import { computed, ref, watch } from "vue";
+import { api } from "../api";
+import { bestNameHint, sourceLabel } from "../inventoryDevices";
+
+const props = defineProps({
+  assetId: { type: [Number, String], required: true },
+});
+const emit = defineEmits(["saved"]);
+
+const CATEGORIES = [
+  "infrastruttura",
+  "media",
+  "computer",
+  "domotica",
+  "stampante",
+  "unknown",
+];
+const STATUSES = ["noto", "nuovo", "ignorato"];
+
+const asset = ref(null);
+const form = ref(null);
+const loading = ref(false);
+const busy = ref(false);
+const msg = ref("");
+const savedFlash = ref(false);
+const aiNamingBusy = ref(false);
+
+const numericId = computed(() => {
+  const n = Number(props.assetId);
+  return Number.isFinite(n) && n > 0 ? n : null;
+});
+
+const proposals = computed(() => asset.value?.proposals || []);
+const hint = computed(() => (asset.value ? bestNameHint(asset.value) : ""));
+
+function catLabel(cat) {
+  if (cat === "infrastruttura") return "Infrastruttura";
+  if (!cat) return "";
+  return cat.charAt(0).toUpperCase() + cat.slice(1);
+}
+
+function confPct(c) {
+  const n = Number(c);
+  if (!Number.isFinite(n)) return "—";
+  return `${Math.round(n <= 1 ? n * 100 : n)}%`;
+}
+
+function formFromAsset(a) {
+  return {
+    name: a.name || "",
+    category: a.category || "unknown",
+    status: a.status || "nuovo",
+    os_guess: a.os_guess && a.os_guess !== "—" ? a.os_guess : "",
+    is_critical: !!a.is_critical,
+    watch_fingerprint: !!a.watch_fingerprint,
+  };
+}
+
+async function load() {
+  const id = numericId.value;
+  if (!id) {
+    asset.value = null;
+    form.value = null;
+    return;
+  }
+  loading.value = true;
+  msg.value = "";
+  try {
+    asset.value = await api.asset(id);
+    form.value = formFromAsset(asset.value);
+  } catch (e) {
+    asset.value = null;
+    form.value = null;
+    msg.value = e.message || "Asset non disponibile";
+  } finally {
+    loading.value = false;
+  }
+}
+
+async function save() {
+  const id = numericId.value;
+  if (!id || !form.value || busy.value) return;
+  busy.value = true;
+  msg.value = "";
+  try {
+    await api.updateAsset(id, {
+      name: form.value.name.trim(),
+      category: form.value.category,
+      status: form.value.status,
+      os_guess: form.value.os_guess.trim(),
+      is_critical: !!form.value.is_critical,
+      watch_fingerprint: !!form.value.watch_fingerprint,
+    });
+    savedFlash.value = true;
+    await load();
+    emit("saved");
+    setTimeout(() => {
+      savedFlash.value = false;
+    }, 800);
+  } catch (e) {
+    msg.value = e.message || String(e);
+  } finally {
+    busy.value = false;
+  }
+}
+
+async function adoptProposal(p) {
+  const id = numericId.value;
+  if (!id || busy.value) return;
+  busy.value = true;
+  try {
+    await api.adoptName(id, p.source);
+    await load();
+    emit("saved");
+  } catch (e) {
+    msg.value = e.message || String(e);
+  } finally {
+    busy.value = false;
+  }
+}
+
+async function proposeAiName() {
+  const id = numericId.value;
+  if (!id || aiNamingBusy.value) return;
+  aiNamingBusy.value = true;
+  msg.value = "";
+  try {
+    const result = await api.aiProposeName(id);
+    await load();
+    emit("saved");
+    if (result?.ok) {
+      msg.value = `Proposta AI: ${result.proposal?.value || "ok"}`;
+    } else {
+      msg.value = result?.error || "Proposta AI non disponibile";
+    }
+  } catch (e) {
+    msg.value = e.message || String(e);
+  } finally {
+    aiNamingBusy.value = false;
+  }
+}
+
+watch(
+  () => props.assetId,
+  () => load(),
+  { immediate: true },
+);
+</script>
+
+<template>
+  <section class="asset-decide inv-p-sec">
+    <div class="inv-p-seclabel you"><span>Tu decidi</span><span class="line" /></div>
+    <div v-if="loading" class="inv-p-note-sugg">caricamento…</div>
+    <template v-else-if="form">
+      <div class="inv-frow">
+        <label>Nome</label>
+        <input v-model="form.name" type="text" :placeholder="hint || ''" />
+      </div>
+      <div class="inv-frow">
+        <label>Categoria</label>
+        <select v-model="form.category">
+          <option v-for="c in CATEGORIES" :key="c" :value="c">{{ catLabel(c) }}</option>
+        </select>
+      </div>
+      <div class="inv-frow">
+        <label>Stato</label>
+        <select v-model="form.status">
+          <option v-for="s in STATUSES" :key="s" :value="s">{{ s }}</option>
+        </select>
+      </div>
+      <div class="inv-frow">
+        <label>OS</label>
+        <input v-model="form.os_guess" type="text" placeholder="—" />
+      </div>
+      <div
+        class="inv-switchrow"
+        :class="{ on: form.is_critical }"
+        @click="form.is_critical = !form.is_critical"
+      >
+        <span class="sw" /><span class="swlbl">Dispositivo critico</span>
+      </div>
+      <div class="inv-swnote">attivo → grafico uptime nel Monitor (ping nativo)</div>
+      <div
+        class="inv-switchrow"
+        :class="{ on: form.watch_fingerprint }"
+        @click="form.watch_fingerprint = !form.watch_fingerprint"
+      >
+        <span class="sw" /><span class="swlbl">Watch + fingerprint all'avvistamento</span>
+      </div>
+      <div class="inv-swnote">
+        all'avvistamento accoda OS fingerprint prioritario; nessun blocco
+      </div>
+
+      <div class="decide-actions">
+        <button type="button" class="inv-btn primary" :disabled="busy" @click="save">
+          Salva
+        </button>
+        <span class="inv-saved" :class="{ show: savedFlash }">Salvato ✓</span>
+      </div>
+
+      <div class="inv-p-seclabel" style="margin-top: 18px">
+        <span>Suggerito</span><span class="line" />
+      </div>
+      <div v-if="!proposals.length" class="inv-p-note-sugg">— nessuna proposta ancora</div>
+      <div
+        v-for="(p, i) in proposals"
+        :key="i"
+        class="inv-prop"
+        :class="{ 'is-ai': (p.source || '').toLowerCase() === 'ai' }"
+      >
+        <span class="src" :class="{ ai: (p.source || '').toLowerCase() === 'ai' }">{{ sourceLabel(p.source) }}</span>
+        <span class="val">{{ p.value }}</span>
+        <span class="conf">{{ confPct(p.confidence) }}</span>
+        <button type="button" class="adopt" :disabled="busy" @click="adoptProposal(p)">Adotta</button>
+        <div v-if="p.evidence" class="inv-prop-ev">{{ p.evidence }}</div>
+      </div>
+      <button
+        type="button"
+        class="inv-btn ai-name"
+        :disabled="busy || aiNamingBusy"
+        @click="proposeAiName"
+      >
+        <span v-if="aiNamingBusy" class="spin" aria-hidden="true" />
+        {{ aiNamingBusy ? "Proposta in corso…" : "Proponi nome (AI)" }}
+      </button>
+      <p v-if="msg" class="decide-msg">{{ msg }}</p>
+    </template>
+    <div v-else class="inv-p-note-sugg">— decisioni non disponibili</div>
+  </section>
+</template>
+
+<style scoped>
+.inv-p-sec { margin-top: 18px; }
+.inv-p-seclabel {
+  font-size: 11px; letter-spacing: 0.12em; text-transform: uppercase;
+  color: var(--inv-faint); margin-bottom: 9px;
+  display: flex; align-items: center; gap: 10px;
+}
+.inv-p-seclabel.you { color: var(--inv-green); }
+.inv-p-seclabel .line { flex: 1; height: 1px; background: var(--inv-border-soft); }
+.inv-p-note-sugg { font-size: 12.5px; color: var(--inv-faint); }
+.inv-frow {
+  display: grid; grid-template-columns: 108px 1fr; gap: 10px;
+  align-items: center; margin-bottom: 8px;
+}
+.inv-frow label { font-size: 12px; color: var(--inv-mut); }
+.inv-frow input, .inv-frow select {
+  background: var(--inv-bg-row); border: 1px solid var(--inv-border); border-radius: 8px;
+  padding: 7px 10px; color: var(--inv-text); font-family: inherit; font-size: 13px; width: 100%;
+}
+.inv-switchrow {
+  display: flex; align-items: center; gap: 10px; margin: 12px 0 2px; cursor: pointer;
+}
+.sw {
+  width: 36px; height: 20px; border-radius: 20px; background: var(--inv-bg-row);
+  border: 1px solid var(--inv-border); position: relative; flex-shrink: 0;
+}
+.sw::after {
+  content: ""; position: absolute; top: 2px; left: 2px; width: 14px; height: 14px;
+  border-radius: 50%; background: var(--inv-faint); transition: all 0.15s;
+}
+.inv-switchrow.on .sw { background: var(--inv-green-deep); border-color: var(--inv-green-dim); }
+.inv-switchrow.on .sw::after { left: 18px; background: var(--inv-green); }
+.swlbl { font-size: 12.5px; color: var(--inv-mut); }
+.inv-switchrow.on .swlbl { color: var(--inv-text); }
+.inv-swnote { font-size: 11px; color: var(--inv-faint); margin: 2px 0 0 46px; }
+.decide-actions { display: flex; align-items: center; gap: 12px; margin-top: 14px; }
+.inv-btn {
+  background: var(--inv-bg-row); border: 1px solid var(--inv-border);
+  border-radius: 8px; padding: 7px 14px; color: var(--inv-mut);
+  font-family: inherit; font-size: 12.5px; cursor: pointer;
+}
+.inv-btn.primary { background: var(--inv-green-deep); border-color: var(--inv-green-dim); color: var(--inv-green); }
+.inv-btn:disabled { opacity: 0.55; cursor: not-allowed; }
+.inv-saved { font-size: 12px; color: var(--inv-green); opacity: 0; transition: opacity 0.2s; }
+.inv-saved.show { opacity: 1; }
+.inv-prop {
+  display: flex; align-items: center; gap: 10px; padding: 7px 0;
+  border-bottom: 1px dashed var(--inv-border-soft); font-size: 12.5px; flex-wrap: wrap;
+}
+.inv-prop .src {
+  font-size: 10px; text-transform: uppercase; border: 1px solid var(--inv-border);
+  border-radius: 5px; padding: 1px 6px; color: var(--inv-faint);
+}
+.inv-prop .src.ai { color: #c4a0ff; border-color: #6b4aa8; background: #1a1228; }
+.inv-prop .val { flex: 1; color: var(--inv-text); }
+.inv-prop .conf { font-size: 11px; color: var(--inv-faint); }
+.inv-prop .adopt {
+  background: none; border: 1px solid var(--inv-green-dim); color: var(--inv-green);
+  border-radius: 7px; padding: 3px 11px; font-family: inherit; font-size: 11.5px; cursor: pointer;
+}
+.inv-prop-ev {
+  flex: 1 1 100%; margin: -2px 0 4px 0; font-size: 11px; color: var(--inv-mut);
+}
+.inv-btn.ai-name {
+  margin-top: 10px; display: inline-flex; align-items: center; gap: 8px;
+  border-color: #6b4aa8; color: #c4a0ff;
+}
+.spin {
+  width: 12px; height: 12px; border: 2px solid #6b4aa8; border-top-color: #c4a0ff;
+  border-radius: 50%; display: inline-block; animation: spin 0.7s linear infinite;
+}
+@keyframes spin { to { transform: rotate(360deg); } }
+.decide-msg { margin: 8px 0 0; font-size: 12px; color: var(--inv-green); }
+</style>
diff --git a/observatory/web/src/components/AssetHabits.vue b/observatory/web/src/components/AssetHabits.vue
index 29ac291..3e1e9b5 100644
--- a/observatory/web/src/components/AssetHabits.vue
+++ b/observatory/web/src/components/AssetHabits.vue
@@ -8,11 +8,11 @@ import {
   formatBytes,
   formatDirPair,
   hourTooltip,
   hoursToLocalBins,
   isEmptySilenceKind,
-  formatHabitsDestName,
+  formatHabitsDestPrimary,
   portChipLabel,
   provenanceLine,
   showDirectionBars,
   sparklineHeights,
   visibleDestinations,
@@ -119,15 +119,14 @@ watch(
             :key="d.dst_ip"
             class="habits-dst"
           >
             <div class="habits-dst-id">
               <span
-                v-if="d.dst_name"
-                class="habits-dst-name"
-                :title="formatHabitsDestName(d.dst_name).full"
-              >{{ formatHabitsDestName(d.dst_name).display }}</span>
-              <span class="habits-dst-ip mono">{{ d.dst_ip }}</span>
+                class="habits-dst-primary"
+                :class="{ context: formatHabitsDestPrimary(d).kind === 'context' }"
+                :title="formatHabitsDestPrimary(d).title"
+              >{{ formatHabitsDestPrimary(d).primary }}</span>
             </div>
             <div class="habits-dst-dir">
               <template v-if="showBars && directionSplit(d)">
                 <span class="habits-dir-lbl out">out</span>
                 <div class="habits-bar" aria-hidden="true">
@@ -254,10 +253,16 @@ watch(
 .wide .habits-dst {
   grid-template-columns: minmax(12rem, 1.1fr) minmax(0, 1.6fr);
   gap: 8px 16px; padding: 8px 0; font-size: 13px;
 }
 .habits-dst-id { min-width: 0; display: flex; flex-direction: column; gap: 1px; }
+.habits-dst-primary {
+  font-size: 12px; color: var(--inv-text); white-space: nowrap; overflow: visible;
+  cursor: default;
+}
+.habits-dst-primary.context { font-weight: 500; }
+.wide .habits-dst-primary { font-size: 13.5px; }
 .habits-dst-name {
   font-size: 11px; color: var(--inv-text); white-space: nowrap; overflow: visible;
 }
 .wide .habits-dst-name { font-size: 12.5px; }
 .habits-dst-ip { color: var(--inv-mut); font-size: 12px; }
diff --git a/observatory/web/src/components/AssetNotes.vue b/observatory/web/src/components/AssetNotes.vue
new file mode 100644
index 0000000..448aec0
--- /dev/null
+++ b/observatory/web/src/components/AssetNotes.vue
@@ -0,0 +1,111 @@
+<script setup>
+import { computed, ref, watch } from "vue";
+import { api } from "../api";
+
+const props = defineProps({
+  assetId: { type: [Number, String], required: true },
+});
+const emit = defineEmits(["saved"]);
+
+const notes = ref("");
+const loading = ref(false);
+const busy = ref(false);
+const msg = ref("");
+const savedFlash = ref(false);
+
+const numericId = computed(() => {
+  const n = Number(props.assetId);
+  return Number.isFinite(n) && n > 0 ? n : null;
+});
+
+async function load() {
+  const id = numericId.value;
+  if (!id) {
+    notes.value = "";
+    return;
+  }
+  loading.value = true;
+  try {
+    const a = await api.asset(id);
+    notes.value = a.notes || "";
+  } catch {
+    notes.value = "";
+  } finally {
+    loading.value = false;
+  }
+}
+
+async function save() {
+  const id = numericId.value;
+  if (!id || busy.value) return;
+  busy.value = true;
+  msg.value = "";
+  try {
+    await api.updateAsset(id, { notes: notes.value });
+    savedFlash.value = true;
+    emit("saved");
+    setTimeout(() => {
+      savedFlash.value = false;
+    }, 800);
+  } catch (e) {
+    msg.value = e.message || String(e);
+  } finally {
+    busy.value = false;
+  }
+}
+
+watch(
+  () => props.assetId,
+  () => load(),
+  { immediate: true },
+);
+</script>
+
+<template>
+  <section class="asset-notes inv-p-sec">
+    <div class="inv-p-seclabel"><span>Note</span><span class="line" /></div>
+    <div v-if="loading" class="inv-p-note-sugg">caricamento…</div>
+    <template v-else>
+      <textarea
+        v-model="notes"
+        class="inv-notes"
+        placeholder="appunti su questo device…"
+      />
+      <div class="notes-actions">
+        <button type="button" class="inv-btn primary" :disabled="busy" @click="save">
+          Salva note
+        </button>
+        <span class="inv-saved" :class="{ show: savedFlash }">Salvato ✓</span>
+      </div>
+      <p v-if="msg" class="notes-msg">{{ msg }}</p>
+    </template>
+  </section>
+</template>
+
+<style scoped>
+.inv-p-sec { margin-top: 18px; }
+.inv-p-seclabel {
+  font-size: 11px; letter-spacing: 0.12em; text-transform: uppercase;
+  color: var(--inv-faint); margin-bottom: 9px;
+  display: flex; align-items: center; gap: 10px;
+}
+.inv-p-seclabel .line { flex: 1; height: 1px; background: var(--inv-border-soft); }
+.inv-p-note-sugg { font-size: 12.5px; color: var(--inv-faint); }
+.inv-notes {
+  width: 100%; min-height: 72px; box-sizing: border-box;
+  background: var(--inv-bg-row); border: 1px solid var(--inv-border);
+  border-radius: 8px; padding: 8px 10px; color: var(--inv-text);
+  font-family: inherit; font-size: 12.5px; resize: vertical;
+}
+.notes-actions { display: flex; align-items: center; gap: 12px; margin-top: 8px; }
+.inv-btn {
+  background: var(--inv-bg-row); border: 1px solid var(--inv-border);
+  border-radius: 8px; padding: 7px 14px; color: var(--inv-mut);
+  font-family: inherit; font-size: 12.5px; cursor: pointer;
+}
+.inv-btn.primary { background: var(--inv-green-deep); border-color: var(--inv-green-dim); color: var(--inv-green); }
+.inv-btn:disabled { opacity: 0.55; cursor: not-allowed; }
+.inv-saved { font-size: 12px; color: var(--inv-green); opacity: 0; transition: opacity 0.2s; }
+.inv-saved.show { opacity: 1; }
+.notes-msg { margin: 6px 0 0; font-size: 12px; color: #c45c5c; }
+</style>
diff --git a/observatory/web/src/habitsUi.js b/observatory/web/src/habitsUi.js
index b3bd530..ed9b595 100644
--- a/observatory/web/src/habitsUi.js
+++ b/observatory/web/src/habitsUi.js
@@ -190,5 +190,34 @@ export function middleEllipsis(text, maxLen = 40) {
 export function formatHabitsDestName(name, maxLen = 40) {
   const full = String(name || "").trim();
   if (!full) return { display: "", full: "" };
   return { display: middleEllipsis(full, maxLen), full };
 }
+
+/**
+ * Primary label for a destination row (Wave 1c context in UI).
+ * Prefer readable dst_context; fall back to middle-ellipsis name.
+ * Tooltip = full technical name · IP.
+ */
+export function formatHabitsDestPrimary(dest, maxLen = 40) {
+  const ip = String(dest?.dst_ip || "").trim();
+  const name = String(dest?.dst_name || "").trim();
+  const cat = String(dest?.dst_category || "").trim();
+  const ctx = String(dest?.dst_context || "").trim();
+  const tooltipParts = [];
+  if (name) tooltipParts.push(name);
+  if (ip) tooltipParts.push(ip);
+  const title = tooltipParts.join(" · ") || ip || "";
+
+  const ctxOk =
+    ctx &&
+    ctx.toLowerCase() !== "non deducibile" &&
+    cat &&
+    cat !== "non_deducibile";
+  if (ctxOk) {
+    return { primary: ctx, title, kind: "context" };
+  }
+  if (name) {
+    return { primary: middleEllipsis(name, maxLen), title, kind: "name" };
+  }
+  return { primary: ip || "—", title, kind: "ip" };
+}
diff --git a/observatory/web/src/habitsUi.test.js b/observatory/web/src/habitsUi.test.js
index 0268bc9..ebf7495 100644
--- a/observatory/web/src/habitsUi.test.js
+++ b/observatory/web/src/habitsUi.test.js
@@ -14,10 +14,11 @@ import {
   sparklineHeights,
   visibleDestinations,
   visiblePorts,
   middleEllipsis,
   formatHabitsDestName,
+  formatHabitsDestPrimary,
 } from "./habitsUi.js";
 
 test("empty_kind testi esatti §7", () => {
   assert.equal(
     emptyKindMessage("silence_observed"),
@@ -122,5 +123,27 @@ test("middleEllipsis preserva coda (dominio)", () => {
   const tencent = "conf-eu-1316693915.cos.ap-singapore.myqcloud.tencentcos.com";
   const tShort = middleEllipsis(tencent, 40);
   assert.match(tShort, /tencentcos\.com$/);
   assert.match(tShort, /…/);
 });
+
+test("formatHabitsDestPrimary preferisce contesto leggibile", () => {
+  const withCtx = formatHabitsDestPrimary({
+    dst_ip: "1.2.3.4",
+    dst_name: "a345.minerva.devices.a2z.com",
+    dst_category: "iot",
+    dst_context: "Amazon Minerva IoT device service",
+  });
+  assert.equal(withCtx.kind, "context");
+  assert.equal(withCtx.primary, "Amazon Minerva IoT device service");
+  assert.match(withCtx.title, /a345\.minerva/);
+  assert.match(withCtx.title, /1\.2\.3\.4/);
+
+  const noCtx = formatHabitsDestPrimary({
+    dst_ip: "1.2.3.4",
+    dst_name: "a345.minerva.devices.a2z.com",
+    dst_category: "non_deducibile",
+    dst_context: "non deducibile",
+  });
+  assert.equal(noCtx.kind, "name");
+  assert.match(noCtx.primary, /…|a345/);
+});
diff --git a/observatory/web/src/views/Dossier.vue b/observatory/web/src/views/Dossier.vue
index a299fcc..3041bdb 100644
--- a/observatory/web/src/views/Dossier.vue
+++ b/observatory/web/src/views/Dossier.vue
@@ -4,11 +4,14 @@ import { useRoute, useRouter } from "vue-router";
 import { api } from "../api";
 import { matchDeviceSearch, composeDevices } from "../inventoryDevices";
 import { formatFreshLabel, freshClass } from "../inventoryDevices";
 import { pushRecentDossier, readRecentDossiers } from "../dossierRecent";
 import PageHeader from "../components/PageHeader.vue";
+import AssetChassis from "../components/AssetChassis.vue";
 import AssetIdentity from "../components/AssetIdentity.vue";
+import AssetDecide from "../components/AssetDecide.vue";
+import AssetNotes from "../components/AssetNotes.vue";
 import AssetHabits from "../components/AssetHabits.vue";
 
 const route = useRoute();
 const router = useRouter();
 
@@ -199,11 +202,14 @@ onMounted(() => {
           <button type="button" class="dossier-btn" @click="goTopology">Topologia</button>
         </div>
       </div>
       <p v-if="error" class="dossier-err">{{ error }}</p>
       <template v-else-if="assetId">
+        <AssetChassis :asset-id="assetId" />
         <AssetIdentity :asset-id="assetId" />
+        <AssetDecide :asset-id="assetId" @saved="loadAsset(assetId)" />
+        <AssetNotes :asset-id="assetId" @saved="loadAsset(assetId)" />
         <AssetHabits :asset-id="assetId" wide />
       </template>
     </template>
   </div>
 </template>
diff --git a/observatory/web/src/views/Inventory.vue b/observatory/web/src/views/Inventory.vue
index f62b25c..a6d5c7a 100644
--- a/observatory/web/src/views/Inventory.vue
+++ b/observatory/web/src/views/Inventory.vue
@@ -1,11 +1,10 @@
 <script setup>
 import { computed, onMounted, onUnmounted, ref, watch } from "vue";
 import { useRoute, useRouter } from "vue-router";
 import { api } from "../api";
 import {
-  bestNameHint,
   composeDevices,
   countDevices,
   formatFreshLabel,
   freshClass,
   identitySources,
@@ -15,10 +14,12 @@ import {
   pathHops,
   sourceLabel,
 } from "../inventoryDevices";
 import { formatDate } from "../formatTime";
 import PageHeader from "../components/PageHeader.vue";
+import AssetDecide from "../components/AssetDecide.vue";
+import AssetNotes from "../components/AssetNotes.vue";
 
 const route = useRoute();
 const router = useRouter();
 const assets = ref([]);
 const chassisPayload = ref({ chassis: [] });
@@ -28,26 +29,14 @@ const view = ref("active"); // active | stale | all | new
 const filter = ref("all");
 const q = ref("");
 const staleOpen = ref(false);
 const panelOpen = ref(false);
 const selected = ref(null);
-const form = ref(null);
-const savedFlash = ref(false);
 const msg = ref("");
 const busy = ref(false);
 const loading = ref(true);
 
-const CATEGORIES = [
-  "infrastruttura",
-  "media",
-  "computer",
-  "domotica",
-  "stampante",
-  "unknown",
-];
-const STATUSES = ["noto", "nuovo", "ignorato"];
-
 const counts = computed(() => countDevices(devices.value));
 
 const activeRows = computed(() =>
   devices.value
     .filter((d) => (view.value === "new" ? isNuovoDaConoscere(d) : !d.stale))
@@ -67,17 +56,13 @@ const showStale = computed(() => view.value === "stale" || view.value === "all")
 
 const panelIdentity = computed(() =>
   selected.value ? identitySources(selected.value) : { sources: {}, bestKey: null },
 );
 const panelHops = computed(() => (selected.value ? pathHops(selected.value) : []));
-const panelHint = computed(() => (selected.value ? bestNameHint(selected.value) : ""));
-const panelProposals = computed(() => selected.value?.proposals || []);
 const panelFacts = computed(() => selected.value?.fingerprint_facts || []);
 const panelIpBindings = computed(() => selected.value?.ip_bindings || []);
 
-const aiNamingBusy = ref(false);
-
 const IP_ROLES = [
   { value: "", label: "—" },
   { value: "vpn", label: "vpn" },
   { value: "mgmt", label: "mgmt" },
   { value: "servizio", label: "servizio" },
@@ -118,28 +103,12 @@ function applyRouteView() {
 
 function setFilter(f) {
   filter.value = f;
 }
 
-function catLabel(cat) {
-  if (cat === "infrastruttura") return "Infrastruttura";
-  if (!cat) return "";
-  return cat.charAt(0).toUpperCase() + cat.slice(1);
-}
-
 function openPanel(device) {
   selected.value = device;
-  form.value = {
-    name: device.name || "",
-    category: device.category || "unknown",
-    status: device.status || "nuovo",
-    os_guess: device.os_guess && device.os_guess !== "—" ? device.os_guess : "",
-    patch: device.patch || "",
-    is_critical: !!device.is_critical,
-    watch_fingerprint: !!device.watch_fingerprint,
-    notes: device.notes || "",
-  };
   panelOpen.value = true;
   document.body.classList.add("panel-open");
 }
 
 function openDossierFromPanel() {
@@ -150,11 +119,10 @@ function openDossierFromPanel() {
 }
 
 function closePanel() {
   panelOpen.value = false;
   selected.value = null;
-  form.value = null;
   document.body.classList.remove("panel-open");
 }
 
 function onKey(e) {
   if (e.key === "Escape" && panelOpen.value) closePanel();
@@ -173,70 +141,19 @@ function confPct(c) {
   const n = Number(c);
   if (!Number.isFinite(n)) return "—";
   return `${Math.round(n <= 1 ? n * 100 : n)}%`;
 }
 
-async function savePanel() {
-  if (!selected.value || !form.value) return;
-  busy.value = true;
-  try {
-    const id = selected.value.primaryId;
-    await api.updateAsset(id, {
-      name: form.value.name.trim(),
-      category: form.value.category,
-      status: form.value.status,
-      os_guess: form.value.os_guess.trim(),
-      notes: form.value.notes,
-      is_critical: !!form.value.is_critical,
-      watch_fingerprint: !!form.value.watch_fingerprint,
-    });
-    savedFlash.value = true;
-    await load();
-    // Refresh selected row from new devices without full page reload.
-    const next = composeDevices(assets.value, chassisPayload.value).find(
-      (d) => d.key === selected.value.key || d.primaryId === id,
-    );
-    if (next) {
-      selected.value = next;
-      form.value.name = next.name || "";
-      form.value.watch_fingerprint = !!next.watch_fingerprint;
-      form.value.is_critical = !!next.is_critical;
-    }
-    setTimeout(() => {
-      savedFlash.value = false;
-      closePanel();
-    }, 600);
-  } catch (e) {
-    msg.value = e.message || String(e);
-  } finally {
-    busy.value = false;
-  }
-}
-
-async function adoptProposal(p) {
-  if (!selected.value || !p?.source) return;
-  busy.value = true;
-  try {
-    await api.adoptName(selected.value.primaryId, p.source);
-    await load();
-    const id = selected.value.primaryId;
-    const next = composeDevices(assets.value, chassisPayload.value).find(
-      (d) => d.primaryId === id || d.key === selected.value.key,
-    );
-    if (next) {
-      selected.value = next;
-      form.value = {
-        ...form.value,
-        name: next.name || form.value.name,
-      };
-    }
-    msg.value = "Nome adottato";
-  } catch (e) {
-    msg.value = e.message || String(e);
-  } finally {
-    busy.value = false;
-  }
+async function refreshSelected() {
+  await load();
+  const id = selected.value?.primaryId;
+  const key = selected.value?.key;
+  if (!id && !key) return;
+  const next = composeDevices(assets.value, chassisPayload.value).find(
+    (d) => d.primaryId === id || d.key === key,
+  );
+  if (next) selected.value = next;
 }
 
 async function adoptFact(f) {
   if (!selected.value || !f?.id) return;
   if (f.kind !== "device_class" && f.kind !== "os") {
@@ -244,23 +161,11 @@ async function adoptFact(f) {
     return;
   }
   busy.value = true;
   try {
     await api.adoptFingerprint(selected.value.primaryId, f.id);
-    await load();
-    const id = selected.value.primaryId;
-    const next = composeDevices(assets.value, chassisPayload.value).find(
-      (d) => d.primaryId === id || d.key === selected.value.key,
-    );
-    if (next) {
-      selected.value = next;
-      form.value = {
-        ...form.value,
-        category: next.category || form.value.category,
-        os_guess: next.os_guess || form.value.os_guess,
-      };
-    }
+    await refreshSelected();
     msg.value = f.kind === "os" ? "OS adottato" : "Categoria adottata";
   } catch (e) {
     msg.value = e.message || String(e);
   } finally {
     busy.value = false;
@@ -272,16 +177,11 @@ async function setBindingRole(binding, role) {
   const nextRole = role == null ? "" : String(role);
   if ((binding.role || "") === nextRole) return;
   busy.value = true;
   try {
     await api.setIpRole(selected.value.primaryId, binding.ip, nextRole);
-    await load();
-    const id = selected.value.primaryId;
-    const next = composeDevices(assets.value, chassisPayload.value).find(
-      (d) => d.primaryId === id || d.key === selected.value.key,
-    );
-    if (next) selected.value = next;
+    await refreshSelected();
     msg.value = `Ruolo ${binding.ip} → ${roleLabel(nextRole)}`;
   } catch (e) {
     msg.value = e.message || String(e);
   } finally {
     busy.value = false;
@@ -294,34 +194,10 @@ function factKindLabel(kind) {
   if (kind === "model") return "Modello";
   if (kind === "ssdp_type") return "SSDP";
   return kind || "fact";
 }
 
-async function proposeAiName() {
-  if (!selected.value) return;
-  aiNamingBusy.value = true;
-  msg.value = "";
-  try {
-    const result = await api.aiProposeName(selected.value.primaryId);
-    await load();
-    const id = selected.value.primaryId;
-    const next = composeDevices(assets.value, chassisPayload.value).find(
-      (d) => d.primaryId === id || d.key === selected.value.key,
-    );
-    if (next) selected.value = next;
-    if (result?.ok) {
-      msg.value = `Proposta AI: ${result.proposal?.value || "ok"}`;
-    } else {
-      msg.value = result?.error || "Proposta AI non disponibile";
-    }
-  } catch (e) {
-    msg.value = e.message || String(e);
-  } finally {
-    aiNamingBusy.value = false;
-  }
-}
-
 function goTopology() {
   if (!selected.value) return;
   router.push({ path: "/topology", query: { asset_id: String(selected.value.primaryId) } });
 }
 
@@ -535,11 +411,11 @@ onUnmounted(() => {
       class="inv-panel"
       :class="{ open: panelOpen }"
       role="dialog"
       aria-modal="true"
     >
-      <template v-if="selected && form">
+      <template v-if="selected">
         <div class="inv-p-head">
           <div class="inv-p-title">
             <div
               class="inv-p-name"
               :class="{ unnamed: !selected.name }"
@@ -564,64 +440,18 @@ onUnmounted(() => {
           <div class="inv-p-sec inv-dossier-cta">
             <button type="button" class="inv-btn primary dossier-open" @click="openDossierFromPanel">
               Apri Dossier
             </button>
             <p class="inv-swnote inv-dossier-hint">
-              identità completa e abitudini di traffico → pagina piena
+              quadro completo: interfacce, decisioni, note, abitudini → pagina piena
             </p>
           </div>
 
-          <div class="inv-p-sec">
-            <div class="inv-p-seclabel you"><span>Tu decidi</span><span class="line" /></div>
-            <div class="inv-frow">
-              <label>Nome</label>
-              <input v-model="form.name" type="text" :placeholder="selected.name ? '' : panelHint" />
-            </div>
-            <div class="inv-frow">
-              <label>Categoria</label>
-              <select v-model="form.category">
-                <option v-for="c in CATEGORIES" :key="c" :value="c">{{ catLabel(c) }}</option>
-              </select>
-            </div>
-            <div class="inv-frow">
-              <label>Stato</label>
-              <select v-model="form.status">
-                <option v-for="s in STATUSES" :key="s" :value="s">{{ s }}</option>
-              </select>
-            </div>
-            <div class="inv-frow">
-              <label>OS</label>
-              <input v-model="form.os_guess" type="text" placeholder="—" />
-            </div>
-            <div class="inv-frow">
-              <label>Porta patch</label>
-              <input
-                v-model="form.patch"
-                type="text"
-                placeholder="es. PP-A 12"
-                title="Il codice patch vive sulla porta switch; qui è informativo"
-              />
-            </div>
-            <div
-              class="inv-switchrow"
-              :class="{ on: form.is_critical }"
-              @click="form.is_critical = !form.is_critical"
-            >
-              <span class="sw" /><span class="swlbl">Dispositivo critico</span>
-            </div>
-            <div class="inv-swnote">attivo → grafico uptime nel Monitor (ping nativo)</div>
-            <div
-              class="inv-switchrow"
-              :class="{ on: form.watch_fingerprint }"
-              @click="form.watch_fingerprint = !form.watch_fingerprint"
-            >
-              <span class="sw" /><span class="swlbl">Watch + fingerprint all'avvistamento</span>
-            </div>
-            <div class="inv-swnote">
-              all'avvistamento accoda OS fingerprint prioritario; nessun blocco
-            </div>
-          </div>
+          <AssetDecide
+            :asset-id="selected.primaryId"
+            @saved="refreshSelected"
+          />
 
           <div class="inv-p-sec">
             <div class="inv-p-seclabel"><span>Indirizzi IP</span><span class="line" /></div>
             <div v-if="!panelIpBindings.length" class="inv-p-note-sugg">— nessun binding IP</div>
             <div
@@ -701,36 +531,10 @@ onUnmounted(() => {
               </template>
             </div>
             <button type="button" class="inv-btn" @click="goTopology">Vedi in topologia</button>
           </div>
 
-          <div class="inv-p-sec">
-            <div class="inv-p-seclabel"><span>Suggerito · cosa potrebbe essere</span><span class="line" /></div>
-            <div v-if="!panelProposals.length" class="inv-p-note-sugg">— nessuna proposta ancora</div>
-            <div
-              v-for="(p, i) in panelProposals"
-              :key="i"
-              class="inv-prop"
-              :class="{ 'is-ai': (p.source || '').toLowerCase() === 'ai' }"
-            >
-              <span class="src" :class="{ ai: (p.source || '').toLowerCase() === 'ai' }">{{ sourceLabel(p.source) }}</span>
-              <span class="val">{{ p.value }}</span>
-              <span class="conf">{{ confPct(p.confidence) }}</span>
-              <button type="button" class="adopt" :disabled="busy" @click="adoptProposal(p)">Adotta</button>
-              <div v-if="p.evidence" class="inv-prop-ev">{{ p.evidence }}</div>
-            </div>
-            <button
-              type="button"
-              class="inv-btn ai-name"
-              :disabled="busy || aiNamingBusy"
-              @click="proposeAiName"
-            >
-              <span v-if="aiNamingBusy" class="spin" aria-hidden="true" />
-              {{ aiNamingBusy ? "Proposta in corso…" : "Proponi nome (AI)" }}
-            </button>
-          </div>
-
           <div class="inv-p-sec">
             <div class="inv-p-seclabel"><span>Fingerprint · classificazione</span><span class="line" /></div>
             <div v-if="!panelFacts.length" class="inv-p-note-sugg">— nessun fact ancora</div>
             <div
               v-for="f in panelFacts"
@@ -750,18 +554,14 @@ onUnmounted(() => {
                 Adotta
               </button>
             </div>
           </div>
 
-          <div class="inv-p-sec">
-            <div class="inv-p-seclabel"><span>Note</span><span class="line" /></div>
-            <textarea v-model="form.notes" class="inv-notes" placeholder="appunti su questo device…" />
-          </div>
-        </div>
-        <div class="inv-p-foot">
-          <button type="button" class="inv-btn primary" :disabled="busy" @click="savePanel">Salva</button>
-          <span class="inv-saved" :class="{ show: savedFlash }">Salvato ✓</span>
+          <AssetNotes
+            :asset-id="selected.primaryId"
+            @saved="refreshSelected"
+          />
         </div>
       </template>
     </aside>
     </Teleport>
   </div>
```
