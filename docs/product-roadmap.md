# Product Roadmap: Agent-Assisted CS System

*Strategic evolution from MVP to intelligent platform*

---

## Vision

Transform Pineapple Travel's customer support from reactive problem-solving to proactive, AI-powered travel assistance that:
- **Resolves issues** before customers notice them
- **Builds trust** through transparency and education
- **Reduces costs** through intelligent automation
- **Increases revenue** through improved retention and guarantee attachment

**Core Principle**: Start conservative (human-in-the-loop), prove value with data, scale intelligently.

---

## Roadmap Overview

```
Phase 1 (Q1 2026): MVP - Human-in-the-Loop
    ↓ Prove value, collect data
Phase 2 (Q2 2026): Selective Automation + Customer Self-Service
    ↓ Automate simple cases, educate customers
Phase 3 (Q3 2026): Proactive Intelligence
    ↓ Predict and prevent issues
Phase 4 (Q4 2026): Advanced AI & Multi-Agent Systems
    ↓ Sophisticated orchestration
Phase 5 (2027+): Ecosystem & Platform
    ↓ Industry leadership
```

---

## Phase 1: MVP (Q1 2026) ✅ 

### Status: In Design

### Scope
**Agent Assistance Only** - Human-in-the-loop for all decisions

**Core Features**:
- Proactive failure detection (flight status monitoring)
- Automated context assembly (RAG pipeline)
- LLM-generated resolution options (Claude Sonnet)
- Prompt-injected rule book (policy compliance)
- Structured output with confidence scores
- Agent dashboard for review/approval
- Full decision trace logging

**Key Components**:
- Booking database integration (verify claims, cross-reference)
- Vector database (policies, historical cases)
- Hybrid search (semantic + keyword)
- Multi-model LLM strategy (GPT-4o mini + Claude Sonnet)

### Success Criteria
- **TTFR**: 10min → 3min (70% reduction)
- **Agent approval rate**: >80%
- **CSAT**: 3.2 → 4.0 (+25%)
- **Cost per case**: <€0.05 in LLM costs
- **Policy compliance**: 100%
- **Hallucination rate**: <2%

### Business Impact
- €114K/year net savings
- Improved customer satisfaction
- Agent productivity +300%
- Data collection for Phase 2 autonomy

### Timeline
- Week 1-4: Build & test
- Week 5-8: Shadow mode (no agent visibility)
- Week 9-12: Pilot with 5 agents
- Month 4+: Full rollout

---

## Phase 2: Selective Automation + Customer Self-Service (Q2 2026)

### CS Automation

**High-Confidence Auto-Execution**:
- Cases with confidence >95% + simple resolution → auto-propose to customer
- Customer approves via SMS/email → auto-execute
- Complex cases still go to human agents
- Human override always available

**Proactive Notifications**:
- System detects issue → contacts customer before they reach out
- "We've detected your flight is delayed. Here are your options..."
- Reduces inbound support volume

**Examples**:
- Simple rebooking (single passenger, clear alternative)
- Refund processing (straightforward eligibility)
- Schedule change notifications with pre-approved alternatives

**Autonomy Criteria**:
- ✅ Confidence score >95%
- ✅ Single passenger booking
- ✅ Clear policy coverage
- ✅ Cost within automated approval limits (<€200)
- ✅ No previous issues on this booking
- ✅ Customer has Guarantee (higher trust)

### Customer Self-Service (NEW)

**Problem Identified**: Research shows "customers say guarantee covers nothing" → transparency gap

**Solution**: Reuse RAG infrastructure for customer-facing applications

#### 1. Guarantee Explainer Bot

**Pre-Purchase** (Booking flow):
```
Customer viewing itinerary with 55min connection time:
┌─────────────────────────────────────────┐
│ 🤔 Is this connection risky?            │
│                                         │
│ ✅ Pineapple Guarantee recommended (+€8)    │
│                                         │
│ Why? Short connection (55min) at busy  │
│ airport. Historical success: 78%.       │
│ Guarantee covers rebooking if missed.   │
│                                         │
│ [Learn More] [Add Guarantee]            │
└─────────────────────────────────────────┘
```

