<!-- BLOCK-ID: OBS-BEHAV-HABITS-CHASSIS-DIFF-013 -->
=== ABITUDINI CHASSIS-AWARE — aggregazione device fisico ===
Data: 2026-07-23
VERSION: invariata (STOP pre-deploy)
Test: pytest test_habits → 12 passed; habitsUi.test → 9 passed

Design:
- Gate resolve invariato; mine WHERE asset_id IN (membri)
- Default scope=chassis se ≥2 membri; ?scope=asset forza NIC
- Coverage = peggiore + motivo composizione
- provenance[] + title/purpose aggregato
- UI: titolo dinamico + «Traffico da: eth #N · wifi #M»

Nota: habitsUi.js può apparire come NEW se 2B non ancora in git HEAD.

diff --git a/observatory/api/app/routers/assets.py b/observatory/api/app/routers/assets.py
index 7c25024..729d5af 100644
--- a/observatory/api/app/routers/assets.py
+++ b/observatory/api/app/routers/assets.py
@@ -10,11 +10,10 @@ from sqlalchemy.orm import Session, joinedload
 from app.auth import audit, check_csrf, require_role, require_user
 from app.config import Settings, get_settings
 from app.db import get_db
 from app.models import Asset, InternetAccessControl, Interface, IpAddress, Monitor, SwitchPort, User
 from app.schemas import AssetOut, AssetUpdate
