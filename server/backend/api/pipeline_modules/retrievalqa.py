from vector_store import VectorStoreManager
from langchain.chains import RetrievalQA

class RetrievalQAManager:
    def __init__(self) -> None:
        self.chain_types = ["stuff", "refine", "map_reduce", "map_re_rank"]
        pass

    def retrievalChain(self, question, index, vector: VectorStoreManager, chain_type):
        if chain_type == "":
            chain_type = "stuff"

        qa_chain = RetrievalQA.from_chain_type(llm=index,
                                                chain_type=chain_type,
                                                verbose=True,
                                                retriever=vector.db.as_retriever(search_kwargs={"k":5}),
                                                chain_type_kwargs={"verbose": False })
        result = qa_chain({"query": question})
        return result["result"]

