""" This module is responsible for the communication with the OpenSearch server. It contains the OpenSearchManager class which is responsible for the communication with the OpenSearch server. It contains the following methods:"""
from opensearchpy import OpenSearch
from utils import Utils

class OpenSearchManager:

    def __init__(self):
        self.utils = Utils()
        host = 'localhost'
        port = 9200
        auth = ('admin', '!akjdaDsdoij!oijadSsajd123120938')

        self.client = OpenSearch(
            hosts = [{'host': host, 'port': port}],
            http_auth = auth,
            use_ssl = True,
            verify_certs = False,
            timeout=100
        )
        self.k = 3
        self.retrieval_list = ["Dense Retrieval", "Sparse Retrieval", "Hybrid Search", "RetrievalQA"]
        self.chain_types = ["stuff", "refine", "map_reduce", "map_re_rank"]

    # The controller takes the retrieval strategy that was requested from front-end and decides which function to call corespondingly
    def controller(self, retrieval_strategy, embedding, question, index, chunk):
        if(retrieval_strategy == self.retrieval_list[0]):
            print("########### Retrieval: Dense Retrieval")
            return self.denseRetrieval(embedding, index, chunk)

        if(retrieval_strategy == self.retrieval_list[1]):
            print("########### Retrieval: Sparse Retrieval")
            return self.sparseRetrieval(question, index, chunk)

        if(retrieval_strategy == self.retrieval_list[2]):
            print("########### ERetrieval: Hybrid Search")
            return self.hybridSearch(question,embedding, index, chunk)

        # if(retrieval_strategy == self.retrieval_list[3]):
        #     print("########### Retrieval: RetrievalQA")
        #     return self.retrievalQA(question, index, chain_type)

    def denseRetrieval(self ,embedding, index, chunk=False):
        if chunk:
            self.k = 10
        knn_search_body = {
        "size": self.k,  # Number of nearest neighbors to retrieve
            "query": {
                "knn": {
                    "vector": {
                        "vector": embedding,
                        "k": self.k  # Number of nearest neighbors to retrieve
                        }
                    }
                    }
                }
        # Execute the search
        response = self.client.search(index=index, body=knn_search_body)

        context, cite = self.extractTextFromResponse(response)

        return context, cite

    def sparseRetrieval(self ,question, index, chunk=False):
        if chunk:
            self.k = 10
        text_search_body = {
        "size" : self.k,
        "query": {
            "match": {
                "text": question
                }
            }
        }

        response = self.client.search(index=index, body=text_search_body)
        context, cite = self.extractTextFromResponse(response)
        return context, cite

    def hybridSearch(self, question,embedding, index, chunk=False):
        if chunk:
            self.k = 10
        route = f"/{index}/_search?search_pipeline=nlp_search-pipeline"

        hybrid_search_body = {
        "_source": {
            "exclude": [
            "vector"
            ]
        },
        "size" : self.k,
        "query": {
            "hybrid": {
            "queries": [
                {
                "match": {
                    "text": {
                    "query": question
                    }
                }
                },
                {
                "knn": {
                    "vector": {
                    "vector": embedding,
                    "k": self.k
                    }
                }
                }
            ]
            }
        }
        }
        response  = self.client.transport.perform_request(method = "GET", url = route, body = hybrid_search_body) 
        context, cite = self.extractTextFromResponse(response)
        return context, cite

    # def retrievalQA(self, question, index, chain_type):
    #     rag_pipeline = RetrievalQA.from_chain_type(
    #                                                 llm=index,
    #                                                 chain_type=chain_type,
    #                                                 verbose=True,
    #                                                 retriever=vectorstore.as_retriever(search_kwargs={"k":5}),
    #                                                 chain_type_kwargs={"verbose": True })
    #     return rag_pipeline(query)

    def extractTextFromResponse(self, response, chunk=False): #intended as a private function
        context = []
        if chunk:
            for _, doc in enumerate(response['hits']['hits']):
                context.append({
                    'id': doc['_id'],
                    'text': doc['_source']['text'],
                    'source': doc['_source']['cite']
            })
            return context
        else:
            context = ""
            hits = response['hits']['hits']
            for _, hit in enumerate(hits[:self.k]): 
                source = hit['_source']
                context = context + f"{source['text']}"
                #print(f"Score: {hit['_score']}, Text: {source['text']}")
            cite = response['hits']['hits'][0]['_source']['cite']
            return context, cite

    def getAllIndices(self):
        allIndices = self.client.indices.get_alias().keys()
        allIndicesList = []
        for index in allIndices:
            allIndicesList.append(index)

        return allIndicesList



