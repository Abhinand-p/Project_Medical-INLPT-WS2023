### This file documents the different approaches we chose for implementing certain parts of the pipeline

## Data Acquisition

1. Crawler
2. API


## Data Storage and Retrieval

1. TF-IDF
2. Cloud based, splitt approach
   -   Storage: Uploading embedding vectors on cloud based VectorDB (Pinecone) and respective abstract's metadata in seperate no-SQL DB (FaunaDB). Use a key to map vectors to metadata between the databases.
   -   Retrieval: Retrieve a document by first finding top k matches between embedded query and stored vectors in Pinecone, use the ids from the top k matches to query text+metadata, implemented via given API keys into our servers backend/frontend 


## Embeddings

1. PubMedBERT, per-abstract chunking
   - BERT model finetuned on PubMed data, information retrieval/ QA, maps into 768 dimensional vectorspace, up to 512 token.
   - Created one embedding per abstract

-----------------------------------------------

ToDo:
- Creating benchmark for retrieval/embeddings to evaulate and compare our different approaches
- Create statistics for size of abstracts to get better understanding of how to segment the abstracts

