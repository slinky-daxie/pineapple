# Build Plan: Agent-Assisted CS System

*Phased implementation approach for Pineapple Travel project*

---

## Overview

**Goal**: Demonstrate PM thinking + technical depth for Principal CS PM role

**Philosophy**: Start simple, prove value, iterate based on learning

**Timeline**: MVP by January 6 (available for interview discussion)

---

## What to Build (Scope)

### In Scope for Interview Demo
1. **Core RAG pipeline** (LangFlow)
   - Policy knowledge base with sample policies
   - Hybrid search (vector + keyword)
   - Context assembly from mock data
   
2. **LLM reasoning** (Claude Sonnet via API)
   - Generate resolution options
   - Include explanations and confidence scores
   
3. **Simple agent UI** (React frontend)
   - Display case context
   - Show LLM-generated options
   - Approve/reject interface (mock execution)
   
4. **Demo scenario**
   - 3-4 realistic failure scenarios from research
   - Show system handling each case type
   - Demonstrate urgency-based prioritisation

### Out of Scope (Acknowledge, Don't Build)
- Real-time flight API integration
- Actual booking system integration
- Full execution layer (rebooking, refunds)
- Production infrastructure (monitoring, scaling)
- Multi-language support
- Historical case database (use mock similar cases)

**Justification**: Interview is about *thinking* and *decision-making*, not production code. Demonstrate architecture understanding without overbuilding.

---

## Three-Phase Strategy

### Phase 1: MVP for Interview (This Week)

**Deliverables**:
1. Documentation (✅ completed):
   - Decision log
   - System design
   - Evaluation framework
   - Build plan (this doc)
   
2. Working prototype:
   - LangFlow RAG pipeline
   - Simple frontend demo
   - 3-4 test scenarios
   
3. Presentation materials:
   - Architecture slides
   - Demo walkthrough
   - "Why I made these choices" talking points

**Success Criteria**:
- Can demonstrate full flow in <5 minutes
- Can explain any technical decision
- Can discuss trade-offs and alternatives
- Shows PM + technical depth

### Phase 2: If I Get the Job (Weeks 1-4)

