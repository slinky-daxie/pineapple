# LangFlow Prototype

**Working prototype** demonstrating the core RAG pipeline for the Pineapple agent-assistance system.

---

## What's Here

### 📊 `pineapple-rag-test.json`

**Working LangFlow flow** that connects to ChromaDB with the sample policy documents and tests retrieval + answer generation.

**What it does:**
- Loads 4 policy documents into ChromaDB vector database:
  - Guarantee Terms
  - EU261 Summary
  - Refund Policy
  - Rule Book
- Retrieves relevant policy chunks based on user questions
- Generates answers using GPT-4o with proper policy citations
- Tests the RAG (Retrieval-Augmented Generation) pipeline

**How to use:**
1. Import `pineapple-rag-test.json` into LangFlow
2. Set your OpenAI API key in the components
3. Make sure ChromaDB path points to `./chroma_db`
4. Run with test queries from `test-prompts.md`

**Components in the flow:**
- Document loaders → Load policy markdown files
- Text splitter → Chunk documents (1000 chars, 200 overlap)
- OpenAI embeddings → Create vector representations
- ChromaDB → Store and retrieve policy chunks
- Prompt template → Format query with retrieved context
- ChatOpenAI (GPT-4o) → Generate answers
- Text output → Display results

---

### 📝 `test-prompts.md`

**Test queries and prompts** for verifying the RAG system works correctly.

Includes:
- RAG query prompt templates
- 6 test queries with expected answers
- Evaluation criteria (how to know if it's working)
- Debugging tips

Use these to verify:
- ChromaDB is returning relevant policy chunks
- LLM is generating accurate, policy-grounded answers
- Citations are correct

---

### 🐍 `verify-chromadb.py`

**Python script** to verify ChromaDB was set up correctly.

Run before testing in LangFlow to confirm:
- Documents are indexed (~50-70 chunks expected)
- Retrieval is working
- Chunks are coming from the right policy files

```bash
python langflow/verify-chromadb.py
```

---

## Quick Start

### 1. Set Up ChromaDB

In LangFlow, run the document loading portion of the flow once to index policies into ChromaDB.

**Expected result:** `./chroma_db/` folder created with ~60 document chunks

**Verify:** Run `python langflow/verify-chromadb.py`

### 2. Test Retrieval

Use test queries from `test-prompts.md`:

```
What does the guarantee cover for missed connections?
```

**Expected:** Returns 3-5 relevant chunks from Guarantee Terms policy

### 3. Test Answer Generation

Run full flow with prompt template + LLM.

**Expected:** Clear answer citing Guarantee Terms, explaining coverage rules

---

## What This Demonstrates

**For PM/AI understanding:**
- ✅ RAG pipeline architecture (retrieve → synthesize → generate)
- ✅ Vector database usage (semantic search over policies)
- ✅ Prompt engineering (grounding LLM in retrieved context)
- ✅ Structured knowledge base (policies as searchable documents)
- ✅ Citation and explainability (answers reference source policies)

**Production differences:**
- Real system would have live booking database integration
- Flight APIs would trigger proactively
- Agent dashboard for human review
- Learning loop to improve over time
- Multi-model orchestration (classifier + reasoner)

But this proves the **core concept works**: LLM can accurately answer policy questions using RAG.

---

## Files NOT Included

- `langflow-plan.md` - Personal implementation notes (in .gitignore)
- `chroma_db/` - Local vector database (in .gitignore)

These are kept private/local and not pushed to GitHub.

---

## Next Steps

Once basic RAG is working:

1. **Add classification layer** - Categorize urgency (GPT-4o mini)
2. **Add booking lookup** - Mock booking data integration
3. **Switch to Claude Sonnet** - Better reasoning for complex cases
4. **Structured output** - Generate resolution options with confidence scores
5. **Test with sample cases** - Use `data/sample-cases.json`

See `../design/system-overview.md` for full architecture vision.

---

*This prototype demonstrates the foundational RAG pipeline. For complete step-by-step implementation guide, see: `langflow-plan.md` (local only)*

