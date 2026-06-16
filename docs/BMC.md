# Business Model Canvas – **mesh‑vlan**

| **Key Partners** | **Key Activities** | **Key Resources** |
|------------------|--------------------|-------------------|
| • Wi‑Fi chipset manufacturers (e.g., Qualcomm, MediaTek) – supply of radios & reference designs | • Develop & maintain firmware (OpenWrt‑based) with VLAN, multi‑SSID, and mesh extensions | • Source code repository (GitHub `arkashira/mesh-vlan`) |
| • Hardware OEMs (router/AP integrators) – co‑manufacture reference AP units | • Design and ship the web UI (React + Vite) for simple VLAN/SSID configuration | • Domain‑specific knowledge base (BRAIN) on networking, VLAN, mesh protocols |
| • Cloud‑edge platform providers (e.g., AWS Greengrass, Azure IoT Edge) – optional remote management | • Integrate with existing Axentx infrastructure (vLLM for AI‑assisted diagnostics, SGLang for structured logs) | • Testing labs (RF anechoic chamber, automated CI/CD pipelines) |
| • Open‑source communities (OpenWrt, OpenMesh) – upstream patches & security updates | • Provide OTA update pipeline and security patch management | • Customer support team (tier‑1/2) |
| • Channel partners (MSPs, system integrators) – resale & deployment services | • Create documentation, SDKs, and partner enablement material | • Legal & compliance (FCC, CE, GDPR) |
| • Payment processors (Stripe, PayPal) – subscription billing | • Collect usage telemetry (opt‑in) for product improvement | • Financial resources for hardware subsidies (initial pilot kits) |

| **Value Proposition** | **Customer Segments** |
|-----------------------|-----------------------|
| • Turn‑key Wi‑Fi AP that **adds VLAN tagging, multiple SSIDs, and SSID‑to‑VLAN mapping** without complex CLI. <br>• **Mesh networking** automatically bridges coverage gaps in dense or obstructed environments. <br>• Intuitive web UI reduces deployment time from days to hours. <br>• Enterprise‑grade security (WPA3, 802.1X, isolated VLANs). <br>• AI‑driven health insights via Axentx’s vLLM engine (predictive fault detection). | • SMBs & branch offices needing segmented guest & staff networks. <br>• Hospitality venues (hotels, conference centers) with multiple SSIDs per floor. <br>• Industrial sites (manufacturing, warehouses) requiring VLAN isolation for IoT devices. <br>• Educational campuses with dorm, admin, and classroom networks. <br>• Managed Service Providers (MSPs) offering network-as‑a‑service. |
| **Channels** | **Revenue Streams** |
| • Direct sales via Axentx website (hardware kit + SaaS subscription). <br>• OEM integration – pre‑installed firmware on partner AP hardware. <br>• Marketplace listings (Amazon Business, CDW). <br>• Channel partner program – MSPs resell and install. <br>• Technical webinars & demo labs (lead generation). | • **Hardware kit** – AP unit (cost‑plus pricing, ~USD 150). <br>• **SaaS subscription** – Cloud‑managed UI, OTA updates, AI diagnostics (USD 9 / device / month). <br>• **Professional services** – deployment, custom VLAN design, training (USD 200 / hour). <br>• **Support contracts** – Tier‑2 SLA (USD 5 / device / month). <br>• **Marketplace royalties** – 5 % of OEM sales. |
| **Cost Structure** |
| • Hardware procurement (AP units, antennas). <br>• R&D salaries (firmware, UI, AI integration). <br>• Cloud hosting (management backend, vLLM inference). <br>• Certification & compliance testing (FCC, CE). <br>• Customer support & success teams. <br>• Marketing & channel incentives. <br>• Continuous security patching (upstream contributions). |
| **Key Metrics** (for internal validation) |
| • Units shipped per month. <br>• Monthly recurring revenue (MRR) from SaaS. <br>• Average deployment time (hours). <br>• Churn rate of SaaS subscriptions. <br>• Mean Time To Resolve (MTTR) for support tickets. <br>• AI diagnostic accuracy (false‑positive/negative rate). |
| **Unfair Advantage** |
| • Integration with Axentx’s AI stack (vLLM, SGLang) provides predictive network health not offered by generic AP vendors. <br>• Proprietary UI that abstracts VLAN complexity while retaining full 802.1Q compliance. <br>• Rapid OTA pipeline leveraging existing Axentx CI/CD infrastructure. |
| **Assumptions & Risks** |
| • Assume customers prefer a managed SaaS overlay to on‑premise controllers. <br>• Risk: hardware supply chain disruptions – mitigated by multiple chipset partners. <br>• Risk: regulatory changes in Wi‑Fi standards – mitigated by active OpenWrt upstream participation. |

---  

*Prepared by the Senior Product/Engineering Lead, Axentx – 2026‑06‑16*
