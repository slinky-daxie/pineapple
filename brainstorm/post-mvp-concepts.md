# Post-MVP Concepts

*Ideas for evolution beyond the human-in-the-loop MVP*

---

## Context

The MVP focuses on **agent assistance** with 100% human-in-the-loop which is most appropriate in a first iteration. These are concepts for what could come next, based on:
- Learning from MVP data
- Building on proven value
- Expanding use cases for the same core technology

---

## 1. Selective Automation / Proactive Resolution

**Concept**: Let high-confidence cases auto-execute after customer approval

**How it works:**
- System generates resolution with >95% confidence
- Customer receives SMS/email: "Your flight is delayed. We can rebook you on BA789. Tap to approve."
- Customer approves → automatic execution
- Low-confidence cases still go to human agents

---

## 2. Customer-Facing Applications (Transparency)

**Concept**: Reuse the same RAG stack for customer self-service

**Why this matters:**
Research finding: *"Customers say the guarantee covers nothing"* → transparency gap

**Potential applications:**

### Guarantee Explainer
- **Pre-purchase**: "Does my itinerary qualify? What does it cover?"
- **During trip**: "Does my guarantee cover this delay?"
- **Post-issue**: "Why was my claim handled this way?"

Uses same RAG infrastructure (policies, rules, historical cases) but surfaces it to customers directly.

---

## 3. Proactive Resolution

Moved this to MVP but still borderline thinkit's better as an iteration.

**Concept**: Contact customers BEFORE they contact us

**How it works:**
- System detects flight delay/cancellation via monitoring
- Cross-references with booking database → identifies affected customers
- Generates resolution options automatically
- Proactively sends: "We've detected your flight is delayed. Here are your options..."

---

## 4. Predictive Features

**Concept**: Predict issues before they happen, prevent, or ensure customers know what they are getting into

### Risk Scoring at Booking
- Show customers upfront: "This itinerary has medium connection risk"
- Suggest: Add guarantee, or see safer alternatives
- Helps customers make informed choices

### Smart Routing Recommendations
- Score itineraries by: price + convenience + risk
- Recommend optimal balance
- Example: "€30 more expensive, but 40% lower risk and 2h faster"

---

## 5. Multi-Agent Systems

**Concept**: Specialised AI agents working together, not just one LLM (not sure they add real value tbh)

### Potential Agent Roles:

**Negotiation Agent:**
- Talks to airline APIs on behalf of customer
- Requests compensation, upgrades, lounge access
- Knows airline-specific policies

**Personalisation Agent:**
- Learns customer preferences over time
- "This customer always picks window seats, prefers morning flights"
- Tailors resolution options to individual preferences

**Sentiment Analysis Agent:**
- Detects frustration in customer messages
- Escalates emotionally charged cases to senior agents
- Adjusts communication tone based on sentiment

**Context Enrichment Agent:**
- Continuously gathers external data (weather, airport congestion, strikes)
- Enriches LLM reasoning with real-time intelligence
- Predicts cascading failures

---

## 6. B2B Platform / Ecosystem

**Concept**: Transform internal tool into external product

### Potential approaches:

**White-Label for OTAs:**
- Package the CS automation system
- Sell to other travel agencies
- Customise for their policies/branding

**API for Insurance Companies:**
- Real-time risk scoring
- Claim validation automation
- Dynamic pricing based on itinerary risk

---

