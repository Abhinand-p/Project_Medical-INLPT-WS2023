import pinecone
import json



class PineconeOperations:

    def __init__(self):

        pinecone.init(
            api_key="4d2c2cd0-cf55-43c5-afb1-11001dc68709",
            environment="gcp-starter"
        )
        self.index = pinecone.Index("inlp-med-ws2324")

    def fetch_stats(self):
        # fetches stats about the index
        stats = self.index.describe_index_stats()
        return str(stats)

    def query(self, query_vector):
        # query from the index, eg: [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3,....]
        response = self.index.query(
            vector=query_vector,
            top_k=3,
        )
        res = json.loads(str(response).replace("'", '"'))
        print(response)
        print(res)
        
        return res