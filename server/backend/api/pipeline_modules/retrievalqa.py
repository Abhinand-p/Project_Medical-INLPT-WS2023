from .vector_store import VectorStoreManager
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import os
class RetrievalQAManager:
    def __init__(self) -> None:
        try:
            api_key = os.getenv("OPENAI_API_KEY") # "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"
            if api_key is None:
                raise ValueError("OPENAI_API_KEY is not set in the environment variables. Please set it and restart the server.")
            else:
                self.llm = ChatOpenAI(api_key=api_key, model='gpt-3.5-turbo-0125')
                self.memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True, output_key='answer')

            self.qa_dict = dict()

        except Exception as varname:
            print(varname)

    def get_qa(self, vector: VectorStoreManager, chain_type):
        if chain_type not in self.qa_dict:
            self.qa_dict[chain_type] = ConversationalRetrievalChain.from_llm(llm=self.llm,
                                                                             retriever=vector.db.as_retriever(search_kwargs={"k":2, "vector_field": "vector"}),
                                                                             chain_type = chain_type,
                                                                             memory=self.memory)
        return self.qa_dict[chain_type]

    # Conversational Retrieval Chain
    def query(self, question, vector: VectorStoreManager, chain_type):

        if chain_type == "":
            chain_type = "stuff"

        qa_conversation = self.get_qa(vector, chain_type)

        result = qa_conversation({"question": question})
        print("result",result)

        return result["answer"]
