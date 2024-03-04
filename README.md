# Project_Medical-INLPT-WS2023

Repository containing all essential details about our project development for the course Natural Language Processing with Transformers.

# Getting Started

This part explains how to deploy a bare back-end and front-end servers to get the RAG system with multiple end points up and running.

### Deployment (No docker required)

* #### Frontend Installation process

  * [Frontend Deployment process](./server/frontend/README.md) `cd ./server/frontend/`

* #### Backend Installation process

  * [Backend Deployment process](./server/backend/README.md) `cd ./server/backend/`

Note: changes should be done the on level of the connection between the backend server and opensearch api, `localhost:port=9200`

### Deployment (docker required) [RECOMENDED]

* #### docker compose is needed for microservices enviroment run

  * `cd ./server/` then `docker compose -f .\docker-compose.yml up`
  * The microservices are devided into 3 entities, which the first entity contains 3 containers for the opensearch, the second entity would be the frontend server based on REACT framework using Node.js and the third entity would be the backend server based on FastAPI using Uvicorn [where the magic happens :) ] **[IMPORTANT DETAILS](./server/DOCKER.md)**

* Azure pipeline
  * Azure pipeline can be used only if you are logged in with your credentials, however we are willing to offer compute resource for now under a username and password for March 2024 **[username]: <abhinand.po@outlook.com>** **[password]: India123#** (*please contact us for the* **code**) -- Note: please follow this [guide](./server/DOCKER.md) under azure reference.

Note: for more *details* about the server pipeline please check [this](./server/SERVER.md).

### Adding data to OpenSearch

* Please refer to download these two files **[LINK_1](https://drive.google.com/file/d/1Z3pYk1MCMUKdVbcpW5b7LgNFN5Av0EoB/view?usp=drive_link)** & **[LINK_2](https://drive.google.com/file/d/1j2OfFyxKbk_obTK2HGY2N_snH_b9hSfZ/view?usp=sharing)** and import them to the volumes that are created by the docker-compose (by default they are called: **server_opensearch-data1** & **server_opensearch-data2**). <br> <br>
**PLEASE IMPORTANT** import the files in order where *LINK_1* is for *data1* and *LINK_2* is for *data2*

### Aditional Notes

* Please be aware that the system is needs alot of resources, as we have LLMs are downloaded in the containers and requires some good specs, yet we alos managed to work on the quantization part for LLaMA-2 which we have it working using cuda-gpus and cpu-accelartors

* Postman web-requests .json exports can be found under `cd ./server/NLPT.postman_collection.json`

* This link is a small show case of what we did in our project. HAVE FUN WATCHING :) [Video]()

# Folder Structutre Description

1. /DataManipulation

* This folder involves all the code we wrote for scraping the pubmed data and formatting it into a Dataset [Check here](./DataManipulation//README.md)

2. /EvaluationMethods

* When we started to think about an evaluation method we knew the first thing we need is some kind of question/answer (where answers are ground truths) so we started with experimeting wit different LLMs and prompts to let them create such a set. However most of them didnt gave us a set with the desired quality, the only thing that worked was the createSyntheticTestData method from ragas. The /experimental folder contains the past attempts.

* Once we had the question/answer set available we had to run it through the different pipeline configurations and collect the retrieved contexts / answers, this data is stored in /ragas_eval_sets
* The Notebook where we utilized the evaluation sets to get the respective metrics is in: ragas/ragasEval_openai.ipynb

3. /Meetings

* This folder contains a log for our weekly meetings

4. /ProjectPath

* This folder contains some documentation on ideas and go to's for our project

5. /Retrieval

* /Embedding: This folder contains all different aproaches we tried to chunk and vectorize our data

* /OpenSearch: On here we have a .yml file to launch and run the whole project inside a docker container as a compose project
* /TF_IDF: Some early experiments with tf-idf

6. /server

* Our end-to-end Chatbot is run on a website. This website is powered by two dedicated servers, one for frontend and one for backend. This folder contains the source code for both of them.

# Design Decisions (based on how to build RAG system)

### Data Acquisition

* Web Crawler where selenium web driver is used for fetching the required Html tags to process the required data and download it
* API as we used one of the two methods that are mentioned. ([please check here)](./DataManipulation/DataAcquisitionMethods/README.md)

### Data Analysis & Data Preprocessor

* So we can properly understand the data we did some analysis to calculate some required information for our project ([please check here](./DataManipulation/DataAnalysis/README.md))

### Retreival

* #### TF_IDF: which were our first approach for data retrival

* #### Embedding: alot of strats were applied their which will be discussed in the documentaion report in DOCUMENTATION.md (please check the notebooks where intresting stuff were going there :) )

* #### **OpenSearch**: we decide at last after going to **FaunaDB** and **PineCone** to settle with OpenSearch engine as well this will be discussed in the DOCUMENTATION.md

### Evaluation Methods

* Evaluation methods were applied here and some of the basic logic of what is discussed in the lectures is also implemented in the pipeline under query transformation using sematic similarity. ([please check here](./EvaluationMethods/README.md))

### Servers

* The servers part is devided as explained under docker compose part to multiple microservices where they are communicating with each other to perform some required functionality which will results to have a working **chatBOT**.

![Server Schema](./server/NLPT%20Project.png)

* As shown in the schematics this is our working [pipeline](./server/SERVER.md).

# Team members and their GitHub-id

1. Behrooz Montazeran: BehroozMontazeran
2. Abhinand Poosarala: Abhinand-p
3. John Hildenbrand  : Johncrtz
4. Hussein Abdulreda : HRida
