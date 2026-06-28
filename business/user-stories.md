# user-stories.md  

## Epic 1 – Device Provisioning & Management  

| # | User Story | Acceptance Criteria | Complexity |
|---|------------|---------------------|------------|
| 1 | **As an IT administrator, I want to add a new access‑point to the fleet via a QR‑code scan, so that I can onboard hardware without manual IP configuration.** | - QR code contains a unique device token and default Wi‑Fi credentials.<br>- Scanning the code from the web UI automatically registers the AP and assigns it a temporary admin password.<br>- The AP appears in the “Unassigned Devices” list within 30 seconds.<br>- Admin can rename the device and move it to a logical group. | S |
| 2 | **As a network operator, I want to view all deployed APs on a geographic map, so that I can quickly locate devices that are offline or mis‑placed.** | - Map shows icons for each AP with status colors (green = online, red = offline, yellow = warning).<br>- Clicking an icon opens a tooltip with device name, firmware version, and last‑seen timestamp.<br>- Filter by site, group, or firmware version.<br>- Map refreshes automatically every 60 seconds. | M |
| 3 | **As a support engineer, I want to push a firmware upgrade to a selected subset of APs, so that I can roll out updates safely.** | - UI allows selection by group, tag, or version range.<br>- Upgrade can be scheduled or executed immediately.<br>- Progress bar shows per‑device status (queued, downloading, installing, rebooting, success/failure).<br>- Rollback option is available if > 10 % of devices report failure. | M |

---

## Epic 2 – Network Configuration (VLAN & SSID)  

| # | User Story | Acceptance Criteria | Complexity |
|---|------------|---------------------|------------|
| 4 | **As a network admin, I want to create multiple SSIDs with custom authentication methods, so that different user groups (staff, guests, IoT) have isolated access.** | - UI form to add SSID name, security type (WPA2‑Enterprise, WPA2‑PSK, Open), and optional RADIUS server settings.<br>- New SSID appears in the AP broadcast list within 15 seconds of saving.<br>- Validation prevents duplicate SSID names on the same site.<br>- Each SSID can be enabled/disabled per‑site. | M |
| 5 | **As a security officer, I want to map each SSID to a specific VLAN ID, so that traffic is segmented at Layer 2.** | - After SSID creation, a dropdown lets the admin select a VLAN ID (1‑4094).<br>- The mapping is stored in the AP configuration and pushed to devices instantly.<br>- AP confirms the mapping via a status API call.<br>- UI displays a matrix view of SSID ↔ VLAN mappings for audit. | S |
| 6 | **As a compliance auditor, I want to export the current SSID‑to‑VLAN configuration as a CSV file, so that I can review it against policy documents.** | - Export button generates a CSV with columns: Site, AP Group, SSID, VLAN ID, Security Type, Last Modified.<br>- File download starts within 5 seconds.<br>- Export respects the current filter view (e.g., only selected sites).<br>- File includes a timestamp and hash for integrity verification. | S |

---

## Epic 3 – Mesh Networking & Performance  

| # | User Story | Acceptance Criteria | Complexity |
|---|------------|---------------------|------------|
| 7 | **As a facilities manager, I want the system to automatically form a mesh topology between nearby APs, so that coverage gaps are filled without manual wiring.** | - APs broadcast mesh‑join beacons on a dedicated backhaul channel.<br>- When two APs detect each other, they negotiate a link and update the topology map.<br>- Mesh links are displayed in the UI with link quality (RSSI, throughput).<br>- Admin can manually disable/enable mesh links per device. | L |
| 8 | **As a network engineer, I want to set a minimum backhaul bandwidth threshold for mesh links, so that low‑quality links are automatically pruned.** | - UI slider to define “Min Backhaul Mbps” (default 50 Mbps).<br>- System monitors each mesh link and disables any that fall below the threshold for > 30 seconds.<br>- Disabled links are logged and an alert is generated.<br>- Re‑enable can be manual or automatic after link recovers. | M |
| 9 | **As a user experience analyst, I want real‑time heat‑maps of client signal strength across the mesh, so that I can identify dead zones.** | - APs report client RSSI values every 10 seconds.<br>- UI renders a floor‑plan overlay heat‑map with color gradients (green = strong, red = weak).<br>- Heat‑map can be filtered by SSID and time window.<br>- Exportable as PNG or PDF for reporting. | L |

---

## Epic 4 – Security & Monitoring  

| # | User Story | Acceptance Criteria | Complexity |
|---|------------|---------------------|------------|
| 10 | **As a SOC analyst, I want to receive alerts when an unauthorized device attempts to connect to any SSID, so that I can investigate potential breaches.** | - APs send authentication failure events to the central event bus.<br>- Alert rule triggers if > 5 failures from the same MAC within 2 minutes.<br>- Alert appears in the dashboard with device MAC, SSID, timestamp, and location.<br>- Integration hook for Slack/Webhook is configurable. | M |
| 11 | **As a compliance officer, I want audit logs of all configuration changes (SSID, VLAN, mesh links), so that I can prove change‑control adherence.** | - Every change creates an immutable log entry with user ID, timestamp, before/after values, and affected device IDs.<br>- Logs are stored in tamper‑evident storage for at least 1 year.<br>- UI provides searchable view with export to CSV.<br>- API endpoint allows SIEM ingestion. | S |
| 12 | **As a network admin, I want to enable “guest captive‑portal” authentication per SSID, so that visitors must accept terms before gaining internet access.** | - Captive‑portal can be toggled per SSID in the UI.<br>- When enabled, first HTTP request from a client is redirected to a customizable landing page.<br>- Admin can set terms of service text and optional email capture.<br>- Successful acceptance updates the client’s VLAN mapping to the guest VLAN. | M |