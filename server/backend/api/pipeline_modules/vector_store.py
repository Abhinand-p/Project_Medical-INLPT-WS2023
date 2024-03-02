from langchain.vectorstores import OpenSearchVectorSearch
from langchain.embeddings import HuggingFaceEmbeddings

class VectorStoreManager:
    def __init__(self) -> None:
        host = 'localhost'
        port = 9200
        auth = ('admin', '!akjdaDsdoij!oijadSsajd123120938')
        self.index_with_chunks = ["distilroberta", "e5-base-v2"]

        self.embeddings = HuggingFaceEmbeddings(model_name="intfloat/e5-base-v2",
                                           model_kwargs={'device':'cpu'}, # Pass the model configuration options
                                           encode_kwargs={'normalize_embeddings': False, 'batch_size': 32}) # Pass the encoding options

        self.db = OpenSearchVectorSearch(opensearch_url=f"http://{host}:{port}",
                                        index_name=self.index_with_chunks[1],
                                        embedding_function = self.embeddings,
                                        use_ssl = True,
                                        verify_certs = False,
                                        http_auth = auth,
                                        space_type="cosinesimil")


