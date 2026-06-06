import os
from groq import Groq
from sentence_transformers import SentenceTransformer
import chromadb
from dotenv import load_dotenv

load_dotenv()

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("housing_guide")
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def ask(question):
    query_embedding = model.encode(question).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )
    
    chunks = results["documents"][0]
    metadatas = results["metadatas"][0]
    sources = list(set([m["source"] for m in metadatas]))
    context = "\n\n".join(chunks)
    
    prompt = f"""You are a helpful assistant for college students looking for off-campus housing advice.
Answer the question using ONLY the information provided in the documents below.
If the documents do not contain enough information to answer, say:
"I don't have enough information on that topic in my documents."
Do not use any outside knowledge.

Documents:
{context}

Question: {question}

Answer:"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    
    answer = response.choices[0].message.content
    return {
        "answer": answer,
        "sources": sources
    }

if __name__ == "__main__":
    test_questions = [
        "How do I protect my security deposit?",
        "What is the best time to start looking for an apartment?",
        "What is the weather like in Paris?"
    ]
    
    for question in test_questions:
        print(f"\nQuestion: {question}")
        result = ask(question)
        print(f"Answer: {result['answer']}")
        print(f"Sources: {result['sources']}")
        print("-" * 50)