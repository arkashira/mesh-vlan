# STORIES.md
**Project:** mesh‑vlan  
**Owner:** Axentx – Product Engineering Lead  
**Target Release:** MVP (v0.1) → Feature‑Complete (v1.0)  

---  

## Table of Contents
1. [Epics Overview](#epics-overview)  
2. [User Story Backlog](#user-story-backlog)  
   - [Epic 1 – Core Access‑Point Engine](#epic‑1)  
   - [Epic 2 – VLAN & SSID Management](#epic‑2)  
   - [Epic 3 – Mesh Networking](#epic‑3)  
   - [Epic 4 – Administration UI](#epic‑4)  
   - [Epic 5 – Deployment & Operations](#epic‑5)  
3. [Prioritisation & MVP Scope](#prioritisation--mvp-scope)  

---  

## Epics Overview
| Epic | Description | MVP Inclusion |
|------|-------------|---------------|
| **E1** | **Core Access‑Point Engine** – Initialise hardware, provide Wi‑Fi radio control, expose basic AP functionality. | ✅ |
| **E2** | **VLAN & SSID Management** – Create multiple SSIDs, map each to a VLAN, enforce isolation. | ✅ |
| **E3** | **Mesh Networking** – Auto‑discover neighbouring nodes, form a resilient mesh, propagate VLAN/SSID config. | ✅ |
| **E4** | **Administration UI** – Simple web UI for provisioning, monitoring, and troubleshooting. | ✅ |
| **E5** | **Deployment & Operations** – Packaging, OTA updates, logging, health checks, and basic analytics. | ✅ (post‑MVP) |

---  

## User Story Backlog  

### Epic 1 – Core Access‑Point Engine
| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| **1.1** | **As a** System Engineer, **I want** the firmware to detect and initialise the Wi‑Fi radio on boot, **so that** the device is ready to serve clients without manual intervention. | 1. Radio driver loads within 5 s of power‑on.<br>2. `ifconfig` shows a valid interface (`wlan0`).<br>3. Log entry `Radio initialized` appears in syslog. |
| **1.2** | **As a** Network Administrator, **I want** the AP to broadcast a default SSID (`mesh‑vlan‑setup`) with open authentication, **so that** I can connect for initial configuration. | 1. SSID appears in Wi‑Fi scans within 3 s of boot.<br>2. No encryption (open) and uses channel 1‑11 auto‑selection.<br>3. Devices can obtain an IP via DHCP from the AP. |
| **1.3** | **As a** Firmware Engineer, **I want** a health‑check endpoint (`/healthz`) exposing `OK`/`FAIL` status, **so that** orchestration tools can monitor device liveness. | 1. HTTP GET `/healthz` returns `200 OK` with JSON `{status:"OK"}` when all subsystems are up.<br>2. Returns `503 Service Unavailable` if radio or DHCP fails.<br>3. Endpoint secured by localhost only. |
| **1.4** | **As a** Security Auditor, **I want** the device to enforce WPA2‑Enterprise (802.1X) for any SSID marked “secure”, **so that** corporate traffic is protected. | 1. When an SSID is flagged `secure:true` in config, the AP advertises WPA2‑Enterprise.<br>2. Authentication failures are logged with client MAC and reason.<br>3. Successful auth results in VLAN tag assignment (see E2). |

### Epic 2 – VLAN & SSID Management
| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| **2.1** | **As a** Network Admin, **I want** to create up to 8 SSIDs, each with a custom name, security mode, and VLAN ID, **so that** I can segment guest, IoT, and staff traffic. | 1. UI/API accepts a JSON payload with `ssid`, `security`, `vlan_id` (1‑4094).<br>2. AP creates the SSID instantly; clients see it in scans.<br>3. Traffic from each SSID is tagged with the configured VLAN ID on the Ethernet interface. |
| **2.2** | **As a** Network Admin, **I want** to edit or delete an existing SSID, **so that** I can adapt to changing policies without rebooting. | 1. Changes take effect within 2 s.<br>2. Deleting an SSID removes its broadcast and associated VLAN tag.<br>3. No residual firewall rules remain. |
| **2.3** | **As a** Compliance Officer, **I want** the AP to reject any configuration that maps an SSID to a reserved VLAN (0, 1, 4095), **so that** network segmentation rules are enforced. | 1. API returns `400 Bad Request` with clear error message.<br>2. UI displays validation error inline. |
| **2.4** | **As a** Monitoring Engineer, **I want** per‑SSID traffic statistics (bytes in/out, client count), **so that** I can verify isolation and usage. | 1. `/api/ssids` returns a list with `tx_bytes`, `rx_bytes`, `client_count` per SSID.<br>2. Stats are refreshed at least every 10 s. |
| **2.5** | **As a** Security Engineer, **I want** optional MAC‑filter lists per SSID, **so that** I can whitelist/blacklist devices. | 1. UI allows upload of MAC list (CSV).<br>2. AP enforces allow/deny mode per SSID.<br>3. Log entries record rejected MAC attempts. |

### Epic 3 – Mesh Networking
| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| **3.1** | **As a** Field Technician, **I want** the AP to discover nearby mesh‑vlan nodes automatically, **so that** I can build a mesh without manual IP configuration. | 1. Nodes broadcast a discovery packet on a dedicated channel every 5 s.<br>2. New neighbours appear in UI under “Mesh Neighbours”. |
| **3.2** | **As a** Network Planner, **I want** the mesh to elect a root node based on signal strength and CPU load, **so that** the topology is optimal. | 1. Root election runs within 30 s of power‑on.<br>2. Root node status is visible in UI (`Root: Yes/No`). |
| **3.3** | **As a** Network Admin, **I want** SSID/VLAN configuration to propagate automatically to all mesh members, **so that** the whole network stays in sync. | 1. When an SSID is added/modified on any node, the change is pushed to all neighbours within 5 s.<br>2. Nodes acknowledge receipt; UI shows “Synced”. |
| **3.4** | **As a** Reliability Engineer, **I want** the mesh to reroute traffic if a node fails, **so that** client connectivity is maintained. | 1. Heartbeat loss > 3 s triggers fail‑over.<br>2. Clients automatically re‑associate to the next best AP.<br>3. No more than 2 s of packet loss observed in simulated failure test. |
| **3.5** | **As a** Security Auditor, **I want** mesh control traffic to be encrypted (AES‑256‑GCM), **so that** configuration cannot be tampered. | 1. All inter‑node packets are encrypted with a pre‑shared key derived from device certificate.<br>2. Failed decryption logs a warning and drops the packet. |

### Epic 4 – Administration UI
| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| **4.1** | **As a** Administrator, **I want** a responsive web UI (desktop + tablet) served over HTTPS, **so that** I can manage the device securely from any browser. | 1. UI loads under 2 s on a 3G connection.<br>2. TLS 1.3 with a self‑signed cert (replaceable via UI). |
| **4.2** | **As a** Admin, **I want** a dashboard showing overall health, number of connected clients, and mesh topology map, **so that** I get a quick status overview. | 1. Dashboard widgets update in real‑time (≤5 s latency).<br>2. Topology map visualises nodes and links with signal strength colour‑coding. |
| **4.3** | **As a** Admin, **I want** wizard‑style onboarding to configure the first SSID and VLAN, **so that** deployment is zero‑touch. | 1. Wizard guides through SSID name, security, VLAN ID.<br>2. “Finish” button applies config and restarts radio without reboot. |
| **4.4** | **As a** Support Engineer, **I want** a log viewer with filtering (level, component, time), **so that** I can troubleshoot issues quickly. | 1. Logs are streamed via WebSocket.<br>2. Filters persist across sessions. |
| **4.5** | **As a** Admin, **I want** role‑based access control (RBAC) – **Viewer**, **Operator**, **Admin** – to limit who can change network settings. | 1. RBAC enforced on every API endpoint.<br>2. UI hides/disables controls based on role. |

### Epic 5 – Deployment & Operations
| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| **5.1** | **As a** DevOps Engineer, **I want** the firmware packaged as a Docker image and a signed OTA binary, **so that** we can roll out updates safely. | 1. `docker build` produces `mesh-vlan:<version>`.<br>2. OTA binary includes SHA‑256 signature verification. |
| **5.2** | **As a** Operator, **I want** the device to report metrics (CPU, memory, temperature, client count) to a central Prometheus endpoint, **so that** we can monitor fleet health. | 1. `/metrics` endpoint conforms to Prometheus exposition format.<br>2. Metrics include `mesh_vlan_cpu_percent`, `mesh_vlan_mem_bytes`, `mesh_vlan_clients_total`. |
| **5.3** | **As a** Security Engineer, **I want** a factory‑reset button (hardware + UI) that wipes all configs and restores the default open SSID, **so that** devices can be redeployed securely. | 1. Physical button held >5 s triggers reset.<br>2. UI “Factory Reset” performs same action after confirmation.<br>3. After reset, device boots to default state (Story 1.2). |
| **5.4** | **As a** Product Manager, **I want** usage analytics (number of SSIDs, mesh nodes, VLANs) exported daily as CSV, **so that** we can assess product adoption. | 1. Daily job writes `usage_YYYYMMDD.csv` to `/data/exports`.<br>2. CSV columns: `date, node_id, ssid_count, vlan_count, mesh_node_count`. |
| **5.5** | **As a** Support Engineer, **I want** a CLI tool (`meshctl`) that can query and modify configuration over SSH, **so that** we have a fallback when the UI is unreachable. | 1. `meshctl get ssids`, `meshctl set vlan --ssid <name> --id <id>` work as documented.<br>2. Commands require admin SSH key authentication. |

---  

## Prioritisation & MVP Scope
| Priority | Epic | Stories Included in MVP |
|----------|------|--------------------------|
| **P1** | E1 – Core Engine | 1.1, 1.2, 1.3 |
| **P2** | E2 – VLAN/SSID | 2.1, 2.2, 2.3 |
| **P3** | E3 – Mesh Basics | 3.1, 3.3, 3.4 |
| **P4** | E4 – Admin UI | 4.1, 4.2, 4.3 |
| **P5** | E5 – Ops Foundations | 5.1, 5.3 |

*Stories marked **P1‑P4** constitute the MVP (v0.1). Remaining stories (P5 and later) will be delivered in subsequent sprints toward v1.0.*  

---  

*End of document.*
