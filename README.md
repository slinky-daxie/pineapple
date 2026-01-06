# 🍍 Pineapple

> AI-powered customer support for travel disruptions. A PM design exercise in human-AI collaboration.

**The Challenge:** Design an LLM system that helps support agents resolve complex travel failures where responsibility is ambiguous and time is critical.

**The Constraint:** Augment humans, don't replace them. Build trust first, automation later.

**Status:** 🚧 Prototype being built in [LangFlow](https://www.langflow.org/) to demonstrate core RAG pipeline and agent experience.

---

## What's Interesting Here?

### Product Decisions
- **Urgency-based prioritization** over FIFO (person in airport ≠ issue in 3 weeks)
- **Phased autonomy:** 100% human approval → selective automation → proactive resolution
- **Platform thinking:** Same RAG stack powers agent tools *and* customer self-service

### AI Architecture
- **Multi-model strategy:** Fast classifier (GPT-4o mini) + deep reasoner (Claude Sonnet)
- **RAG over fine-tuning** for MVP (no training data yet; policies change frequently)
- **Prompt-injected guardrails:** Version-controlled rule book, no code deploys to update policies
- **Structured outputs:** Confidence scores + policy citations + reasoning = fast human review

### Production Thinking
- **Graceful degradation:** LLM fails → agents still get assembled context
- **Cross-referenced data:** Flight APIs + booking DB = proactive detection *and* fraud prevention
- **Full audit trail:** Every decision logged for compliance and continuous learning

---

## Architecture (10-second version)

```
Flight APIs + Customer Contact
         ↓
   Categorize & Prioritize (GPT-4o mini)
         ↓
   Context Assembly (RAG: bookings, policies, history)
         ↓
   LLM Reasoning (Claude Sonnet + rule book)
         ↓
   Structured Output (options, confidence, citations)
         ↓
   Human Review → Resolution
         ↓
   Learning Loop
```

**Key principle:** Never block the human. If AI fails, agents keep working.

---

## What's in the Docs?

📁 **[`design/system-overview.md`](design/system-overview.md)** 
   - Architecture diagrams, user journeys, integration requirements
   - Failure handling, scaling considerations, metrics

📁 **[`brainstorm/decision-log.md`](brainstorm/decision-log.md)** - Technical decisions with rationale  
   - Why Claude over GPT-4? Why RAG over fine-tuning? Why multi-model?
   - Shows decision-making process, not just outcomes

📁 **[`agentic-flow-v1`](design/agentic-flow-v1.md)** - Visual flow diagram  
   - Mermaid diagram showing end-to-end case processing
   - Step-by-step walkthrough

---

## Why I Built This

Wanted to understand modern AI product development beyond "add ChatGPT":
- Which LLM decisions actually matter?
- How do you balance innovation with safety?
- What makes AI useful vs frustrating for end users?
- How do technical constraints shape product strategy?

**Personal project** - No real bookings, flights, or customers. Just deep thinking about AI product design.

---



