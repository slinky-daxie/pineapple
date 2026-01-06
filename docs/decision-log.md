# LLM Architecture Decision Log

*Agent-Assisted Customer Support System for Pineapple Travel*

This document records all major LLM and AI architecture decisions, including rationale, alternatives considered, and trade-offs.

---

## Decision 1: Multi-Model Strategy (Not Single LLM)

**Date**: January 2026  
**Status**: Proposed for MVP

### Context
Need to process customer support cases involving complex virtual interlining failures. Different components have different requirements (speed, cost, reasoning depth).

### Decision
Use **multiple specialised LLMs** rather than one model for everything:
- GPT-4o mini for urgency classification
- Claude 3.5 Sonnet for resolution reasoning
- Open-source embeddings for RAG retrieval

### Rationale
- **Speed**: Classification needs <500ms response
- **Cost**: Classification happens on every case; reasoning only on complex ones
- **Quality**: Reasoning needs deep multi-constraint thinking
- **Control**: Embeddings should be under our control for data privacy

### Alternatives Considered
1. **Single model (Claude Sonnet for everything)**
   - Pros: Simpler architecture, consistent behavior
   - Cons: Too expensive for high-volume classification, slower
   - Why rejected: Economics don't work at scale

2. **All GPT models**
   - Pros: Single vendor, easier management
   - Cons: GPT-4 less transparent in reasoning, more expensive
   - Why rejected: Claude's chain-of-thought superior for explainability

3. **All open-source (Llama 3, etc)**
   - Pros: No API costs, full control
   - Cons: Quality not reliable enough for production decisions yet
   - Why rejected: Risk too high for customer-facing decisions

### Trade-offs
- **Complexity**: Managing multiple models vs simpler single-model
- **Vendor risk**: Dependent on OpenAI + Anthropic
- **Cost**: Optimised cost structure vs predictability
- **Verdict**: Optimisation worth the complexity

### Success Criteria
- Classification accuracy >95%
- Reasoning quality measured by agent approval rate >80%
- P95 latency <3 seconds end-to-end
- Cost per case <$0.05

---

## Decision 2: Claude Sonnet for Resolution Reasoning

**Date**: January 2026  
**Status**: Proposed for MVP

### Context
Core reasoning engine must generate resolution options for complex multi-flight, multi-airline failures with competing constraints (cost, customer satisfaction, policy compliance).

### Decision
Use **Claude 3.5 Sonnet** as primary reasoning engine.

### Rationale
- **Transparency**: Superior chain-of-thought reasoning (shows work)
- **Constraint satisfaction**: Excellent at balancing multiple requirements
- **Structured output**: Reliable JSON generation
- **Context window**: 200k tokens handles full case context
- **Explainability**: Critical for compliance and trust

### Alternatives Considered
1. **GPT-4 / GPT-4o**
   - Pros: Slightly faster, $2.50/M tokens vs $3/M
   - Cons: Less transparent reasoning, weaker at showing work
   - Why not chosen: Explainability non-negotiable

2. **GPT-4 Turbo**
   - Pros: Cheaper ($1/M input)
   - Cons: Less capable than flagship models
   - Why not chosen: This is our core value-add, can't compromise

3. **Open-source (Llama 3 70B+)**
   - Pros: Self-hosted, no usage costs
   - Cons: Reasoning quality gap, infrastructure burden
   - Why not chosen: Not production-ready for this use case

### Trade-offs
- **Cost**: ~$3/M tokens (input) vs cheaper alternatives
- **Speed**: 2-3 seconds vs 1-2s for GPT-4o
- **Quality**: Best reasoning vs faster/cheaper
- **Verdict**: Quality justifies cost for this critical component

### Success Criteria
- Agent approval rate >80% (agents accept LLM suggestions)
- Explainability score >4/5 (from agent surveys)
- Hallucination rate <2% (invalid suggestions)
- Policy compliance 100% (validated by rule engine)

---

## Decision 3: RAG Over Fine-Tuning for MVP

**Date**: January 2026  
**Status**: Proposed for MVP

### Context
Need to incorporate Pineapple Travel's policies, guarantee terms, historical cases, and airline rules into LLM decision-making.

### Decision
Use **RAG (Retrieval-Augmented Generation)** in MVP, defer fine-tuning to Phase 2.

### Rationale
- **Data availability**: Don't have 1000+ labeled training cases yet
- **Iteration speed**: Can update policies without retraining
- **Explainability**: Can cite specific policy sections
- **Cost**: No training costs, immediate deployment
- **Flexibility**: Easy to test different retrieval strategies

