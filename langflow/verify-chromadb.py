"""
Verify ChromaDB Setup for Pineapple Travel Policies

This script checks if your policy documents were successfully loaded into ChromaDB
and tests basic retrieval functionality.

Usage:
    python langflow/verify-chromadb.py

Requirements:
    pip install chromadb
"""

import chromadb
from typing import Optional


def verify_chromadb(
    persist_directory: str = "./chroma_db",
    collection_name: str = "pineapple_policies"
) -> None:
    """
    Verify ChromaDB collection exists and contains expected data.
    
    Args:
        persist_directory: Path to ChromaDB persistence directory
        collection_name: Name of the collection to verify
    """
    
    print("=" * 60)
    print("CHROMADB VERIFICATION TEST")
    print("=" * 60)
    
    try:
        # Connect to ChromaDB
        print(f"\n1. Connecting to ChromaDB at: {persist_directory}")
        client = chromadb.PersistentClient(path=persist_directory)
        print("   ✅ Connected successfully")
        
        # Get collection
        print(f"\n2. Getting collection: {collection_name}")
        collection = client.get_collection(name=collection_name)
        print("   ✅ Collection found")
        
        # Check document count
        count = collection.count()
        print(f"\n3. Document count: {count}")
        
        if count == 0:
            print("   ❌ ERROR: Collection is empty!")
            print("   → Re-run your document loading flow in LangFlow")
            return
        elif count < 40:
            print("   ⚠️  WARNING: Count seems low (expected ~50-70 chunks)")
            print("   → Check if all 4 policy files were loaded")
        else:
            print("   ✅ Document count looks good")
        
        # Peek at documents
        print("\n4. Sample documents (first 3 chunks):")
        results = collection.peek(limit=3)
        for i, doc in enumerate(results['documents'], 1):
            print(f"\n   --- Chunk {i} ---")
            print(f"   {doc[:200]}...")
            if results.get('metadatas') and results['metadatas'][i-1]:
                source = results['metadatas'][i-1].get('source', 'unknown')
                print(f"   Source: {source}")
        
        # Test queries
        print("\n" + "=" * 60)
        print("RUNNING TEST QUERIES")
        print("=" * 60)
        
        test_queries = [
            "What does the guarantee cover for missed connections?",
            "What are EU261 compensation amounts?",
            "What is the refund policy for airline cancellations?",
            "How should we classify case urgency?"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n{i}. Query: {query}")
            
            query_results = collection.query(
                query_texts=[query],
                n_results=3
            )
            
            print(f"   Retrieved {len(query_results['documents'][0])} results:")
            
            for j, doc in enumerate(query_results['documents'][0], 1):
                print(f"\n   Result {j}:")
                print(f"   {doc[:250]}...")
                
                # Show source if available
                if query_results.get('metadatas') and query_results['metadatas'][0]:
                    metadata = query_results['metadatas'][0][j-1]
                    if 'source' in metadata:
                        print(f"   📄 Source: {metadata['source']}")
                
                # Show distance/score if available
                if query_results.get('distances') and query_results['distances'][0]:
                    distance = query_results['distances'][0][j-1]
                    print(f"   📊 Distance: {distance:.4f} (lower = more relevant)")
        
        # Summary
        print("\n" + "=" * 60)
        print("VERIFICATION SUMMARY")
        print("=" * 60)
        print(f"✅ ChromaDB collection exists: {collection_name}")
        print(f"✅ Total documents indexed: {count}")
        print(f"✅ Query retrieval working: Yes")
        print("\n🎉 ChromaDB setup looks good!")
        print("\nNext steps:")
        print("- Test queries in LangFlow with RAG prompt")
        print("- Verify answers match policy documents")
        print("- Adjust chunk size/k if retrieval quality is poor")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nTroubleshooting:")
        print("- Check persist_directory path is correct")
        print("- Make sure you ran the document loading flow in LangFlow")
        print("- Verify collection_name matches what you used in LangFlow")
        print("- Try deleting ./chroma_db and re-indexing")


def test_specific_query(
    query: str,
    persist_directory: str = "./chroma_db",
    collection_name: str = "pineapple_policies",
    n_results: int = 5
) -> None:
    """
    Test a specific query against ChromaDB.
    
    Args:
        query: Question to ask
        persist_directory: Path to ChromaDB
        collection_name: Collection name
        n_results: Number of results to return
    """
    client = chromadb.PersistentClient(path=persist_directory)
    collection = client.get_collection(name=collection_name)
    
    print(f"\nQuery: {query}")
    print("=" * 60)
    
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    for i, doc in enumerate(results['documents'][0], 1):
        print(f"\nResult {i}:")
        print(doc)
        print("-" * 60)


if __name__ == "__main__":
    # Run verification
    verify_chromadb()
    
    # Uncomment to test a specific query:
    # test_specific_query("What does the guarantee cover for missed connections?")