**During Disruption** (Proactive):
```
Flight delayed detected:
┌─────────────────────────────────────────┐
│ Your flight BA123 is delayed 45min     │
│                                         │
│ ✅ You have Pineapple Guarantee              │
│ ✅ Connection still possible (70% conf) │
│                                         │
│ If you miss connection, we'll:          │
│ • Rebook you automatically              │
│ • Cover cost difference                 │
│ • Provide updates via SMS               │
│                                         │
│ [Track Flight] [See Alternatives]       │
└─────────────────────────────────────────┘
```

**Post-Purchase Clarity**:
```
Customer: "Does my guarantee cover this weather delay?"

Bot: Based on your booking KW123456:
✅ YES - Your Guarantee covers weather-related missed connections
📋 Relevant rule: RULE-001 (Guarantee Terms Section 3.2)
💰 Cost to you: €0 for rebooking
⏱️ We can help within 5 minutes

[Get Help Now] [Read Full Terms]
```

#### 2. Risk Transparency Dashboard

**My Trips page**:
```
┌─────────────────────────────────────────┐
│ Upcoming Trip: Prague → Dublin → Boston │
│                                          │
│ 🟢 Connection 1: Low Risk (3h buffer)   │
│ 🟡 Connection 2: Medium Risk (1h)       │
│    → Consider adding Guarantee          │
│                                          │
│ ⚠️ Weather alert: Snow forecast Boston  │
│    → We're monitoring your flights      │
└─────────────────────────────────────────┘
```

#### 3. "What If?" Scenarios

**Pre-Booking Tool**:
```
Planning a trip? Check coverage:

"What if I miss my connection due to first flight delay?"
→ Shows: Guarantee coverage, typical resolution time, cost

"What if the airline cancels my flight?"
→ Shows: Airline vs Pineapple Travel responsibility, EU261 rights, options

"What if I need to change my booking?"
→ Shows: Change fees, flexibility options, cost breakdown
```

### Success Criteria (Phase 2)

**Automation**:
- 20% of cases auto-resolved (high-confidence)
- Auto-resolution CSAT >4.2/5
- Zero escalations due to automation errors
- TTFR for automated cases: <2 minutes

**Customer Self-Service**:
- Guarantee attachment rate: +15% (from transparency)
- Support ticket deflection: 30% reduction for "what if" questions
- Customer trust score improvement: +20%
- Time to customer understanding: 10min → 30sec

### Business Impact
- **Cost savings**: €180K/year (automation + deflection)
- **Revenue increase**: €200K/year (higher guarantee attachment)
- **Customer LTV**: +12% (increased trust and retention)

---

## Phase 3: Proactive Intelligence (Q3 2026)

### Predictive Features

#### 1. Risk Scoring at Booking Time

**Integration Point**: During booking flow, before customer confirms

**Functionality**:
- ML model analyzes itinerary risk factors:
  - Connection times
  - Airport congestion patterns
  - Airline on-time performance
  - Weather patterns (seasonal)
  - Historical miss rates for similar routes
- Real-time risk score: 0-100

**Customer Experience**:
```
You're booking: LHR → CDG → BCN
┌─────────────────────────────────────────┐
│ ⚠️ Connection Risk: Medium (65/100)     │
│                                          │
│ Factors:                                 │
│ • 1h 15min connection at CDG            │
│ • Peak travel time (Friday 6pm)         │
│ • Terminal change required              │
│                                          │
│ Historical success rate: 73%             │
│                                          │
│ Recommendations:                         │
│ ✅ Add Pineapple Guarantee (+€8)             │
│ 🔄 See safer alternatives (+45min)      │
└─────────────────────────────────────────┘
```

**Business Logic**:
- Low risk (0-40): Guarantee optional
- Medium risk (41-70): Guarantee recommended
- High risk (71-100): Guarantee strongly recommended + show alternatives

#### 2. Pre-emptive Rebooking Suggestions

**Trigger**: Before disruption impacts customer

**Example Flow**:
```
System detects:
- Customer flight BA456 departs in 6 hours
- First leg BA123 showing 80% probability of 2h delay (weather)
- Customer will likely miss BA456

Proactive action:
1. Hold seat on alternative flight BA789
2. Send notification: "We're monitoring a potential delay..."
3. Customer clicks link → sees held alternative
4. Customer confirms switch → automatic rebooking
5. Original booking cancelled, no cost to customer
```

