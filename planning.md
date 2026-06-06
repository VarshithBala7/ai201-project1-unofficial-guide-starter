## Domain
Off-campus housing experiences for college students. This knowledge is valuable because official university websites only provide generic housing resources and approved landlord lists. The real student experience — which landlords are responsive, which apartments have hidden problems, what costs are actually involved — is shared informally between students and is hard to find in one place.

## Documents
1. doc1.txt - Reddit r/college: Move-in inspection tips and what to check before signing
2. doc2.txt - Reddit r/Apartmentliving: Landlord problems and tenant rights
3. doc3.txt - Reddit r/college: Real monthly cost breakdown for off-campus apartment
4. doc4.txt - Reddit r/college: Roommate problems and written agreements
5. doc5.txt - Reddit r/college: Questions to ask before signing a lease
6. doc6.txt - Reddit r/Apartmentliving: How to get your full security deposit back
7. doc7.txt - Reddit r/college: When and how to search for apartments
8. doc8.txt - Reddit r/Apartmentliving: Safety tips for first-time renters
9. doc9.txt - Reddit r/Apartmentliving: Maintenance and repair guide
10. doc10.txt - Reddit r/college: Dorms vs off-campus honest comparison

## Chunking Strategy
Chunk size: 300 characters with 50 character overlap.
These documents are short to medium length Reddit posts with distinct tips and comments. Each tip or comment is a self-contained thought. Smaller chunks of 300 characters ensure each chunk contains one specific piece of advice that can be matched precisely to a user query. Overlap of 50 characters ensures that tips split across a boundary are still retrievable.

## Retrieval Approach
Embedding model: all-MiniLM-L6-v2 from sentence-transformers. Runs locally with no API key.
Vector store: ChromaDB running locally.
Top-k: retrieve top 5 chunks per query.
Semantic search finds relevant chunks even when the query uses different words than the document because the model understands meaning not just keywords.
Production tradeoffs: all-MiniLM-L6-v2 is fast and free but has limited context length of 256 tokens. For production I would consider text-embedding-3-small from OpenAI for better accuracy or a multilingual model if serving international students.

## Evaluation Plan
Q1: How do I protect my security deposit when moving in?
Expected answer: Take photos and video of everything on move-in day and email them to landlord with timestamp.

Q2: What should I do if my landlord refuses to make repairs?
Expected answer: Submit repair requests in writing via email, contact city housing code enforcement if ignored.

Q3: How much does off-campus housing actually cost per month?
Expected answer: Approximately $1,100 to $1,200 per month per person including rent, utilities, groceries, and insurance.

Q4: When should I start looking for an apartment for next fall?
Expected answer: Start searching in January or February, about 7 to 8 months before move-in.

Q5: What are my rights if my roommate stops paying rent?
Expected answer: Both tenants on a joint lease are responsible for full rent. You can pay and sue roommate in small claims court.

## Anticipated Challenges
Documents may have inconsistent formatting since they came from Reddit posts.
Some chunks may be too short to carry enough semantic meaning if tips are very brief.
Queries using formal language may not match informal Reddit-style writing in chunks.
Source attribution must be programmatically guaranteed not left to the LLM to add.

## AI Tool Plan
I will use Claude to generate the ingestion and chunking script based on this planning.md.
I will use Claude to generate the embedding and ChromaDB storage code.
I will use Claude to generate the Groq LLM connection and prompt template.
I will use Claude to generate the Gradio interface code.
I will review and test all generated code myself before running it.

## Architecture
Document Ingestion (plain text loader)
        ↓
Chunking (RecursiveCharacterTextSplitter, size=300, overlap=50)
        ↓
Embedding (sentence-transformers all-MiniLM-L6-v2)
        ↓
Vector Store (ChromaDB local)
        ↓
Retrieval (top-5 semantic search)
        ↓
Generation (Groq llama-3.3-70b-versatile)
        ↓
Answer with Source Attribution (Gradio UI)