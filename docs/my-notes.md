# Ideation on Kiwi and Customer Support

## Kiwi's USP

Kiwi is an OTA, but not a traditional one.

What makes it different?:

- Focus on routing and price discovery rather than airline partnerships
- Ability to combine flights across non-partner airlines using virtual interlining
- Willingness to take on complexity in exchange for better prices and flexibility for customers
    - **Think about Travix:** Global ticketing offices, making savings by taking booking in Netherlands, routing through AU office to obtain cheaper price than advised to customer (and Travix would take the difference). What does Kiwi do? Pass to customer? How does Kiwi make money, the guarantee?
    - Offers a guarantee to fix any carrier related problems for X cost - if the customer does not buy the guarantee do they accept the risk?

Probably causes above “normal” downstream problems:

- Missed connections that no airline “owns”
- Ambiguity around responsibility - who owns the risk, the customer (without the kiwi guarantee?)
- Complexity when trying to resolve for customers and CS staff (large CS team? long queues?)
- A constant trade-off between cost, speed, and customer trust
    - **Think of Skyscanner - accuracy vs coverage vs speed AND vs cost vs customer trust balancing act?**
    - **Travix “waiting line” to speak to agents, high levels of dissatisfaction with CS**

Customer Support is central to keeping customers happy when things go wrong in a high risk virtual interlining travel agency.

## CS PM Role at Kiwi

- Product strategy
- New tech / power of Gen AI / Agents
- Operational realities

The answer is not chatbots!

- Present travellers with options relevant to their situation (auto resolution?) > full understanding
- Equip support agents with full context and better judgment tools
- Reduce time to resolution for complex, failure-prone journeys
- **Assumption based on experience:** Simplify an architecture that currently carries a lot of historical complexity
- Introduce (/build on existing) AI in a way that is fast, safe, and **explainable**

What stands out to me in the JD:

- Daily releases and speed of execution
- Heavy collaboration with engineering
- A strong push toward AI-powered support and communication platforms
- Ownership of both vision and delivery, not just requirements

**Key requirement:** Product maturity AND technical curiosity

## Success might look like…

- Lower handling time without sacrificing resolution quality
- Fewer repeat contacts on the same issue
- Clear accountability in decision making
- Support agents spending more time helping customers and less time looking up situation / rules / understanding context
- Being able to answer why we did something (if AI gen)

## (Imaginary) Problem Summary

Kiwi’s USP delivers amazing savings for users, but also creates unavoidable failure scenarios.

The problem is not the failures themselves, but how (potentially) inconsistently, expensively, and opaquely they are resolved.

How might we improve the quality, speed, and consistency of customer support decisions in virtual interlining failures, without increasing risk or operational cost?

## Exploration of Agentic AI System for Resolving Interlining Failures

Given Kiwi’s USP, a large share of customer support complexity comes from **things going wrong in itineraries that no single airline fully owns**.

Out of scope: Other customer service issues (baggage, seats, etc)

Why this problem? It’s a problem specific to Kiwi, less general OTA problem.

I am going to explore an agent-assisted system that:

- Detects failure scenarios in virtual interlining journeys, looking for problems before the customer contacts Kiwi and categorises (if customer first contact, then categorise)
- Gathers all relevant context automatically: flight status, connection time, ticket conditions, guarantee eligibility, historical outcomes
- Produces ranked resolution options that are all valid within Kiwi’s policies for example: rebooking, refund, partial compensation, or mixed solutions
- Explains why each option is recommended
- When confidence is high enough to act automatically, auto resolution OR human intervention required (give customer override also?)
    - Confidence boundaries OR **decision boundaries**, not automation:
    - Clear confidence thresholds
    - Clear no-go zones
    - Clear escalation paths
    - Auto-resolution as an *exception*, not a goal

The goal is never to replace humans, but to augment and assist!

- Reduce cognitive load
- Make decisions more consistent
- Preserve human interaction for edge cases / certain types of customer (should there be an immediate “I want to speak to a human?”)
- Create a clear audit trail for why the robots made a decision

Why this system:

- Improve time to resolution
- Give leadership visibility into where support cost is coming from
- Clear confidence thresholds
- Human override by default
- Decision traces that can be reviewed afterward

## My Process

### Brainstorming

- Document initial thoughts in Notion (messy, stream of consciousness, incomplete)
- Brainstorm with GPT5.2 to sharpen and expand ideas (why? I have a sub, save cursor tokens, and it’s good for brainstorming in my experience)

### Building and Documenting

Building and documenting in Cursor (using various models) and GitHub:

- Make thinking more concrete
- Show how I approach complex, ambiguous problems and systems
- Design system
- Invite discussion and critique
- Demonstrate how I work with modern tools

### RAG Build

- (In the event I have time) using LangFlow and GPT4o mini

### Present
TBD…in Github? And an 'exec' summary in slide show?