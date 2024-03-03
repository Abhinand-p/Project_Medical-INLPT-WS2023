import torch
from langchain.vectorstores import OpenSearchVectorSearch
from langchain_community.embeddings import VoyageEmbeddings, HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
import os

class VectorStoreManager:
    def __init__(self) -> None:
        host = 'localhost'
        port = 9200
        auth = ('admin', '!akjdaDsdoij!oijadSsajd123120938')

        #Config mbedding models
        self.index_list = ["voyage-2-large", "text-embedding-3-large","distilroberta", "e5-base-v2"]

        device = 'cpu' if torch.cuda.is_available() else 'cuda'
        self.embedding_kwargs = dict(
            model_kwargs={'device': device}, # Pass the model configuration options
            encode_kwargs={'normalize_embeddings': False, 'batch_size': 32},
        )

        self.embedding_models = dict()

        self.db = OpenSearchVectorSearch(opensearch_url=f"http://{host}:{port}",
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
            self.embedding_models[index] = VoyageEmbeddings(voyage_api_key=os.getenv("VOYAGE_API_KEY"), model="voyage-2-large")
        elif index == "text-embedding-3-large":
            self.embedding_models[index] = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"), model="text-embedding-3-large", model_kwargs=self.embedding_kwargs["model_kwargs"])
        elif index == "distilroberta":
            self.embedding_models[index] = HuggingFaceEmbeddings(model_name="sentence-transformers/all-distilroberta-v1", **self.embedding_kwargs)
        elif index == "e5-base-v2":
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
