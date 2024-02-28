from opensearchpy import OpenSearch

class openSearchManager:

    def __init__(self):

        host = 'localhost'
        port = 9200
        auth = ('admin', 'admin')

        self.client = OpenSearch(
            hosts = [{'host': host, 'port': port}],
            http_auth = auth,
            use_ssl = True,
            verify_certs = False,
            timeout=100
        )
        self.k = 3 
        self.retrieval_list = ["Dense Retrieval", "Sparse Retrieval", "Hybrid Search"]

    # The controller takes the retrieval strategy that was requested from front-end and decides which function to call corespondingly
    def controller(self, retrieval_strategy, embedding, question, index):
        if(retrieval_strategy == self.retrieval_list[0]):
            print("########### Retrieval: Dense Retrieval")
            return self.denseRetrieval(embedding, index)
        
        if(retrieval_strategy == self.retrieval_list[1]):
            print("########### Retrieval: Sparse Retrieval")
            return self.sparseRetrieval(question, index)
        
        if(retrieval_strategy == self.retrieval_list[2]):
            print("########### ERetrieval: Hybrid Search")
            return self.hybridSearch(question,embedding, index)
    

    def denseRetrieval(self ,embedding, index):

        knn_search_body = {
        "size": 5,  # Number of nearest neighbors to retrieve
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
    

    def sparseRetrieval(self ,question, index):
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
    

    def hybridSearch(self, question,embedding, index):
        route = f"/{index}/_search?search_pipeline=nlp_search-pipeline"

        hybrid_search_body = {
        "_source": {
            "exclude": [
            "vector"
            ]
        },
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
    

    def extractTextFromResponse(self, response): #intended as a private function
        context = ""
        hits = response['hits']['hits']
        for id, hit in enumerate(hits[:self.k]): 
            source = hit['_source']
            context = context + f"""Chunk {id}: {source['text']}"""
            #print(f"Score: {hit['_score']}, Text: {source['text']}")
        cite = response['hits']['hits'][0]['_source']['cite']
        return context, cite
    

    def getAllIndices(self):
        allIndices = self.client.indices.get_alias().keys()
        allIndicesList = []
        for index in allIndices:
            allIndicesList.append(index)

        return allIndicesList
    
    


