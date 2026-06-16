# Product Requirements Document (PRD)  
**Project:** mesh‑vlan  
**Owner:** Senior Product/Engineering Lead  
**Date:** 2026‑06‑16  

---  

## 1. Problem Statement  

Enterprises, co‑working spaces, and large‑scale venues (e.g., hotels, campuses, factories) often struggle with Wi‑Fi coverage and network segmentation:

* **Signal loss** in complex floor plans, metal structures, or outdoor‑indoor transitions leads to dead zones.  
* **Flat network topology** forces all devices onto a single broadcast domain, creating security, performance, and compliance issues.  
* Existing AP solutions either lack **mesh capability** (requiring costly wired back‑haul) or provide **VLAN/SSID isolation** only in expensive enterprise‑grade gear.  

Result: IT teams spend excessive time provisioning, troubleshooting, and securing Wi‑Fi, while users experience intermittent connectivity and data‑leak risks.

## 2. Target Users & Personas  

| Persona | Role | Pain Points | Why mesh‑vlan helps |
|---------|------|-------------|----------------------|
| **Network Administrator** | IT Ops, Enterprise IT | Complex VLAN mapping, manual AP placement, limited visibility | Central UI to define SSID‑to‑VLAN mapping, auto‑mesh topology, real‑time health dashboard |
| **Facilities Manager** | Building Ops | Physical cabling constraints, need for quick Wi‑Fi rollout | Wireless back‑haul eliminates new cabling; plug‑and‑play APs |
| **Security Officer** | Compliance/InfoSec | Flat networks expose sensitive traffic, audit difficulty | Enforced VLAN isolation per SSID, audit logs, role‑based UI |
| **End‑User (Employee/Guest)** | Device user | Spotty Wi‑Fi, wrong network access | Seamless roaming across mesh nodes, correct SSID automatically places device in proper VLAN |

## 3. Goals & Success Metrics  

| Goal | Metric | Target (6 mo) |
|------|--------|---------------|
| **Coverage** | % of floor‑plan area with ≥ RSSI ‑70 dBm | ≥ 95 % |
| **Segmentation** | Number of distinct VLANs supported per deployment | ≥ 32 |
| **Usability** | Avg. time to provision a new SSID with VLAN mapping (UI) | ≤ 5 min |
| **Reliability** | Mesh link loss events per month | ≤ 2 per 100 APs |
| **Adoption** | New paying customers for mesh‑vlan product | 30 + (validated ARR ≥ $150k) |
| **Compliance** | Audit log completeness (100 % of config changes) | 100 % |

## 4. Scope  

### In‑Scope (Must‑Have)  

1. **AP Firmware**  
   * Support 802.11ax (Wi‑Fi 6) and 802.11ac fallback.  
   * Integrated VLAN tagging (802.1Q) on both wired uplink and wireless frames.  
   * Mesh back‑haul over 5 GHz with automatic neighbor discovery and self‑optimizing routing.  

2. **Management UI (Web) – Simple, responsive**  
   * Dashboard: topology map, AP health, client count per SSID/VLAN.  
   * SSID wizard: create SSID → assign VLAN ID → optional captive portal toggle.  
   * VLAN pool manager: define VLAN ranges, reserve IDs, view usage.  
   * Firmware OTA updates (per‑AP or group).  

3. **Controller Service (cloud‑hosted SaaS)**  
   * Stateless API layer (REST + gRPC) for UI and AP communication.  
   * Persistent store (PostgreSQL) for config, audit logs, topology.  
   * Metrics collector (Prometheus‑compatible) for health alerts.  

4. **Security**  
   * Role‑Based Access Control (admin, operator, auditor).  
   * TLS‑encrypted control channel (mTLS between AP & controller).  
   * Audit log of every config change, exported as CSV/JSON.  

5. **Installation & Deployment**  
   * Docker‑compose starter kit for on‑prem controller (optional).  
   * Zero‑touch provisioning via QR code or DHCP option 43.  

### Out‑of‑Scope (Will Not Be Delivered in Initial Release)  

| Item | Reason |
|------|--------|
| **Advanced RF analytics** (e.g., AI‑driven channel selection) | Planned for v2 after data collection. |
| **Integration with third‑party RADIUS/SSO** | Will be added via API extensions later. |
| **5G back‑haul** | Not required for Wi‑Fi‑only mesh use‑case. |
| **Hardware design** | We will ship as firmware for existing Axentx AP hardware (model AX‑AP‑X1). |
| **On‑prem controller HA clustering** | Single‑node SaaS sufficient for MVP; HA in future enterprise tier. |

## 5. Key Features (Prioritized)  