### Alternatives Considered
1. **Fine-tuning from day 1**
   - Pros: Potentially better quality, embedded knowledge
   - Cons: Need training data first, expensive, harder to update
   - Why not chosen: Cart before horse—need data from MVP first

2. **Pure prompt engineering (no RAG)**
   - Pros: Simplest architecture
   - Cons: Limited by context window, can't scale knowledge
   - Why not chosen: Policies too complex to fit in prompt

3. **Hybrid: RAG + few-shot fine-tune**
   - Pros: Best of both worlds
   - Cons: Complexity, premature optimisation
   - Why not chosen: Save for Phase 2 after validation

### Trade-offs
- **Latency**: Retrieval adds ~500ms vs pure LLM
- **Quality**: RAG might miss nuance that fine-tuning captures
- **Maintenance**: Need to maintain vector store and embeddings
- **Verdict**: RAG's flexibility essential for MVP learning phase

### Success Criteria
- Retrieval precision >90% (relevant docs in top-5)
- Retrieval recall >80% (find all relevant policies)
- End-to-end latency <3 seconds (including retrieval)
- Zero policy violations (critical rules always found)

---

## Decision 4: Open-Source Embeddings (Not OpenAI)

**Date**: January 2026  
**Status**: Proposed for MVP

### Context
Need to embed policies, historical cases, and queries for RAG retrieval.

### Decision
Use **open-source embedding model** (bge-large-en-v1.5 or gte-large) hosted internally.

### Rationale
- **Cost**: Zero API costs vs $0.13/M tokens for OpenAI
- **Privacy**: Customer data stays internal
- **Control**: Can optimize for our domain
- **Performance**: Modern open-source models match OpenAI quality
- **Latency**: Local inference faster than API calls

### Alternatives Considered
1. **OpenAI text-embedding-3-large**
   - Pros: Good quality, zero infrastructure
   - Cons: $0.13/M tokens, data leaves premises, API dependency
   - Why not chosen: Economics + privacy concerns

2. **Cohere embeddings**
   - Pros: Competitive quality and pricing
   - Cons: Still external API, vendor lock-in
   - Why not chosen: Open-source eliminates these issues

3. **Train custom embeddings**
   - Pros: Optimised for Pineapple Travel domain
   - Cons: Need training data, expertise, time
   - Why not chosen: Premature—use off-the-shelf first

### Trade-offs
- **Infrastructure**: Need to host model vs API simplicity
- **Updates**: Manual model updates vs automatic API improvements
- **Support**: Self-service vs vendor support
- **Verdict**: Control and cost benefits outweigh convenience trade-off

### Success Criteria
- Embedding quality: >0.85 on internal eval set
- Inference latency: <50ms per query
- Infrastructure cost: <$100/month (CPU inference sufficient)

---

## Decision 5: Hybrid Search (Vector + Keyword)

**Date**: January 2026  
**Status**: Proposed for MVP

### Context
Need to retrieve relevant policies and historical cases from knowledge base. Some queries need semantic matching, others need exact terms (flight numbers, booking IDs).

### Decision
Implement **hybrid search**: vector similarity + BM25 keyword matching with score fusion.

### Rationale
- **Semantic queries**: "missed connection due to weather" → vector search
- **Exact terms**: "Flight BA123" → keyword search
- **Best of both**: Covers all query types
- **Proven pattern**: Industry standard for production RAG

### Alternatives Considered
1. **Pure vector search**
   - Pros: Simpler, handles semantic queries well
   - Cons: Misses exact term matches, struggles with IDs/codes
   - Why not chosen: Too many false negatives on flight numbers

2. **Pure keyword (BM25/Elasticsearch)**
   - Pros: Perfect for exact matches
   - Cons: Terrible at semantic similarity
   - Why not chosen: Most queries are semantic

3. **LLM-based rewriting** (query → multiple variants → vector)
   - Pros: Potentially best recall
   - Cons: Adds latency and cost, more complexity
   - Why not chosen: Hybrid search solves the problem more simply

### Trade-offs
- **Complexity**: Two search systems vs one
- **Tuning**: Need to balance vector vs keyword weights
- **Latency**: Two searches + fusion adds ~100ms
- **Verdict**: Recall improvement worth the complexity

### Success Criteria
- Recall improvement >15% vs vector alone
- Precision maintained >90%
- Latency overhead <150ms

---

## Decision 6: Human-in-the-Loop for All MVP Decisions

**Date**: January 2026  
**Status**: Proposed for MVP

### Context
System will generate resolution suggestions. Need to decide level of autonomy.

