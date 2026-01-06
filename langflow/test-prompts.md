# LangFlow Test Prompts

**Purpose**: Prompts and test queries for verifying the Pineapple RAG system in LangFlow.

---

## RAG Query Prompt (Basic Testing)

Use this prompt to test if ChromaDB retrieval is working correctly.

### Prompt Template

```
You are a knowledgeable assistant for Pineapple Travel customer support policies.

Your task is to answer questions based ONLY on the provided policy documents. Do not use external knowledge.

### RETRIEVED POLICY CONTEXT:
{context}

### USER QUESTION:
{question}

### INSTRUCTIONS:
1. Read the retrieved policy context carefully
2. Answer the question clearly and concisely
3. ONLY use information from the provided context
4. If the context doesn't contain the answer, say "I don't have enough information in the policies provided to answer this question."
5. Cite which policy section you're referencing (e.g., "According to the Guarantee Terms...")
6. Keep your answer focused and practical - imagine you're helping a CS agent understand the policy

### FORMAT YOUR ANSWER AS:
- Direct answer (2-3 sentences)
- Relevant policy citation
- Any important caveats or conditions

Answer:
```

### How to Use in LangFlow

**Components:**
```
TextInput (question)
    ↓
ChromaDB Retriever (gets relevant chunks)
    ↓
PromptTemplate (this prompt)
    ↓
ChatOpenAI or ChatAnthropic
    ↓
TextOutput (answer)
```

**Template Variables:**
- `{question}` ← Connected to TextInput
- `{context}` ← Connected to ChromaDB Retriever output

---

## Alternative: Simpler Prompt

If the above is too verbose, use this shorter version:

```
You are a Pineapple Travel policy assistant.

Answer this question using ONLY the provided policy context:

CONTEXT:
{context}

QUESTION:
{question}

Provide a clear, concise answer (2-3 sentences). Cite the policy source. 
If the context doesn't contain the answer, say so.

Answer:
```

---

## Test Queries

Use these queries to verify each policy document is properly indexed.

### Test 1: Guarantee Coverage

**Query:**
```
What does the guarantee cover for missed connections?
```

**Expected Answer Should Include:**
- Coverage for short layovers (<2 hours): FULLY COVERED
- Coverage for reasonable layovers (2-4 hours): COVERED if delay unavoidable
- Long layovers (>4 hours): Customer responsibility unless extraordinary circumstances
- Citation: "According to Guarantee Terms, Section: Missed Connections"

**Tests:** `guarantee-terms.md` is indexed

---

### Test 2: EU261 Compensation

**Query:**
```
What are the EU261 compensation amounts for flight delays?
```

**Expected Answer Should Include:**
- Short distance (<1,500 km): €250 for delays >3 hours
- Medium distance (1,500-3,500 km): €400 for delays >3 hours
- Long distance (>3,500 km): €300 for 3-4 hours, €600 for >4 hours
- Citation: "According to EU261 Summary"
- Note about extraordinary circumstances exemption

**Tests:** `eu261-summary.md` is indexed

---

### Test 3: Refund Policy

**Query:**
```
What is the refund policy if an airline cancels my flight?
```

**Expected Answer Should Include:**
- Full refund of affected segments
- No Pineapple fees charged
- Guarantee holders: 24-48 hour processing
- Additional compensation voucher for guarantee holders
- Citation: "According to Refund Policy, Airline-Initiated Cancellations"

**Tests:** `refund-policy.md` is indexed

---

### Test 4: Urgency Classification

**Query:**
```
How should we classify the urgency of a customer support case?
```

**Expected Answer Should Include:**
- URGENT: Customer in airport, flight <3 hours, stranded
- HIGH: Departure in 3-24 hours
- MEDIUM: Departure in 1-7 days
- LOW: Departure >7 days or general inquiries
- Citation: "According to Rule Book, Urgency Classification Rules"
- Response time requirements for each level

**Tests:** `rule-book.md` is indexed

---

### Test 5: Coverage Decision (Complex)

**Query:**
```
If a customer misses their connection because they arrived late to the gate due to security delays, is this covered by the guarantee?
```

