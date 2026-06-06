import os
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_documents(folder_path="documents"):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            documents.append({
                "text": text,
                "source": filename
            })
            print(f"Loaded: {filename}")
    return documents

def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50
    )
    
    all_chunks = []
    for doc in documents:
        chunks = splitter.split_text(doc["text"])
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "text": chunk,
                "source": doc["source"],
                "position": i
            })
    return all_chunks

if __name__ == "__main__":
    print("Loading documents...")
    documents = load_documents()
    print(f"\nLoaded {len(documents)} documents")
    
    print("\nChunking documents...")
    chunks = chunk_documents(documents)
    print(f"Total chunks created: {len(chunks)}")
    
    print("\n--- 5 SAMPLE CHUNKS ---")
    for i in range(min(5, len(chunks))):
        print(f"\nChunk {i+1} (from {chunks[i]['source']}):")
        print(chunks[i]['text'])
        print("-" * 40)