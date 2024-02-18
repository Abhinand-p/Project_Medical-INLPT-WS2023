### This file documents the different approaches we chose for implementing certain parts of the pipeline

## Data Acquisition

1. Crawler:
   - Using this method we implement a crawler using selenium to extract each abstract, its title and the respective authors from Pubmed one by one
2. API:
   - By this approach we downloaded the xml file, which was later processed and the usefull data extracted using the preprocessing notbook and finally the csv file of the related data was created. As the whole dataset was too big to be pushed to github, we used hugging-face to host our dataset. This will be changed later by putting all datasets in our private domain in a cloud. 
## Data Preprocessing
   - In this phase of the project we used the xml file of data from Pubmed and extract 17 usefull metadata from them with respective data.
   - in the next phase we create anothe dataset containg only Ids (PMID) and concatenated columns of abstracts, titles, data of publication, authors, medical keys related to each abstracts and name of journal. By which we can answer more type of questions based our dataset.
## Data Storage

1. Cloud based, split approach
   - Storage: Uploading embedding vectors on cloud based VectorDB (Pinecone) and respective abstract's metadata in seperate no-SQL DB (FaunaDB). Use a key to map vectors to metadata between the databases.
   - Retrieval: Retrieve a document by first finding top k matches between embedded query and stored vectors (cosine similarity) in Pinecone, use the ids from the top k matches to query text+metadata, implemented via given API keys into our servers backend/frontend

## Data Retrieval
## 1. TF-IDF
   - In this Approach we used the TfidfVectorizer from sklearn and sset the analyzing level to characters which provided us the misspelling tolerance. Moreover, we used nltk to add the synonyms to the search of most k relevant abstacts. 
## 2. Embeddings
### 1. Approach
1. PubMedBERT, per-abstract embedding
   - BERT model finetuned on PubMed data, information retrieval/ QA, maps into 768 dimensional vectorspace, up to 512 token.
   - Created one embedding per abstract
     -> Turned out to be badly implemented because models max input size was not taken into consideration
2. e5-large-V2, embed chunks and store chunks in abstract
   - "E5 is a general-purpose embedding model for tasks requiring a single-vector representation of texts such as retrieval, clustering, and classification, achieving strong performance in both zero-shot and fine-tuned settings." 1024 Output dimension, 512 input size
   - Chunk abstract after 512 tokens, between each chunk of an abstract create overlapping chunks
   - Added 'local context' to each chunks metadata which is the text that appears before and after the chunk (local context appr. 20% of abstracts size). This will later on be concatinated with the chunks text so that the model in charge of answering the prompt has a better understanding of the chunk role in the abstract itself (context)
   - We embedded and stored each chunk to our vector space which resulted in appr. 68k vectors
   - Code can be found at: embedding\INLPT2023_2024.ipynb
3. One could also take the embedded chunks of an abstract and combine them by f.e. mean pooling, this way we end up with one embedding per abstarct agin
   - Not sure about the quality of the resulting embedding

### 2. Approach

### Adding LLM to pipeline for QA

General: This part involves adding a LLM to the pipeline and putting it all together such that the LLM can answer the questions

1. ## Local approach: Whenever backend server is initialized the LLM for answering the questions and the embedding model for embedding the user query will be downloaded and operate locally

---

ToDo:

- Finish the prototype
