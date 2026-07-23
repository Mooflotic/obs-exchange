<!-- BLOCK-ID: OBS-DOSSIER-PAGE-DIFF-021 -->

# OBS-DOSSIER-PAGE-DIFF-021 — Dossier pagina piena + sidebar RADAR/MAPPA

**VERSION:** invariata (`0.10.9` live) · bump **0.10.10** al deploy  
**STOP pre-deploy**  
**Test:** `node --test src/dossierRecent.test.js src/habitsUi.test.js` → 11 passed

## Cosa

1. **Estrazione:** `AssetIdentity.vue` + `AssetHabits.vue` — prop `assetId`, fetch autonomo, reset su cambio prop; azioni OS (scan/opt-out) e busy/msg **dentro** Identity.
2. **`/dossier` + `/dossier/:id`:** hub search client-side + ultimi consultati; pagina piena con header + Identity + Habits `wide`.
3. **Sidebar RADAR / MAPPA** — stub onesti Oggi / Osservatorio / Come funziona.
4. **Drawer Inventario** — anteprima (presente/IP/nome) + Tu decidi + **Apri Dossier**; niente Identity/Habits complete.

## File nuovi

- `web/src/components/AssetIdentity.vue`
- `web/src/components/AssetHabits.vue`
- `web/src/views/Dossier.vue`
- `web/src/views/RadarStub.vue`
- `web/src/dossierRecent.js` (+ test)

## Diff (tracked)

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
```

## File nuovi (path)

- `observatory/web/src/components/AssetIdentity.vue` (310 linee)
- `observatory/web/src/components/AssetHabits.vue` (328 linee)
- `observatory/web/src/views/Dossier.vue` (308 linee)
- `observatory/web/src/views/RadarStub.vue` (25 linee)
- `observatory/web/src/dossierRecent.js` (33 linee)
- `observatory/web/src/dossierRecent.test.js` (24 linee)

## Deploy (dopo review)

```bash
# da macchina locale (percorso autorizzato)
cd observatory && ./scripts/deploy.sh api web
# poi bump VERSION → 0.10.10 se non già nel tree
```

**STOP pre-deploy.**
