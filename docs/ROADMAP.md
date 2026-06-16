# 📅 mesh‑vlan Roadmap  

*Product*: **mesh‑vlan** – A Wi‑Fi access‑point solution with a clean UI, VLAN‑aware SSIDs, SSID‑to‑VLAN mapping, and mesh networking to eliminate dead‑spots.  

---

## 🎯 Vision  

Enable any organization—SMBs, schools, or enterprises—to deploy a self‑healing, VLAN‑segmented Wi‑Fi fabric with zero‑touch provisioning and a single pane‑of‑glass UI, while staying fully compatible with Axentx’s AI‑driven analytics platform.

---

## 🚀 MVP (Launch) – **Must‑Have for Release**  

| # | Feature | Description | MVP‑Critical |
|---|---------|-------------|--------------|
| 1️⃣ | **Base Firmware & Radio Stack** | Integration with OpenWrt/LEDE (or equivalent) providing stable 2.4 GHz / 5 GHz drivers. | ✅ |
| 2️⃣ | **Simple Web UI** | Responsive UI for configuring SSID, passphrase, VLAN ID, and mesh mode. | ✅ |
| 3️⃣ | **VLAN Tagging** | Ability to tag traffic per‑SSID and forward to configured VLANs on the uplink switch. | ✅ |
| 4️⃣ | **SSID‑to‑VLAN Mapping Engine** | One‑to‑one mapping table stored in flash; applied at association time. | ✅ |
| 5️⃣ | **Basic Mesh (802.11s)** | Automatic peer discovery, back‑haul selection, and seamless roaming between nodes. | ✅ |
| 6️⃣ | **Security Baseline** | WPA2‑Personal / WPA3‑Personal, admin login (hashed password + optional 2FA). | ✅ |
| 7️⃣ | **OTA Firmware Updates** | Secure over‑the‑air updates with rollback on failure. | ✅ |
| 8️⃣ | **Health Dashboard** | Real‑time client count, RSSI heat‑map, and VLAN traffic counters. | ✅ |
| 9️⃣ | **Quick‑Start Documentation** | PDF/HTML guide covering hardware setup, UI walkthrough, and troubleshooting. | ✅ |
| 🔟 | **Automated Test Suite** | CI pipeline that validates UI flow, VLAN tagging, and mesh connectivity on emulated hardware. | ✅ |

*All items above are flagged as **MVP‑Critical**; the product cannot be shipped without them.*

---

## 📈 Version 1 – Enterprise‑Ready Expansion  

**Theme:** *Scalability, Observability, and Policy Control*  

| Milestone | Target Quarter | Features |
|-----------|----------------|----------|
| **V1.0 – Centralized Mesh Management** | Q3 2026 | • Dashboard that aggregates all mesh nodes, shows topology map, and allows bulk config pushes.<br>• Node health alerts (CPU, memory, radio errors). |
| **V1.1 – Role‑Based Access Control (RBAC)** | Q4 2026 | • Admin / Operator / Viewer roles.<br>• LDAP / RADIUS integration for user authentication. |
| **V1.2 – Advanced QoS & Traffic Shaping** | Q1 2027 | • Per‑VLAN/SSID bandwidth limits.<br>• Priority queues for VoIP / video. |
| **V1.3 – Multi‑SSID & Guest Portal** | Q2 2027 | • Support for ≥ 8 simultaneous SSIDs.<br>• Built‑in captive portal with optional external authentication. |
| **V1.4 – Public API & Automation** | Q3 2027 | • REST/GraphQL endpoints for provisioning, monitoring, and OTA triggers.<br>• SDK samples in Python & Go. |
| **V1.5 – Analytics Integration** | Q4 2027 | • Export telemetry to Axentx BRAIN for usage patterns, anomaly detection, and capacity planning.<br>• Pre‑built Grafana dashboards. |
| **V1.6 – Reliability Hardenings
