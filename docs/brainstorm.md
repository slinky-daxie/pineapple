# Brainstorming Session: Agent-Assisted CS System for Pineapple Travel
*Date: January 1, 2026*


## Context

Building an agent-assisted system for resolving virtual interlining failures at Pineapple Travel. The system will augment (not replace) human CS agents, focusing on:
- Missed connections on self-transfer itineraries
- Schedule changes and cancellations
- Complex multi-airline failures

**Key Philosophy**: Human-in-the-loop from day 1, gradual autonomy based on learning.

---

## Initial Questions & Answers

### Detection & Categorisation

**Q: How does the system know a failure is happening?**
A: Multiple triggers:
- Real-time flight status APIs (3rd party trackers)
- Customer-initiated contact (chat/email)
- Proactive monitoring of bookings

**Q: What failure types matter most?**
A: **Urgency-based prioritisation**, not category-based:
- Ticket error 4 weeks out = low urgency
- Missed connection (person in airport/in air) = high urgency
- Time-to-resolve is the key metric

**Q: Should categorisation happen before or after customer contact?**
A: **Both**:
- Before: If we detect a problem via API, categorise and proactively reach out
- After: If customer initiates, categorise their issue immediately

### Context Gathering

**Data sources**:
- Booking data: Pineapple Travel's internal database
- Flight status: Third-party APIs (FlightAware, OAG)
- Policy knowledge base: Internal docs (Guarantee terms, refund policies)
- Historical resolutions: Support ticket system
- Customer profile: Value, history, preferences

**Handling missing/contradictory data**:
- Example: API says "on time" but customer says "delayed"
- Strategy: Surface conflict to agent with confidence flag, don't auto-decide

**Latency tolerance**:
- Proactive notifications: Minutes OK (batch processing)
- Customer-initiated: <5 seconds (customer is waiting)

### Decision Boundaries (MVP)

**What can auto-resolve?**
- **MVP: Nothing** - Everything needs human confirmation
- Purpose: Training data collection, build trust
- Future: Gradually enable auto-resolution for high-confidence cases

**What needs human review?**
- **MVP: Everything**
- Future: Maintain human review for:
  - Multiple problems on same customer
  - High-value customers
  - Multi-leg failures
  - Edge cases with low confidence

**What's absolutely escalated?**
- Safety issues
- Legal gray areas
- Complex multi-party disputes
- Note: Human still gets full context automatically assembled

### Explainability

**Who needs explanations?**
- Leadership/compliance: Need to understand why AI made decisions
- Audit trail for regulatory compliance
- Post-incident analysis

**Level of detail?**
- **Full decision trace** with:
  - Input data used
  - Policies considered
  - Options generated
  - Confidence scores
  - Final recommendation + rationale

**Confidence scores**:
- LLM outputs log probabilities (token probability)
- Set thresholds: >0.9 = high confidence, <0.5 = needs review
- Surface in UI: 🟢 High / 🟡 Medium / 🔴 Low confidence

### Success Metrics

**North Star**: Time to First Resolution (TTFR)
- Direct link to cost savings
- Measurable impact on customer satisfaction

**Supporting metrics**:
- Agent cognitive load → Employee CSAT
- Customer CSAT (disrupted trips specifically)
- Repeat contact rate
- Cost per resolution
- Agent approval rate (% of LLM suggestions accepted)

---

## System Architecture Overview

### Trigger Layer
- Flight Status APIs
- Customer Chat/Contact
- Booking System Events

### Detection & Triage
- Event Processor
- Urgency Scorer (time-sensitive prioritisation)
- Category Classifier

### Context Assembly (RAG)
- Booking Data retrieval
- Flight Status lookup
- Policy Knowledge Base search
- Historical Resolutions similarity search
- Customer Profile enrichment

### LLM Reasoning Engine
- Context Synthesizer
- Option Generator
- Policy Validator
- Explainer (decision rationale)

### Human Interface
- Agent Dashboard (see suggestions + context)
- Customer Chat (if approved, communicate)
- Approval Queue (human review)

### Learning Loop
- Decision Logger (what was suggested)
- Outcome Tracker (what actually happened)
- Model Evaluator (compare, improve)

---

## LLM Strategy Decisions

### Multi-Model Approach (Not One Size Fits All)

**Urgency Scoring**: GPT-4o mini
- Why: Fast (<500ms), cheap, good at structured output
- Alternative: Claude Haiku
- Trade-off: Speed over nuance; urgency is relatively binary

**Option Generation**: Claude 3.5 Sonnet
- Why: Best reasoning for complex multi-constraint problems, excellent at showing work
- Alternative: GPT-4
- Trade-off: Cost vs quality; Sonnet's reasoning transparency worth extra cost

