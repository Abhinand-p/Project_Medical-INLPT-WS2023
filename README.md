# Project_Medical-INLPT-WS2023

Repository containing all essential details about our project development for the course Natural Language Processing with Transformers.

# Getting Started

This part explains how to deploy the back-end and front-end servers to get the RAG system up and running.

### Installation

#### Frontend Installation process

change current direcotery

`cd ./server/frontend/`

npm install to install all the required dependencies from package.json

`npm install`

### Deployment

* [Frontend Deployment process](./server/frontend/README.md)
* [Backend Deployment process](./server/backend/README.md)

# Folder Structutre Description

### Data Analysis

[Check here](./Data%20Analysis/README.md)

### Data Pool

### Embeddings

### Evaluation Methods

### Retreival

### Server

# How to build RAG System

How to Build such System? (Step 1)

* Start with data acquisition.
* Collect the document subset needed.
* Find a way to properly store the data.
* Find a way to search through the documents.

What metadata is needed?

* Only abstracts are required
* Document has multiple sections
* Do you keep the structure?

How to Build such System? (Step 2)

* Create a system that considers the entire document set or a small relevant subset to generate the correct answer.
* Mainly two stages
  * Retrieval: find documents that are relevant for the question.
  * Answer generation: generate an answer based on the selected subset.

How to Build such System? (Step 3)

* Build an interface for the user to connect with the system.
* Command line in simplest form
* Website, mobile app…. (be creative!)

How to Build such System? (Step 4)

* Come up with an evaluation strategy
  * Make use of manual annotation.
  * Find an automated annotation strategy.
  * Use correct metrics.
* You learn about evaluation metrics in the course
* Take care of edge cases and know the limitations of your system.

# Design Decisions (based on how to build RAG system part :) )

### Data Acquisition

1. Web Crawler where selenium web driver is used for fetching the required Html tags to process the required data and download it
2. API where there is 2 methods ([Check here)](./Data%20Pool/Data%20Acquisition%20Methods/README.md)
   * Used case parallel threading <<<<<<<<<<<<<<<<<<<<
3. Uploading the data on both FaunaDB and PineCone with same uuid which will be the coupling id between two systems
4. FaunaDB (Metadata database) -> bcz on Pinecone for free version we are not allowed more than certain word count per text
5. PineCone (Vector database)
6. embedding model (intfloat/e5-large-v) local download
7. biobert-pubmed-qa (using azure) [extractive QA model] get_answer_1 + get_model
8. langChain (GPT-3.5-turbo used as a model)
9. OpenSearch

# Changelogs

# Team members and their GitHub-id

1. Behrooz Montazeran: BehroozMontazeran
2. Abhinand Poosarala: Abhinand-p
3. John Hildenbrand  : Johncrtz
4. Hussein Abdulreda : HRida (3769915)
