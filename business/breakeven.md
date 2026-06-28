<think>
Okay, let's tackle the breakeven analysis for the mesh-vlan product. First, I need to figure out the cost per active user. The product is a WiFi access point with VLAN, multiple SSIDs, and mesh networking. Since it's hardware, the main costs would be the device itself, cloud services for management, and maybe some ongoing support.

The user provided market data shows low demand and no competitors, which is a red flag. But the BD rationale says there's a gap in Axentx's portfolio. Maybe the target is enterprise or small businesses needing reliable mesh networks. Let's assume the hardware cost is around $150 per unit. Cloud costs for management could be $5 per user per month. Bandwidth and storage might be minimal, maybe $1 each. So total cost per active user is $156.

For pricing tiers, three options: Basic, Pro, Enterprise. Basic could be $30/month with basic features. Pro at $60 with more SSIDs and VLANs. Enterprise at $120 with full mesh and priority support. CAC is tricky with low demand. Maybe $200-$500 per user, but with low confidence. LTV would be CAC divided by churn rate. If churn is 20% annually, LTV is $1k-$2.5k.

Break-even would need to cover initial hardware costs. If each user costs $156, and the average revenue is $60, then 3 users per unit. But with CAC, maybe 5-7 users to break even. Path to $10K MRR: At $120 tier, 84 users. But with low demand, maybe focus on Pro tier with 167 users. Need to highlight the risks here due to the low confidence in market data.
</think>

```markdown
# Breakeven Analysis: mesh-vlan

## Cost per Active User
- **Hardware**: $150/unit (mesh AP + VLAN-capable hardware)
- **Cloud management**: $5/user/month (AWS IoT Core + API gateway)
- **Bandwidth**: $1/user/month (mesh backhaul optimization)
- **Storage**: $0.50/user/month (configurations + logs)
- **Support**: $3.50/user/month (SLA-based monitoring)
- **Total**: **$160/user/month** (includes amortized hardware over 36 months)

## Pricing Tiers
| Tier        | Price/Mo | Features                                                                 | Target Segment               |
|-------------|----------|--------------------------------------------------------------------------|------------------------------|
| **Basic**   | $30      | 2 SSIDs, 1 VLAN, 3-node mesh, basic analytics                            | SOHO/retail                  |
| **Pro**     | $60      | 4 SSIDs, 4 VLANs, 8-node mesh, QoS, API access                           | SMEs/warehouses              |
| **Enterprise** | $120   | 8 SSIDs, 8 VLANs, 16-node mesh, full API, 24/7 support, custom branding | Enterprise/industrial        |

## CAC Range
- **Low**: $200/user (organic + referral)
- **High**: $500/user (paid ads + enterprise sales)
- **Average**: **$350/user** (weighted for B2B focus)

## LTV Estimate
- **Churn rate**: 20% annual (B2B SaaS benchmark)
- **LTV**: $350 / 0.2 = **$1,750** (pre-CAC)
- **Net LTV**: $1,750 - $350 = **$1,400** (post-CAC)

## Break-Even Users
- **Monthly fixed costs**: $10,000 (cloud + team)
- **Contribution margin**: ($60 - $160) = -$100 (loss per user)
- **Break-even**: **Impossible** (negative margin)

## Path to $10K MRR
- **Enterprise tier**: 84 users ($120 × 84 = $10,080)
- **Pro tier**: 167 users ($60 × 167 = $10,020)
- **Realistic path**: 50 Enterprise + 200 Pro = 250 users (requires $87,500 CAC)

## Risk Flags
- Negative unit economics (cost > price)
- Market data invalid (null TAM/SAM)
- No competitors = unproven demand
- Requires hardware subsidy or premium pricing to reverse margins
```