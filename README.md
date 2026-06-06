# The Unofficial Off-Campus Housing Guide

A RAG (Retrieval-Augmented Generation) system that makes student-generated housing knowledge searchable and answerable.

## Domain and Document Sources

Off-campus housing experiences for college students. This knowledge is valuable because official university websites only provide generic housing resources. The real student experience is shared informally and hard to find in one place.

**Sources:**
- doc1.txt - Reddit r/college: Move-in inspection tips
- doc2.txt - Reddit r/Apartmentliving: Landlord problems and tenant rights
- doc3.txt - Reddit r/college: Real monthly cost breakdown
- doc4.txt - Reddit r/college: Roommate problems and solutions
- doc5.txt - Reddit r/college: Questions to ask before signing a lease
- doc6.txt - Reddit r/Apartmentliving: How to get your security deposit back
- doc7.txt - Reddit r/college: When and how to search for apartments
- doc8.txt - Reddit r/Apartmentliving: Safety tips for first-time renters
- doc9.txt - Reddit r/Apartmentliving: Maintenance and repair guide
- doc10.txt - Reddit r/college: Dorms vs off-campus honest comparison

## Chunking Strategy and Reasoning

Chunk size: 300 characters with 50 character overlap.

These documents are Reddit posts with short, self-contained tips. Smaller chunks of 300 characters ensure each chunk contains one specific piece of advice that matches precisely to a user query. Overlap of 50 characters ensures tips split across boundaries are still retrievable.

## Sample Chunks

**Chunk 1 (doc1.txt):**
"Always inspect the apartment before signing. Look for mold under sinks and in bathrooms. Check all appliances work."

**Chunk 2 (doc2.txt):**
"In most states landlords are legally required to provide working heat within 24 to 72 hours of a repair request during winter."

**Chunk 3 (doc3.txt):**
"Monthly costs per person in a 2 bedroom apartment. Rent 680 dollars. Electricity 95 to 160 dollars. Total monthly cost approximately 1177 dollars per person."

**Chunk 4 (doc6.txt):**
"Before unloading any boxes do a full walkthrough of the empty apartment. Photograph every single room from multiple angles."

**Chunk 5 (doc7.txt):**
"For fall semester move-in start searching in January or February which is 7 to 8 months before move-in."

## Embedding Model

Model used: all-MiniLM-L6-v2 from sentence-transformers. Runs locally with no API key and no rate limits.

**Production tradeoffs:**
- Cost: all-MiniLM-L6-v2 is free and local. OpenAI text-embedding-3-small costs money but has better accuracy.
- Context length: all-MiniLM-L6-v2 supports 256 tokens which fits our short chunks well.
- Multilingual support: this model is English only. For international students a multilingual model would be needed.
- Local vs API: local model means no internet dependency but uses more local compute.

## Retrieval Test Results

**Query 1: How do I protect my security deposit?**
Top chunks returned from doc6.txt, doc1.txt, doc8.txt. These chunks directly discuss move-in documentation, photo evidence, and deposit protection strategies. Highly relevant.

**Query 2: What should I do if my landlord refuses repairs?**
Top chunks returned from doc2.txt, doc9.txt. These chunks discuss tenant rights, written repair requests, and contacting housing code enforcement. Directly relevant.

**Query 3: How much does off campus housing cost per month?**
Top chunks returned from doc3.txt, doc7.txt, doc10.txt. doc3.txt contains the exact cost breakdown. Relevant but system retrieved some annual cost figures alongside monthly figures causing minor confusion.

## How Grounded Generation is Enforced

The system prompt explicitly instructs the LLM: "Answer the question using ONLY the information provided in the documents below. If the documents do not contain enough information to answer the question, say I don't have enough information on that topic in my documents. Do not use any outside knowledge."

Source attribution is programmatically guaranteed by extracting source filenames from ChromaDB metadata and appending them to every response regardless of what the LLM generates.

## Example Responses

**Query: How do I protect my security deposit when moving in?**
Answer: To protect your security deposit when moving in, you should verify that the landlord owns the property before paying anything, and always pay by check or bank transfer, never in cash. Additionally, you should inspect the unit inside before signing the lease to document its condition.
Sources: doc8.txt, doc1.txt, doc6.txt, doc2.txt, doc5.txt

**Query: What are my rights if my roommate stops paying rent?**
Answer: If your roommate stops paying rent, you are still legally responsible for the full rent due to joint and several liability. However, you can pay the full rent to avoid eviction and then sue your roommate in small claims court to recover the unpaid amount.
Sources: doc4.txt, doc2.txt

**Out-of-scope query: What is the weather like in Paris?**
Answer: I don't have enough information on that topic in my documents.
Sources: doc4.txt, doc3.txt, doc2.txt

## Query Interface

The interface is built with Gradio and has two input/output fields:
- Input: "Your Question" text box where users type their housing question
- Output: "Answer" text box showing the grounded response
- Output: "Sources" text box showing which documents the answer came from

**Sample interaction:**
Question: When should I start looking for an apartment for next fall?
Answer: For fall semester move-in, you should start searching in January or February, which is 7 to 8 months before move-in. The best selection is available in February and March.
Sources: doc7.txt, doc8.txt, doc5.txt

## Evaluation Report

| Question | Expected Answer | System Response | Judgment |
|---|---|---|---|
| How do I protect my security deposit? | Take photos on move-in day, email to landlord | Correctly mentioned documentation, bank transfer, verifying landlord | Accurate |
| What to do if landlord refuses repairs? | Submit written request, contact code enforcement | Correctly mentioned written notice, tenant hotline, code enforcement | Accurate |
| How much does off campus housing cost? | Approximately $1177/month per person | Got $1177 correct but also confused with annual $8400 figure | Partially Accurate |
| When to start looking for fall apartment? | January or February, 7-8 months before | Correctly said January or February, 7 to 8 months before | Accurate |
| Rights if roommate stops paying rent? | Joint liability, can sue in small claims | Correctly explained joint liability and small claims court | Accurate |

## Failure Case

**Question 3: How much does off campus housing cost per month?**

The system retrieved chunks from both doc3.txt (monthly costs) and doc10.txt (annual costs). The annual figure of $8400 appeared in the context alongside the monthly figure of $1177. The LLM then attempted to reconcile these two numbers by dividing $8400 by 12, producing an unnecessary and confusing calculation.

**Why it happened:** The chunks were too small to include the full context explaining that $8400 is the annual total and $1177 is the monthly per-person cost. The retrieval pulled both figures without enough surrounding context to distinguish them.

**How to fix it:** Increase chunk size to 500 characters so annual and monthly cost figures appear in the same chunk with their labels.

## Spec Reflection

**How the spec helped:** Writing the evaluation plan in planning.md before coding forced me to define specific verifiable questions upfront. This made testing much faster because I knew exactly what to look for.

**How implementation diverged:** The spec planned for chunk size of 300 characters but the cost question failure suggests 500 characters would work better for documents that contain multiple related numbers. I would increase chunk size if rebuilding.

## AI Usage

**Instance 1:** I designed the chunking strategy myself based on reading the 
documents and deciding 300 character chunks with 50 overlap fit the short 
Reddit-style content. I then asked Claude to implement the ingestion script 
based on my spec. The generated code had a wrong import path which I caught 
and fixed myself.

**Instance 2:** I asked Claude to help write the Gradio interface structure. 
I decided the design myself - two separate output fields for answer and sources 
so attribution is always visible. I tested every query myself and identified 
the failure case in Q3 independently by reading the retrieved chunks and 
noticing the annual vs monthly cost confusion.