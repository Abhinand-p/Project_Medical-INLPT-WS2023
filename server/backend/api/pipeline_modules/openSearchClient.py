""" This module is responsible for the communication with the OpenSearch server. It contains the OpenSearchManager class which is responsible for the communication with the OpenSearch server. It contains the following methods:"""
from opensearchpy import OpenSearch
from utils import Utils
from fuzzywuzzy import fuzz

class OpenSearchManager:

    def __init__(self):
        self.utils = Utils()
        host = 'opensearch-node1' #'localhost'
        # port = 9200
        auth = ('admin', '!akjdaDsdoij!oijadSsajd123120938')

        self.client = OpenSearch(
            hosts = [{'host': host}], # 'port': port
            http_auth = auth,
            use_ssl = True,
            verify_certs = False,
            timeout=100
        )
        self.k = 2
        self.retrieval_list = ["Dense Retrieval", "Sparse Retrieval", "Hybrid Search"]

        #The following indices involve a different retrieval process
        self.index_with_chunks = ["distilroberta", "e5-base-v2"]

    # The controller takes the retrieval strategy that was requested from front-end and decides which function to call corespondingly
    def controller(self, retrieval_strategy, embedding, question, index):

        if(self.checkQuery(question)):
            return None, None

        if(retrieval_strategy == self.retrieval_list[0]):
            print("########### Retrieval: Dense Retrieval")
            return self.denseRetrieval(embedding, index)

        if(retrieval_strategy == self.retrieval_list[1]):
            print("########### Retrieval: Sparse Retrieval")
            return self.sparseRetrieval(question, "voyage-2-large")

        if(retrieval_strategy == self.retrieval_list[2]):
            print("########### ERetrieval: Hybrid Search")
            return self.hybridSearch(question, embedding, index)

    #if one of these key phrases is inside the query it strogly suggests that we dont need an IR
    def checkQuery(self, question):
        non_IR_keyphrase = ["your last answer", "thank you", "summarize it", "make it shorter", "rephrase it", "say it again", "Hello", "How are you?", "Repeat it"] 
        for keyword in non_IR_keyphrase:
            ratio = fuzz.ratio(question, keyword)
            #ratio of 80 mean a moderate match,  100 would mean completley strict match
            if ratio >= 80:
                return False

    def denseRetrieval(self ,embedding, index):
        if index in self.index_with_chunks:
            self.k = 10
        else: self.k = 2
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

        context = self.extractTextFromResponse(response,index)

        return context

    def sparseRetrieval(self ,question, index):
        if index in self.index_with_chunks:
            self.k = 10
        else: self.k = 2
        text_search_body = {
        "size" : self.k,
        "query": {
            "match": {
                "text": question
                }
            }
        }

        response = self.client.search(index=index, body=text_search_body)
        context = self.extractTextFromResponse(response,index)
        return context

    def hybridSearch(self, question,embedding, index):
        if index in self.index_with_chunks:
            self.k = 10
        else: self.k = 2
        print(question)
        print(embedding)
        route = f"/{index}/_search?search_pipeline=nlp_search-pipeline"

        hybrid_search_body = {
        "_source": {
            "exclude": [
            "vector"
            ]
        },
        "size" : 5,
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
        context = self.extractTextFromResponse(response,index)
        return context

    #private
    def extractTextFromResponse(self, response, index):
        context = []
        if index in self.index_with_chunks:
            for _, doc in enumerate(response['hits']['hits']):
                context.append({
                    'id': doc['_id'],
                    'context': doc['_source']['text'],
                    'source': doc['_source']['cite']
            })
            return context
        else:
            context = ""
            hits = response['hits']['hits']
            for i, hit in enumerate(hits[:self.k]):
                source = hit['_source']
                context = context + f"Context {i}: {source['text']}"
                #print(f"Score: {hit['_score']}, Text: {source['text']}")
            return context

    def getAllIndices(self):
        # url = "_alias"
        # allIndices = self.client.transport.perform_request(method = "GET", url = url)

        allIndices = self.client.indices.get_alias().keys()
        allIndicesList = []
        for index in allIndices:
            allIndicesList.append(index)

        return allIndicesList



