# TECH_SPEC.md – mesh‑vlan  

**Version:** 1.0.0  
**Last Updated:** 2026‑06‑16  
**Owner:** AxentX – Senior Product/Engineering Lead  

---  

## Table of Contents
1. [Overview](#1-overview)  
2. [Goals & Success Metrics](#2-goals--success-metrics)  
3. [Architecture Overview](#3-architecture-overview)  
4. [Core Components](#4-core-components)  
5. [Data Model](#5-data-model)  
6. [Key APIs & Interfaces](#6-key-apis--interfaces)  
7. [Technology Stack](#7-technology-stack)  
8. [External Dependencies](#8-external-dependencies)  
9. [Deployment & Operations](#9-deployment--operations)  
10. [Security & Compliance](#10-security--compliance)  
11. [Observability & Telemetry](#11-observability--telemetry)  
12. [Testing Strategy](#12-testing-strategy)  
13. [Future Extensions](#13-future-extensions)  
14. [Appendix](#14-appendix)  

---  

## 1. Overview
**mesh‑vlan** is a Wi‑Fi access‑point (AP) platform that provides:

* A lightweight, browser‑based UI for configuration.  
* Support for multiple SSIDs with per‑SSID VLAN tagging.  
* Dynamic SSID‑to‑VLAN mapping (policy‑driven).  
* Full mesh networking (802.11s) to extend coverage in dense or obstructed environments.  

The product is intended for enterprise, hospitality, and industrial deployments where network segmentation and reliable coverage are mandatory.

---  

## 2. Goals & Success Metrics  

| Goal | Success Metric |
|------|----------------|
| **Zero‑touch provisioning** | ≤ 30 seconds from power‑on to operational AP |
| **VLAN isolation** | 100 % traffic separation verified by automated packet‑capture tests |
| **Mesh stability** | ≥ 99.5 % node‑to‑node link uptime over 30‑day window |
| **UI simplicity** | < 5 clicks to create a new SSID‑VLAN mapping |
| **Scalability** | Support ≥ 128 APs per mesh cluster with < 10 ms latency for control plane messages |
| **Security** | All management traffic encrypted with TLS 1.3; WPA3‑Enterprise support |

---  

## 3. Architecture Overview  

```
+-------------------+        +-------------------+        +-------------------+
|   Front‑End UI    | <----> |   AP Management   | <----> |   Mesh Radio Stack|
| (React SPA)       |        | Service (Go)      |        | (OpenWrt + hostapd)|
+-------------------+        +-------------------+        +-------------------+
          ^                         ^                         ^
          | REST/WS                 | gRPC                    | netlink
          |                         |                         |
+-------------------+        +-------------------+        +-------------------+
|   Configuration   | <----> |   VLAN Engine     | <----> |   Linux Kernel    |
|   Store (SQLite) |        | (DPDK/ebtables)   |        | (netfilter)       |
+-------------------+        +-------------------+        +-------------------+
```

* **Front‑End UI** – React SPA served over HTTPS, communicates via WebSocket for real‑time status and REST for CRUD.  
* **AP Management Service** – Go microservice running on each AP (or on a central controller for managed deployments). Handles configuration persistence, policy enforcement, and mesh control.  
* **Mesh Radio Stack** – OpenWrt base with hostapd‑mesh (802.11s) and hostapd‑multi‑ssid. Provides low‑level radio control, channel selection, and neighbor discovery.  
* **VLAN Engine** – Uses Linux bridge + ebtables/iptables to tag/untag frames per SSID. For high‑throughput paths, DPDK can be enabled on capable hardware.  
* **Configuration Store** – Embedded SQLite (single‑file, ACID) replicated via Raft (optional) for multi‑controller setups.  

---  

## 4. Core Components  

| Component | Language | Responsibility | Key Files/Dirs |
|-----------|----------|----------------|----------------|
| **UI** | TypeScript/React | Dashboard, SSID/VLAN CRUD, mesh topology view | `ui/`, `ui/src/components/`, `ui/public/` |
| **AP‑Mgr** | Go (1.22) | REST/WS API, config validation, mesh orchestration, VLAN rule generation | `cmd/apmgr/`, `internal/api/`, `internal/mesh/`, `internal/vlan/` |
| **Mesh Daemon** | C (hostapd) + shell scripts | 802.11s mesh formation, neighbor link monitoring | `mesh/hostapd/`, `mesh/scripts/` |
| **VLAN Engine** | Bash + iproute2/ebtables | Bridge creation, VLAN tagging per SSID, cleanup | `vlan/bridge.sh`, `vlan/ebtables.rules` |
| **Config Store** | SQLite (via Go driver) | Persistent storage, schema migrations | `db/migrations/`, `internal/store/` |
| **Telemetry Agent** | Go | Export Prometheus metrics, health checks | `internal/telemetry/` |

---  

## 5. Data Model  

### 5.1 SQLite Schema (simplified)

```sql
CREATE TABLE ssid (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL UNIQUE,
    password    TEXT,
    auth_mode   TEXT CHECK(auth_mode IN ('open','wpa2','wpa3')),
    vlan_id     INTEGER NOT NULL,
    enabled     BOOLEAN NOT NULL DEFAULT 1,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE mesh_node (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    mac_address TEXT NOT NULL UNIQUE,
    hostname    TEXT,
    status      TEXT CHECK(status IN ('online','offline','degraded')),
    last_seen   DATETIME,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE vlan_policy (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    ssid_id     INTEGER REFERENCES ssid(id) ON DELETE CASCADE,
    vlan_id     INTEGER NOT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

*All passwords are stored as salted bcrypt hashes; WPA‑PSK is derived at runtime, never persisted.*

### 5.2 In‑memory Structures (Go)

```go
type SSID struct {
    ID        int64
    Name      string
    AuthMode  string
    VLANID    int
    Enabled   bool
    Password  string // hashed
}
type MeshNode struct {
    ID        int64
    MAC       string
    Hostname  string
    Status    string
    LastSeen  time.Time
}
```

---  

## 6. Key APIs & Interfaces  

### 6.1 REST (JSON) – Management API  

| Method | Path | Description | Request Body | Response |
|--------|------|-------------|--------------|----------|
| `GET` | `/api/v1/ssids` | List all SSIDs | – | `[{id, name, vlan_id, enabled, auth_mode}]` |
| `POST`| `/api/v1/ssids` | Create new SSID | `{name, password, auth_mode, vlan_id}` | `201 Created` + object |
| `PUT` | `/api/v1/ssids/{id}` | Update SSID | same as POST | `200 OK` |
| `DELETE`| `/api/v1/ssids/{id}` | Delete SSID | – | `204 No Content` |
| `GET` | `/api/v1/mesh/nodes` | Mesh topology snapshot | – | `[{mac, hostname, status, last_seen}]` |
| `POST`| `/api/v1/mesh/rejoin` | Force node to re‑join mesh | `{mac}` | `202 Accepted` |

All endpoints require JWT‑Bearer token (`Authorization: Bearer <token>`). Tokens issued by internal auth service (OAuth2 password grant).

### 6.2 WebSocket – Real‑time Events  

*Endpoint:* `wss://<ap>/ws/events`  

Message Types (JSON):

```json
{ "type": "node_status", "payload": { "mac":"AA:BB:CC:DD:EE:FF", "status":"online" } }
{ "type": "ssid_update", "payload": { "id":12, "enabled":false } }
```

### 6.3 Internal gRPC – Mesh Control (controller ↔ AP)  

*Proto file:* `proto/mesh.proto`  

Key RPCs:

```proto
service MeshControl {
  rpc GetTopology (Empty) returns (Topology);
  rpc SetChannel (ChannelRequest) returns (Ack);
  rpc TriggerRejoin (NodeId) returns (Ack);
}
```

---  

## 7. Technology Stack  

| Layer | Technology | Reason |
|-------|------------|--------|
| UI | React 18 + Vite + TailwindCSS | Fast dev, small bundle, responsive |
| Backend | Go 1.22 (net/http, chi router) | Concurrency, static binary, easy cross‑compilation |
| Radio OS | OpenWrt 23.05 (kernel 6.6) | Proven on embedded AP hardware |
| Mesh | hostapd 2.11 (802.11s) | Native Linux mesh support |
| VLAN | Linux bridge + ebtables/iptables (DPDK optional) | No extra kernel modules, works on commodity NICs |
| DB | SQLite 3.45 (WAL mode) | Zero‑config, ACID, fits AP footprint |
| Telemetry | Prometheus client (go) + node_exporter | Standard observability |
| CI/CD | GitHub Actions, Docker multi‑arch builds | Automated testing & release |
| Containerisation (optional) | Alpine‑based multi‑stage Docker images | For controller deployments |

---  

## 8. External Dependencies  

| Dependency | Version | License | Usage |
|------------|---------|---------|-------|
| `github.com/go-chi/chi` | v5.0.8 | MIT | HTTP routing |
| `github.com/mattn/go-sqlite3` | v2.0.0 | MIT | SQLite driver |
| `github.com/golang-jwt/jwt/v5` | v5.2.0 | MIT | JWT handling |
| `github.com/prometheus/client_golang` | v1.18.0 | Apache‑2.0 | Metrics |
| `hostapd` | 2.11 | BSD‑3 | Mesh & SSID handling |
| `openwrt` | 23.05 | GPL‑2.0 | Base OS |
| `ebtables` | 2.0.10 | GPL‑2.0 | VLAN tagging |
| `dpdk` (optional) | 23.11 | BSD‑3 | High‑throughput datapath |

All dependencies are listed in `go.mod` and Dockerfile `apk add` sections.

---  

## 9. Deployment & Operations  

### 9.1 Target Platforms  

| Platform | CPU | RAM | Storage | Notes |
|----------|-----|-----|---------|-------|
| **Edge AP** | ARM Cortex‑A53 (or x86_64) | ≥ 256 MiB | ≥ 64 MiB flash | Runs OpenWrt + static `apmgr` binary |
| **Controller (optional)** | x86_64 / ARM64 | ≥ 2 GiB | ≥ 10 GiB SSD | Runs same binary in “controller” mode, stores aggregated config |

### 9.2 Build Pipeline  

1. **Static Build** – `GOOS=linux GOARCH=arm64 go build -ldflags "-s -w" -o apmgr ./cmd/apmgr`  
2. **Docker Image** – Multi‑stage:  
   *Stage 1:* `golang:1.22-alpine` → compile.  
   *Stage 2:* `alpine:3.19` → copy binary, `apk add --no-cache hostapd ebtables`.  
3. **Firmware Integration** – Binary placed under `/usr/bin/apmgr` in OpenWrt image via custom `imagebuilder`.  

### 9.3 Runtime Startup  

```sh
# on AP
/etc/init.d/apmgr enable
/etc/init.d/apmgr start
```

Systemd is not available; OpenWrt’s `procd` service script (`/etc/init.d/apmgr`) handles restart on crash.

### 9.4 Configuration Flow  

1. User accesses UI (`https://<ap>/`) → authenticates.  
2. UI POSTs SSID/VLAN definitions → AP‑Mgr writes to SQLite.  
3. AP‑Mgr generates ebtables rules & bridge config → executes `vlan/bridge.sh`.  
4. hostapd is reloaded (`/etc/init.d/hostapd restart`).  
5. Mesh daemon updates neighbor table automatically.

---  

## 10. Security & Compliance  

| Aspect | Implementation |
|--------|----------------|
| **Transport** | HTTPS (TLS 1.3) with self‑signed certs provisioned at first boot; optional ACME for managed deployments. |
| **Authentication** | Local admin accounts stored as bcrypt hashes; JWT for API. |
| **Authorization** | Role‑based (admin, read‑only). Future RBAC via external IdP (OIDC). |
| **Data at Rest** | SQLite file owned by `apmgr` user (chmod 600). |
| **VLAN Isolation** | Enforced by kernel bridge + ebtables; no cross‑VLAN forwarding unless explicitly configured. |
| **WPA3** | hostapd compiled with `CONFIG_IEEE80211W=y` and `CONFIG_SAE=y`. |
| **Supply‑Chain** | All third‑party binaries built from verified commits (see `vendor/` lockfile). |
| **Compliance** | Licenses: MIT, Apache‑2.0, BSD‑3, GPL‑2 (OpenWrt). No GPL‑incompatible code. |

---  

## 11. Observability & Telemetry  

* **Prometheus Metrics** (`/metrics` endpoint) – counters for: `apmgr_ssid_created_total`, `apmgr_mesh_node_up`, `apmgr_vlan_rule_errors`.  
* **Health Checks** – `GET /healthz` returns 200 if DB reachable, hostapd running, mesh daemon alive.  
* **Logging** – Structured JSON logs to `stdout`; rotated via `logrotate` on the AP.  
* **Mesh Topology Export** – `/api/v1/mesh/nodes` JSON + optional gRPC `GetTopology`.  

---  

## 12. Testing Strategy  

| Layer | Tool | Coverage Goal |
|-------|------|---------------|
| Unit | `go test ./...` (cover) | ≥ 80 % |
| Integration | Docker Compose (controller + mock AP) | Scenario: create SSID → verify ebtables rule via `iptables -L` |
| End‑to‑End | Selenium + Playwright (UI) | Critical path: UI → AP config → mesh join |
| Performance | `wrk` for API, `iperf3` for VLAN throughput | ≥ 1 Gbps on DPDK‑enabled hardware |
| Security | `gosec`, `bandit` (Python scripts), `openvas` scan of firmware image | No high‑severity findings |

CI pipeline runs all tests on PRs; nightly job runs performance baseline against a reference hardware set.

---  

## 13. Future Extensions  

| Feature | Description | Impact |
|---------|-------------|--------|
| **Zero‑Touch Cloud Provisioning** | Device contacts AxentX cloud for config push via MQTT | Faster roll‑outs, multi‑site management |
| **AI‑Driven Channel Selection** | Use vLLM inference to predict optimal channel based on environment scans | Improves mesh stability |
| **Dynamic VLAN Assignment** | RADIUS attributes map user to VLAN at authentication time | Per‑user segmentation |
| **High‑Availability Controller** | Raft‑based config replication across multiple controllers | Eliminates single point of failure |
| **Edge‑AI Offload** | Deploy SGLang models for local interference detection | Proactive mesh healing |

---  

## 14. Appendix  

### 14.1 Directory Layout  

```
mesh-vlan/
├─ ui/                     # React SPA
│  ├─ src/
│  └─ public/
├─ cmd/
│  └─ apmgr/               # main entry point
├─ internal/
│  ├─ api/                 # REST & WS handlers
│  ├─ mesh/                # mesh control logic
│  ├─ vlan/                # bridge/ebtables helpers
│  ├─ store/               # SQLite wrapper + migrations
│  └─ telemetry/
├─ mesh/
│  ├─ hostapd/             # config templates
│  └─ scripts/             # mesh daemon wrappers
├─ vlan/
│  └─ bridge.sh
├─ proto/
│  └─ mesh.proto
├─ Dockerfile
├─ go.mod / go.sum
└─ README.md
```

### 14.2 Sample `bridge.sh`  

```bash
#!/bin/sh
set -e

BRIDGE=br0
IPTABLES=/sbin/iptables
EBTABLES=/sbin/ebtables

# create bridge if missing
ip link add name $BRIDGE type bridge || true
ip link set dev $BRIDGE up

# flush old rules
$EBTABLES -F
$IPTABLES -F

# apply per‑SSID VLAN rules (generated by apmgr)
while read -r ssid vlan; do
    # assume hostapd creates interface wlan0_<ssid>
    IF="wlan0_${ssid}"
    ip link set dev $IF master $BRIDGE
    $EBTABLES -t broute -A BROUTING -i $IF -j redirect --redirect-target DROP
    $EBTABLES -t nat -A POSTROUTING -o $IF -j dnat --to-destination :$vlan
done < /run/apmgr/ssid_vlan.map
```

### 14.3 Migration Example  

`db/migrations/20240601_create_tables.sql`

```sql
BEGIN;
-- tables defined in section 5.1
COMMIT;
```

---  

*Prepared for internal review and subsequent implementation.*