**Success Metrics**:
- Predict issues 4+ hours before impact: >60% of cases
- Customer acceptance of pre-emptive rebooking: >70%
- Reduce "in-airport emergencies": -40%

#### 3. Smart Routing Recommendations

**At Booking Time**:
- Analyze multiple routing options
- Score by: price + convenience + risk
- Recommend optimal balance

**Example**:
```
Option A: €350, 2 stops, Medium risk (55)
Option B: €380, 1 stop, Low risk (25) ← RECOMMENDED
Option C: €320, 3 stops, High risk (78)

Why we recommend B:
• Only €30 more than cheapest
• 40% lower risk than Option A
• Saves 3h total travel time
• Direct connection (no terminal changes)
```

### Real-Time Intelligence

#### Live Status + Personalized Impact

**Customer View** (Mobile app/SMS):
```
🔴 LIVE: Your flight BA123 to Dublin

Status: Delayed 45 minutes
Departure: 14:00 → 14:45

Impact on you:
✅ Connection still safe (70% confidence)
⏱️ New connection buffer: 1h 20min
🎯 Gate change likely - we'll notify you

We're monitoring alternatives if needed.

Last updated: 2 min ago
```

#### Smart Notifications

**Tiered Alerts**:
- 🟢 **FYI**: "Minor delay, connection safe"
- 🟡 **Watch**: "Monitoring closely, alternatives ready"
- 🔴 **Action**: "Need to rebook, tap to see options"

### Success Criteria (Phase 3)

- Pre-emptive actions taken: 40% of disruptions
- Customer satisfaction with proactive comms: >4.5/5
- "In-airport emergencies" reduced by 50%
- Average stress score (survey): -30%
- Guarantee renewal rate: +20%

### Business Impact
- **Cost savings**: €250K/year (fewer emergency resolutions)
- **Customer retention**: +15% (reduced travel stress)
- **NPS improvement**: +18 points

---

## Phase 4: Advanced AI (Q4 2026)

### Multi-Agent System Architecture

**Beyond single LLM** → Specialised agents working together

#### Agent Roles

**1. Negotiation Agent**
- Talks to airline APIs on customer's behalf
- Requests compensation, upgrades, lounge access
- Understands airline-specific policies
- Negotiates best outcome for customer

**Example**:
```
Customer missed connection (airline fault)
→ Negotiation Agent contacts airline API
→ Requests: rebooking + lounge access + meal voucher
→ Airline approves 2/3
→ Agent accepts, informs customer
```

**2. Personalization Agent**
- Learns customer preferences over time
- Remembers: preferred airlines, seat choices, dietary needs
- Applies preferences to resolution options
- Improves satisfaction through tailored solutions

**Example**:
```
Customer history: Always picks window seat, prefers morning flights
Rebooking needed
→ Personalisation Agent prioritises:
  - Morning flight options first
  - Reserves window seat automatically
  - Filters out red-eye flights
```

**3. Sentiment Analysis Agent**
- Monitors customer messages for frustration/urgency
- Escalates emotionally charged cases to senior agents
- Adjusts communication tone based on sentiment
- Flags VIP customers needing white-glove service

**Example**:
```
Customer message: "This is the THIRD TIME my flight is cancelled!!! I have a wedding!!!"
→ Sentiment Agent detects: High frustration + urgency
→ Escalates to senior agent immediately
→ Flags for expedited resolution + compensation
→ Suggests empathetic communication template
```

**4. Context Enrichment Agent**
- Continuously gathers additional context
- Weather, airport delays, airline strikes, news
- Enriches LLM reasoning with real-time data
- Predicts cascading failures

### Context Expansion

#### External Data Integration

**1. Weather Intelligence**
- NOAA API integration
- Predict weather-related delays 24-48h ahead
- Proactive notifications: "Snow forecast for your departure city"

**2. Airport Congestion Modeling**
- Real-time security wait times
- Terminal traffic patterns
- Historical connection success rates by airport

**3. Airline Performance Analytics**
- Historical on-time performance by route
- Airline-specific delay patterns
- Maintenance schedule awareness (public data)

**4. Geopolitical Events**
- Strike notifications
- Air traffic control issues
- Regulatory changes (visa requirements, etc.)

### Success Criteria (Phase 4)