**Expected Answer Should Include:**
- Depends on delay length
- <30 min: Customer responsibility
- 30-60 min: Case-by-case (some airports have known long queues)
- >60 min: Likely covered as extraordinary
- Citation: "According to Rule Book, Common Edge Cases"
- Shows ability to handle nuanced questions

**Tests:** Complex retrieval and reasoning

---

### Test 6: Multi-Policy Query

**Query:**
```
What compensation is a customer entitled to if their EU flight is delayed 4 hours and they have the Pineapple guarantee?
```

**Expected Answer Should Include:**
- EU261 rights: €400-600 depending on distance (airline pays)
- Pineapple Guarantee: Rebooking or refund options (Pineapple covers)
- Customer may be entitled to BOTH
- Citations from both EU261 and Guarantee Terms
- Note: Pineapple assists with EU261 claim but airline pays that compensation

**Tests:** Multi-document retrieval and synthesis

---

## Evaluation Criteria

### ✅ Good Signs (RAG is Working)

1. **Answers reference correct policies** - Cites specific sections
2. **Specific details match your files** - Numbers, rules, conditions are accurate
3. **No hallucinations** - Doesn't make up information not in policies
4. **Says "I don't know" appropriately** - When context insufficient
5. **Pulls from multiple docs when needed** - Test 6 should reference both EU261 + Guarantee

### ❌ Red Flags (Issues to Fix)

1. **Generic answers** - "Generally, airlines..." (not from your docs)
2. **Wrong numbers or terms** - Retrieval failed or hallucination
3. **No citations** - LLM not seeing context properly
4. **Confident wrong answers** - Wrong chunks retrieved
5. **Ignores context** - Uses general knowledge instead of policies

---

## Debugging Tips

### If Answers Are Wrong

**Step 1: Check Retrieved Context**

Add a TextOutput after ChromaDB Retriever to see actual chunks:

```
Question → Retriever → TextOutput (debug: see chunks)
                    ↓
                Prompt → LLM → Answer
```

Look for:
- Are chunks relevant to the question?
- Are they from the right policy file?
- Is there enough context in each chunk?

**Step 2: Adjust Retrieval**

If chunks aren't relevant:
- Increase `k` (number of results): Try 5-6 instead of 3-4
- Adjust chunk size: Try 800-1200 range
- Check chunk overlap: Should be 150-200
- Rephrase query to be more specific

**Step 3: Make Prompt Stricter**

If LLM is hallucinating, add to prompt:

```
CRITICAL: You must ONLY use the provided context. 
If the answer is not in the context, respond EXACTLY: 
"This information is not in the provided policies."

Do NOT use your general knowledge. Do NOT make assumptions.
```

---

## Advanced: Resolution Generation Prompt

Once basic RAG is working, use this prompt for the full resolution system:

```
You are an expert CS resolution assistant for Pineapple Travel.

RULE BOOK (MUST FOLLOW):
{rule_book}

CASE CONTEXT:
{assembled_context}

Your task: Generate 2-4 resolution options for this customer case.

For each option provide:
1. Action: What to do (be specific)
2. Confidence: 0-100 (how certain this is correct)
3. Cost estimate: Approximate cost to company
4. Policy citations: Which rules apply (cite specific sections)
5. Reasoning: Why this option is valid (2-3 sentences)
6. Pros: Benefits
7. Cons: Drawbacks or risks

Also include:
- escalation_needed: true/false
- uncertainty_flags: Any missing data
- recommended_option: Which option (1-4)

Output as valid JSON:
{
  "options": [
    {
      "id": 1,
      "action": "...",
      "confidence": 85,
      "cost_estimate": "£150",
      "policy_citations": ["..."],
      "reasoning": "...",
      "pros": ["...", "..."],
      "cons": ["..."]
    }
  ],
  "escalation_needed": false,
  "uncertainty_flags": [],
  "recommended_option": 1,
  "overall_reasoning": "..."
}

Be conservative with confidence. If missing data, flag for human review.
```

This is the prompt from Phase 6 of the main implementation guide.

---

*For complete implementation instructions, see: `../langflow.md`*