### Decision
**Zero autonomous resolution in MVP**. All LLM suggestions require human agent approval before execution.

### Rationale
- **Trust building**: Agents must trust system before autonomy
- **Training data**: Collect human decisions to improve model
- **Risk mitigation**: Avoid costly mistakes during learning phase
- **Compliance**: Human accountability for customer outcomes
- **Learning**: Understand where model succeeds/fails

### Alternatives Considered
1. **Partial autonomy** (auto-resolve simple cases)
   - Pros: Immediate TTFR reduction
   - Cons: Risk of errors, no training data for those cases
   - Why not chosen: Premature without validation

2. **Full autonomy with monitoring**
   - Pros: Maximum efficiency gains
   - Cons: Unacceptable risk in MVP
   - Why not chosen: Need to earn the right to autonomy

3. **Customer-approved autonomy** (suggest → customer accepts → auto-execute)
   - Pros: Customer consent reduces risk
   - Cons: Still risky without agent validation first
   - Why not chosen: Phase 2 feature after proven accuracy

### Trade-offs
- **Efficiency**: Miss immediate automation gains
- **Learning**: Perfect training data collection
- **Trust**: Agents see value before threat
- **Verdict**: Long-term success requires conservative start

### Success Criteria (to enable Phase 2 autonomy)
- Agent approval rate >85% sustained for 3 months
- Hallucination rate <1%
- Customer CSAT on resolved cases >4.0/5
- Zero compliance violations

---

## Decision 7: Full Decision Trace (Not Summary)

**Date**: January 2026  
**Status**: Proposed for MVP

### Context
Need explainability for compliance, audit, and improvement. Decide level of detail to log.

### Decision
Log **full decision trace** including:
- Input data (booking, flight status, customer history)
- Retrieved policies (with relevance scores)
- LLM prompt and response
- Reasoning chain (chain-of-thought)
- Confidence scores
- Human decision (approve/modify/reject)
- Execution outcome

### Rationale
- **Compliance**: May need to explain decisions to regulators
- **Debugging**: Understand why LLM made specific suggestions
- **Improvement**: Identify patterns in failures
- **Audit trail**: Legal protection
- **Model improvement**: Training data for future fine-tuning

### Alternatives Considered
1. **Summary only** (decision + outcome)
   - Pros: Minimal storage, simple
   - Cons: Can't debug, can't improve, compliance risk
   - Why not chosen: False economy

2. **Selective logging** (only log rejections/errors)
   - Pros: Reduced storage costs
   - Cons: Miss patterns in successful cases
   - Why not chosen: Need full picture for ML improvement

3. **Sampling** (log 10% of cases fully)
   - Pros: Cost reduction
   - Cons: Might miss rare edge cases
   - Why not chosen: Storage cheap relative to value

### Trade-offs
- **Storage cost**: ~1KB per case, ~1M cases/year = 1GB/year (~$20/year)
- **Privacy**: Need to secure sensitive data
- **Complexity**: More data to manage
- **Verdict**: Storage costs negligible vs value

### Success Criteria
- 100% of decisions logged with complete trace
- Audit queries complete in <1 second
- Zero data loss
- Compliance audit pass rate 100%

---

## Decision 8: Confidence Thresholds (Not Binary)

**Date**: January 2026  
**Status**: Proposed for MVP

### Context
LLM outputs have varying levels of certainty. Need to communicate this to agents.

### Decision
Implement **three-tier confidence system**:
- 🟢 High (>0.85): Strong recommendation
- 🟡 Medium (0.60-0.85): Suggestion, review carefully  
- 🔴 Low (<0.60): Multiple options, needs human judgment

### Rationale
- **Transparency**: Agents know when to trust vs scrutinize
- **Prioritisation**: Agents can tackle low-confidence cases first
- **Safety**: Clear signal when LLM uncertain
- **Future autonomy**: High-confidence candidates for auto-resolution

### Alternatives Considered
1. **Binary** (confident / not confident)
   - Pros: Simpler
   - Cons: Loses nuance
   - Why not chosen: Middle cases benefit from nuanced signal

2. **Five tiers** (very high, high, medium, low, very low)
   - Pros: More granular
   - Cons: Too complex, agents won't distinguish 5 levels
   - Why not chosen: Diminishing returns beyond 3

3. **No confidence scores** (treat all suggestions equally)
   - Pros: Simplest
   - Cons: Agents can't prioritise, no safety signal
   - Why not chosen: Dangerous to hide uncertainty

