<!-- BLOCK-ID: OBS-DOSSIER-PAGE-DIFF-021B -->

# OBS-DOSSIER-PAGE-DIFF-021B — Dossier + sidebar (diff completo con file nuovi)

**VERSION:** invariata (`0.10.9` live) · bump **0.10.10** al deploy  
**STOP pre-deploy**  
**Nota:** `git add -N` sui file nuovi così compaiono in `git diff -U5`.

## Cosa

1. **Estrazione:** `AssetIdentity.vue` + `AssetHabits.vue` — prop `assetId`, fetch autonomo, OS actions nel componente.
2. **`/dossier` + `/dossier/:id`:** hub search + recenti; pagina piena Identity + Habits `wide`.
3. **Sidebar RADAR / MAPPA** + stub onesti.
4. **Drawer Inventario:** anteprima + Tu decidi + Apri Dossier.

## Diff (`git diff -U5`, include intent-to-add)

```diff
diff --git a/observatory/CHANGELOG.md b/observatory/CHANGELOG.md
index d468cc4..9566268 100644
--- a/observatory/CHANGELOG.md
+++ b/observatory/CHANGELOG.md
@@ -1,7 +1,75 @@
 # Changelog
 
+## 0.10.10 — pending deploy (STOP)
+
+- **Dossier pagina piena + sidebar RADAR/MAPPA (OBS-DOSSIER-PAGE-021):** `AssetIdentity` / `AssetHabits` estratti (fetch autonomo, OS actions nel componente); `/dossier` hub + `/dossier/:id`; drawer Inventario = anteprima + Tu decidi + «Apri Dossier»; stub onesti Oggi/Osservatorio/Come funziona.
+
+## 0.10.9 — 2026-07-23
+
+- **Abitudini — leggibilità destinazioni (OBS-UI-DEST-READABILITY-019):** label speciali senza query (`broadcast LAN` da `network_cidr`, `broadcast globale`, SSDP/mDNS/multicast); middle-ellipsis sui nomi lunghi (coda = dominio) + tooltip pieno; niente CSS end-clip.
+- **Wave 1c live:** contesto AI applicato a ~392 hostname distinti (`ip_intel.context`); script riprendibile, batch 10 sotto TPM Groq.
+
+## 0.10.8 — 2026-07-23
+
+- **Wave 1c — contesto destinazioni (manuale):** colonne `ip_intel.context` / `context_source` / `ai_fetched_at`; classificazione hostname completo via Groq (batch 10–12 sotto TPM, `non_deducibile` valido); script `scripts/ip_intel_context_run.py` (niente job notturno). TTL 90g.
+
+## 0.10.7 — 2026-07-23
+
+- **Wave 1b — nomi destinazioni osservati:** tabella `ip_intel` (DNS A/AAAA + SNI `:443` confermato via `conn.uid`); provider `zeek_intel` → `POST /api/ingest/ip-intel` (cold start: offset EOF, niente backlog); Habits riempie `dst_name` (pubblici da cache, privati da asset locale). Nessun AI context in questo pezzo.
+- **Zeek prune:** entrypoint esteso a `ssl*` / `http*` / `files*` (oltre conn/dns/dhcp); niente bare mode.
+
+## 0.10.6 — 2026-07-23
+
+- **Abitudini chassis-aware:** aggregazione per device fisico (`scope=chassis` default se ≥2 membri). Gate `resolve_asset_by_ip_at` invariato + union post-risoluzione; coverage = peggiore dei membri con motivo composto; provenienza per interfaccia (`Traffico da: eth #N · wifi #M`). Stesso quadro da primary o sibling; asset senza chassis invariato.
+
+## 0.10.5 — 2026-07-23
+
+- **Wave 1a completa — sezione «Abitudini» nel Dossier Inventario:** badge coverage (completo/parziale/sconosciuto), destinazioni con direzione out|in (Opzione A), volume 7g + sparkline ore locali (`Europe/Rome`), porte a scomparsa, stati vuoti onesti (`empty_kind`). Descrittivo; reset habits su `closePanel`.
+
+## 0.10.4 — 2026-07-23
+
+- **Bootstrap — trust dry_run prefetch:** 2 aggregati (`MIN`/`MAX` portal `seen_at` per MAC + `MAX(last_fdb_at)` per asset) prima del loop; da ~2N+1 query a ~3. Equivalenza col legacy N+1 coperta da test. Log: `mode=prefetch queries=N`.
+- Allinea in tree anche il §5 già live in **0.10.3** (backup trust selettivo: solo strutturali; refresh soli timestamp senza backup; `start_period` 180s).
+
+## 0.10.3 — 2026-07-23
+
+- **Bootstrap — backup trust selettivo:** backup solo su modifiche strutturali (`trust_level` / quarantine / proposte archiviate). I refresh di soli timestamp (`portal_*` / `presence_state`) applicano senza backup (~60s risparmiati sui boot ordinari). `BOOTSTRAP_BACKUP=always` resta scappatoia. Healthcheck api `start_period: 180s`.
+
+## 0.10.2 — 2026-07-23
+
+- **Fix perdita ora chiusa su timeout POST flow:** batch N=100 su `POST /api/ingest/flows`, retry con ack per chunk (pending resta se fail), tetto K=3 / M=3000 con log `[zeek_conn] DROP ora …`, timeout flow 120s, observations post 60s. Non drop silenzioso in `finally`.
+
+## 0.10.1 — 2026-07-23
+
+- **Wave 1a Parte 2A — `GET /api/assets/{id}/habits`:** rollup 7g gate SQL temporale (binding history, tie→escludi), coverage 3 stati da topologia, mix-aware `bytes_out`/`bytes_in`, `empty_kind`, ore UTC + `timezone: Europe/Rome`. Mirror sources hardcoded (`DEBT-MIRROR-SOURCES`). Solo API — UI Abitudini = 2B.
+
+## 0.10.0 — 2026-07-23
+
+- **Wave 1a Parte 1 — pipeline direzione flow:** `bytes_out` / `bytes_in` / `byte_layer` end-to-end (Zeek `conn.log` → aggregate → ingest → `flow_observations` → `flows_summary`). App-layer primario; fallback IP-bytes (`byte_layer=ip`); mai null→0 silenzioso. Migration Alembic `h8e4f5a6b7c8` (+ colonne idempotenti in `schema_migrations`). Storico: out/in NULL. Inizia il filone behavioural.
+
+## 0.9.12 — 2026-07-22
+
+- Attribuzione OS **chassis-aware**: se nmap risponde col MAC di un sibling dello stesso chassis (gate: `origin` ∈ {auto, manuale}, ≥1 di C1/C2/C3, no X1), l’OS va all’**owner** del MAC + mirror sul target dello scan; stats `os_attributed_via_chassis_sibling`. Nessun merge identity; `chassis_grouping` non toccato.
+
+## 0.9.11 — 2026-07-22
+
+- Osservabilità attribuzione OS su MAC mismatch: `fingerprint_stats.mac_mismatches` (+ `os_discarded_mac_mismatch` / messaggio), `scan_run.message` esplicito, Dossier label «OS non attribuito (MAC discordante — vedi dettagli)» con tooltip. Nessuna fusion identity, nessun cambio worker.
+
+## 0.9.10 — 2026-07-22
+
+- **DEBT-COLLECTOR-PRIVILEGED risolto per rimozione:** nmap **in-image** nel collector (`apt install nmap`); `nmap_scan.py` esegue il binario locale (no `docker run` / no `instrumentisto/nmap`).
+- Compose collector: **drop** `/var/run/docker.sock`, **drop** `privileged: true` — restano solo `NET_RAW` + `NET_ADMIN` (pattern Zeek).
+- `SCANNER_PRIVILEGED` resta **false** al deploy finché staging non conferma ARP (`-sn` con MAC) e un `os_fingerprint` mirato con flag true. Accensione OS = solo dopo quella verifica.
+
+## 0.9.9 — 2026-07-22
+
+- Dossier «Chi sei»: parser identità pulito (`GET /api/assets/{id}/identity`), OUI resident (`oui_vendors` + `scripts/oui_refresh.py` manuale), sezione UI nel pannello Inventario con ignoti dichiarati.
+- Opt-out OS per-asset (`meta.os_fingerprint_opt_out`, default per tipo iot/domotica/media — **zero brand** hardcoded); toggle «Proteggi da scansione OS».
+- Semaforo `GET /api/system/scan-readiness` (green/yellow/red + motivo) sul bottone «Rileva OS ora».
+- OS detection **canale spento**: `SCANNER_PRIVILEGED=false`; `/scan-os` → «OS non disponibile, scanner non privilegiato». Accensione OS = cantiere 0.9.10 (`DEBT-COLLECTOR-PRIVILEGED`: nmap-in-image, drop docker.sock/privileged).
+
 ## 0.9.8 — 2026-07-22
 
 - LEVA B SQLite lock: `reconcile_all_asset_presence` solo su `/fdb-reconcile` (collector `reconcile_presence=False` su nmap/ssdp/printer/fritz/scan-batch); anti-burst `PRESENCE_RECONCILE_MIN_INTERVAL_SEC=600` (~1–2 pass/15'). Log `[fdb-reconcile] presence pass|coalesced`.
 
 ## 0.9.7 — 2026-07-22
diff --git a/observatory/web/src/App.vue b/observatory/web/src/App.vue
index c272992..b1ac11d 100644
--- a/observatory/web/src/App.vue
+++ b/observatory/web/src/App.vue
@@ -112,29 +112,25 @@ onMounted(() => {
       <div class="calibration-chrome">
         <CalibrationBadge v-if="user" :payload="dash" />
       </div>
       <nav class="nav">
         <div class="nav-group">
-          <div class="nav-label">Operativo</div>
-          <router-link to="/" title="Panoramica">Dashboard</router-link>
+          <div class="nav-label">RADAR</div>
+          <router-link to="/oggi" title="Panoramica del giorno">Oggi</router-link>
+          <router-link to="/osservatorio" title="Radar traffico">Osservatorio</router-link>
+          <router-link to="/dossier" title="Approfondisci un device">Dossier</router-link>
+          <router-link to="/come-funziona" title="Guida leggera">Come funziona</router-link>
+        </div>
+        <div class="nav-group">
+          <div class="nav-label">MAPPA</div>
           <router-link to="/inventory" title="Dispositivi e nomi">Inventario</router-link>
           <router-link to="/plant" title="Porte e patch">Impianto</router-link>
           <router-link to="/topology" title="Come sono collegati">Topologia</router-link>
-        </div>
-        <div class="nav-group">
-          <div class="nav-label">Salute</div>
           <router-link to="/monitoring">Monitor</router-link>
-          <router-link to="/incidents">Incidenti</router-link>
-          <router-link to="/findings">Findings</router-link>
           <router-link to="/timeline">Timeline</router-link>
-        </div>
-        <div class="nav-group">
-          <div class="nav-label">Controllo</div>
-          <router-link to="/suggestions">Proposte</router-link>
+          <router-link to="/findings">Findings</router-link>
           <router-link to="/actions">Azioni</router-link>
-          <router-link to="/runbook">Runbook</router-link>
-          <router-link to="/ai">AI</router-link>
         </div>
       </nav>
       <div class="sidebar-foot">
         <LocalClock />
         <div class="muted" style="display: flex; align-items: center; gap: 0.45rem; font-size: 0.8rem">
diff --git a/observatory/web/src/components/AssetHabits.vue b/observatory/web/src/components/AssetHabits.vue
new file mode 100644
index 0000000..29ac291
--- /dev/null
+++ b/observatory/web/src/components/AssetHabits.vue
@@ -0,0 +1,328 @@
+<script setup>
+import { computed, ref, watch } from "vue";
+import { api } from "../api";
+import {
+  directionMetaLine,
+  directionSplit,
+  emptyKindMessage,
+  formatBytes,
+  formatDirPair,
+  hourTooltip,
+  hoursToLocalBins,
+  isEmptySilenceKind,
+  formatHabitsDestName,
+  portChipLabel,
+  provenanceLine,
+  showDirectionBars,
+  sparklineHeights,
+  visibleDestinations,
+  visiblePorts,
+} from "../habitsUi";
+
+const props = defineProps({
+  assetId: { type: [Number, String], required: true },
+  days: { type: Number, default: 7 },
+  /** Full-width layout for dossier page (bars/spark breathe). */
+  wide: { type: Boolean, default: false },
+});
+
+const habits = ref(null);
+const loading = ref(false);
+const destExpanded = ref(false);
+const portsExpanded = ref(false);
+
+const numericId = computed(() => {
+  const n = Number(props.assetId);
+  return Number.isFinite(n) && n > 0 ? n : null;
+});
+
+const localHours = computed(() => {
+  if (!habits.value?.hours) return [];
+  const tz = habits.value.timezone || "Europe/Rome";
+  return hoursToLocalBins(habits.value.hours, tz);
+});
+const spark = computed(() => sparklineHeights(localHours.value));
+const destView = computed(() =>
+  visibleDestinations(habits.value?.destinations, destExpanded.value),
+);
+const portsView = computed(() =>
+  visiblePorts(habits.value?.ports, portsExpanded.value),
+);
+const showBars = computed(() => showDirectionBars(habits.value));
+const directionMeta = computed(() => directionMetaLine(habits.value));
+const provenance = computed(() => provenanceLine(habits.value));
+const emptyText = computed(() => emptyKindMessage(habits.value?.empty_kind));
+const isEmptySilence = computed(() => isEmptySilenceKind(habits.value?.empty_kind));
+const isThin = computed(() => habits.value?.empty_kind === "thin_sample");
+const sectionTitle = computed(() => habits.value?.title || "Abitudini");
+const purpose = computed(
+  () =>
+    habits.value?.purpose ||
+    "Chi parla, quanto, quando — solo osservato sullo SPAN",
+);
+
+async function load() {
+  const id = numericId.value;
+  habits.value = null;
+  destExpanded.value = false;
+  portsExpanded.value = false;
+  if (!id) return;
+  loading.value = true;
+  try {
+    habits.value = await api.assetHabits(id, props.days);
+  } catch {
+    habits.value = null;
+  } finally {
+    loading.value = false;
+  }
+}
+
+watch(
+  () => [props.assetId, props.days],
+  () => load(),
+  { immediate: true },
+);
+</script>
+
+<template>
+  <section class="asset-habits inv-p-sec inv-habits" :class="{ wide }">
+    <div class="inv-p-seclabel"><span>{{ sectionTitle }}</span><span class="line" /></div>
+    <p class="inv-purpose">{{ purpose }}</p>
+    <div v-if="loading" class="inv-p-note-sugg">caricamento…</div>
+    <template v-else-if="habits">
+      <div
+        class="habits-cov"
+        :class="habits.coverage?.state || 'sconosciuto'"
+        :title="habits.coverage?.reason || undefined"
+      >
+        <span class="habits-cov-dot" aria-hidden="true" />
+        <span class="habits-cov-label">{{ habits.coverage?.label || "Traffico: copertura sconosciuta" }}</span>
+      </div>
+      <p v-if="habits.coverage?.reason" class="habits-cov-reason">{{ habits.coverage.reason }}</p>
+      <p v-if="provenance" class="habits-meta habits-prov">{{ provenance }}</p>
+      <p v-if="directionMeta" class="habits-meta">{{ directionMeta }}</p>
+
+      <template v-if="isEmptySilence">
+        <p class="habits-empty">{{ emptyText }}</p>
+      </template>
+      <template v-else>
+        <div class="habits-block">
+          <div class="habits-block-h">Con chi parla</div>
+          <p v-if="showBars" class="habits-legend">out = verso destinazione · in = dalla destinazione</p>
+          <p
+            v-else-if="(habits.direction_sample_ratio || 0) > 0 && (habits.direction_sample_ratio || 0) < 0.2"
+            class="habits-legend"
+          >direzione ancora scarsa</p>
+          <div v-if="!destView.shown.length" class="inv-p-note-sugg">— nessuna destinazione</div>
+          <div
+            v-for="d in destView.shown"
+            :key="d.dst_ip"
+            class="habits-dst"
+          >
+            <div class="habits-dst-id">
+              <span
+                v-if="d.dst_name"
+                class="habits-dst-name"
+                :title="formatHabitsDestName(d.dst_name).full"
+              >{{ formatHabitsDestName(d.dst_name).display }}</span>
+              <span class="habits-dst-ip mono">{{ d.dst_ip }}</span>
+            </div>
+            <div class="habits-dst-dir">
+              <template v-if="showBars && directionSplit(d)">
+                <span class="habits-dir-lbl out">out</span>
+                <div class="habits-bar" aria-hidden="true">
+                  <span class="seg out" :style="{ width: directionSplit(d).outPct + '%' }" />
+                  <span class="seg in" :style="{ width: directionSplit(d).inPct + '%' }" />
+                </div>
+                <span class="habits-dir-lbl in">in</span>
+                <span class="habits-dir-pair mono">{{ formatDirPair(d) }}</span>
+              </template>
+              <template v-else>
+                <span class="habits-vol mono">{{ formatBytes(d.bytes) }}</span>
+                <span class="habits-dir-na">—</span>
+              </template>
+            </div>
+          </div>
+          <button
+            v-if="destView.hidden > 0"
+            type="button"
+            class="habits-more"
+            @click="destExpanded = true"
+          >+{{ destView.hidden }} altre</button>
+        </div>
+
+        <div class="habits-block">
+          <div class="habits-volrow">
+            <span class="habits-block-h">Volume {{ habits.window_days || days }}g</span>
+            <span class="habits-vol-total mono">{{ formatBytes(habits.totals?.bytes) }}</span>
+            <span v-if="isThin" class="habits-thin">campione ancora sottile</span>
+          </div>
+          <div class="habits-when">
+            <span class="habits-when-lbl">Quando</span>
+            <div class="habits-spark" role="img" aria-label="Volume per ora">
+              <span
+                v-for="(bin, i) in localHours"
+                :key="bin.hour"
+                class="habits-spark-cell"
+                :title="hourTooltip(bin)"
+              >
+                <span
+                  class="habits-spark-bar"
+                  :style="{ height: (spark[i] * 100) + '%' }"
+                />
+              </span>
+            </div>
+            <div class="habits-spark-axis mono">
+              <span>0</span><span>6</span><span>12</span><span>18</span><span>23</span>
+            </div>
+            <p class="habits-tz">ore {{ habits.timezone || "Europe/Rome" }}</p>
+          </div>
+        </div>
+
+        <div class="habits-block">
+          <div class="habits-block-h">Porte</div>
+          <div class="habits-ports">
+            <span
+              v-for="p in portsView.shown"
+              :key="`${p.proto}-${p.port}`"
+              class="habits-port-chip mono"
+              :title="`${formatBytes(p.bytes)} · ${p.samples} oss.`"
+            >{{ portChipLabel(p) }}</span>
+            <button
+              v-if="portsView.hidden > 0"
+              type="button"
+              class="habits-more"
+              @click="portsExpanded = true"
+            >mostra tutte</button>
+            <span v-if="!portsView.shown.length" class="inv-p-note-sugg">—</span>
+          </div>
+        </div>
+      </template>
+    </template>
+    <div v-else class="inv-p-note-sugg">— abitudini non disponibili</div>
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
+.inv-purpose {
+  margin: 0 0 10px; font-size: 12px; color: var(--inv-faint); line-height: 1.35;
+}
+.inv-p-note-sugg { font-size: 12.5px; color: var(--inv-faint); }
+.habits-cov {
+  display: inline-flex; align-items: center; gap: 7px;
+  font-size: 11.5px; letter-spacing: 0.02em;
+  color: var(--inv-mut); border: 1px solid var(--inv-border);
+  border-radius: 6px; padding: 3px 9px 3px 7px; margin-top: 2px;
+}
+.habits-cov-dot {
+  width: 8px; height: 8px; border-radius: 50%; background: var(--inv-faint); flex-shrink: 0;
+}
+.habits-cov.completo { border-color: var(--inv-green-dim); color: var(--inv-green); }
+.habits-cov.completo .habits-cov-dot { background: var(--inv-green); }
+.habits-cov.parziale { border-color: color-mix(in srgb, var(--inv-amber) 55%, var(--inv-border)); color: var(--inv-amber); }
+.habits-cov.parziale .habits-cov-dot { background: var(--inv-amber); }
+.habits-cov.sconosciuto { border-color: var(--inv-border); color: var(--inv-faint); }
+.habits-cov-reason {
+  margin: 6px 0 0; font-size: 11.5px; line-height: 1.4; color: var(--inv-faint);
+}
+.habits-meta { margin: 8px 0 0; font-size: 11.5px; color: var(--inv-mut); }
+.habits-empty {
+  margin: 12px 0 0; font-size: 12.5px; line-height: 1.45; color: var(--inv-mut);
+}
+.habits-block { margin-top: 14px; }
+.habits-block-h {
+  font-size: 11px; letter-spacing: 0.06em; text-transform: uppercase;
+  color: var(--inv-faint); margin-bottom: 6px;
+}
+.habits-legend {
+  margin: 0 0 8px; font-size: 11px; color: var(--inv-faint); line-height: 1.35;
+}
+.habits-dst {
+  display: grid;
+  grid-template-columns: minmax(7.5rem, 0.9fr) minmax(0, 1.4fr);
+  gap: 6px 10px; align-items: center;
+  padding: 5px 0; border-bottom: 1px dashed var(--inv-border-soft);
+  font-size: 12px;
+}
+.wide .habits-dst {
+  grid-template-columns: minmax(12rem, 1.1fr) minmax(0, 1.6fr);
+  gap: 8px 16px; padding: 8px 0; font-size: 13px;
+}
+.habits-dst-id { min-width: 0; display: flex; flex-direction: column; gap: 1px; }
+.habits-dst-name {
+  font-size: 11px; color: var(--inv-text); white-space: nowrap; overflow: visible;
+}
+.wide .habits-dst-name { font-size: 12.5px; }
+.habits-dst-ip { color: var(--inv-mut); font-size: 12px; }
+.habits-dst-dir {
+  display: flex; align-items: center; gap: 5px; min-width: 0; flex-wrap: wrap;
+}
+.habits-dir-lbl {
+  font-size: 9.5px; letter-spacing: 0.04em; text-transform: uppercase;
+  color: var(--inv-faint); flex-shrink: 0;
+}
+.habits-dir-lbl.out { color: var(--inv-green-dim); }
+.habits-dir-lbl.in { color: var(--inv-amber); }
+.habits-bar {
+  display: flex; flex: 1; min-width: 4.5rem; max-width: 11rem; height: 8px;
+  border-radius: 2px; overflow: hidden; background: var(--inv-green-deep);
+  border: 1px solid var(--inv-border-soft);
+}
+.wide .habits-bar { min-width: 8rem; max-width: 22rem; height: 10px; }
+.habits-bar .seg.out { background: var(--inv-green); }
+.habits-bar .seg.in { background: var(--inv-amber); }
+.habits-dir-pair { font-size: 11px; color: var(--inv-mut); white-space: nowrap; }
+.habits-vol { font-size: 12px; color: var(--inv-mut); }
+.habits-dir-na { font-size: 11px; color: var(--inv-faint); }
+.habits-more {
+  background: none; border: none; color: var(--inv-green-dim);
+  font-size: 11.5px; padding: 4px 0; cursor: pointer; min-height: 0;
+  text-decoration: underline; text-underline-offset: 2px;
+}
+.habits-more:hover { color: var(--inv-green); }
+.habits-volrow {
+  display: flex; align-items: baseline; gap: 10px; flex-wrap: wrap;
+}
+.habits-vol-total { font-size: 14px; color: var(--inv-text); }
+.wide .habits-vol-total { font-size: 18px; }
+.habits-thin {
+  font-size: 11px; color: var(--inv-amber);
+}
+.habits-when { margin-top: 4px; }
+.habits-when-lbl {
+  font-size: 11px; letter-spacing: 0.06em; text-transform: uppercase;
+  color: var(--inv-faint);
+}
+.habits-spark {
+  display: flex; align-items: flex-end; gap: 2px; height: 48px; margin-top: 6px;
+}
+.wide .habits-spark { height: 72px; gap: 3px; }
+.habits-spark-cell {
+  flex: 1; min-width: 0; height: 100%; display: flex; align-items: flex-end;
+}
+.habits-spark-bar {
+  width: 100%; background: var(--inv-green-dim); border-radius: 1px 1px 0 0;
+  min-height: 1px;
+}
+.habits-spark-cell:hover .habits-spark-bar { background: var(--inv-green); }
+.habits-spark-axis {
+  display: flex; justify-content: space-between; margin-top: 4px;
+  font-size: 10px; color: var(--inv-faint);
+}
+.habits-tz {
+  margin: 4px 0 0; font-size: 11px; color: var(--inv-faint);
+}
+.habits-ports { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
+.habits-port-chip {
+  border: 1px solid var(--inv-border); border-radius: 5px;
+  padding: 2px 7px; font-size: 11px; color: var(--inv-mut);
+}
+.mono { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
+</style>
diff --git a/observatory/web/src/components/AssetIdentity.vue b/observatory/web/src/components/AssetIdentity.vue
new file mode 100644
index 0000000..ce6ff9a
--- /dev/null
+++ b/observatory/web/src/components/AssetIdentity.vue
@@ -0,0 +1,310 @@
+<script setup>
+import { computed, ref, watch } from "vue";
+import { api } from "../api";
+import { formatDate } from "../formatTime";
+
+const props = defineProps({
+  assetId: { type: [Number, String], required: true },
+});
+
+const emit = defineEmits(["changed"]);
+
+const identity = ref(null);
+const loading = ref(false);
+const error = ref("");
+const technicalOpen = ref(false);
+const osScanBusy = ref(false);
+const osScanMsg = ref("");
+const actionBusy = ref(false);
+const actionMsg = ref("");
+
+const numericId = computed(() => {
+  const n = Number(props.assetId);
+  return Number.isFinite(n) && n > 0 ? n : null;
+});
+
+async function load({ technical = technicalOpen.value } = {}) {
+  const id = numericId.value;
+  if (!id) {
+    identity.value = null;
+    error.value = "";
+    return;
+  }
+  loading.value = true;
+  error.value = "";
+  osScanMsg.value = "";
+  try {
+    identity.value = await api.assetIdentity(id, technical);
+  } catch (e) {
+    identity.value = null;
+    error.value = e.message || "Identità non disponibile";
+  } finally {
+    loading.value = false;
+  }
+}
+
+function fmtSeen(iso) {
+  return formatDate(iso);
+}
+
+async function toggleTechnical() {
+  technicalOpen.value = !technicalOpen.value;
+  await load({ technical: technicalOpen.value });
+}
+
+async function toggleOsProtect() {
+  const id = numericId.value;
+  if (!id || !identity.value || actionBusy.value) return;
+  const current = !!(identity.value.os_scan && identity.value.os_scan.opt_out);
+  const next = !current;
+  actionBusy.value = true;
+  actionMsg.value = "";
+  try {
+    await api.updateAsset(id, { os_fingerprint_opt_out: next });
+    await load({ technical: technicalOpen.value });
+    emit("changed");
+  } catch (e) {
+    actionMsg.value = e.message || "Impossibile aggiornare protezione OS";
+  } finally {
+    actionBusy.value = false;
+  }
+}
+
+async function detectOsNow() {
+  const id = numericId.value;
+  if (!id || osScanBusy.value) return;
+  let readiness = identity.value?.scan_readiness || null;
+  try {
+    readiness = await api.scanReadiness("os_fingerprint");
+    if (identity.value) identity.value = { ...identity.value, scan_readiness: readiness };
+  } catch (_) {
+    /* keep existing readiness */
+  }
+  if (readiness?.confirm_required) {
+    const promptText =
+      readiness.confirm_prompt ||
+      readiness.reason ||
+      "Il ciclo di scansione è vicino. Lanciare comunque l’analisi OS?";
+    if (!window.confirm(promptText)) return;
+  }
+  osScanBusy.value = true;
+  osScanMsg.value = "";
+  try {
+    const row = await api.scanAssetOs(id);
+    osScanMsg.value =
+      row.os_attribution?.message || row.message || "OS fingerprint accodata";
+    await load({ technical: technicalOpen.value });
+    if (identity.value?.os_attribution?.message) {
+      osScanMsg.value = identity.value.os_attribution.message;
+    }
+    emit("changed");
+  } catch (e) {
+    osScanMsg.value = e.message || "OS scan non avviata";
+  } finally {
+    osScanBusy.value = false;
+  }
+}
+
+watch(
+  () => props.assetId,
+  () => {
+    technicalOpen.value = false;
+    osScanMsg.value = "";
+    actionMsg.value = "";
+    load({ technical: false });
+  },
+  { immediate: true },
+);
+</script>
+
+<template>
+  <section class="asset-identity inv-p-sec inv-chi-sei">
+    <div class="inv-p-seclabel"><span>Chi sei</span><span class="line" /></div>
+    <p class="inv-purpose">Chi è questo device — identità osservata</p>
+    <div v-if="loading" class="inv-p-note-sugg">caricamento…</div>
+    <template v-else-if="identity">
+      <div class="inv-kv inv-identity-kv">
+        <span class="k">Vendor</span>
+        <span class="v">
+          {{ identity.labels.vendor }}
+          <span
+            v-if="identity.vendor && !identity.vendor_reliable"
+            class="badge-privacy"
+            title="MAC locally-administered: OUI non affidabile"
+          >privacy</span>
+        </span>
+        <span class="k">OS</span>
+        <span
+          class="v"
+          :class="{
+            'os-mac-mismatch': identity.os_attribution?.kind === 'mac_mismatch',
+            'os-chassis-sibling': identity.os_attribution?.kind === 'chassis_sibling',
+          }"
+          :title="identity.os_attribution?.message || undefined"
+        >{{ identity.labels.os }}</span>
+        <span class="k">Hostname</span><span class="v">{{ identity.labels.hostname }}</span>
+        <span class="k">Servizi</span><span class="v">{{ identity.labels.services }}</span>
+        <span class="k">Tipo</span><span class="v">{{ identity.labels.device_type }}</span>
+        <span class="k">MAC</span>
+        <span class="v">
+          {{ identity.labels.mac }}
+          <span v-if="identity.is_private" class="badge-privacy">U/L</span>
+        </span>
+        <span class="k">Prima volta</span><span class="v">{{ fmtSeen(identity.first_seen) || identity.labels.first_seen }}</span>
+        <span class="k">Presence</span><span class="v">{{ identity.labels.presence }}</span>
+      </div>
+      <div
+        class="inv-switchrow"
+        :class="{ on: identity.os_scan && identity.os_scan.opt_out }"
+        @click="toggleOsProtect"
+      >
+        <span class="sw" /><span class="swlbl">Proteggi da scansione OS (device fragile)</span>
+      </div>
+      <div class="inv-swnote">
+        <template v-if="identity.os_scan && identity.os_scan.opt_out_source === 'default_device_type'">
+          suggerito: tipo «{{ identity.os_scan.device_type }}» — puoi togliere la spunta
+        </template>
+        <template v-else-if="identity.os_scan && identity.os_scan.opt_out_explicit">
+          scelta salvata sul device
+        </template>
+        <template v-else>
+          gli IoT/media restano protetti di default; nessun brand in codice
+        </template>
+      </div>
+      <div class="inv-os-actions">
+        <span
+          v-if="identity.scan_readiness"
+          class="scan-sema"
+          :class="identity.scan_readiness.level"
+          :title="identity.scan_readiness.reason"
+        >
+          <span class="dot" aria-hidden="true" />
+          <span class="sema-label">{{ identity.scan_readiness.labels?.level || identity.scan_readiness.level }}</span>
+        </span>
+        <button
+          type="button"
+          class="inv-btn"
+          :disabled="
+            osScanBusy ||
+            actionBusy ||
+            (identity.os_scan && identity.os_scan.excluded) ||
+            (identity.os_scan && identity.os_scan.os_detection_available === false)
+          "
+          @click="detectOsNow"
+        >
+          {{ osScanBusy ? "Scansione…" : "Rileva OS ora" }}
+        </button>
+        <span
+          v-if="identity.os_scan && identity.os_scan.excluded"
+          class="inv-os-excl"
+        >{{ identity.os_scan.message || "escluso (IoT fragile)" }}</span>
+        <span
+          v-else-if="identity.os_scan && identity.os_scan.os_detection_available === false"
+          class="inv-os-excl"
+        >{{ identity.os_scan.unavailable_message || "OS non disponibile, scanner non privilegiato" }}</span>
+        <span v-else-if="osScanMsg" class="inv-os-msg">{{ osScanMsg }}</span>
+      </div>
+      <p v-if="actionMsg" class="inv-os-excl">{{ actionMsg }}</p>
+      <p
+        v-if="identity.scan_readiness"
+        class="scan-sema-reason"
+      >{{ identity.scan_readiness.reason }}</p>
+      <button type="button" class="inv-btn ghost" @click="toggleTechnical">
+        {{ technicalOpen ? "Nascondi dettagli tecnici" : "Mostra dettagli tecnici" }}
+      </button>
+      <pre
+        v-if="technicalOpen && identity.technical"
+        class="inv-tech"
+      >{{ JSON.stringify(identity.technical, null, 2) }}</pre>
+    </template>
+    <div v-else class="inv-p-note-sugg">{{ error || "— identità non disponibile" }}</div>
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
+.inv-purpose {
+  margin: 0 0 10px; font-size: 12px; color: var(--inv-faint); line-height: 1.35;
+}
+.inv-p-note-sugg { font-size: 12.5px; color: var(--inv-faint); }
+.inv-kv {
+  display: grid; grid-template-columns: 108px 1fr; gap: 8px 10px;
+  font-size: 12.5px; margin-top: 12px;
+}
+.inv-kv .k { color: var(--inv-faint); }
+.inv-kv .v { color: var(--inv-mut); word-break: break-all; }
+.inv-identity-kv { margin-top: 0; }
+.inv-identity-kv .os-mac-mismatch {
+  cursor: help;
+  border-bottom: 1px dotted color-mix(in srgb, var(--inv-warn, #c9a227) 70%, transparent);
+}
+.inv-identity-kv .os-chassis-sibling {
+  cursor: help;
+  border-bottom: 1px dotted color-mix(in srgb, var(--inv-green, #3d9a5f) 55%, transparent);
+}
+.badge-privacy {
+  display: inline-block; margin-left: 6px; font-size: 10px; letter-spacing: 0.04em;
+  text-transform: uppercase; border: 1px solid var(--inv-border); border-radius: 4px;
+  padding: 0 5px; color: var(--inv-faint); vertical-align: middle;
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
+.inv-os-actions {
+  display: flex; flex-wrap: wrap; align-items: center; gap: 8px; margin: 12px 0 8px;
+}
+.inv-os-excl, .inv-os-msg { font-size: 11.5px; color: var(--inv-faint); }
+.inv-os-excl { color: var(--inv-mut); }
+.scan-sema {
+  display: inline-flex; align-items: center; gap: 6px;
+  font-size: 11px; letter-spacing: 0.04em; text-transform: uppercase;
+  color: var(--inv-faint); border: 1px solid var(--inv-border);
+  border-radius: 6px; padding: 2px 8px 2px 6px;
+}
+.scan-sema .dot {
+  width: 8px; height: 8px; border-radius: 50%; background: var(--inv-faint);
+}
+.scan-sema.green { border-color: var(--inv-green-dim); color: var(--inv-green); }
+.scan-sema.green .dot { background: var(--inv-green); }
+.scan-sema.yellow { border-color: #a68b2c; color: #c4a035; }
+.scan-sema.yellow .dot { background: #c4a035; }
+.scan-sema.red { border-color: #8b3a3a; color: #c45c5c; }
+.scan-sema.red .dot { background: #c45c5c; }
+.scan-sema-reason {
+  margin: 0 0 8px; font-size: 11.5px; line-height: 1.4; color: var(--inv-faint);
+}
+.inv-btn {
+  background: var(--inv-bg-row); border: 1px solid var(--inv-border);
+  border-radius: 8px; padding: 7px 12px; color: var(--inv-mut);
+  font-family: inherit; font-size: 12.5px; cursor: pointer;
+}
+.inv-btn:disabled { opacity: 0.5; cursor: not-allowed; }
+.inv-btn.ghost {
+  background: transparent; border-style: dashed; margin-top: 4px;
+}
+.inv-tech {
+  margin: 8px 0 0; padding: 10px; max-height: 220px; overflow: auto;
+  font-size: 10.5px; line-height: 1.35; color: var(--inv-faint);
+  background: var(--inv-bg-row); border: 1px solid var(--inv-border-soft);
+  border-radius: 6px; white-space: pre-wrap; word-break: break-word;
+}
+</style>
diff --git a/observatory/web/src/dossierRecent.js b/observatory/web/src/dossierRecent.js
new file mode 100644
index 0000000..523799b
--- /dev/null
+++ b/observatory/web/src/dossierRecent.js
@@ -0,0 +1,33 @@
+/** Recent dossier visits (localStorage). */
+
+const KEY = "obs.dossier.recent";
+const MAX = 8;
+
+export function readRecentDossiers() {
+  try {
+    const raw = localStorage.getItem(KEY);
+    const list = raw ? JSON.parse(raw) : [];
+    return Array.isArray(list) ? list.filter((x) => x && x.id) : [];
+  } catch {
+    return [];
+  }
+}
+
+export function pushRecentDossier(entry) {
+  const id = Number(entry?.id);
+  if (!Number.isFinite(id) || id <= 0) return readRecentDossiers();
+  const next = {
+    id,
+    name: String(entry.name || "").trim() || `Asset #${id}`,
+    ip: String(entry.ip || "").trim(),
+    at: new Date().toISOString(),
+  };
+  const prev = readRecentDossiers().filter((x) => Number(x.id) !== id);
+  const out = [next, ...prev].slice(0, MAX);
+  try {
+    localStorage.setItem(KEY, JSON.stringify(out));
+  } catch {
+    /* ignore quota */
+  }
+  return out;
+}
diff --git a/observatory/web/src/dossierRecent.test.js b/observatory/web/src/dossierRecent.test.js
new file mode 100644
index 0000000..6fb3bd4
--- /dev/null
+++ b/observatory/web/src/dossierRecent.test.js
@@ -0,0 +1,24 @@
+import test from "node:test";
+import assert from "node:assert/strict";
+import { pushRecentDossier, readRecentDossiers } from "./dossierRecent.js";
+
+test("dossierRecent push dedupes and caps", () => {
+  const key = "obs.dossier.recent";
+  globalThis.localStorage = {
+    _d: {},
+    getItem(k) {
+      return this._d[k] ?? null;
+    },
+    setItem(k, v) {
+      this._d[k] = String(v);
+    },
+  };
+  pushRecentDossier({ id: 1, name: "A", ip: "1.1.1.1" });
+  pushRecentDossier({ id: 2, name: "B", ip: "2.2.2.2" });
+  pushRecentDossier({ id: 1, name: "A2", ip: "1.1.1.1" });
+  const list = readRecentDossiers();
+  assert.equal(list[0].id, 1);
+  assert.equal(list[0].name, "A2");
+  assert.equal(list.length, 2);
+  assert.equal(key in globalThis.localStorage._d, true);
+});
diff --git a/observatory/web/src/inventoryDevices.js b/observatory/web/src/inventoryDevices.js
index a8aa79e..86eb83f 100644
--- a/observatory/web/src/inventoryDevices.js
+++ b/observatory/web/src/inventoryDevices.js
@@ -346,10 +346,11 @@ export function matchDeviceSearch(device, q) {
   const needle = q.trim().toLowerCase();
   if (!needle) return true;
   if ((device.name || "").toLowerCase().includes(needle)) return true;
   if ((device.vendor || "").toLowerCase().includes(needle)) return true;
   if ((device.ip || "").toLowerCase().includes(needle)) return true;
+  if ((device.hostname || "").toLowerCase().includes(needle)) return true;
   return (device.ifaces || []).some(
     (i) =>
       (i.mac || "").toLowerCase().includes(needle) ||
       (i.ip || "").toLowerCase().includes(needle),
   );
diff --git a/observatory/web/src/router.js b/observatory/web/src/router.js
index 5b8e528..f415deb 100644
--- a/observatory/web/src/router.js
+++ b/observatory/web/src/router.js
@@ -9,17 +9,48 @@ import Timeline from "./views/Timeline.vue";
 import Suggestions from "./views/Suggestions.vue";
 import Actions from "./views/Actions.vue";
 import Runbook from "./views/Runbook.vue";
 import AiConsole from "./views/AiConsole.vue";
 import Findings from "./views/Findings.vue";
+import Dossier from "./views/Dossier.vue";
+import RadarStub from "./views/RadarStub.vue";
 import Login from "./views/Login.vue";
 import NotFound from "./views/NotFound.vue";
 import { auth } from "./auth";
 
 const routes = [
   { path: "/login", component: Login, meta: { public: true } },
   { path: "/", component: Dashboard },
+  {
+    path: "/oggi",
+    component: RadarStub,
+    props: {
+      title: "Oggi",
+      blurb:
+        "Oggi · panoramica del giorno (cosa è cambiato sulla LAN) — in preparazione; nel frattempo usa Dashboard (/) e Dossier.",
+    },
+  },
+  {
+    path: "/osservatorio",
+    component: RadarStub,
+    props: {
+      title: "Osservatorio",
+      blurb:
+        "Osservatorio · radar del traffico — richiede ~7 giorni di dati direzionali, disponibile dal ~30 luglio.",
+    },
+  },
+  { path: "/dossier", component: Dossier },
+  { path: "/dossier/:id", component: Dossier },
+  {
+    path: "/come-funziona",
+    component: RadarStub,
+    props: {
+      title: "Come funziona",
+      blurb:
+        "Come funziona · guida leggera a SPAN, presence e Abitudini — bozza prevista dopo il radar Osservatorio (~agosto).",
+    },
+  },
   { path: "/inventory", component: Inventory },
   { path: "/plant", component: Plant },
   { path: "/topology", component: Topology },
   { path: "/monitor", redirect: "/monitoring" },
   { path: "/monitoring", component: Monitoring },
@@ -52,12 +83,10 @@ router.beforeEach(async (to) => {
     return true;
   }
 
   if (user) return true;
 
-  // Solo 401 (sessione assente/scaduta) forza il login.
-  // Altri errori: lascia passare — la shell mostra feedback inline, niente splash eterno.
   if (authError && authError.status !== 401) {
     return true;
   }
 
   return {
diff --git a/observatory/web/src/views/Dossier.vue b/observatory/web/src/views/Dossier.vue
new file mode 100644
index 0000000..a299fcc
--- /dev/null
+++ b/observatory/web/src/views/Dossier.vue
@@ -0,0 +1,308 @@
+<script setup>
+import { computed, onMounted, ref, watch } from "vue";
+import { useRoute, useRouter } from "vue-router";
+import { api } from "../api";
+import { matchDeviceSearch, composeDevices } from "../inventoryDevices";
+import { formatFreshLabel, freshClass } from "../inventoryDevices";
+import { pushRecentDossier, readRecentDossiers } from "../dossierRecent";
+import PageHeader from "../components/PageHeader.vue";
+import AssetIdentity from "../components/AssetIdentity.vue";
+import AssetHabits from "../components/AssetHabits.vue";
+
+const route = useRoute();
+const router = useRouter();
+
+const assetId = computed(() => {
+  const raw = route.params.id;
+  if (raw == null || raw === "") return null;
+  const n = Number(raw);
+  return Number.isFinite(n) && n > 0 ? n : null;
+});
+
+const isHub = computed(() => assetId.value == null);
+
+const q = ref("");
+const loading = ref(false);
+const error = ref("");
+const assets = ref([]);
+const chassisPayload = ref({ chassis: [] });
+const asset = ref(null);
+const recent = ref(readRecentDossiers());
+
+const devices = computed(() => composeDevices(assets.value, chassisPayload.value));
+
+const searchHits = computed(() => {
+  if (!q.value.trim()) return [];
+  return devices.value.filter((d) => matchDeviceSearch(d, q.value)).slice(0, 40);
+});
+
+const presenceLabel = computed(() => {
+  if (!asset.value) return "—";
+  if (asset.value.presence_state) return String(asset.value.presence_state);
+  return asset.value.status || "—";
+});
+
+const primaryIp = computed(() => {
+  const bindings = asset.value?.ip_bindings || [];
+  const cur = bindings.find((b) => b.is_current);
+  if (cur?.ip) return cur.ip;
+  const ips = asset.value?.ips || [];
+  return ips[0] || "—";
+});
+
+const primaryMac = computed(() => {
+  const macs = asset.value?.macs || [];
+  return macs[0] || "—";
+});
+
+async function loadHubList() {
+  loading.value = true;
+  error.value = "";
+  try {
+    const [a, c] = await Promise.all([
+      api.assets({ include_historical: "true" }),
+      api.chassis(),
+    ]);
+    assets.value = a;
+    chassisPayload.value = c;
+  } catch (e) {
+    error.value = e.message || "Caricamento fallito";
+  } finally {
+    loading.value = false;
+  }
+}
+
+async function loadAsset(id) {
+  loading.value = true;
+  error.value = "";
+  asset.value = null;
+  try {
+    asset.value = await api.asset(id);
+    pushRecentDossier({
+      id,
+      name: asset.value.name,
+      ip: primaryIpFrom(asset.value),
+    });
+    recent.value = readRecentDossiers();
+  } catch (e) {
+    error.value = e.message || "Asset non trovato";
+  } finally {
+    loading.value = false;
+  }
+}
+
+function primaryIpFrom(row) {
+  const bindings = row?.ip_bindings || [];
+  const cur = bindings.find((b) => b.is_current);
+  if (cur?.ip) return cur.ip;
+  return (row?.ips || [])[0] || "";
+}
+
+function openDossier(id) {
+  router.push(`/dossier/${id}`);
+}
+
+function goInventory() {
+  router.push("/inventory");
+}
+
+function goTopology() {
+  router.push({ path: "/topology", query: { highlight: String(assetId.value || "") } });
+}
+
+watch(
+  assetId,
+  (id) => {
+    if (id) loadAsset(id);
+    else {
+      asset.value = null;
+      loadHubList();
+      recent.value = readRecentDossiers();
+    }
+  },
+  { immediate: true },
+);
+
+onMounted(() => {
+  recent.value = readRecentDossiers();
+});
+</script>
+
+<template>
+  <div class="dossier">
+    <!-- Hub: search -->
+    <template v-if="isHub">
+      <PageHeader
+        title="Dossier"
+        help="Cerca un device per nome, IP o MAC e apri il quadro completo (identità + abitudini)."
+      />
+      <p class="dossier-lead">Non so cosa cerco — cerca e approfondisci.</p>
+      <input
+        v-model="q"
+        class="dossier-search"
+        type="search"
+        placeholder="cerca nome, IP, MAC…"
+        autocomplete="off"
+      />
+      <p v-if="error" class="dossier-err">{{ error }}</p>
+      <p v-else-if="loading" class="dossier-muted">caricamento inventario…</p>
+
+      <section v-if="q.trim()" class="dossier-sec">
+        <h2 class="dossier-h">Risultati</h2>
+        <div v-if="!searchHits.length" class="dossier-muted">nessun match</div>
+        <button
+          v-for="d in searchHits"
+          :key="d.key"
+          type="button"
+          class="dossier-hit"
+          @click="openDossier(d.primaryId)"
+        >
+          <span class="name" :class="{ unnamed: !d.name }">{{ d.name || "senza nome" }}</span>
+          <span class="meta mono">{{ d.ip || "—" }} · {{ d.macs?.[0] || "—" }}</span>
+          <span class="fresh" :class="freshClass(d)">{{ formatFreshLabel(d) }}</span>
+        </button>
+      </section>
+
+      <section v-if="recent.length" class="dossier-sec">
+        <h2 class="dossier-h">Ultimi consultati</h2>
+        <button
+          v-for="r in recent"
+          :key="r.id"
+          type="button"
+          class="dossier-hit"
+          @click="openDossier(r.id)"
+        >
+          <span class="name">{{ r.name }}</span>
+          <span class="meta mono">{{ r.ip || "—" }}</span>
+        </button>
+      </section>
+    </template>
+
+    <!-- Full page dossier -->
+    <template v-else>
+      <div class="dossier-head">
+        <div class="dossier-head-main">
+          <button type="button" class="dossier-back" @click="router.push('/dossier')">← Dossier</button>
+          <h1 class="dossier-title" :class="{ unnamed: asset && !asset.name }">
+            {{ loading ? "…" : (asset?.name || "Device senza nome") }}
+          </h1>
+          <div class="dossier-sub mono">
+            <span class="presence">{{ presenceLabel }}</span>
+            <span>·</span>
+            <span>{{ primaryIp }}</span>
+            <span>·</span>
+            <span>{{ primaryMac }}</span>
+          </div>
+        </div>
+        <div class="dossier-actions">
+          <button type="button" class="dossier-btn" @click="goInventory">Inventario</button>
+          <button type="button" class="dossier-btn" @click="goTopology">Topologia</button>
+        </div>
+      </div>
+      <p v-if="error" class="dossier-err">{{ error }}</p>
+      <template v-else-if="assetId">
+        <AssetIdentity :asset-id="assetId" />
+        <AssetHabits :asset-id="assetId" wide />
+      </template>
+    </template>
+  </div>
+</template>
+
+<style scoped>
+.dossier {
+  max-width: 980px;
+  margin: 0 auto;
+  padding-bottom: 48px;
+  font-family: var(--inv-mono, ui-monospace, SFMono-Regular, Menlo, monospace);
+  color: var(--inv-text, var(--text));
+}
+.dossier-lead {
+  margin: -0.2rem 0 1rem;
+  font-size: 13px;
+  color: var(--inv-faint, var(--muted));
+}
+.dossier-search {
+  width: 100%;
+  max-width: 36rem;
+  box-sizing: border-box;
+  background: var(--inv-bg-row, var(--panel));
+  border: 1px solid var(--inv-border, var(--line));
+  border-radius: 9px;
+  padding: 10px 14px;
+  color: inherit;
+  font-family: inherit;
+  font-size: 14px;
+  margin-bottom: 1.25rem;
+}
+.dossier-search:focus {
+  outline: none;
+  border-color: var(--inv-green-dim, var(--accent));
+}
+.dossier-sec { margin-top: 1.5rem; }
+.dossier-h {
+  font-size: 11px;
+  letter-spacing: 0.1em;
+  text-transform: uppercase;
+  color: var(--inv-faint, var(--muted));
+  margin: 0 0 0.6rem;
+  font-weight: 500;
+}
+.dossier-hit {
+  display: grid;
+  grid-template-columns: 1fr auto;
+  grid-template-rows: auto auto;
+  gap: 2px 12px;
+  width: 100%;
+  text-align: left;
+  background: var(--inv-bg-row, var(--panel));
+  border: 1px solid var(--inv-border-soft, var(--line));
+  border-radius: 8px;
+  padding: 10px 12px;
+  margin-bottom: 6px;
+  color: inherit;
+  font-family: inherit;
+  cursor: pointer;
+}
+.dossier-hit:hover { border-color: var(--inv-green-dim, var(--accent)); }
+.dossier-hit .name { font-size: 14px; font-weight: 500; grid-column: 1; }
+.dossier-hit .name.unnamed { font-style: italic; color: var(--inv-mut, var(--muted)); font-weight: 400; }
+.dossier-hit .meta { font-size: 12px; color: var(--inv-faint, var(--muted)); grid-column: 1; }
+.dossier-hit .fresh { font-size: 11px; color: var(--inv-mut, var(--muted)); grid-column: 2; grid-row: 1 / span 2; align-self: center; }
+.dossier-muted { font-size: 13px; color: var(--inv-faint, var(--muted)); }
+.dossier-err { color: #c45c5c; font-size: 13px; }
+.dossier-head {
+  display: flex;
+  flex-wrap: wrap;
+  align-items: flex-start;
+  justify-content: space-between;
+  gap: 1rem;
+  margin-bottom: 0.5rem;
+  padding-bottom: 1rem;
+  border-bottom: 1px solid var(--inv-border-soft, var(--line));
+}
+.dossier-back {
+  background: none; border: none; color: var(--inv-green-dim, var(--accent));
+  font-family: inherit; font-size: 12px; padding: 0; cursor: pointer; margin-bottom: 6px;
+}
+.dossier-title {
+  margin: 0; font-size: 1.55rem; font-weight: 600; line-height: 1.2;
+}
+.dossier-title.unnamed { font-style: italic; font-weight: 400; color: var(--inv-mut, var(--muted)); }
+.dossier-sub {
+  margin-top: 6px; font-size: 13px; color: var(--inv-mut, var(--muted));
+  display: flex; flex-wrap: wrap; gap: 0.4rem;
+}
+.dossier-sub .presence {
+  text-transform: uppercase; letter-spacing: 0.04em; font-size: 11px;
+  border: 1px solid var(--inv-border, var(--line)); border-radius: 4px; padding: 1px 6px;
+}
+.dossier-actions { display: flex; gap: 8px; flex-wrap: wrap; }
+.dossier-btn {
+  background: var(--inv-bg-row, var(--panel));
+  border: 1px solid var(--inv-border, var(--line));
+  border-radius: 8px; padding: 7px 12px;
+  color: var(--inv-mut, var(--muted)); font-family: inherit; font-size: 12.5px; cursor: pointer;
+}
+.dossier-btn:hover { border-color: var(--inv-green-dim, var(--accent)); color: var(--inv-text, var(--text)); }
+.mono { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
+</style>
diff --git a/observatory/web/src/views/Inventory.vue b/observatory/web/src/views/Inventory.vue
index b0f3c6b..f62b25c 100644
--- a/observatory/web/src/views/Inventory.vue
+++ b/observatory/web/src/views/Inventory.vue
@@ -71,10 +71,11 @@ const panelIdentity = computed(() =>
 const panelHops = computed(() => (selected.value ? pathHops(selected.value) : []));
 const panelHint = computed(() => (selected.value ? bestNameHint(selected.value) : ""));
 const panelProposals = computed(() => selected.value?.proposals || []);
 const panelFacts = computed(() => selected.value?.fingerprint_facts || []);
 const panelIpBindings = computed(() => selected.value?.ip_bindings || []);
+
 const aiNamingBusy = ref(false);
 
 const IP_ROLES = [
   { value: "", label: "—" },
   { value: "vpn", label: "vpn" },
@@ -139,10 +140,17 @@ function openPanel(device) {
   };
   panelOpen.value = true;
   document.body.classList.add("panel-open");
 }
 
+function openDossierFromPanel() {
+  if (!selected.value?.primaryId) return;
+  const id = selected.value.primaryId;
+  closePanel();
+  router.push(`/dossier/${id}`);
+}
+
 function closePanel() {
   panelOpen.value = false;
   selected.value = null;
   form.value = null;
   document.body.classList.remove("panel-open");
@@ -539,19 +547,31 @@ onUnmounted(() => {
             >
               {{ selected.name || "Device senza nome" }}
             </div>
             <div
               class="inv-p-sub"
-              :title="`${selected.macs[0] || '—'} · ${selected.ip || 'nessun IP'}`"
+              :title="`${selected.stale ? 'non presente' : 'presente'} · ${selected.macs[0] || '—'} · ${selected.ip || 'nessun IP'}`"
             >
-              {{ selected.macs[0] || "—" }}{{ selected.interfaceCount > 1 ? ` +${selected.interfaceCount - 1}` : "" }}
+              <span class="inv-p-presence" :class="selected.stale ? 'stale' : 'present'">
+                {{ selected.stale ? "non presente" : "presente" }}
+              </span>
               · {{ selected.ip || "nessun IP" }}
+              · {{ selected.macs[0] || "—" }}{{ selected.interfaceCount > 1 ? ` +${selected.interfaceCount - 1}` : "" }}
             </div>
           </div>
           <button type="button" class="inv-p-close" aria-label="Chiudi" @click="closePanel">×</button>
         </div>
         <div class="inv-p-body">
+          <div class="inv-p-sec inv-dossier-cta">
+            <button type="button" class="inv-btn primary dossier-open" @click="openDossierFromPanel">
+              Apri Dossier
+            </button>
+            <p class="inv-swnote inv-dossier-hint">
+              identità completa e abitudini di traffico → pagina piena
+            </p>
+          </div>
+
           <div class="inv-p-sec">
             <div class="inv-p-seclabel you"><span>Tu decidi</span><span class="line" /></div>
             <div class="inv-frow">
               <label>Nome</label>
               <input v-model="form.name" type="text" :placeholder="selected.name ? '' : panelHint" />
@@ -916,10 +936,19 @@ onUnmounted(() => {
 .inv-p-name.unnamed { color: var(--inv-mut); font-style: italic; font-weight: 400; }
 .inv-p-sub {
   font-size: 12px; color: var(--inv-faint); margin-top: 3px;
   overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
 }
+.inv-p-presence {
+  font-size: 10px; letter-spacing: 0.05em; text-transform: uppercase;
+  border: 1px solid var(--inv-border); border-radius: 4px; padding: 1px 5px;
+}
+.inv-p-presence.present { border-color: var(--inv-green-dim); color: var(--inv-green); }
+.inv-p-presence.stale { color: var(--inv-faint); }
+.inv-dossier-cta { margin-top: 12px; }
+.inv-dossier-cta .dossier-open { width: 100%; justify-content: center; }
+.inv-dossier-hint { margin-left: 0 !important; margin-top: 6px; }
 .inv-p-close {
   background: none; border: 1px solid var(--inv-border); color: var(--inv-mut);
   border-radius: 8px; width: 40px; height: 40px; min-width: 40px; min-height: 40px;
   cursor: pointer; font-family: inherit; flex: 0 0 auto; font-size: 1.35rem; line-height: 1;
   z-index: 3;
@@ -1015,10 +1044,11 @@ onUnmounted(() => {
 }
 .inv-kv .k { color: var(--inv-faint); }
 .inv-kv .v { color: var(--inv-mut); word-break: break-all; }
 .inv-kv .v b { color: var(--inv-text); font-weight: 500; }
 
+
 .inv-iface {
   display: grid; grid-template-columns: 1fr auto; gap: 10px;
   padding: 6px 0; border-bottom: 1px dashed var(--inv-border-soft); font-size: 12.5px;
 }
 .inv-iface .imac { color: var(--inv-mut); }
diff --git a/observatory/web/src/views/RadarStub.vue b/observatory/web/src/views/RadarStub.vue
new file mode 100644
index 0000000..73072b1
--- /dev/null
+++ b/observatory/web/src/views/RadarStub.vue
@@ -0,0 +1,25 @@
+<script setup>
+import PageHeader from "../components/PageHeader.vue";
+
+defineProps({
+  title: { type: String, required: true },
+  blurb: { type: String, required: true },
+});
+</script>
+
+<template>
+  <div class="radar-stub">
+    <PageHeader :title="title" help="Sezione RADAR in preparazione — contenuto onesto, non una pagina vuota." />
+    <p class="blurb">{{ blurb }}</p>
+  </div>
+</template>
+
+<style scoped>
+.radar-stub { max-width: 40rem; }
+.blurb {
+  margin: 0.5rem 0 0;
+  font-size: 14px;
+  line-height: 1.55;
+  color: var(--inv-mut, var(--muted));
+}
+</style>
```

## Deploy (dopo review)

```bash
cd observatory && ./scripts/deploy.sh api web
```

**STOP pre-deploy.**