**Embeddings (RAG)**: Open source (bge-large or gte-large)
- Why: No API costs, runs locally, data privacy
- Alternative: OpenAI ada-002
- Trade-off: Control + cost vs convenience

**Policy Validation**: Rule engine + LLM hybrid
- Why: Guarantee compliance, hard rules for legal requirements
- Alternative: Pure LLM (too risky)
- Trade-off: Some rigidity, but necessary for compliance

### Why NOT Fine-Tuning in MVP?
- Not enough labeled data yet (will collect from human approvals)
- Prompt engineering + RAG faster to iterate
- Fine-tuning comes in Phase 2 after 1000+ human-approved decisions

---

## RAG Architecture Details

**Why RAG for this use case?**
- Pineapple Travel's policies are complex and change frequently
- Historical resolutions are valuable (similar cases)
- Need explainability (can cite sources)
- Can update knowledge without retraining

**Key decisions**:

1. **Chunking strategy**: Policy sections (logical units)
   - Why: Preserve meaning, better retrieval precision
   - Alternative: Arbitrary 512 tokens (loses context)

2. **Hybrid search**: Vector + keyword (BM25)
   - Why: Flight numbers, booking IDs need exact match
   - Alternative: Pure vector (misses exact terms)

3. **Reranking**: Cross-encoder for top-k results
   - Why: Improve relevance, reduce LLM context cost
   - Alternative: Send all results (expensive + noisy)

---

## Phased Autonomy Approach

### Phase 1: MVP (Human-in-the-loop)
- LLM suggests resolution options
- Agent reviews ALL suggestions
- Agent approves/modifies/rejects
- Log every decision for training data

**Goal**: Build trust, collect data, prove value

### Phase 2: Assisted Autonomy
- LLM suggests with confidence scores
- High-confidence cases: Auto-propose to customer
- Customer can accept or request human agent
- Simple cases auto-execute after customer confirmation

**Goal**: Reduce TTFR for straightforward cases

### Phase 3: Proactive Resolution
- System detects issues before customer contact
- Auto-proposes solutions proactively
- Human escalation for edge cases
- Continuous learning from outcomes

**Goal**: Shift from reactive to proactive support

---

## Why This Shows Strong PM Thinking

1. **Risk management**: Start conservative, prove value, then scale
2. **Data strategy**: Use MVP to collect training data
3. **Human-centered**: Augment, don't replace
4. **Measurable**: Clear metrics tied to business outcomes
5. **Technical depth**: Specific model choices with rationale
6. **Realistic**: Acknowledges limitations and unknowns

---

## Convey Thinking Through Documentation

### 1. Decision Log
- Every major technical choice documented
- Rationale, alternatives, trade-offs explicit
- Shows systematic thinking

### 2. System Design Doc
- Architecture diagrams
- Data flows
- Integration points
- Error handling

### 3. Evaluation Framework
- How to measure success
- Offline and online testing
- Continuous improvement

### 4. Build Plan
- Phased approach
- MVP scope clearly defined
- Future roadmap

---

## Next Steps

1. Create detailed documentation (decision log, system design, evaluation framework, build plan)
2. Build MVP in LangFlow (RAG pipeline with sample policies)
3. Create simple frontend to demonstrate agent experience
4. Prepare presentation for interview

**Goal**: Show how I work with LLMs in real life, making informed decisions with clear rationale.

---

## Refinements (January 3, 2026)

### MVP-Critical Architectural Changes

**1. Prompt-Injected Rule Book**
- **What**: Add explicit rule book as part of LLM system prompt (Step 4)
- **Why**: 
  - Faster iteration than hard-coded validation logic
  - Easy to audit and version control
  - Clear compliance boundaries for LLM
  - Can be tested and validated independently
- **Feeds into**: LLM Reasoning step as part of context

**2. Structured Output Format**
- **What**: Formalize LLM output with explicit fields
- **Why**: 
  - Agents need fast review capability
  - Reduces cognitive load
  - Enables metrics tracking
  - Critical for production readiness
- **Includes**:
  - 2-4 resolution options
  - Confidence scores per option (0-100%)
  - Policy citations (which rules apply)
  - Reasoning explanations
  - Uncertainty flags (missing data, edge cases)
  - Escalation triggers

**3. Booking Database Integration**
- **What**: Explicit connection to customer booking database in Context Assembly (Step 3)
- **Why**:
  - **Verify claim legitimacy**: Confirm customer has actual booking
  - **Cross-reference with Flight API**: Validate delays/cancellations against actual bookings
  - **Enable proactive detection**: Monitor bookings for flight issues before customer complains
  - **Provide resolution context**: Pull specific booking details (dates, routes, prices, class)
  - **Prevent fraud**: Ensure claims match real bookings