| Priority | Feature | Description | Acceptance Criteria |
|----------|---------|-------------|----------------------|
| **P1** | **SSID‑to‑VLAN Mapping Engine** | UI allows admin to bind each SSID to a VLAN ID; AP enforces tagging on all client frames. | • Create, edit, delete mapping via UI.<br>• AP forwards correctly tagged frames to uplink.<br>• Traffic isolation verified with packet capture. |
| **P1** | **Self‑Forming Mesh Network** | APs discover peers, negotiate optimal parent/child links, and maintain redundancy. | • Deploy 5 APs; UI shows mesh topology automatically.<br>• Link failover occurs within 2 s of a node loss. |
| **P1** | **Centralized Dashboard** | Real‑time view of AP status, client counts per SSID/VLAN, and mesh health. | • Dashboard refreshes ≤ 5 s.<br>• Alerts appear for AP offline or high packet loss. |
| **P2** | **OTA Firmware Management** | Push firmware updates to individual or groups of APs with rollback. | • Upload new firmware version; 100 % of selected APs report success.<br>• Rollback restores previous version without service interruption. |
| **P2** | **Role‑Based Access Control** | Granular permissions for admin, operator, auditor. | • Auditor can view logs but cannot edit config.<br>• Operator can provision SSIDs but not delete VLANs. |
| **P3** | **Zero‑Touch Provisioning** | New AP auto‑registers with controller using QR code or DHCP option. | • Scan QR code; AP appears in UI within 30 s.<br>• No manual IP configuration required. |
| **P3** | **Exportable Audit Log** | Full change history downloadable in CSV/JSON. | • Export contains timestamp, user, changed fields, old/new values. |
| **P4** | **Basic Captive Portal** (optional) | Simple splash page for guest SSIDs. | • Enable portal; guest devices redirected to configurable URL. |

## 6. Technical Requirements  

| Area | Requirement |
|------|-------------|
| **Platform** | Firmware built on OpenWrt 22.03 LTS; controller on Ubuntu 22.04 LTS (Docker). |
| **Languages** | Firmware: C / Lua; Controller/API: Go (v1.22); UI: React + TypeScript. |
| **AP Hardware** | Existing Axentx AP‑X1 (dual‑band 2.4/5 GHz, 2× Gigabit Ethernet, 256 MiB RAM). |
| **Scalability** | Controller must handle ≥ 5 000 APs, 200 000 concurrent clients. |
| **Performance** | Mesh latency ≤ 15 ms hop‑to‑hop; VLAN tagging overhead < 2 %. |
| **Security** | TLS 1.3, AES‑256‑GCM for control channel; firmware signed with Ed25519. |
| **Compliance** | Data at rest encrypted (AES‑256); GDPR‑compliant logging (no personal data stored). |
| **Observability** | Export Prometheus metrics: ap_up, mesh_link_quality, client_per_vlan. |
| **Testing** | Unit tests ≥ 80 % coverage; integration tests for mesh formation and VLAN isolation; CI pipeline using GitHub Actions. |

## 7. Milestones & Timeline  

| Milestone | Deliverable | Owner | Target Date |
|-----------|-------------|-------|-------------|
| **M1 – Foundations** | Repo scaffolding, CI pipeline, basic AP firmware stub | Eng Lead | 2026‑06‑30 |
| **M2 – VLAN Engine** | SSID‑to‑VLAN UI + API, VLAN tagging on AP | Backend / Firmware | 2026‑07‑21 |
| **M3 – Mesh Core** | Auto‑discovery, routing protocol (BATMAN‑adv), topology UI | Firmware / Network | 2026‑08‑15 |
| **M4 – Dashboard & RBAC** | Real‑time dashboard, role‑based login | Frontend / Auth | 2026‑09‑05 |
| **M5 – OTA & Zero‑Touch** | Firmware OTA service, QR‑code provisioning flow | DevOps / Firmware | 2026‑09‑25 |
| **M6 – Beta Release** | Private beta with 3 pilot customers, audit logging | PM / QA | 2026‑10‑10 |
| **M7 – GA Launch** | Public SaaS offering, documentation, support handoff | All | 2026‑11‑01 |

## 8. Risks & Mitigations  

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| **Mesh instability** in dense RF environments | Service outage | Medium | Use proven BATMAN‑adv; add link‑quality thresholds; extensive field testing. |
| **VLAN mis‑configuration** leading to security breach | High | Low | Enforce validation rules in UI; audit logs with immutable storage. |
| **Firmware compatibility** across hardware revisions | Medium | Medium | Maintain hardware abstraction layer; CI matrix for each revision. |
| **Regulatory compliance** (e.g., GDPR) for logging | High | Low | Store only non‑PII; provide data‑deletion API for auditors. |
| **Performance bottleneck** in controller scaling | Medium | Medium | Design stateless API; horizontal scaling via Kubernetes; load testing before GA. |

## 9. Open Questions  

1. Should we expose an API for third‑party RADIUS integration in v1 or reserve for v2?  
2. What is the preferred licensing model (subscription per AP vs. flat‑fee SaaS) for early adopters?  
3. Will we need to support IPv6 VLAN tagging out‑of‑the‑box?  

---  

*Prepared by the Senior Product/Engineering Lead, Axentx*
