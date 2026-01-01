# System Design: Agent-Assisted CS Resolution System

*Agent-assisted customer support system for virtual interlining failure resolution at Kiwi.com*

---

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Component Details](#component-details)
4. [Data Flows](#data-flows)
5. [Integration Points](#integration-points)
6. [Error Handling](#error-handling)
7. [Scalability Considerations](#scalability-considerations)

---

## Overview

### Problem Statement
Kiwi's virtual interlining creates complex failure scenarios (missed connections, schedule changes) where:
- No single airline owns the problem
- Responsibility is ambiguous
- Resolutions are inconsistent and slow
- Support agents lack context and decision support

### Solution
An LLM-powered agent-assistance system that:
- Detects failures proactively or via customer contact
- Gathers all relevant context automatically
- Generates valid resolution options with explanations
- Requires human approval for all MVP decisions
- Creates audit trail for learning and compliance

### Key Principles
1. **Human augmentation, not replacement**
2. **Urgency-based prioritization** (not category-based)
3. **Explainability by default**
4. **Conservative start, gradual autonomy**
5. **Continuous learning from human decisions**

---

## System Architecture

### High-Level Architecture

```mermaid
flowchart TB
    subgraph external [External Systems]
        API1[Flight Status APIs]
        API2[Booking System]
        API3[Customer Chat Platform]
        API4[Airline APIs]
    end
    
    subgraph ingestion [Ingestion Layer]
        I1[Event Collector]
        I2[Data Normalizer]
    end
    
    subgraph detection [Detection & Triage]
        D1[Event Processor]
        D2[Urgency Scorer]
        D3[Category Classifier]
        D4[Priority Queue]
    end
    
    subgraph context [Context Assembly RAG]
        C1[Booking Retriever]
        C2[Flight Status Enricher]
        C3[Policy Search]
        C4[Historical Case Finder]
        C5[Customer Profile]
        C6[Vector Store]
    end
    
    subgraph reasoning [LLM Reasoning]
        R1[Context Synthesizer]
        R2[Option Generator]
        R3[Policy Validator]
        R4[Confidence Scorer]
        R5[Explainer]
    end
    
    subgraph human [Human Interface]
        H1[Agent Dashboard]
        H2[Approval Interface]
        H3[Customer Communication]
    end
    
    subgraph execution [Execution Layer]
        E1[Rebooking Service]
        E2[Refund Processor]
        E3[Notification Service]
    end
    
    subgraph learning [Learning & Analytics]
        L1[Decision Logger]
        L2[Outcome Tracker]
        L3[Model Evaluator]
        L4[Analytics Dashboard]
    end
    
    external --> ingestion
    ingestion --> detection
    detection --> context
    context --> reasoning
    reasoning --> human
    human --> execution
    human --> learning
    execution --> learning
    learning -.feedback.-> reasoning
    C6 --> C3
    C6 --> C4
```

### Technology Stack (Proposed)

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| **Orchestration** | LangFlow / LangChain | Visual pipeline building, rapid prototyping |
| **Vector Store** | Qdrant or Weaviate | Open-source, scalable, good performance |
| **Embeddings** | bge-large-en-v1.5 | SOTA open-source, cost-effective |
| **Keyword Search** | Elasticsearch | Industry standard, proven at scale |
| **Fast LLM** | GPT-4o mini | Speed + cost for classification |
| **Reasoning LLM** | Claude 3.5 Sonnet | Best reasoning quality + explainability |
| **Backend** | Python/FastAPI | Fast development, great LLM ecosystem |
| **Frontend** | React + TypeScript | Agent dashboard needs interactivity |
| **Database** | PostgreSQL | Structured data, audit logs |
| **Queue** | Redis | Fast priority queue for cases |
| **Monitoring** | Datadog / New Relic | Observability for LLM systems |

---

## Component Details

### 1. Ingestion Layer

**Purpose**: Collect events from multiple sources and normalize into standard format

**Components**:
- **Event Collector**: Webhooks, polling, message queue subscriptions
- **Data Normalizer**: Convert diverse formats to internal schema

**Event Types**:
```json
{
  "event_type": "flight_delay|missed_connection|schedule_change|customer_contact",
  "timestamp": "2026-01-07T14:30:00Z",
  "booking_id": "KW123456",
  "flight_numbers": ["BA123", "EI456"],
  "urgency_hint": "high|medium|low",
  "source": "flight_api|customer|system",
  "raw_data": {}
}
```

**Integration Points**:
- FlightAware / FlightStats API (polling every 5 min for active bookings)
- Kiwi booking system (webhooks on changes)
- Customer service platform (chat/email webhooks)

---

### 2. Detection & Triage

**Purpose**: Identify failures, assess urgency, categorize, and prioritize

#### Urgency Scorer (GPT-4o mini)

**Inputs**:
- Event data
- Current time vs departure time
- Customer location (if available)
- Booking value

**Output**:
```json
{
  "urgency": "critical|high|medium|low",
  "urgency_score": 0.95,
  "reasoning": "Customer in-airport with departure in 2 hours",
  "time_to_resolve_target": "5 minutes"
}
```

**Urgency Criteria**:
- **Critical**: In-airport, departure <3 hours, already missed connection
- **High**: In-transit, departure <24 hours
- **Medium**: Departure 1-7 days
- **Low**: Departure >7 days

**Latency**: <500ms (GPT-4o mini)

#### Category Classifier (GPT-4o mini)

**Categories**:
- Missed connection (self-transfer)
- Schedule change (airline-initiated)
- Cancellation (full/partial)
- Ticket error
- Multiple issues (compound)

**Latency**: <500ms

#### Priority Queue

Redis sorted set, scored by:
```python
priority_score = urgency_score * 1000 + (current_time - event_time)
```

Ensures:
- Most urgent cases processed first
- FIFO within same urgency level
- No starvation of lower-priority cases

---

### 3. Context Assembly (RAG)

**Purpose**: Gather all information needed for decision-making

#### Data Sources & Retrieval

```mermaid
flowchart LR
    subgraph sources [Data Sources]
        S1[Booking DB]
        S2[Flight Status API]
        S3[Policy KB]
        S4[Case History DB]
        S5[Customer DB]
    end
    
    subgraph retrieval [Retrieval]
        R1[Direct Query]
        R2[Hybrid Search]
        R3[Similarity Search]
    end
    
    subgraph output [Assembled Context]
        O1[Context Bundle]
    end
    
    S1 -->|SQL| R1
    S2 -->|API| R1
    S5 -->|SQL| R1
    S3 -->|BM25 + Vector| R2
    S4 -->|Vector| R3
    R1 --> O1
    R2 --> O1
    R3 --> O1
```

#### Context Bundle Structure

```json
{
  "case_id": "CASE_20260107_001",
  "booking": {
    "booking_id": "KW123456",
    "flights": [...],
    "guarantee_purchased": true,
    "total_value": 450.00,
    "currency": "EUR"
  },
  "flights": [
    {
      "flight_number": "BA123",
      "status": "delayed",
      "scheduled": "2026-01-07T14:00:00Z",
      "estimated": "2026-01-07T16:30:00Z",
      "delay_reason": "weather"
    }
  ],
  "customer": {
    "customer_id": "CUST_789",
    "tier": "standard",
    "previous_issues": 1,
    "lifetime_value": 2300.00
  },
  "relevant_policies": [
    {
      "policy_id": "POL_001",
      "title": "Kiwi Guarantee - Missed Connections",
      "content": "...",
      "relevance_score": 0.94
    }
  ],
  "similar_cases": [
    {
      "case_id": "CASE_20251215_045",
      "similarity": 0.88,
      "resolution": "rebooking",
      "outcome": "resolved",
      "customer_satisfaction": 4.5
    }
  ]
}
```

#### Policy Knowledge Base

**Structure**:
- Kiwi Guarantee terms (chunked by section)
- Refund policies (by scenario)
- Airline partner rules
- Legal requirements (EU261, etc)
- Internal guidelines

**Indexing**:
- Vector embeddings (bge-large-en-v1.5)
- Keyword index (Elasticsearch)
- Metadata filters (policy_type, region, effective_date)

**Retrieval Strategy**:
1. Hybrid search (vector + BM25, weighted 70/30)
2. Retrieve top 10 candidates
3. Rerank with cross-encoder
4. Return top 5 with relevance scores

**Latency Budget**: <1 second

---

### 4. LLM Reasoning Engine

**Purpose**: Generate resolution options with explanations

#### Option Generator (Claude 3.5 Sonnet)

**Prompt Structure**:
```
You are an expert customer support agent for Kiwi.com, specializing in 
resolving complex virtual interlining failures.

CURRENT SITUATION:
{context_bundle}

RELEVANT POLICIES:
{retrieved_policies}

SIMILAR PAST CASES:
{similar_cases}

TASK:
Generate 2-4 resolution options ranked by:
1. Customer satisfaction (prioritize their needs)
2. Policy compliance (must be valid per our terms)
3. Cost to Kiwi (lower is better, but don't compromise #1)

For each option provide:
- Specific actions to take
- Expected cost to Kiwi
- Expected customer satisfaction
- Policy justification (cite specific policy sections)
- Pros and cons
- Confidence score (0-1)

Format your response as JSON following this schema:
{schema}
```

**Output Schema**:
```json
{
  "options": [
    {
      "option_id": 1,
      "title": "Rebook on next available flight (BA789)",
      "actions": [
        "Book customer on BA789 departing 18:00",
        "Provide lounge access voucher",
        "Send SMS with new itinerary"
      ],
      "cost_to_kiwi": {
        "amount": 125.00,
        "currency": "EUR",
        "breakdown": {
          "rebooking_fee": 100.00,
          "lounge_voucher": 25.00
        }
      },
      "customer_satisfaction_estimate": 4.0,
      "policy_justification": [
        {
          "policy_id": "POL_001",
          "section": "3.2 Weather-Related Delays",
          "quote": "Kiwi will rebook on next available flight..."
        }
      ],
      "pros": [
        "Gets customer to destination same day",
        "Covered by Guarantee",
        "Similar to past successful resolutions"
      ],
      "cons": [
        "Cost to Kiwi",
        "4-hour delay for customer"
      ],
      "confidence": 0.89,
      "reasoning": "High confidence because..."
    }
  ],
  "recommended_option_id": 1,
  "overall_confidence": 0.89,
  "escalation_recommended": false,
  "reasoning_trace": "..."
}
```

**Validation**:
- Policy Validator checks each option against hard rules
- Cost Validator ensures within authorization limits
- Feasibility Validator checks flight availability (API calls)

**Latency Budget**: <3 seconds

---

### 5. Human Interface

#### Agent Dashboard

**Key Features**:
1. **Case Queue**
   - Sorted by urgency
   - Color-coded by confidence (🟢🟡🔴)
   - Click to view full context

2. **Case Detail View**
   - Customer info + timeline
   - Full context displayed (booking, flights, policies)
   - LLM-generated options with confidence
   - Side-by-side comparison of options

3. **Decision Interface**
   - Approve option (click to execute)
   - Modify option (edit before executing)
   - Reject all (escalate to human brainstorming)
   - Request more info (trigger additional research)

4. **Communication Panel**
   - Template messages (auto-populated)
   - Send to customer (email/SMS/chat)
   - Real-time typing indicator

**Mockup Wireframe**:
```
┌─────────────────────────────────────────────────────────────┐
│ Case Queue                                    [Filters ▼]    │
├─────────────────────────────────────────────────────────────┤
│ 🔴 CASE_001 | Missed connection | In airport | 2 min ago   │
│ 🟡 CASE_002 | Schedule change  | Departs 4h  | 5 min ago   │
│ 🟢 CASE_003 | Ticket error     | Departs 2d  | 12 min ago  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ CASE_001: Missed connection - BA123 → EI456                 │
├─────────────────────────────────────────────────────────────┤
│ Customer: Jane Doe (Tier: Standard, 1st issue)              │
│ Status: In Dublin airport, waiting for connecting flight    │
│ BA123 delayed 2.5h (weather) → missed EI456 to London       │
│                                                              │
│ 🤖 AI Suggestions (Confidence: 🟢 High - 89%)               │
│                                                              │
│ ✅ Option 1: Rebook on BA789 (18:00) + lounge              │
│    Cost: €125  |  Est. CSAT: 4.0/5  |  Same-day arrival   │
│    Policy: Covered by Guarantee (Section 3.2)               │
│    [View Details] [Approve] [Modify]                        │
│                                                              │
│ ⭕ Option 2: Refund €315 (70%) + rebooking advice          │
│    Cost: €315  |  Est. CSAT: 3.2/5  |  Customer self-books│
│    Policy: Standard refund per terms 5.1                    │
│    [View Details] [Approve] [Modify]                        │
│                                                              │
│ [Reject All - Escalate to Senior Agent]                     │
└─────────────────────────────────────────────────────────────┘
```

---

### 6. Execution Layer

**Purpose**: Execute approved resolutions

**Services**:
- **Rebooking Service**: Book new flights via airline APIs
- **Refund Processor**: Initiate refunds through payment system
- **Notification Service**: Send SMS/email/push to customer
- **Audit Logger**: Record all actions with timestamps

**Transaction Handling**:
- All operations logged before execution
- Idempotency keys prevent duplicate bookings
- Rollback capability if partial failure
- Customer notified at each step

---

### 7. Learning & Analytics

**Purpose**: Track outcomes, improve model, measure impact

#### Decision Logger

Logs every case:
```json
{
  "case_id": "CASE_20260107_001",
  "timestamp": "2026-01-07T15:22:00Z",
  "context": {...},
  "llm_suggestions": [...],
  "agent_decision": {
    "selected_option_id": 1,
    "modifications": null,
    "approval_time_seconds": 45
  },
  "execution_result": "success",
  "customer_satisfaction": 4.5,
  "resolution_cost": 125.00,
  "time_to_first_resolution_seconds": 180
}
```

#### Model Evaluator

**Weekly Analysis**:
- Agent approval rate by case type
- Confidence calibration (are high-confidence cases actually approved more?)
- Cost accuracy (estimated vs actual)
- CSAT prediction accuracy
- Identify systematic errors

**Output**: Recommendations for prompt tuning, policy updates, escalation criteria

---

## Data Flows

### Flow 1: Proactive Detection (Flight Delay)

```mermaid
sequenceDiagram
    participant FA as FlightAware API
    participant IC as Ingestion
    participant DT as Detection & Triage
    participant CA as Context Assembly
    participant LLM as Reasoning Engine
    participant UI as Agent Dashboard
    participant AG as Agent
    
    FA->>IC: Flight BA123 delayed 2.5h
    IC->>DT: Normalized event
    DT->>DT: Check affected bookings
    DT->>DT: Calculate urgency (HIGH)
    DT->>CA: Request context for booking KW123456
    CA->>CA: Fetch booking, flights, policies, history
    CA->>LLM: Assembled context bundle
    LLM->>LLM: Generate resolution options
    LLM->>UI: Display options with confidence
    UI->>AG: Notification: High-priority case
    AG->>UI: Review and approve Option 1
    UI->>AG: Execute rebooking
```

**Latency**:
- Detection: <1 second
- Context assembly: <1 second
- LLM reasoning: <3 seconds
- **Total: <5 seconds** from event to agent notification

### Flow 2: Customer-Initiated Contact

```mermaid
sequenceDiagram
    participant CU as Customer
    participant CH as Chat Platform
    participant DT as Detection & Triage
    participant CA as Context Assembly
    participant LLM as Reasoning Engine
    participant AG as Agent
    
    CU->>CH: "I missed my connecting flight"
    CH->>DT: Customer message + booking ID
    DT->>DT: Extract booking, classify issue
    DT->>CA: Request context
    CA->>LLM: Context bundle
    LLM->>AG: Options ready in dashboard
    AG->>AG: Review (45 seconds)
    AG->>CU: "We can rebook you on BA789..."
    CU->>AG: "Yes please"
    AG->>CU: Executes + confirms
```

**Latency**:
- Customer wait time: <5 seconds for first response template
- Agent decision time: 30-60 seconds (vs 5-10 min without system)
- **Total TTFR: <90 seconds** (vs 10-15 min baseline)

---

## Integration Points

### External APIs

| System | Purpose | Protocol | SLA |
|--------|---------|----------|-----|
| FlightAware | Real-time flight status | REST API | 99.9% uptime |
| Kiwi Booking System | Booking data, modifications | Internal API | 99.95% uptime |
| Airline APIs | Rebooking, availability | REST/SOAP | Varies by airline |
| Payment Gateway | Refund processing | REST API | 99.9% uptime |
| Customer Service Platform | Chat, email, SMS | Webhooks + API | 99.5% uptime |

### Authentication & Security
- API keys rotated monthly
- All customer data encrypted at rest and in transit
- PCI DSS compliance for payment data
- GDPR compliance for EU customers
- Role-based access control (RBAC) for agents

---

## Error Handling

### LLM Failures

**Failure Modes**:
1. **Timeout** (>10s response)
   - Retry once
   - If fails again: Escalate to human without suggestions
   
2. **Invalid JSON** (parsing error)
   - Log error with full context
   - Retry with simplified prompt
   - If fails: Escalate to human

3. **Policy Violation** (validator rejects)
   - Log violation details
   - Request alternative from LLM
   - If persistent: Escalate to human

4. **Hallucination** (suggests impossible option)
   - Feasibility validator catches
   - Log for model improvement
   - Filter out invalid option
   - If no valid options: Escalate

**Fallback Strategy**:
- Always degrade gracefully to human-only mode
- Agent sees all context even if LLM fails
- System never blocks human from working

### Integration Failures

**Booking System Down**:
- Queue cases until system recovers
- Prioritize by urgency when back online
- Manual workaround: Agent can enter data manually

**Flight API Down**:
- Use cached flight data (if recent)
- Display "Data may be stale" warning
- Agent can manually verify

---

## Scalability Considerations

### Current MVP Scale
- 100 cases/day
- 5 concurrent agents
- <$100/day in LLM costs

### Growth Path
| Metric | Phase 1 | Phase 2 | Phase 3 |
|--------|---------|---------|---------|
| Cases/day | 100 | 1,000 | 10,000 |
| Agents | 5 | 50 | 200 |
| Response time | <5s | <3s | <2s |
| LLM cost/case | $0.05 | $0.03 | $0.01 |

### Bottlenecks & Mitigations

**LLM API rate limits**:
- Cache repeated queries
- Batch non-urgent cases
- Self-hosted open-source models for classification

**Vector search at scale**:
- Shard by region/time
- Approximate nearest neighbor (ANN)
- Separate hot/cold data

**Database writes (decision logs)**:
- Async logging (don't block agent)
- Batch writes
- Time-series database for analytics

---

## Monitoring & Observability

### Key Metrics

**System Health**:
- Latency (p50, p95, p99) for each component
- Error rates (LLM failures, API timeouts)
- Queue depth and wait time

**Business Metrics**:
- Time to First Resolution (TTFR)
- Agent approval rate
- Customer CSAT (per resolution type)
- Cost per resolution
- Repeat contact rate

**ML Metrics**:
- Confidence calibration
- Hallucination rate
- Policy compliance rate
- Similar case retrieval accuracy

### Alerts

**Critical** (page on-call):
- System down >5 minutes
- Error rate >10%
- High-urgency cases waiting >10 minutes

**Warning** (email team):
- Agent approval rate drops below 70%
- LLM latency p95 >5 seconds
- Cost per case exceeds budget by 20%

---

## Security & Compliance

### Data Privacy
- Customer PII encrypted at rest (AES-256)
- PII redacted from LLM prompts where possible
- Audit log of all PII access
- Right to deletion supported (GDPR)

### Compliance
- **EU261**: System enforces passenger rights
- **PCI DSS**: Payment data handling compliant
- **GDPR**: Data minimization, consent tracking
- **Internal**: All decisions auditable

### Access Control
- Agents: Read access to assigned cases only
- Senior agents: Can override system recommendations
- Managers: Full audit log access
- Engineers: Anonymized data only for model improvement

---

## Future Enhancements

### Phase 2: Selective Autonomy
- Auto-execute high-confidence (>0.95) rebookings after customer approval
- Proactive customer communication ("We've found an alternative...")
- Predictive rebooking (before customer notices issue)

### Phase 3: Advanced Features
- Multi-language support (translate policies, generate responses)
- Sentiment analysis for escalation (detect frustrated customers)
- Personalization (learn customer preferences)
- Predictive analytics (identify failure-prone itineraries at booking time)

### Phase 4: Ecosystem Integration
- Share resolution patterns with airline partners
- Industry-wide knowledge base (anonymized)
- API for third-party travel insurance providers

