""" This file is responsible for managing the embedding models and their respective functions."""
from openai  import  OpenAI
import voyageai
from langchain_community.embeddings import HuggingFaceEmbeddings

#One index corresponds to 1 embedding model

class EmbeddingManager:

    def __init__(self):
        # config = configparser.ConfigParser()
        # config.read('config.ini')
        #voyageai.api_key = config['API_KEY']['VOYAGE_API_KEY']
        voyageai.api_key = "pa-3xpcuUhVVgmOQPDBiG7ObYUA58rGn1eB1ZMaowr5xy0"

        #Config mbedding models
        self.embedding_list = ["voyage-2-large", "text-embedding-3-large","distilroberta", "e5-base-v2"]

        self.voyageAIClient = voyageai.Client()

        self.openAIClient = OpenAI(api_key= "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")

        self.distilroberta = HuggingFaceEmbeddings(
            model_name='sentence-transformers/all-distilroberta-v1')

        self.e5 = HuggingFaceEmbeddings(model_name="intfloat/e5-base-v2",
                                        model_kwargs={'device':'cpu'}, # Pass the model configuration options
                                        encode_kwargs={'normalize_embeddings': False,
                                        'batch_size': 32} # Pass the encoding options
                                        )

    # The controller takes the embedding model that was requested from front-end (inferred by the index) and decides which function to call corespondingly
    def controller(self, question,retrieval_strategy, embedding_model):

        if(retrieval_strategy == "Sparse Retrieval"):
            return
        elif(embedding_model == self.embedding_list[0]):
            print("########### Emb Model: voyage-2-large")
            return self.voyage_2_large(question)
        elif(embedding_model == self.embedding_list[1]):
            print("########### Emb Model: text-embedding-3-large")
            return self.text_embedding_3_large( question)
        elif(embedding_model == self.embedding_list[2]):
            print("########### Emb Model: distilroberta")
            return self.distilroberta_recursive( question)
        elif(embedding_model == self.embedding_list[3]):
            print("########### Emb Model: intfloat/e5-base-v2")
            return self.intfloat_e5_base_v2(question)
        return 0

    def distilroberta_recursive(self, question):
        embedded_question = self.distilroberta.embed_documents(question)[0]
        print(type(embedded_question))
        return embedded_question

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

    def intfloat_e5_base_v2(self,question):
        response = self.e5.embed_query(question)
        return response