- **Critical for MVP**: Without this, we're trusting customer claims without verification

### Impact on Architecture

These additions strengthen MVP viability by:
- Making system auditable (rule book + structured output)
- Enabling fast agent review (structured output + confidence)
- Ensuring data integrity (booking database verification)
- Supporting proactive case detection (booking + flight status cross-reference)

All changes documented in:
- `design/agentic-flow-v1.md` (updated diagram + flow steps)
- `docs/decision-log.md` (decision #9 on prompt-injected rules)

---

## Future Vision & Roadmap Discussion (January 3, 2026 - Evening)

### Context
With 1 day before sharing GitHub, need to show:
- Not just MVP thinking → where does this go?
- End state vision (automation, advanced features)
- Strategic PM thinking beyond the immediate build

### Key Insights

**1. Customer-Facing Applications** (High-value insight)
- Problem: Research shows "customers say guarantee covers nothing"
- Root cause: Transparency gap → customers don't understand coverage
- Solution: Reuse same RAG infrastructure for customer education
- **Brilliant leverage**: Same tech stack, different interface, solves trust issue

**Applications**:
- Pre-purchase: "Should I buy Guarantee for this risky connection?"
- During trip: "What does my Guarantee cover in this situation?"
- Post-issue: "Why this happened" explainer

**Business Impact**:
- Higher guarantee attachment rate (transparency → trust)
- Reduced disappointment (set expectations upfront)
- Ticket deflection (answer "what if" questions proactively)
- Customer education scales with AI (no human cost)

**2. Proactive Intelligence** (Phase 3)
- Don't wait for customer to contact us → detect and resolve first
- Predictive features:
  - Risk scoring at booking time (show upfront)
  - Pre-emptive rebooking (before disruption happens)
  - Smart routing recommendations (optimise price/risk/convenience)
- Shift from reactive support → proactive travel assistance

**3. Multi-Agent Systems** (Phase 4)
- Beyond single LLM → specialised agents working together
- Negotiation agent (talks to airlines)
- Personalization agent (learns preferences)
- Sentiment agent (detects frustration, escalates)
- Context enrichment agent (real-time external data)
- More sophisticated than simple automation

**4. Platform & Ecosystem** (Phase 5)
- B2B applications: White-label for other OTAs
- API for travel insurance companies
- Partner airline integration
- Industry leadership through shared learnings
- Transform from internal tool → platform revenue

### Roadmap Structure Created

**5 Phases**:
1. MVP (Q1 2026) - Human-in-the-loop, prove value
2. Selective Automation + Customer Self-Service (Q2 2026)
3. Proactive Intelligence (Q3 2026)
4. Advanced AI & Multi-Agent (Q4 2026)
5. Ecosystem & Platform (2027+)

**Evolution of Metrics**:
- Phase 1-2: TTFR (efficiency)
- Phase 3-4: Customer stress reduction (experience)
- Phase 5: LTV (business value)

**Technical Maturity Path**:
- Single-agent RAG → Multi-model orchestration → Predictive systems → Multi-agent collaboration → Platform

### Innovation Highlights to Emphasise

1. **Proactive not reactive** (industry standard: wait for complaints)
2. **Transparent AI** (not black box)
3. **Human-AI partnership** (augment, don't replace)
4. **Customer-first data use** (minimize stress, not just cost)
5. **Platform thinking** (build once, leverage everywhere)

### Questions for Tomorrow's Review

- Customer-facing apps: In-app? Web? SMS? All three?
- Does transparency increase or decrease guarantee attachment?
- How much proactive communication is helpful vs annoying?
- Is Phase 4 multi-agent over-engineering?
- Should B2B platform come earlier (Phase 3)?
- Data sharing ethics: What level of anonymization?

### Documents Created
- `docs/product-roadmap.md` - Full 5-phase vision with:
  - Business metrics per phase
  - Technical evolution
  - Innovation callouts
  - Risk mitigation
  - Open questions for discussion

### Next Steps (Tomorrow)
1. Review roadmap with fresh eyes
2. Refine phases (too ambitious? Missing pieces?)
3. Prioritise "must show" vs "nice to have"
4. Validate assumptions (are these good ideas?)
5. More brainstorming on specific features
6. Decide what to emphasise in interview

### Why This Matters
Shows interviewer:
- Strategic thinking (beyond MVP)
- Customer empathy (transparency solves research finding)
- Technical vision (AI capabilities evolution)
- Business model thinking (platform revenue)
- Not just "builder" but "product thinker"