- Multi-agent coordination success rate: >95%
- Customer satisfaction with personalized solutions: >4.6/5
- Sentiment-based escalation accuracy: >90%
- Negotiation win rate (securing extras): >60%

### Business Impact
- **Customer LTV**: +25% (personalization improves retention)
- **Cost per resolution**: -30% (better negotiation with airlines)
- **NPS**: +25 points (customers feel "truly understood")

---

## Phase 5: Ecosystem & Platform (2027+)

### B2B2C Applications

#### 1. White-Label Solution for OTAs

**Product**: "Pineapple Intelligence Platform"
- Package the CS automation system
- Sell to other online travel agencies
- Customizable for their policies/branding
- Revenue: SaaS model (per case + setup fee)

**Target Market**:
- Mid-size OTAs lacking AI capabilities
- Regional travel agencies
- Corporate travel management companies

**Business Model**:
- Setup fee: €50K-€100K
- Per-case fee: €0.10-€0.20
- Enterprise tier: €200K/year unlimited

#### 2. API for Travel Insurance Companies

**Product**: "Disruption Intelligence API"
- Real-time risk scoring
- Claim validation automation
- Fraud detection
- Policy recommendation engine

**Use Case**:
```
Insurance company uses API:
1. Customer buys travel insurance
2. API scores trip risk
3. Dynamic pricing based on risk
4. Real-time claim validation
5. Faster payouts (automated)
```

**Revenue**: Per-API-call pricing + enterprise contracts

#### 3. Partner Airline Integration

**Collaboration Model**:
- Share disruption data (anonymized) with partner airlines
- Airlines get early warning of cascading delays
- Pineapple Travel gets priority rebooking access
- Win-win: Better outcomes for shared customers

### Industry Leadership

#### 1. Shared Industry Knowledge Base

**Vision**: Raise the bar for entire industry

**Concept**:
- Anonymized resolution patterns shared across OTAs
- "What worked" database (open source)
- Best practices for virtual interlining
- Ethical AI in travel standards

**Benefit**:
- Position Pineapple Travel as industry leader
- Attract top talent (working on cutting-edge)
- Partnerships with research institutions
- Speaking opportunities at conferences

#### 2. Research & Publications

**Topics**:
- "Human-in-the-loop AI for high-stakes decisions"
- "Building trust in AI through transparency"
- "Proactive customer support at scale"

**Impact**:
- Thought leadership
- Recruiting advantage
- Industry credibility

### Success Criteria (Phase 5)

- B2B customers: 5+ OTAs using platform
- API revenue: €500K+/year
- Industry partnerships: 3+ airlines
- Conference talks: 10+/year
- Open-source contributions: Active community

### Business Impact
- **New revenue streams**: €2M+/year (B2B)
- **Brand value**: Industry leader positioning
- **Talent acquisition**: Top 1% AI/PM talent
- **Strategic moats**: Network effects, data advantage

---

## Innovation Highlights

### What Makes This Cutting-Edge?

1. **Proactive, Not Reactive**
   - Industry standard: Wait for customer complaint
   - Pineapple Travel approach: Detect and resolve before complaint

2. **Transparent AI**
   - Industry standard: Black box automation
   - Pineapple Travel approach: Explainable decisions, cited rules, customer education

3. **Human-AI Partnership**
   - Industry standard: Replace humans OR ignore AI
   - Pineapple Travel approach: Augment humans, gradual autonomy based on trust

4. **Customer-First Data Use**
   - Industry standard: Use data to minimize cost
   - Pineapple Travel approach: Use data to minimize customer stress

5. **Platform Thinking**
   - Industry standard: Build for internal use only
   - Pineapple Travel approach: Build once, leverage everywhere (CS + customer-facing + B2B)

---

## Technical Evolution

### Architecture Maturity Path

**Phase 1**: Single-agent RAG system
- One LLM per task (classification, reasoning)
- Prompt engineering + RAG
- Human approval for all

**Phase 2**: Multi-model orchestration
- Specialised models for specialised tasks
- Confidence-based routing
- Selective automation

**Phase 3**: Predictive + real-time systems
- ML models for risk prediction
- Streaming data processing
- Event-driven architecture

**Phase 4**: Multi-agent collaboration
- Autonomous agents with specialised roles
- Agent-to-agent communication
- Complex orchestration

