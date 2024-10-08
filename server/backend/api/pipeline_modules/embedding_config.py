""" This file is responsible for managing the embedding models and their respective functions."""
from openai  import  OpenAI
import voyageai
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv, find_dotenv

#One index corresponds to 1 embedding model

class EmbeddingManager:

    def __init__(self):
        try:
            # Load .env file
            # load_dotenv(dotenv_path=find_dotenv())
            print("######### Embdding #############")
            print(os.getenv("HF_AUTH"))
            print(os.getenv("OPENAI_API_KEY"))
            print(os.getenv("VOYAGE_API_KEY"))
            print("###############################")

            voyageai.api_key =  os.getenv("VOYAGE_API_KEY")
            print(os.getenv("VOYAGE_API_KEY"))
            #Config mbedding models
            self.embedding_list = ["voyage-2-large", "text-embedding-3-large","distilroberta", "e5-base-v2"]

            self.voyageAIClient = voyageai.Client()
            print("voyageAIClient")
            self.openAIClient = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            print("openAIClient")
            self.distilroberta = HuggingFaceEmbeddings(model_name='sentence-transformers/all-distilroberta-v1')
            print("distilroberta")
            self.e5 = HuggingFaceEmbeddings(model_name="intfloat/e5-base-v2",
                                            model_kwargs={'device':'cpu'},
                                            encode_kwargs={'normalize_embeddings': False,
                                            'batch_size': 32})
            print("e5")
        except Exception as varname:
            print(varname)

    # The controller takes the embedding model that was requested from front-end (inferred by the index) and decides which function to call corespondingly
    def controller(self, question, retrieval_strategy, index):

        if(retrieval_strategy == "Sparse Retrieval"):
            return
        elif(index == self.embedding_list[0]):
            print("########### Emb Model: voyage-2-large")
            return self.voyage_2_large(question)
        elif(index == self.embedding_list[1]):
            print("########### Emb Model: text-embedding-3-large")
            return self.text_embedding_3_large( question)
        elif(index == self.embedding_list[2]):
            print("########### Emb Model: distilroberta")
            return self.distilroberta_recursive( question)
        elif(index == self.embedding_list[3]):
            print("########### Emb Model: intfloat/e5-base-v2")
            return self.intfloat_e5_base_v2(question)

    def voyage_2_large(self,question):
        response = self.voyageAIClient.embed(question,
                                                model="voyage-large-2",
                                                input_type="document"
                                            ).embeddings[0]
        return  response

    def text_embedding_3_large(self, question ):
            response = self.openAIClient.embeddings.create(
                model="text-embedding-3-large",
                input=question,
                dimensions = 1024
            ).data[0].embedding
            return response

    def distilroberta_recursive(self, question):
        embedded_question = self.distilroberta.embed_documents(question)[0]
        print(type(embedded_question))
        return embedded_question

    def intfloat_e5_base_v2(self,question):
        response = self.e5.embed_query(question)
        return response