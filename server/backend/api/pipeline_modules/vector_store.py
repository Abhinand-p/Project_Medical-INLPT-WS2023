import torch
from langchain.vectorstores import OpenSearchVectorSearch
from langchain_community.embeddings import VoyageEmbeddings, HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv, find_dotenv

class VectorStoreManager:
    def __init__(self) -> None:
        # Load .env file
        load_dotenv(dotenv_path=find_dotenv())
        print("######### VectorStore #############")
        print(os.getenv("HF_AUTH"))
        print(os.getenv("OPENAI_API_KEY"))
        print(os.getenv("VOYAGE_API_KEY"))
        print("####################################")

        host = 'opensearch-node1' # be aware of the host name for docker
        # port = 9200
        auth = ('admin', 'admin')

        #Config mbedding models
        self.index_list = ["voyage-2-large", "text-embedding-3-large","distilroberta", "e5-base-v2"]

        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.embedding_kwargs = dict(
            model_kwargs={'device': device}, # Pass the model configuration options
            encode_kwargs={'normalize_embeddings': False, 'batch_size': 32},
        )

        self.embedding_models = dict()

        self.db = OpenSearchVectorSearch(opensearch_url=f"http://{host}", # :{port} remove port and change hostname for docker
                                        index_name="",
                                        embedding_function = "",
                                        use_ssl = True,
                                        verify_certs = False,
                                        http_auth = auth,
                                        space_type="cosinesimil")

    def get_embedding_model(self, index):
        if index not in self.embedding_models:
            self.create_embedding(index)
        return self.embedding_models[index]

    def create_embedding(self, index):
        if index == "voyage-2-large":
            print("Creating voyage-2-large in vecor store")
            self.embedding_models[index] = VoyageEmbeddings(voyage_api_key=os.getenv("VOYAGE_API_KEY"), model="voyage-large-2")
        elif index == "text-embedding-3-large":
            print("Creating text-embedding-3-large in vecor store")
            self.embedding_models[index] = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"), model="text-embedding-3-large", dimensions=1024)
        elif index == "distilroberta":
            print("Creating distilroberta in vecor store")
            self.embedding_models[index] = HuggingFaceEmbeddings(model_name="sentence-transformers/all-distilroberta-v1", **self.embedding_kwargs)
        elif index == "e5-base-v2":
            print("Creating e5-base-v2 in vecor store")
            self.embedding_models[index] = HuggingFaceEmbeddings(model_name="intfloat/e5-base-v2", **self.embedding_kwargs)

    def update_index_model(self, index):
        try:
            if index in self.index_list:
                self.db.index_name = index
                self.db.embedding_function = self.get_embedding_model(index)
            else:
                raise ValueError("Index not found, please select a valid index [voyage-2-large, text-embedding-3-large, distilroberta, e5-base-v2]")
            return True, ""
        except Exception as varname:
            return False, varname