**Phase 5**: Platform + ecosystem
- API-first architecture
- Multi-tenancy support
- Self-service configuration

### ML/AI Capabilities Evolution

| Phase | Capability | Technique |
|-------|-----------|-----------|
| 1 | Context retrieval | RAG (vector + keyword) |
| 1 | Option generation | LLM prompting |
| 1 | Classification | Fine-tuned GPT-4o mini |
| 2 | Confidence scoring | Calibrated probabilities |
| 2 | Customer Q&A | Conversational RAG |
| 3 | Risk prediction | Supervised ML (XGBoost) |
| 3 | Disruption forecasting | Time-series models |
| 4 | Personalization | Collaborative filtering + LLM |
| 4 | Sentiment analysis | Fine-tuned BERT |
| 4 | Multi-agent coordination | Reinforcement learning |
| 5 | Cross-company learning | Federated learning |

---

## Business Metrics Evolution

### North Star Metric Shift

**Phase 1-2**: Time to First Resolution (TTFR)
- Efficiency focused
- Agent productivity

**Phase 3-4**: Customer Stress Reduction
- Experience focused  
- Proactive = less stress

**Phase 5**: Customer Lifetime Value (LTV)
- Business focused
- Long-term retention

### Expected ROI by Phase

| Phase | Investment | Annual Savings | New Revenue | Net Impact |
|-------|-----------|---------------|-------------|------------|
| 1 | €150K | €114K | - | -€36K (Y1) |
| 2 | €200K | €180K | €200K | +€180K |
| 3 | €250K | €250K | €100K | +€100K |
| 4 | €300K | €150K | €300K | +€150K |
| 5 | €400K | - | €2,000K | +€1,600K |
| **Total** | €1,300K | €694K | €2,600K | **+€1,994K** |

*Note: Phase 1 investment pays back in Phase 2+*

---

## Risk Mitigation

### Risks by Phase

**Phase 1-2**:
- ⚠️ Agents don't trust system → Mitigation: Full transparency, human override
- ⚠️ LLM makes mistakes → Mitigation: Human review, validation layers
- ⚠️ Costs exceed budget → Mitigation: Caching, batch processing, model optimisation

**Phase 3-4**:
- ⚠️ Predictions wrong → Mitigation: Conservative thresholds, human fallback
- ⚠️ Customers dislike proactive contact → Mitigation: Opt-in preferences, A/B test
- ⚠️ Multi-agent complexity → Mitigation: Incremental rollout, robust monitoring

**Phase 5**:
- ⚠️ Security concerns (multi-tenant) → Mitigation: Isolated deployments, SOC 2 compliance
- ⚠️ Competitive response → Mitigation: First-mover advantage, network effects
- ⚠️ Regulatory changes → Mitigation: Flexible architecture, compliance team

---

## Open Questions for Discussion

1. **Phase 2 Customer-Facing**: Should this be in-app, web, or SMS-based? All three?

2. **Guarantee Attachment Strategy**: Does transparency increase or decrease attachment rate? Need A/B test.

3. **Proactive Communication Limits**: How much is helpful vs annoying? Customer preferences?

4. **B2B Timing**: Too early in Phase 5? Could white-label in Phase 3?

5. **Data Sharing Ethics**: What level of anonymization for industry knowledge base?

6. **Personalization Privacy**: How to balance personalization with privacy concerns?

7. **Multi-Agent Complexity**: Is Phase 4 over-engineering? Could simpler approaches work?

8. **Platform Economics**: Build vs buy for Phase 5 infrastructure?

---

## Success Definition

### MVP Success (Phase 1)
- Proves AI can assist agents effectively
- Collects data for future autonomy
- Achieves measurable TTFR improvement
- Builds organizational confidence in AI

### Long-Term Success (Phase 5)
- Pineapple Travel becomes industry leader in AI-powered travel support
- Customer experience differentiation drives market share
- Platform revenue creates new business line
- Sets industry standards for responsible AI use

### Ultimate Vision
**Transform customer support from cost center to competitive advantage and revenue generator.**

---

*Document Status*: Draft for review
*Next Steps*: Review, refine, prioritise, validate assumptions
*Owner*: Product Team + Engineering + Customer Success