-from app.services.identity import score_identity
 from app.services.event_maintenance import split_name_proposals
 from app.services.inventory import (
     current_ip,
     is_synthetic_fritz_name,
     ping_ip,
@@ -488,15 +487,99 @@ def get_asset(asset_id: int, db: Session = Depends(get_db), user: User = Depends
         raise HTTPException(404, "Asset non trovato")
     return _serialize(db, asset, with_path=True)
 
 
 @router.get("/{asset_id}/identity")
-def identity(asset_id: int, db: Session = Depends(get_db), user: User = Depends(require_user)):
-    asset = db.get(Asset, asset_id)
+def identity(
+    asset_id: int,
+    technical: bool = Query(False, description="Includi grezzi fingerprint/proposals"),
+    db: Session = Depends(get_db),
+    user: User = Depends(require_user),
+):
+    """Fatti puliti «Chi sei» (+ score/grezzi se technical=1)."""
+    from app.services.asset_identity import build_asset_identity, load_asset_for_identity
+
+    asset = load_asset_for_identity(db, asset_id)
     if not asset:
         raise HTTPException(404, "Asset non trovato")
-    return score_identity(asset)
+    return build_asset_identity(db, asset, include_technical=technical)
+
+
+@router.get("/{asset_id}/habits")
+def habits(
+    asset_id: int,
+    days: int = Query(7, ge=1, le=30),
+    scope: Optional[str] = Query(
+        None,
+        description="chassis|asset — default auto (chassis se ≥2 membri)",
+    ),
+    db: Session = Depends(get_db),
+    user: User = Depends(require_user),
+):
+    """Wave 1a: abitudini di traffico (descrittivo, gate resolve IP@t).
+
+    Con chassis: aggrega flow già risolti ai membri (gate invariato).
+    """
+    from app.services.habits import asset_habits
+
+    if scope is not None and scope not in {"chassis", "asset"}:
+        raise HTTPException(400, "scope deve essere chassis|asset")
+    payload = asset_habits(db, asset_id, days=days, scope=scope)
+    if payload is None:
+        raise HTTPException(404, "Asset non trovato")
+    return payload
+
+
+@router.post("/{asset_id}/scan-os")
+def scan_os(
+    asset_id: int,
+    request: Request,
+    db: Session = Depends(get_db),
+    settings: Settings = Depends(get_settings),
+    user: User = Depends(require_role("operator")),
+):
+    """On-demand OS fingerprint (nmap -O via profilo os_fingerprint). Mai nel discovery."""
+    from app.services.scans import enqueue_on_demand_os_fingerprint
+    from sqlalchemy.orm import joinedload
+
+    check_csrf(request, settings)
+    asset = db.scalar(
+        select(Asset)
+        .where(Asset.id == asset_id)
+        .options(
+            joinedload(Asset.interfaces).joinedload(Interface.addresses),
+            joinedload(Asset.name_proposals),
+        )
+    )
+    if not asset:
+        raise HTTPException(404, "Asset non trovato")
+    result = enqueue_on_demand_os_fingerprint(
+        db, asset, settings=settings, user_id=user.id
+    )
+    if result.get("excluded"):
+        raise HTTPException(409, result.get("message") or "device escluso da OS scan per fragilità")
+    if result.get("unavailable"):
+        raise HTTPException(
+            503, result.get("message") or "OS non disponibile, scanner non privilegiato"
+        )
+    if not result.get("ok"):
+        raise HTTPException(400, result.get("message") or "Impossibile avviare OS scan")
+    from app.services.asset_identity import latest_os_mac_mismatch_attribution
+
+    attribution = latest_os_mac_mismatch_attribution(db, asset_id)
+    if attribution:
+        result["os_attribution"] = attribution
+    audit(
+        db,
+        user=user,
+        action="scan.os_ondemand",
+        entity="asset",
+        entity_id=str(asset_id),
+        detail={"scan_id": result.get("scan_id"), "target": result.get("target")},
+    )
+    db.commit()
+    return result
 
 
 @router.patch("/{asset_id}", response_model=AssetOut)
 def update_asset(
     asset_id: int,
@@ -510,10 +593,11 @@ def update_asset(
     asset = db.get(Asset, asset_id)
     if not asset:
         raise HTTPException(404, "Asset non trovato")
     data = body.model_dump(exclude_unset=True)
     watch_flag = data.pop("watch_fingerprint", None)
+    os_opt_out = data.pop("os_fingerprint_opt_out", None)
     old_crit, old_cat = asset.is_critical, asset.category
     for k, v in data.items():
         setattr(asset, k, v)
     if watch_flag is True:
         from app.services.watch import enable_watch
@@ -525,18 +609,25 @@ def update_asset(
         )
     elif watch_flag is False:
         from app.services.watch import disable_watch
 
         disable_watch(asset)
+    if os_opt_out is not None:
+        from app.services.os_scan_guard import set_os_fingerprint_opt_out
+
+        set_os_fingerprint_opt_out(asset, bool(os_opt_out))
     touch_monitor = ("is_critical" in data and asset.is_critical != old_crit) or (
         "category" in data and asset.category != old_cat
     )
     meta = dict(asset.meta or {})
     overrides = set(meta.get("manual_overrides") or [])
     overrides.update(data)
     if watch_flag is not None:
         overrides.add("watch_fingerprint")
+    if os_opt_out is not None:
+        overrides.add("os_fingerprint_opt_out")
+        meta["os_fingerprint_opt_out"] = bool(os_opt_out)
     meta["manual_overrides"] = sorted(overrides)
     sources = dict(meta.get("field_sources") or {})
     now = datetime.utcnow()
     for field in data:
         sources[field] = {
@@ -548,15 +639,26 @@ def update_asset(
         sources["watch_fingerprint"] = {
             "source": "manuale",
             "confidence": 1.0,
             "last_seen": now.isoformat() + "Z",
         }
+    if os_opt_out is not None:
+        sources["os_fingerprint_opt_out"] = {
+            "source": "manuale",
+            "confidence": 1.0,
+            "last_seen": now.isoformat() + "Z",
+        }
     meta["field_sources"] = sources
     # Re-read watch keys into meta after enable/disable mutated asset.meta
     watch_meta = dict((asset.meta or {}).get("watch") or {})
     if watch_meta:
         meta["watch"] = watch_meta
+    # Keep opt-out if set earlier on asset.meta (watch path may have replaced meta)
+    if os_opt_out is not None:
+        meta["os_fingerprint_opt_out"] = bool(os_opt_out)
+    elif "os_fingerprint_opt_out" in (asset.meta or {}):
+        meta["os_fingerprint_opt_out"] = bool((asset.meta or {}).get("os_fingerprint_opt_out"))
     asset.meta = meta
     asset.updated_at = now
     if touch_monitor:
         from app.services.monitoring import reconcile_asset_monitor
 
@@ -569,11 +671,19 @@ def update_asset(
         db,
         user=user,
         action="asset.update",
         entity="asset",
         entity_id=str(asset.id),
-        detail={**data, **({"watch_fingerprint": watch_flag} if watch_flag is not None else {})},
+        detail={
+            **data,
+            **({"watch_fingerprint": watch_flag} if watch_flag is not None else {}),
+            **(
+                {"os_fingerprint_opt_out": os_opt_out}
+                if os_opt_out is not None
+                else {}
+            ),
+        },
         ip=request.client.host if request.client else "",
     )
     db.commit()
     db.refresh(asset)
     return _serialize(db, asset)
diff --git a/observatory/web/src/views/Inventory.vue b/observatory/web/src/views/Inventory.vue
index b0f3c6b..1d9b0e7 100644
--- a/observatory/web/src/views/Inventory.vue
+++ b/observatory/web/src/views/Inventory.vue
@@ -15,10 +15,26 @@ import {
   pathHops,
   sourceLabel,
 } from "../inventoryDevices";
 import { formatDate } from "../formatTime";
 import PageHeader from "../components/PageHeader.vue";
+import {
+  directionMetaLine,
+  directionSplit,
+  emptyKindMessage,
+  formatBytes,
+  formatDirPair,
+  hourTooltip,
+  hoursToLocalBins,
+  isEmptySilenceKind,
+  portChipLabel,
+  provenanceLine,
+  showDirectionBars,
+  sparklineHeights,
+  visibleDestinations,
+  visiblePorts,
+} from "../habitsUi";
 
 const route = useRoute();
 const router = useRouter();
 const assets = ref([]);
 const chassisPayload = ref({ chassis: [] });
@@ -33,10 +49,19 @@ const selected = ref(null);
 const form = ref(null);
 const savedFlash = ref(false);
 const msg = ref("");
 const busy = ref(false);
 const loading = ref(true);
+const identity = ref(null);
+const identityLoading = ref(false);
+const identityTechnicalOpen = ref(false);
+const osScanBusy = ref(false);
+const osScanMsg = ref("");
+const habits = ref(null);
+const habitsLoading = ref(false);
+const habitsDestExpanded = ref(false);
+const habitsPortsExpanded = ref(false);
 
 const CATEGORIES = [
   "infrastruttura",
   "media",
   "computer",
@@ -71,10 +96,35 @@ const panelIdentity = computed(() =>
 const panelHops = computed(() => (selected.value ? pathHops(selected.value) : []));
 const panelHint = computed(() => (selected.value ? bestNameHint(selected.value) : ""));
 const panelProposals = computed(() => selected.value?.proposals || []);
 const panelFacts = computed(() => selected.value?.fingerprint_facts || []);
 const panelIpBindings = computed(() => selected.value?.ip_bindings || []);
+
+const habitsLocalHours = computed(() => {
+  if (!habits.value?.hours) return [];
+  const tz = habits.value.timezone || "Europe/Rome";
+  return hoursToLocalBins(habits.value.hours, tz);
+});
+const habitsSpark = computed(() => sparklineHeights(habitsLocalHours.value));
+const habitsDestView = computed(() =>
+  visibleDestinations(habits.value?.destinations, habitsDestExpanded.value),
+);
+const habitsPortsView = computed(() =>
+  visiblePorts(habits.value?.ports, habitsPortsExpanded.value),
+);
+const habitsShowBars = computed(() => showDirectionBars(habits.value));
+const habitsDirectionMeta = computed(() => directionMetaLine(habits.value));
+const habitsProvenance = computed(() => provenanceLine(habits.value));
+const habitsEmptyText = computed(() => emptyKindMessage(habits.value?.empty_kind));
+const habitsIsEmptySilence = computed(() => isEmptySilenceKind(habits.value?.empty_kind));
+const habitsIsThin = computed(() => habits.value?.empty_kind === "thin_sample");
+const habitsSectionTitle = computed(() => habits.value?.title || "Abitudini");
+const habitsPurpose = computed(
+  () =>
+    habits.value?.purpose ||
+    "Chi parla, quanto, quando — solo osservato sullo SPAN",
+);
 const aiNamingBusy = ref(false);
 
 const IP_ROLES = [
   { value: "", label: "—" },
   { value: "vpn", label: "vpn" },
@@ -137,16 +187,112 @@ function openPanel(device) {
     watch_fingerprint: !!device.watch_fingerprint,
     notes: device.notes || "",
   };
   panelOpen.value = true;
   document.body.classList.add("panel-open");
+  loadIdentity(device.primaryId);
+  loadHabits(device.primaryId);
+}
+
+async function loadHabits(assetId) {
+  habits.value = null;
+  habitsDestExpanded.value = false;
+  habitsPortsExpanded.value = false;
+  if (!assetId) return;
+  habitsLoading.value = true;
+  try {
+    habits.value = await api.assetHabits(assetId, 7);
+  } catch {
+    habits.value = null;
+    /* non bloccare il pannello: Abitudini è additiva */
+  } finally {
+    habitsLoading.value = false;
+  }
+}
+
+async function loadIdentity(assetId, { technical = identityTechnicalOpen.value } = {}) {
+  if (!assetId) {
+    identity.value = null;
+    return;
+  }
+  identityLoading.value = true;
+  osScanMsg.value = "";
+  try {
+    identity.value = await api.assetIdentity(assetId, technical);
+  } catch (e) {
+    identity.value = null;
+    msg.value = e.message || "Identità non disponibile";
+  } finally {
+    identityLoading.value = false;
+  }
+}
+
+async function toggleIdentityTechnical() {
+  identityTechnicalOpen.value = !identityTechnicalOpen.value;
+  if (!selected.value) return;
+  await loadIdentity(selected.value.primaryId, { technical: identityTechnicalOpen.value });
+}
+
+async function toggleOsProtect() {
+  if (!selected.value || !identity.value || busy.value) return;
+  const current = !!(identity.value.os_scan && identity.value.os_scan.opt_out);
+  const next = !current;
+  busy.value = true;
+  try {
+    await api.updateAsset(selected.value.primaryId, { os_fingerprint_opt_out: next });
+    await loadIdentity(selected.value.primaryId, { technical: identityTechnicalOpen.value });
+  } catch (e) {
+    msg.value = e.message || "Impossibile aggiornare protezione OS";
+  } finally {
+    busy.value = false;
+  }
+}
+
+async function detectOsNow() {
+  if (!selected.value || osScanBusy.value) return;
+  let readiness = identity.value?.scan_readiness || null;
+  try {
+    readiness = await api.scanReadiness("os_fingerprint");
+    if (identity.value) identity.value = { ...identity.value, scan_readiness: readiness };
+  } catch (_) {
+    /* usa readiness già in identity se il refresh fallisce */
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
+    const row = await api.scanAssetOs(selected.value.primaryId);
+    osScanMsg.value =
+      row.os_attribution?.message || row.message || "OS fingerprint accodata";
+    await loadIdentity(selected.value.primaryId, { technical: identityTechnicalOpen.value });
+    if (identity.value?.os_attribution?.message) {
+      osScanMsg.value = identity.value.os_attribution.message;
+    }
+  } catch (e) {
+    osScanMsg.value = e.message || "OS scan non avviata";
+  } finally {
+    osScanBusy.value = false;
+  }
 }
 
 function closePanel() {
   panelOpen.value = false;
   selected.value = null;
   form.value = null;
+  identity.value = null;
+  identityTechnicalOpen.value = false;
+  osScanMsg.value = "";
+  habits.value = null;
+  habitsLoading.value = false;
+  habitsDestExpanded.value = false;
+  habitsPortsExpanded.value = false;
   document.body.classList.remove("panel-open");
 }
 
 function onKey(e) {
   if (e.key === "Escape" && panelOpen.value) closePanel();
@@ -599,10 +745,230 @@ onUnmounted(() => {
             <div class="inv-swnote">
               all'avvistamento accoda OS fingerprint prioritario; nessun blocco
             </div>
           </div>
 
+          <div class="inv-p-sec inv-chi-sei">
+            <div class="inv-p-seclabel"><span>Chi sei</span><span class="line" /></div>
+            <p class="inv-purpose">Chi è questo device — identità osservata</p>
+            <div v-if="identityLoading" class="inv-p-note-sugg">caricamento…</div>
+            <template v-else-if="identity">
+              <div class="inv-kv inv-identity-kv">
+                <span class="k">Vendor</span>
+                <span class="v">
+                  {{ identity.labels.vendor }}
+                  <span
+                    v-if="identity.vendor && !identity.vendor_reliable"
+                    class="badge-privacy"
+                    title="MAC locally-administered: OUI non affidabile"
+                  >privacy</span>
+                </span>
+                <span class="k">OS</span>
+                <span
+                  class="v"
+                  :class="{
+                    'os-mac-mismatch': identity.os_attribution?.kind === 'mac_mismatch',
+                    'os-chassis-sibling': identity.os_attribution?.kind === 'chassis_sibling',
+                  }"
+                  :title="identity.os_attribution?.message || undefined"
+                >{{ identity.labels.os }}</span>
+                <span class="k">Hostname</span><span class="v">{{ identity.labels.hostname }}</span>
+                <span class="k">Servizi</span><span class="v">{{ identity.labels.services }}</span>
+                <span class="k">Tipo</span><span class="v">{{ identity.labels.device_type }}</span>
+                <span class="k">MAC</span>
+                <span class="v">
+                  {{ identity.labels.mac }}
+                  <span v-if="identity.is_private" class="badge-privacy">U/L</span>
+                </span>
+                <span class="k">Prima volta</span><span class="v">{{ fmtSeen(identity.first_seen) || identity.labels.first_seen }}</span>
+                <span class="k">Presence</span><span class="v">{{ identity.labels.presence }}</span>
+              </div>
+              <div
+                class="inv-switchrow"
+                :class="{ on: identity.os_scan && identity.os_scan.opt_out }"
+                @click="toggleOsProtect"
+              >
+                <span class="sw" /><span class="swlbl">Proteggi da scansione OS (device fragile)</span>
+              </div>
+              <div class="inv-swnote">
+                <template v-if="identity.os_scan && identity.os_scan.opt_out_source === 'default_device_type'">
+                  suggerito: tipo «{{ identity.os_scan.device_type }}» — puoi togliere la spunta
+                </template>
+                <template v-else-if="identity.os_scan && identity.os_scan.opt_out_explicit">
+                  scelta salvata sul device
+                </template>
+                <template v-else>
+                  gli IoT/media restano protetti di default; nessun brand in codice
+                </template>
+              </div>
+              <div class="inv-os-actions">
+                <span
+                  v-if="identity.scan_readiness"
+                  class="scan-sema"
+                  :class="identity.scan_readiness.level"
+                  :title="identity.scan_readiness.reason"
+                >
+                  <span class="dot" aria-hidden="true" />
+                  <span class="sema-label">{{ identity.scan_readiness.labels?.level || identity.scan_readiness.level }}</span>
+                </span>
+                <button
+                  type="button"
+                  class="inv-btn"
+                  :disabled="
+                    osScanBusy ||
+                    busy ||
+                    (identity.os_scan && identity.os_scan.excluded) ||
+                    (identity.os_scan && identity.os_scan.os_detection_available === false)
+                  "
+                  @click="detectOsNow"
+                >
+                  {{ osScanBusy ? "Scansione…" : "Rileva OS ora" }}
+                </button>
+                <span
+                  v-if="identity.os_scan && identity.os_scan.excluded"
+                  class="inv-os-excl"
+                >{{ identity.os_scan.message || "escluso (IoT fragile)" }}</span>
+                <span
+                  v-else-if="identity.os_scan && identity.os_scan.os_detection_available === false"
+                  class="inv-os-excl"
+                >{{ identity.os_scan.unavailable_message || "OS non disponibile, scanner non privilegiato" }}</span>
+                <span v-else-if="osScanMsg" class="inv-os-msg">{{ osScanMsg }}</span>
+              </div>
+              <p
+                v-if="identity.scan_readiness"
+                class="scan-sema-reason"
+              >{{ identity.scan_readiness.reason }}</p>
+              <button type="button" class="inv-btn ghost" @click="toggleIdentityTechnical">
+                {{ identityTechnicalOpen ? "Nascondi dettagli tecnici" : "Mostra dettagli tecnici" }}
+              </button>
+              <pre
+                v-if="identityTechnicalOpen && identity.technical"
+                class="inv-tech"
+              >{{ JSON.stringify(identity.technical, null, 2) }}</pre>
+            </template>
+            <div v-else class="inv-p-note-sugg">— identità non disponibile</div>
+          </div>
+
+          <div class="inv-p-sec inv-habits">
+            <div class="inv-p-seclabel"><span>{{ habitsSectionTitle }}</span><span class="line" /></div>
+            <p class="inv-purpose">{{ habitsPurpose }}</p>
+            <div v-if="habitsLoading" class="inv-p-note-sugg">caricamento…</div>
+            <template v-else-if="habits">
+              <div
+                class="habits-cov"
+                :class="habits.coverage?.state || 'sconosciuto'"
+                :title="habits.coverage?.reason || undefined"
+              >
+                <span class="habits-cov-dot" aria-hidden="true" />
+                <span class="habits-cov-label">{{ habits.coverage?.label || "Traffico: copertura sconosciuta" }}</span>
+              </div>
+              <p v-if="habits.coverage?.reason" class="habits-cov-reason">{{ habits.coverage.reason }}</p>
+              <p v-if="habitsProvenance" class="habits-meta habits-prov">{{ habitsProvenance }}</p>
+              <p v-if="habitsDirectionMeta" class="habits-meta">{{ habitsDirectionMeta }}</p>
+
+              <template v-if="habitsIsEmptySilence">
+                <p class="habits-empty">{{ habitsEmptyText }}</p>
+              </template>
+              <template v-else>
+                <div class="habits-block">
+                  <div class="habits-block-h">Con chi parla</div>
+                  <p
+                    v-if="habitsShowBars"
+                    class="habits-legend"
+                  >out = verso destinazione · in = dalla destinazione</p>
+                  <p
+                    v-else-if="(habits.direction_sample_ratio || 0) > 0 && (habits.direction_sample_ratio || 0) < 0.2"
+                    class="habits-legend"
+                  >direzione ancora scarsa</p>
+                  <div v-if="!habitsDestView.shown.length" class="inv-p-note-sugg">— nessuna destinazione</div>
+                  <div
+                    v-for="d in habitsDestView.shown"
+                    :key="d.dst_ip"
+                    class="habits-dst"
+                  >
+                    <div class="habits-dst-id">
+                      <span v-if="d.dst_name" class="habits-dst-name">{{ d.dst_name }}</span>
+                      <span class="habits-dst-ip mono">{{ d.dst_ip }}</span>
+                    </div>
+                    <div class="habits-dst-dir">
+                      <template v-if="habitsShowBars && directionSplit(d)">
+                        <span class="habits-dir-lbl out">out</span>
+                        <div class="habits-bar" aria-hidden="true">
+                          <span class="seg out" :style="{ width: directionSplit(d).outPct + '%' }" />
+                          <span class="seg in" :style="{ width: directionSplit(d).inPct + '%' }" />
+                        </div>
+                        <span class="habits-dir-lbl in">in</span>
+                        <span class="habits-dir-pair mono">{{ formatDirPair(d) }}</span>
+                      </template>
+                      <template v-else>
+                        <span class="habits-vol mono">{{ formatBytes(d.bytes) }}</span>
+                        <span class="habits-dir-na">—</span>
+                      </template>
+                    </div>
+                  </div>
+                  <button
+                    v-if="habitsDestView.hidden > 0"
+                    type="button"
+                    class="habits-more"
+                    @click="habitsDestExpanded = true"
+                  >+{{ habitsDestView.hidden }} altre</button>
+                </div>
+
+                <div class="habits-block">
+                  <div class="habits-volrow">
+                    <span class="habits-block-h">Volume {{ habits.window_days || 7 }}g</span>
+                    <span class="habits-vol-total mono">{{ formatBytes(habits.totals?.bytes) }}</span>
+                    <span v-if="habitsIsThin" class="habits-thin">campione ancora sottile</span>
+                  </div>
+                  <div class="habits-when">
+                    <span class="habits-when-lbl">Quando</span>
+                    <div class="habits-spark" role="img" aria-label="Volume per ora">
+                      <span
+                        v-for="(bin, i) in habitsLocalHours"
+                        :key="bin.hour"
+                        class="habits-spark-cell"
+                        :title="hourTooltip(bin)"
+                      >
+                        <span
+                          class="habits-spark-bar"
+                          :style="{ height: (habitsSpark[i] * 100) + '%' }"
+                        />
+                      </span>
+                    </div>
+                    <div class="habits-spark-axis mono">
+                      <span>0</span><span>6</span><span>12</span><span>18</span><span>23</span>
+                    </div>
+                    <p class="habits-tz">ore {{ habits.timezone || "Europe/Rome" }}</p>
+                  </div>
+                </div>
+
+                <div class="habits-block">
+                  <div class="habits-block-h">Porte</div>
+                  <div class="habits-ports">
+                    <span
+                      v-for="p in habitsPortsView.shown"
+                      :key="`${p.proto}-${p.port}`"
+                      class="habits-port-chip mono"
+                      :title="`${formatBytes(p.bytes)} · ${p.samples} oss.`"
+                    >{{ portChipLabel(p) }}</span>
+                    <button
+                      v-if="habitsPortsView.hidden > 0"
+                      type="button"
+                      class="habits-more"
+                      @click="habitsPortsExpanded = true"
+                    >mostra tutte</button>
+                    <span
+                      v-if="!habitsPortsView.shown.length"
+                      class="inv-p-note-sugg"
+                    >—</span>
+                  </div>
+                </div>
+              </template>
+            </template>
+            <div v-else class="inv-p-note-sugg">— abitudini non disponibili</div>
+          </div>
+
           <div class="inv-p-sec">
             <div class="inv-p-seclabel"><span>Indirizzi IP</span><span class="line" /></div>
             <div v-if="!panelIpBindings.length" class="inv-p-note-sugg">— nessun binding IP</div>
             <div
               v-for="b in panelIpBindings"
@@ -1015,10 +1381,169 @@ onUnmounted(() => {
 }
 .inv-kv .k { color: var(--inv-faint); }
 .inv-kv .v { color: var(--inv-mut); word-break: break-all; }
 .inv-kv .v b { color: var(--inv-text); font-weight: 500; }
 
+.inv-purpose {
+  margin: 0 0 10px; font-size: 12px; color: var(--inv-faint); line-height: 1.35;
+}
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
+.inv-btn.ghost {
+  background: transparent; border-style: dashed; margin-top: 4px;
+}
+.inv-tech {
+  margin: 8px 0 0; padding: 10px; max-height: 220px; overflow: auto;
+  font-size: 10.5px; line-height: 1.35; color: var(--inv-faint);
+  background: var(--inv-bg-row); border: 1px solid var(--inv-border-soft);
+  border-radius: 6px; white-space: pre-wrap; word-break: break-word;
+}
+
+/* —— Abitudini (Wave 1a 2B) —— */
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
+.habits-meta {
+  margin: 8px 0 0; font-size: 11.5px; color: var(--inv-mut);
+}
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
+.habits-dst-id { min-width: 0; display: flex; flex-direction: column; gap: 1px; }
+.habits-dst-name {
+  font-size: 11px; color: var(--inv-text); white-space: nowrap;
+  overflow: hidden; text-overflow: ellipsis;
+}
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
+  display: flex; flex-wrap: wrap; align-items: baseline; gap: 8px 12px;
+  margin-bottom: 8px;
+}
+.habits-vol-total { font-size: 14px; color: var(--inv-text); }
+.habits-thin {
+  font-size: 11px; color: var(--inv-amber); letter-spacing: 0.02em;
+}
+.habits-when { margin-top: 4px; }
+.habits-when-lbl {
+  display: block; font-size: 11px; color: var(--inv-faint); margin-bottom: 4px;
+}
+.habits-spark {
+  display: flex; align-items: flex-end; gap: 2px; height: 36px;
+  padding: 0 1px;
+}
+.habits-spark-cell {
+  flex: 1; height: 100%; display: flex; align-items: flex-end;
+  cursor: default;
+}
+.habits-spark-bar {
+  width: 100%; min-height: 0; background: var(--inv-green-dim);
+  border-radius: 1px 1px 0 0;
+}
+.habits-spark-cell:hover .habits-spark-bar { background: var(--inv-green); }
+.habits-spark-axis {
+  display: flex; justify-content: space-between;
+  font-size: 9.5px; color: var(--inv-faint); margin-top: 3px; padding: 0 1px;
+}
+.habits-tz {
+  margin: 4px 0 0; font-size: 10.5px; color: var(--inv-faint);
+}
+.habits-ports { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
+.habits-port-chip {
+  font-size: 11px; color: var(--inv-mut);
+  border: 1px solid var(--inv-border); border-radius: 5px;
+  padding: 2px 7px; background: var(--inv-bg-row);
+}
+
 .inv-iface {
   display: grid; grid-template-columns: 1fr auto; gap: 10px;
   padding: 6px 0; border-bottom: 1px dashed var(--inv-border-soft); font-size: 12.5px;
 }
 .inv-iface .imac { color: var(--inv-mut); }

=== NEW FILE: observatory/web/src/habitsUi.js ===
diff --git a/observatory/web/src/habitsUi.js b/observatory/web/src/habitsUi.js
new file mode 100644
index 0000000..8d7cd04
--- /dev/null
+++ b/observatory/web/src/habitsUi.js
@@ -0,0 +1,172 @@
+/** Wave 1a Parte 2B — presentazione Abitudini (descrittivo, niente giudizi). */
+
+import { formatBytes } from "./spanUi.js";
+
+export const HABITS_VISIBLE_DEST = 8;
+export const HABITS_VISIBLE_PORTS = 5;
+export const HABITS_DIR_RATIO_MIN = 0.2;
+
+export const EMPTY_KIND_TEXT = {
+  silence_observed:
+    "Nessun flusso osservato in 7 giorni. Con copertura completa, questo è silenzio osservato sullo SPAN.",
+  maybe_unmirrored:
+    "Nessun flusso in 7 giorni. Può esserci traffico non mirrorato (es. WiFi↔WiFi).",
+  unknown_gap:
+    "Nessun flusso in 7 giorni — non sappiamo se il device è quieto o fuori dallo SPAN.",
+};
+
+export { formatBytes };
+
+export function emptyKindMessage(emptyKind) {
+  if (!emptyKind) return null;
+  return EMPTY_KIND_TEXT[emptyKind] || null;
+}
+
+export function isEmptySilenceKind(emptyKind) {
+  return (
+    emptyKind === "silence_observed" ||
+    emptyKind === "maybe_unmirrored" ||
+    emptyKind === "unknown_gap"
+  );
+}
+
+/** Format direction_since ISO for the meta line (short date). */
+export function formatDirectionSince(iso) {
+  if (!iso) return "";
+  const d = new Date(iso);
+  if (Number.isNaN(d.getTime())) return "";
+  return new Intl.DateTimeFormat("it-IT", {
+    timeZone: "Europe/Rome",
+    day: "numeric",
+    month: "short",
+    year: "numeric",
+  }).format(d);
+}
+
+export function directionMetaLine(habits) {
+  if (!habits) return null;
+  const ratio = Number(habits.direction_sample_ratio) || 0;
+  if (ratio <= 0) return null;
+  const pct = Math.round(ratio * 100);
+  const since = formatDirectionSince(habits.direction_since);
+  if (since) {
+    return `Direzione dal ${since} · ${pct}% delle osservazioni`;
+  }
+  return `Direzione · ${pct}% delle osservazioni`;
+}
+
+/** "Traffico da: eth #51 (90 oss) · wifi #30 (0 oss)" */
+export function provenanceLine(habits) {
+  const list = Array.isArray(habits?.provenance) ? habits.provenance : [];
+  if (!list.length || habits?.scope !== "chassis") return null;
+  const parts = list.map((p) => {
+    const media = p.media || "iface";
+    const n = Number(p.samples) || 0;
+    return `${media} #${p.asset_id} (${n} oss)`;
+  });
+  return `Traffico da: ${parts.join(" · ")}`;
+}
+
+/**
+ * Remap UTC hour bins → dense 0–23 in Europe/Rome (or given tz).
+ * Same-calendar-day UTC anchors; DST handled by Intl.
+ */
+export function hoursToLocalBins(hours, timezone = "Europe/Rome", refDate = new Date()) {
+  const local = Array.from({ length: 24 }, (_, hour) => ({
+    hour,
+    bytes: 0,
+    samples: 0,
+  }));
+  const y = refDate.getUTCFullYear();
+  const m = refDate.getUTCMonth();
+  const day = refDate.getUTCDate();
+  for (const bin of hours || []) {
+    const utcH = Number(bin.hour);
+    if (!Number.isFinite(utcH) || utcH < 0 || utcH > 23) continue;
+    const d = new Date(Date.UTC(y, m, day, utcH, 0, 0));
+    let localH = Number(
+      new Intl.DateTimeFormat("en-GB", {
+        timeZone: timezone,
+        hour: "numeric",
+        hour12: false,
+      }).format(d),
+    );
+    if (localH === 24) localH = 0;
+    if (!Number.isFinite(localH) || localH < 0 || localH > 23) continue;
+    local[localH].bytes += Number(bin.bytes) || 0;
+    local[localH].samples += Number(bin.samples) || 0;
+  }
+  return local;
+}
+
+export function hourTooltip(bin) {
+  const h = String(bin.hour).padStart(2, "0");
+  return `${h}:00 · ${formatBytes(bin.bytes)} · ${bin.samples} oss.`;
+}
+
+export function sparklineHeights(bins) {
+  const max = Math.max(0, ...bins.map((b) => Number(b.bytes) || 0));
+  return bins.map((b) => {
+    const n = Number(b.bytes) || 0;
+    if (max <= 0 || n <= 0) return 0;
+    return Math.max(0.08, n / max);
+  });
+}
+
+/** Whether destination rows may show out|in bars. */
+export function showDirectionBars(habits) {
+  const ratio = Number(habits?.direction_sample_ratio);
+  return Number.isFinite(ratio) && ratio >= HABITS_DIR_RATIO_MIN;
+}
+
+/**
+ * Split bar fractions for Opzione A. Null if row has no direction data.
+ * Returns { outPct, inPct } in 0–100 of the directed subset.
+ */
+export function directionSplit(dest) {
+  const out = dest?.bytes_out;
+  const inn = dest?.bytes_in;
+  if (out == null || inn == null) return null;
+  const o = Number(out);
+  const i = Number(inn);
+  if (!Number.isFinite(o) || !Number.isFinite(i) || o < 0 || i < 0) return null;
+  const sum = o + i;
+  if (sum <= 0) return { outPct: 50, inPct: 50 };
+  return {
+    outPct: (o / sum) * 100,
+    inPct: (i / sum) * 100,
+  };
+}
+
+export function formatDirPair(dest) {
+  if (dest?.bytes_out == null || dest?.bytes_in == null) return null;
+  return `${formatBytes(dest.bytes_out)} | ${formatBytes(dest.bytes_in)}`;
+}
+
+export function visibleDestinations(destinations, expanded) {
+  const list = Array.isArray(destinations) ? destinations : [];
+  if (expanded || list.length <= HABITS_VISIBLE_DEST) {
+    return { shown: list, hidden: 0 };
+  }
+  return {
+    shown: list.slice(0, HABITS_VISIBLE_DEST),
+    hidden: list.length - HABITS_VISIBLE_DEST,
+  };
+}
+
+export function visiblePorts(ports, expanded) {
+  const list = Array.isArray(ports) ? ports : [];
+  if (expanded || list.length <= HABITS_VISIBLE_PORTS) {
+    return { shown: list, hidden: 0 };
+  }
+  return {
+    shown: list.slice(0, HABITS_VISIBLE_PORTS),
+    hidden: list.length - HABITS_VISIBLE_PORTS,
+  };
+}
+
+export function portChipLabel(port) {
+  const p = port?.port ?? "?";
+  const proto = (port?.proto || "").toLowerCase();
+  return proto && proto !== "tcp" ? `${p}/${proto}` : String(p);
+}

=== NEW FILE: observatory/web/src/habitsUi.test.js ===
diff --git a/observatory/web/src/habitsUi.test.js b/observatory/web/src/habitsUi.test.js
new file mode 100644
index 0000000..b69ff65
--- /dev/null
+++ b/observatory/web/src/habitsUi.test.js
@@ -0,0 +1,107 @@
+import assert from "node:assert/strict";
+import { test } from "node:test";
+import {
+  EMPTY_KIND_TEXT,
+  directionMetaLine,
+  directionSplit,
+  emptyKindMessage,
+  formatDirectionSince,
+  hoursToLocalBins,
+  hourTooltip,
+  isEmptySilenceKind,
+  provenanceLine,
+  showDirectionBars,
+  sparklineHeights,
+  visibleDestinations,
+  visiblePorts,
+} from "./habitsUi.js";
+
+test("empty_kind testi esatti §7", () => {
+  assert.equal(
+    emptyKindMessage("silence_observed"),
+    EMPTY_KIND_TEXT.silence_observed,
+  );
+  assert.match(emptyKindMessage("silence_observed"), /silenzio osservato sullo SPAN/);
+  assert.match(emptyKindMessage("maybe_unmirrored"), /non mirrorato/);
+  assert.match(emptyKindMessage("unknown_gap"), /non sappiamo/);
+  assert.equal(emptyKindMessage("thin_sample"), null);
+  assert.equal(isEmptySilenceKind("silence_observed"), true);
+  assert.equal(isEmptySilenceKind("thin_sample"), false);
+});
+
+test("directionSplit Opzione A proporzioni", () => {
+  const s = directionSplit({ bytes_out: 400_000, bytes_in: 3_600_000 });
+  assert.ok(s);
+  assert.ok(Math.abs(s.outPct - 10) < 0.01);
+  assert.ok(Math.abs(s.inPct - 90) < 0.01);
+  assert.equal(directionSplit({ bytes_out: null, bytes_in: 1 }), null);
+  assert.equal(directionSplit({ bytes_out: 1, bytes_in: null }), null);
+});
+
+test("showDirectionBars soglia 0.20", () => {
+  assert.equal(showDirectionBars({ direction_sample_ratio: 0.19 }), false);
+  assert.equal(showDirectionBars({ direction_sample_ratio: 0.2 }), true);
+  assert.equal(showDirectionBars({ direction_sample_ratio: 0 }), false);
+});
+
+test("hoursToLocalBins remappa UTC → Europe/Rome", () => {
+  // Winter-ish: use a fixed January UTC date so CET = UTC+1
+  const ref = new Date(Date.UTC(2026, 0, 15, 12, 0, 0));
+  const bins = hoursToLocalBins(
+    [{ hour: 20, bytes: 12_000_000, samples: 34 }],
+    "Europe/Rome",
+    ref,
+  );
+  assert.equal(bins[21].bytes, 12_000_000);
+  assert.equal(bins[21].samples, 34);
+  assert.equal(bins[20].bytes, 0);
+  assert.equal(hourTooltip(bins[21]), "21:00 · 12 MB · 34 oss.");
+});
+
+test("sparklineHeights normalizza su max", () => {
+  const h = sparklineHeights([
+    { bytes: 0 },
+    { bytes: 50 },
+    { bytes: 100 },
+  ]);
+  assert.equal(h[0], 0);
+  assert.equal(h[2], 1);
+  assert.ok(h[1] > 0 && h[1] < 1);
+});
+
+test("visibleDestinations max 8 + hidden", () => {
+  const list = Array.from({ length: 12 }, (_, i) => ({ dst_ip: `1.1.1.${i}` }));
+  const { shown, hidden } = visibleDestinations(list, false);
+  assert.equal(shown.length, 8);
+  assert.equal(hidden, 4);
+  assert.equal(visibleDestinations(list, true).hidden, 0);
+});
+
+test("visiblePorts max 5", () => {
+  const list = Array.from({ length: 8 }, (_, i) => ({ port: i }));
+  assert.equal(visiblePorts(list, false).shown.length, 5);
+  assert.equal(visiblePorts(list, false).hidden, 3);
+});
+
+test("directionMetaLine solo se ratio > 0", () => {
+  assert.equal(directionMetaLine({ direction_sample_ratio: 0 }), null);
+  const line = directionMetaLine({
+    direction_sample_ratio: 0.38,
+    direction_since: "2026-07-23T00:00:00Z",
+  });
+  assert.match(line, /Direzione dal/);
+  assert.match(line, /38% delle osservazioni/);
+  assert.ok(formatDirectionSince("2026-07-23T00:00:00Z"));
+});
+
+test("provenanceLine solo scope chassis", () => {
+  assert.equal(provenanceLine({ scope: "asset", provenance: [{ asset_id: 1, media: "eth", samples: 3 }] }), null);
+  const line = provenanceLine({
+    scope: "chassis",
+    provenance: [
+      { asset_id: 51, media: "eth", samples: 90 },
+      { asset_id: 30, media: "wifi", samples: 0 },
+    ],
+  });
+  assert.equal(line, "Traffico da: eth #51 (90 oss) · wifi #30 (0 oss)");
+});
