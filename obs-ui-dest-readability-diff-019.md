<!-- BLOCK-ID: OBS-UI-DEST-READABILITY-DIFF-019 -->

# OBS-UI-DEST-READABILITY-DIFF-019 — leggibilità destinazioni Abitudini

**VERSION:** invariata ora (`0.10.8` live) · bump **0.10.9** al deploy  
**STOP DEPLOY** finché `obs-ip-intel-ctx` (run AI context) è in corso — contesa lock DB.  
**Test:** `pytest tests/test_ip_intel.py` → 11 passed · `node --test src/habitsUi.test.js` → 10 passed

## Cosa

1. **Indirizzi speciali** in `special_destination_label` (niente query DB), usati da `enrich_destination_names` prima di ip_intel/asset:
   - broadcast della `network_cidr` configurata → `broadcast LAN` (es. `/22` → `192.168.3.255`; non hardcodato)
   - `255.255.255.255` → `broadcast globale`
   - `239.255.255.250` → `SSDP (discovery UPnP)`
   - `224.0.0.251` → `mDNS (Bonjour)`
   - resto `224.0.0.0/4` → `multicast`
2. **Middle-ellipsis** (FINDING-14) su destinazioni Abitudini: bias coda (~70%) così resta il dominio vendor; `title` = nome pieno. Rimosso `overflow: hidden` CSS che ritagliava di nuovo in coda.

## File

| Path | Ruolo |
|------|--------|
| `api/app/services/ip_intel.py` | label speciali da CIDR |
| `tests/test_ip_intel.py` | assert wording + CIDR non hardcodata |
| `web/src/habitsUi.js` | `middleEllipsis` / `formatHabitsDestName` |
| `web/src/habitsUi.test.js` | coda amazonaws + tencentcos |
| `web/src/views/Inventory.vue` | Abitudini: display + tooltip; CSS no end-clip |
| `CHANGELOG.md` | voce 0.10.9 pending deploy |

## Deploy (dopo fine run AI)

```bash
# sul NAS, solo quando /tmp/ip_intel_context_resume.log dice "done" / pending 0
./scripts/deploy.sh api web
```

## Diff (hunk rilevanti)

```diff
--- a/observatory/api/app/services/ip_intel.py
+++ b/observatory/api/app/services/ip_intel.py
@@ special_destination_label
-            return "broadcast limitato"
+            return "broadcast globale"
         if network_cidr:
             ...
                 if ... addr == net.broadcast_address:
                     return "broadcast LAN"
-        if addr == ipaddress.IPv4Address("239.255.255.250"):
-            return "multicast SSDP"
-        if addr == ipaddress.IPv4Address("224.0.0.251"):
-            return "multicast mDNS"
+        if addr == ipaddress.IPv4Address("239.255.255.250"):
+            return "SSDP (discovery UPnP)"
+        if addr == ipaddress.IPv4Address("224.0.0.251"):
+            return "mDNS (Bonjour)"
         if addr.is_multicast:  # 224.0.0.0/4
             return "multicast"
```

```diff
--- a/observatory/web/src/habitsUi.js
+++ b/observatory/web/src/habitsUi.js
@@ middleEllipsis
-  const head = Math.max(3, Math.floor(budget * 0.35));
-  const tail = Math.max(6, budget - head);
+  const head = Math.max(3, Math.floor(budget * 0.3));
+  const tail = Math.max(8, budget - head);
```

```diff
--- a/observatory/web/src/views/Inventory.vue
+++ b/observatory/web/src/views/Inventory.vue
-  middleEllipsis,
+  formatHabitsDestName,
...
-                      :title="d.dst_name"
-                    >{{ middleEllipsis(d.dst_name) }}</span>
+                      :title="formatHabitsDestName(d.dst_name).full"
+                    >{{ formatHabitsDestName(d.dst_name).display }}</span>
...
-.habits-dst-name {
-  font-size: 11px; color: var(--inv-text); white-space: nowrap;
-  overflow: hidden;
-}
+.habits-dst-name {
+  /* Truncation is middle-ellipsis in JS (FINDING-14); no CSS end-clip. */
+  font-size: 11px; color: var(--inv-text); white-space: nowrap;
+  overflow: visible;
+}
```

```diff
--- a/observatory/tests/test_ip_intel.py
+++ b/observatory/tests/test_ip_intel.py
@@ test_special_destination_labels
-    assert special_destination_label("255.255.255.255", cidr) == "broadcast limitato"
-    assert special_destination_label("239.255.255.250", cidr) == "multicast SSDP"
-    assert special_destination_label("224.0.0.251", cidr) == "multicast mDNS"
+    assert special_destination_label("255.255.255.255", cidr) == "broadcast globale"
+    assert special_destination_label("239.255.255.250", cidr) == "SSDP (discovery UPnP)"
+    assert special_destination_label("224.0.0.251", cidr) == "mDNS (Bonjour)"
+    assert special_destination_label("192.168.1.255", "192.168.1.0/24") == "broadcast LAN"
+    assert special_destination_label("192.168.3.255", "192.168.1.0/24") is None
```

## Note

- `enrich_destination_names` già chiamato da `habits.py` con `get_settings().network_cidr`.
- Nessun rsync/deploy eseguito in questo pezzo (run AI context ancora attivo).
