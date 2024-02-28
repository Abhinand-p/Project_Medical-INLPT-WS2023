""" This file is responsible for managing the embedding models and their respective functions."""
from openai  import  OpenAI
import voyageai
import configparser

#One index corresponds to 1 embedding model

class EmbeddingManager:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        voyageai.api_key = config['API_KEY']['VOYAGE_API_KEY']

        self.voyageAIClient = voyageai.Client()

        self.openAIClient = OpenAI()

        self.embedding_list = ["voyage-2-large", "text-embedding-3-large"]
        
    # The controller takes the embedding model that was requested from front-end (inferred by the index) and decides which function to call corespondingly    
    def controller(self, question,retrieval_strategy, embedding_model ):
        
        if(retrieval_strategy == "Sparse Retrieval"):
            return 
        elif(embedding_model == self.embedding_list[0]):
            print("########### Emb Model: voyage-2-large")
            return self.voyage_2_large( question)
        elif(embedding_model == self.embedding_list[1]):
            print("########### Emb Model: text-embedding-3-large")
            return self.text_embedding_3_large( question)
        return 0
    

    def text_embedding_3_large(self, question ):
        response = self.openAIClient.embeddings.create(
            model="text-embedding-3-large",
            input=question,
            dimensions = 1024
        ).data[0].embedding
        
        return response


    def voyage_2_large(self,question):
        response = self.voyageAIClient.embed(question, model="voyage-large-2", input_type="document").embeddings[0]
        return  response