**Real MVP with Pineapple Travel team**:
- Integrate with real Pineapple Travel booking system
- Connect to flight status APIs
- Deploy to staging environment
- Run shadow mode (collect data, don't show to agents)
- Tune based on real cases

**Success Criteria**:
- System processes real cases in shadow mode
- Agreement rate with agent decisions >60%
- No crashes, acceptable latency
- Green light for Phase 3

### Phase 3: Production Rollout (Months 2-3)

**Pilot with 5 agents**:
- Agents see suggestions, can approve/reject
- Collect approval rates and feedback
- Iterate on prompts and UX
- Measure TTFR improvement

**Success Criteria**:
- Agent approval rate >75%
- TTFR reduction >30%
- CSAT improvement measurable
- Expand to full team

---

## Detailed Build Plan (MVP for Interview)

### Day 1: Foundation (January 2)

**Morning: Documentation** ✅
- [x] Create decision log
- [x] Create system design doc
- [x] Create evaluation framework
- [x] Create build plan

**Afternoon: Environment Setup**
- [ ] Install LangFlow locally
- [ ] Set up Anthropic API key (Claude)
- [ ] Set up OpenAI API key (embeddings fallback if needed)
- [ ] Test basic LangFlow flow

**Evening: Policy KB**
- [ ] Extract Pineapple Guarantee terms (from research)
- [ ] Create 5-10 sample policy documents
- [ ] Chunk policies (by section)
- [ ] Generate embeddings

**Time estimate**: 6-8 hours

### Day 2: RAG Pipeline (January 3)

**Morning: Vector Store**
- [ ] Set up Qdrant (local Docker container)
- [ ] Load policy embeddings
- [ ] Test vector search with sample queries

**Afternoon: Hybrid Search**
- [ ] Add keyword search component (simple BM25)
- [ ] Implement score fusion
- [ ] Test retrieval quality (manual spot check)

**Evening: Context Assembly**
- [ ] Create mock booking data (3-4 scenarios)
- [ ] Create mock flight status data
- [ ] Create mock customer profiles
- [ ] Build context assembly logic

**Time estimate**: 6-8 hours

### Day 3: LLM Reasoning (January 4)

**Morning: Prompt Engineering**
- [ ] Design system prompt for Claude
- [ ] Add few-shot examples (2-3 good resolutions)
- [ ] Define output schema (JSON)

**Afternoon: Integration**
- [ ] Connect RAG output to Claude API
- [ ] Implement option generation
- [ ] Add policy validation logic
- [ ] Test with 3-4 scenarios

**Evening: Refinement**
- [ ] Tune confidence scoring
- [ ] Improve explanations
- [ ] Add edge case handling
- [ ] Test quality on all scenarios

**Time estimate**: 6-8 hours

### Day 4: Frontend Demo (January 5)

**Morning: Setup**
- [ ] Create React app (Vite for speed)
- [ ] Design agent dashboard wireframe
- [ ] Implement basic layout

**Afternoon: Core UI**
- [ ] Case queue view
- [ ] Case detail view
- [ ] Options display with confidence indicators
- [ ] Approve/reject buttons (mock actions)

**Evening: Polish**
- [ ] Add styling (clean, professional)
- [ ] Add loading states
- [ ] Test full flow end-to-end
- [ ] Fix bugs

**Time estimate**: 8 hours

### Day 5: Demo Prep (January 6)

**Morning: Scenarios**
- [ ] Create 4 demo scenarios:
  1. **High urgency**: Missed connection (in airport)
  2. **Medium urgency**: Schedule change (departs tomorrow)
  3. **Low urgency**: Ticket error (departs in 2 weeks)
  4. **Complex**: Multiple issues (missed + refund)

**Afternoon: Walkthrough**
- [ ] Practice demo flow
- [ ] Time it (<5 min for full demo)
- [ ] Prepare "deep dive" talking points for each decision
- [ ] Anticipate questions

**Evening: Presentation Slides** (Optional)
- [ ] Architecture overview (1 slide)
- [ ] LLM decisions (1 slide)
- [ ] Evaluation strategy (1 slide)
- [ ] Roadmap (1 slide)
- [ ] Live demo (primary)

**Time estimate**: 6 hours

---

## Demo Scenarios (Detailed)

### Scenario 1: Missed Connection - High Urgency

**Context**:
```
Customer: Sarah Chen
Location: Dublin Airport
Booking: KW789012
Flights: 
  - BA123 (London → Dublin) - Landed 2.5h late (weather)
  - EI456 (Dublin → Paris) - Departed on time, MISSED
Current Time: 14:30
Next available: EI789 (18:00) or AF234 (20:30)
Pineapple Guarantee: Purchased (✅)
Customer value: €450 booking, standard tier
```

**Expected LLM Output**:
- **Option 1** (High confidence): Rebook on EI789 + lounge voucher (€125 cost)
- **Option 2** (Medium confidence): Rebook on AF234 (€80 cost, longer wait)
- **Option 3** (Low confidence): Partial refund €315 + self-book

**Demonstrates**:
- Urgency detection (critical → <5 min response)
- Policy application (Guarantee covers this)
- Multiple valid options with trade-offs
- Cost vs satisfaction balance

### Scenario 2: Schedule Change - Medium Urgency

**Context**:
```
Customer: Miguel Rodríguez
Location: Home (Madrid)
Booking: KW445566
Flights:
  - IB901 (Madrid → Rome) - Cancelled by airline
  - AZ102 (Rome → Athens) - Still valid
Departure: Tomorrow (18h from now)
Pineapple Guarantee: NOT purchased
Customer value: €280 booking, 3rd booking with Pineapple Travel
```

**Expected LLM Output**:
- **Option 1** (High confidence): Rebook on IB903 (earlier) - €60 cost
- **Option 2** (Medium confidence): Rebook on VY2105 (budget) - €40 cost
- **Option 3** (Low confidence): Full refund €280 (no guarantee, but airline fault)

**Demonstrates**:
- Without Guarantee (different policy application)
- Airline fault (EU261 considerations)
- Customer loyalty consideration (3rd booking)
- Time pressure (tomorrow) but not critical

### Scenario 3: Ticket Error - Low Urgency

**Context**:
```
Customer: Alex Johnson
Location: Home (UK)
Booking: KW112233
Issue: Name misspelled (Jonson vs Johnson) in booking
Flight: BA567 (London → Barcelona)
Departure: 14 days from now
Pineapple Guarantee: Purchased
Customer value: €120 booking, new customer
```

**Expected LLM Output**:
- **Option 1** (High confidence): Correct name with airline (free, guaranteed)
- **Option 2** (Low confidence): Rebook with correct name (€30 cost if airline refuses)

**Demonstrates**:
- Urgency scoring (low despite issue)
- Simple resolution (name correction)
- Guarantee value (even for small issues)
- Proactive communication (contact before customer stressed)

### Scenario 4: Complex - Multiple Issues

**Context**:
```
Customer: Lisa Wang
Location: Tokyo (just arrived)
Booking: KW998877
Issue: 
  - Flight 1 (BA889) landed 1h late
  - Missed Flight 2 (JL234)
  - Luggage is on JL234 (heading to Sydney without her)
  - Hotel reservation in Sydney for tonight (non-refundable)
Pineapple Guarantee: Purchased
Customer value: €1,850 booking, Gold tier (15 previous bookings)
```

**Expected LLM Output**:
- **Option 1** (Medium confidence): 
  - Rebook on next flight to Sydney (JL456, departs 4h)
  - Luggage tracking + delivery
  - Hotel voucher for tonight
  - Total cost: €450
- **Option 2** (Low confidence):
  - Escalate to senior agent (multiple moving parts)
  
**Demonstrates**:
- Complex scenario handling
- Multiple constraints (flight + luggage + hotel)
- High-value customer (different treatment)
- Appropriate escalation (low confidence → human)

---

## Technical Stack (MVP)

### Backend

```
LangFlow (orchestration)
  ├─ Python 3.11+
  ├─ Qdrant (vector store, Docker)
  ├─ Claude API (Anthropic)
  ├─ bge-large-en-v1.5 (embeddings, local)
  └─ FastAPI (for frontend integration)
```

### Frontend

```
React + TypeScript
  ├─ Vite (build tool)
  ├─ TailwindCSS (styling)
  ├─ React Query (state management)
  └─ Axios (API calls)
```

### Infrastructure

```
Local development:
  ├─ Docker (Qdrant)
  ├─ Node.js 18+
  └─ Python virtual environment
  
(Production would need: K8s, monitoring, etc - out of scope)
```

---

## Demo Flow (5 Minutes)

### Minute 1: Context Setting (Talking)
- "Pineapple Travel's virtual interlining creates complex failures"
- "Current CS: slow, inconsistent, opaque"
- "My solution: Agent-assisted system with LLMs"
- "Let me show you how it works"

### Minutes 2-4: Live Demo (Showing)

**Step 1**: Case arrives (missed connection)
- Show: Urgency scorer (HIGH), context assembly
- "System pulled booking, flight status, policies, similar cases"

**Step 2**: LLM generates options
- Show: 3 options with confidence, explanations, costs
- "Claude Sonnet reasoning through trade-offs"
- Point out: Policy citations, confidence scores

**Step 3**: Agent reviews
- "Agent sees everything, approves Option 1"
- "Human still in control, but 10min → 90sec"

**Step 4**: Quick second scenario
- "Low urgency case - system deprioritizes correctly"
- "Shows it's urgency-based, not just first-come-first-served"

### Minute 5: Technical Deep Dive (If Asked)

**Anticipated questions**:
- "Why Claude over GPT-4?" → Show decision log, explain transparency
- "How do you handle errors?" → Explain fallbacks, human escalation
- "What about costs?" → Show calculation, €0.05/case
- "How do you measure success?" → Explain evaluation framework

---

## Presentation Materials

### Slide 1: Problem

```
┌───────────────────────────────────────────┐
│ The Problem                               │
├───────────────────────────────────────────┤
│                                           │
│ Pineapple Travel's USP (virtual interlining)          │
│        ↓                                  │
│ Creates complex failures                  │
│        ↓                                  │
│ CS struggles:                             │
│   • Slow (10-15 min TTFR)                │
│   • Inconsistent resolutions              │
│   • Agent cognitive overload              │
│   • Poor CSAT (3.2/5 on disrupted trips) │
│                                           │
│ From research: Support agents "powerless  │
│ to override system decisions"             │
└───────────────────────────────────────────┘
```

### Slide 2: Solution

```
┌───────────────────────────────────────────┐
│ The Solution: Agent-Assisted System       │
├───────────────────────────────────────────┤
│                                           │
│ [Architecture diagram from system design] │
│                                           │
│ Key Principles:                           │
│ ✓ Human augmentation (not replacement)    │
│ ✓ Urgency-based prioritisation           │
│ ✓ Explainable by design                  │
│ ✓ Start conservative, learn, scale       │
└───────────────────────────────────────────┘
```

### Slide 3: LLM Decisions

```
┌───────────────────────────────────────────┐
│ LLM Architecture Decisions                │
├───────────────────────────────────────────┤
│                                           │
│ Multi-model approach:                     │
│  • GPT-4o mini: Fast classification       │
│  • Claude Sonnet: Deep reasoning          │
│  • Open-source: Embeddings (cost/privacy)│
│                                           │
│ Why Claude for reasoning?                 │
│  ✓ Best chain-of-thought transparency     │
│  ✓ Strong multi-constraint solving        │
│  ✓ Critical for compliance explainability│
│                                           │
│ RAG over fine-tuning (MVP):               │
│  ✓ No training data yet                   │
│  ✓ Policies change frequently             │
│  ✓ Can cite sources                       │
│  → Fine-tune in Phase 2 after 1000+ cases │
└───────────────────────────────────────────┘
```

### Slide 4: Impact & Roadmap

```
┌───────────────────────────────────────────┐
│ Expected Impact & Roadmap                 │
├───────────────────────────────────────────┤
│                                           │
│ MVP Targets (3 months):                   │
│  • TTFR: 10min → 3min (70% reduction)    │
│  • Agent approval rate: >85%              │
│  • CSAT: 3.2 → 4.0 (+25%)                │
│  • Cost: <€0.05/case in LLM              │
│  • Savings: €114K/year net                │
│                                           │
│ Roadmap:                                  │
│  Phase 1 (Q1): Human-in-loop, learn      │
│  Phase 2 (Q2): Selective autonomy        │
│  Phase 3 (Q3): Proactive resolution      │
│                                           │
│ Always: Continuous learning & improvement │
└───────────────────────────────────────────┘
```

---

## Talking Points (For Interview)

### Why This Problem?
- "Specific to Pineapple Travel's model (virtual interlining)"
- "Not a generic chatbot - solves real pain from research"
- "Aligns with JD: AI-powered support, daily releases, high impact"

### Design Philosophy
- "Start conservative: 100% human approval in MVP"
- "Collect training data, build trust, then autonomy"
- "This is how you responsibly deploy AI in high-stakes situations"

### Technical Depth
- "Multi-model strategy optimises for speed, cost, quality"
- "RAG before fine-tuning - learn what to fine-tune on"
- "Hybrid search for semantic + exact matching"
- "Confidence calibration enables safe autonomy later"

### PM Thinking
- "Every decision documented with alternatives and trade-offs"
- "Evaluation framework: offline → shadow → pilot → full rollout"
- "Success tied to business metrics: TTFR → cost savings"
- "Qualitative + quantitative: agent surveys matter too"

### Real-World Experience
- "At Travix, saw CS teams struggle with similar issues"
- "Long queues, scripted responses, agents wanting better tools"
- "This system would have addressed their core pain points"

### What I'd Do First If Hired
- "Week 1: Shadow mode with real cases, learn patterns"
- "Week 2-3: Iterate on prompts based on real data"
- "Week 4: Pilot with 5 agents, daily check-ins"
- "Don't rush autonomy - earn it through proven accuracy"

---

## Risk Mitigation

### Technical Risks

**Risk**: LLM hallucinates (suggests impossible flights)
- **Mitigation**: Validators, manual review in MVP, low tolerance (<2%)

**Risk**: API costs spiral
- **Mitigation**: Budget caps, caching, shift to self-hosted if needed

**Risk**: Latency too high (agents get impatient)
- **Mitigation**: <3s target, parallel processing, loading states

### Adoption Risks

**Risk**: Agents don't trust system
- **Mitigation**: Full transparency, human override always, gradual rollout

**Risk**: Customers feel "automated away"
- **Mitigation**: Human still involved, quality of resolution matters

### Business Risks

**Risk**: Doesn't improve TTFR enough to justify cost
- **Mitigation**: Clear break-even analysis, gate criteria before Phase 2

**Risk**: Leadership wants immediate autonomy (too risky)
- **Mitigation**: Show data on error rates, argue for conservative approach

---

## Success Definition (Interview Context)

**I'll consider the interview prep successful if I can**:

1. ✅ Explain the problem clearly (with research backing)
2. ✅ Walk through architecture with confidence
3. ✅ Defend every LLM decision with rationale
4. ✅ Demo working prototype (even if simple)
5. ✅ Discuss trade-offs and alternatives knowledgeably
6. ✅ Connect technical choices to business outcomes
7. ✅ Show realistic roadmap (not overpromising)
8. ✅ Demonstrate PM + technical depth

**Interview success** = Show I can:
- Think systematically about complex problems
- Make informed technical decisions
- Balance innovation with risk management
- Work effectively with engineers (speak their language)
- Measure and iterate based on data
- Keep customer needs central

---

## Post-Interview (If Interested in Continuing)

### If Offer Extended
- Discuss: What's Pineapple Travel's current CS tech stack?
- Understand: Where does this fit in their roadmap?
- Negotiate: Timeline, resources, team support

### If Not Proceeding
- Portfolio piece: Clean up, document, open-source?
- Blog post: "How I'd build an AI CS system"
- Case study for future PM interviews

---

## Appendix: Commands & Setup

### LangFlow Setup
```bash
pip install langflow
langflow run
# Open http://localhost:7860
```

### Qdrant Setup
```bash
docker run -p 6333:6333 qdrant/qdrant
```

### React App Setup
```bash
npm create vite@latest pineapple-demo -- --template react-ts
cd pineapple-demo
npm install
npm install tailwindcss axios react-query
npm run dev
```

### Environment Variables
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..." # if needed
```

---

## Time Tracking

**Planned**: 32-36 hours (Jan 2-6)
**Actual**: [To be filled during build]

**Breakdown**:
- Documentation: 6-8h ✅
- LangFlow + RAG: 12-14h
- Frontend: 8h
- Demo prep: 6h
- Buffer: 4h

