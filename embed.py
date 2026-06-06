import os
from sentence_transformers import SentenceTransformer
import chromadb
from ingest import load_documents, chunk_documents

def embed_and_store(chunks):
    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    print("Setting up ChromaDB...")
    client = chromadb.PersistentClient(path="./chroma_db")
    
    # Delete existing collection if it exists
    try:
        client.delete_collection("housing_guide")
    except:
        pass
    
    collection = client.create_collection("housing_guide")
    
    print(f"Embedding {len(chunks)} chunks...")
    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk["text"]).tolist()
        collection.add(
            documents=[chunk["text"]],
            embeddings=[embedding],
            metadatas=[{"source": chunk["source"], "position": chunk["position"]}],
            ids=[f"chunk_{i}"]
        )
        if (i+1) % 10 == 0:
            print(f"  Embedded {i+1}/{len(chunks)} chunks...")
    
    print(f"\nDone! {len(chunks)} chunks stored in ChromaDB.")
    return collection, model

def retrieve(query, collection, model, k=5):
    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )
    return results

if __name__ == "__main__":
    # Load and chunk documents
    documents = load_documents()
    chunks = chunk_documents(documents)
    
    # Embed and store
    collection, model = embed_and_store(chunks)
    
    # Test retrieval with 3 queries
    test_queries = [
        "How do I protect my security deposit?",
        "What should I do if my landlord refuses to make repairs?",
        "How much does off campus housing cost per month?"
    ]
    
    print("\n--- RETRIEVAL TEST ---")
    for query in test_queries:
        print(f"\nQuery: {query}")
        results = retrieve(query, collection, model)
        for j, (doc, meta, dist) in enumerate(zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        )):
            print(f"  Result {j+1} (source: {meta['source']}, distance: {dist:.3f}):")
            print(f"  {doc[:150]}...")
        print("-" * 40)