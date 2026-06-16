# REQUIREMENTS.md  

## Project Overview  
**mesh-vlan** is an Axentx product delivering a Wi‑Fi access‑point solution with a lightweight web UI. It must support:  

* Multiple SSIDs per device  
* SSID‑to‑VLAN mapping (static and dynamic)  
* Mesh networking to extend coverage in challenging environments  
* Secure, zero‑touch provisioning and OTA updates  

The solution will run on commodity ARM‑based routers (OpenWrt‑compatible) and be packaged as a Docker‑style container for easy deployment in Axentx’s edge‑fleet.

---

## 1. Functional Requirements  

| ID | Description | Acceptance Criteria |
|----|-------------|----------------------|
| **FR‑1** | **Multi‑SSID Management** | Admin UI allows creation, edit, enable/disable of up to 8 SSIDs per device. Each SSID stores: SSID name, security mode (WPA2‑PSK, WPA3‑SAE), passphrase, broadcast flag. |
| **FR‑2** | **SSID‑to‑VLAN Mapping** | For each SSID, admin can assign a VLAN ID (1‑4094). The mapping is persisted and applied to the underlying Linux bridge. |
| **FR‑3** | **Dynamic VLAN Assignment (RADIUS)** | When RADIUS is configured, the system must accept `Tunnel-Private-Group-ID` attribute and override the static VLAN mapping for that client. |
| **FR‑4** | **Mesh Node Discovery & Join** | Nodes discover each other via 802.11s mesh beacons. A node can join an existing mesh by entering the mesh ID and optional pre‑shared key. UI shows mesh topology (graph view). |
| **FR‑5** | **Back‑haul Selection** | Mesh nodes automatically select the best back‑haul (wireless mesh link vs. wired Ethernet) based on link quality metrics (RSSI, TX‑rate, latency). |
| **FR‑6** | **Zero‑Touch Provisioning (ZTP)** | New devices boot, contact Axentx provisioning service (HTTPS, mutual TLS), retrieve configuration (SSID list, VLAN map, mesh ID) and apply without manual intervention. |
| **FR‑7** | **OTA Firmware & Config Updates** | Admin UI can push firmware images and configuration bundles to selected nodes. Nodes acknowledge receipt and report success/failure. |
| **FR‑8** | **Web UI** | Responsive single‑page UI (React + Material‑UI) reachable at `https://<device>/`. Supports login (local admin or LDAP), dashboard, SSID/VLAN config, mesh topology, logs. |
| **FR‑9** | **Logging & Metrics** | System logs (syslog) and Prometheus metrics for: client association count, per‑SSID throughput, mesh link quality, VLAN usage, CPU/memory. UI displays key metrics. |
| **FR‑10** | **Access Control** | Role‑based access: **Super‑admin** (full control), **Network‑admin** (config only), **Read‑only** (view dashboards). |
| **FR‑11** | **Backup & Restore** | Admin can export full configuration (JSON) and import it on another device or after factory reset. |
| **FR‑12** | **Failover & Redundancy** | If a mesh node fails, remaining nodes re‑calculate routes within 5 seconds and maintain client connectivity. |
| **FR‑13** | **Compliance with IEEE 802.11s** | Mesh implementation must conform to the 802.11s standard (mesh IDs, mesh peering management). |

---

## 2. Non‑Functional Requirements  

| ID | Category | Requirement |
|----|----------|-------------|
| **NFR‑1** | **Performance** | Support ≥ 500 concurrent clients across the mesh with ≤ 30 ms average latency per client request. |
| **NFR‑2** | **Throughput** | Minimum aggregate throughput of 1 Gbps (wireless) when using 5 GHz 802.11ac/ax radios. |
| **NFR‑3** | **Scalability** | Mesh can scale to at least 32 nodes without manual topology configuration. |
| **NFR‑4** | **Security** | All management traffic (UI, ZTP, OTA) must use TLS 1.3 with mutual authentication. WPA3‑SAE is required for new SSIDs; WPA2‑PSK allowed only for legacy devices. |
| **NFR‑5** | **Reliability** | Mean Time Between Failures (MTBF) ≥ 200 000 hours per node. Automatic mesh re‑routing within 5 s after node loss. |
| **NFR‑6** | **Availability** | System uptime ≥ 99.9 % (excluding scheduled maintenance). |
| **NFR‑7** | **Resource Utilization** | CPU ≤ 30 % on a typical ARM Cortex‑A53 (1 GHz) under full load; RAM ≤ 256 MiB. |
| **NFR‑8** | **Observability** | Export Prometheus metrics on `/metrics` endpoint; logs rotatable with 7‑day retention. |
| **NFR‑9** | **Maintainability** | Codebase follows Axentx C++/Python style guide; unit test coverage ≥ 80 %; CI pipeline runs static analysis (clang‑tidy, bandit). |
| **NFR‑10** | **Portability** | Build system must support OpenWrt 22.03+ and Debian 12 containers. |
| **NFR‑11** | **Compliance** | Must pass FCC Part 15 and CE Mark requirements for RF emissions. |
| **NFR‑12** | **Data Privacy** | No client‑side data (passwords, traffic) is stored; only hashed PSKs (SHA‑256) and anonymized metrics. |
| **NFR‑13** | **Documentation** | End‑user guide, admin guide, and API reference generated via MkDocs; versioned with each release. |

---

## 3. Constraints  

1. **Hardware** – Target devices are ARM‑based routers with at least two radios (2.4 GHz & 5 GHz) and a Gigabit Ethernet port.  
2. **Licensing** – All third‑party libraries must be compatible with Apache‑2.0 or MIT licenses (no GPL‑v3).  
3. **Deployment Model** – Must run as a single Docker‑compatible container (`mesh-vlan:latest`) on top of OpenWrt’s `containerd` or as a native binary for bare‑metal.  
4. **Network Stack** – Must use Linux `nl80211` and `mac80211_hwsim` for mesh management; no proprietary SDKs.  
5. **Time‑to‑Market** – First MVP (supporting FR‑1, FR‑2, FR‑4, FR‑6, FR‑8) must be ship‑ready within 8 weeks.  

---

## 4. Assumptions  

| ID | Assumption |
|----|------------|
| **A‑1** | Customers have a RADIUS server available for dynamic VLAN assignment if they need it. |
| **A‑2** | The provisioning service (ZTP) is already deployed in Axentx’s cloud and reachable via a stable DNS name. |
| **A‑3** | Devices will have a pre‑installed root certificate bundle for mutual TLS. |
| **A‑4** | Mesh nodes are placed within 100 m line‑of‑sight of at least one neighbor (typical indoor/warehouse scenario). |
| **A‑5** | Administrators have basic networking knowledge; UI does not need to expose low‑level driver settings. |
| **A‑6** | Firmware images are signed with Axentx’s RSA‑4096 key; OTA process validates the signature before flashing. |
| **A‑7** | The underlying OpenWrt kernel includes the `cfg80211` and `mac80211` modules with mesh support compiled. |

---  

*Prepared by the Senior Product/Engineering Lead, Axentx – mesh‑vlan project.*
