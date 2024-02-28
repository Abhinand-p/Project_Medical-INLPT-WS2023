import os
from openai  import  OpenAI
import voyageai
from dotenv import load_dotenv

#One index corresponds to 1 embedding model

class embeddingManager:

    def __init__(self): 
        load_dotenv()
        voyageai.api_key =  "pa-3xpcuUhVVgmOQPDBiG7ObYUA58rGn1eB1ZMaowr5xy0"

        self.voyageAIClient = voyageai.Client()

        self.openAIClient = OpenAI()

        self.embedding_list = ["voyage-2-large", "text-embedding-3-large"]
        
    # The controller takes the embedding model that was requested from front-end (inferred by the index) and decides which function to call corespondingly    
    def controller(self, question,retrieval_strategy, embedding_model ):
        
        if(retrieval_strategy == "Sparse Retrieval"):
            return 
        if(embedding_model == self.embedding_list[0]):
            print("########### Emb Model: voyage-2-large")
            return self.voyage_2_large( question)
        if(embedding_model == self.embedding_list[1]):
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