### Trade-offs
- **Calibration**: Need to tune thresholds based on real data
- **Confusion**: Agents need training on what confidence means
- **Misuse**: Risk of agents rubber-stamping high-confidence cases
- **Verdict**: Benefits outweigh risks with proper training

### Success Criteria
- Confidence calibration: High-confidence cases approved >95%
- Medium-confidence cases approved >70%
- Low-confidence cases flagged for senior review
- Agent survey: Confidence scores "useful" >4/5

---

## Decision 9: Prompt-Injected Rule Book (Not Hard-Coded Validation)

**Date**: January 3, 2026  
**Status**: Proposed for MVP

### Context
LLM needs to generate resolution options that comply with Pineapple Travel's policies, guarantee terms, and legal requirements. Need to decide how to enforce these rules.

### Decision
Use **prompt-injected rule book** where policies and compliance rules are passed as part of the system prompt to Claude Sonnet, rather than hard-coded validation logic.

### Rationale
- **Iteration speed**: Can update rules without code changes
- **Auditability**: Rules visible in prompt logs, easy to inspect
- **Version control**: Rules as text files, trackable in git
- **Testing**: Can test rule changes independently
- **Transparency**: LLM reasoning references specific rules
- **Flexibility**: Easy to A/B test different rule formulations

### Alternatives Considered
1. **Hard-coded validation rules** (if-then logic)
   - Pros: Guaranteed enforcement, no LLM interpretation
   - Cons: Slow to update, rigid, hard to maintain as rules grow
   - Why not chosen: Inflexible, requires code deploys for policy changes

2. **Fine-tuned model with embedded rules**
   - Pros: Rules "learned" by model, no prompt overhead
   - Cons: Black box, hard to audit, expensive to retrain
   - Why not chosen: Can't explain which rule was violated

3. **Hybrid: LLM generates + separate validator**
   - Pros: Defense in depth, catch LLM errors
   - Cons: Duplicate rule logic, synchronization issues
   - Why not chosen: Adds complexity; may add as Phase 2 safeguard

4. **External rules engine** (e.g. Drools)
   - Pros: Industry-standard approach, powerful
   - Cons: Overhead, requires integration layer
   - Why not chosen: Over-engineering for MVP

### Trade-offs
- **Enforcement guarantee**: Slightly weaker than hard-coded (LLM could misinterpret)
- **Flexibility**: Much higher (update rules in minutes, not days)
- **Explainability**: Better (LLM cites rules in reasoning)
- **Maintenance**: Easier (rules as documentation)
- **Verdict**: MVP benefits outweigh risk; add validation layer if needed after testing

### Implementation Details
- Rules stored in `rules/policy-rulebook.md` as structured markdown
- Injected into system prompt before each LLM call
- Version controlled with git (track rule changes over time)
- Each rule has unique ID for citation (e.g. "RULE-001: Guarantee covers missed connections")

### Success Criteria
- 100% policy compliance (validated by human review in MVP)
- Rule citation rate >90% (LLM references specific rules)
- Zero "unknown rule" cases (all scenarios covered)
- Rule update latency <5 minutes (edit → deploy)
- Agent feedback: Rules "clear and consistent" >4/5

---

## Future Decisions (To Be Made)

### Fine-Tuning Strategy (Phase 2)
- When to fine-tune vs continue with RAG?
- Which base model to fine-tune?
- How much training data is enough?
- How to maintain fine-tuned models?

### Autonomous Resolution Criteria (Phase 2)
- Which case types eligible for autonomy?
- What confidence threshold for auto-resolution?
- How to handle customer override ("I want a human")?
- Error budget for autonomous decisions?

### Multi-Language Support (Phase 3)
- Translate policies or use multilingual models?
- Which languages to prioritise?
- How to maintain quality across languages?

### Advanced Features (Future)
- Sentiment analysis for escalation?
- Customer intent prediction?
- Proactive issue detection before customer contact?
- Predictive rebooking for likely-to-miss connections?

---

## Decision Framework Template

For future decisions, use this structure:

```markdown
## Decision N: [Title]

**Date**: [Date]  
**Status**: [Proposed/Approved/Implemented/Deprecated]

### Context
[What problem are we solving? What are the constraints?]

### Decision
[What did we decide? Be specific.]

### Rationale
[Why this decision? What evidence supports it?]

### Alternatives Considered
1. [Alternative 1]
   - Pros: [Benefits]
   - Cons: [Drawbacks]
   - Why not chosen: [Reason]

### Trade-offs
[What are we giving up? What are we gaining?]

### Success Criteria
[How will we know this was the right decision?]
```

