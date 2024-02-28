from langchain_openai import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
from dotenv import load_dotenv
import os

class GPTManager:

    def __init__(self): 
        load_dotenv()
        self.chat = ChatOpenAI(
            openai_api_key= os.getenv("OPENAI_API_KEY"),
            model='gpt-3.5-turbo-0125'
        )

        self.messages  = [
            SystemMessage(content="You are a friendly Assistant that will answer Questions"),
        ]
        

    def query(self, question, context):
        print("###########  LLM: GPT")
        augmented_prompt = f"""Answer the question with the given Contexts. If the contexts can't answer the question explicitly say so and answer the question with your own knowledge.:
        Query: {question}
        Contexts:
        {context}"""
  
        #ToDo: Check Size of messages so we dont exceed conext window of 16835 tokens
        #Naive approach; keep mesages in memory shorter than 3
        #if(len(self.messages) > 4):
        #    self.messages.pop(1)

        self.messages.append(
            HumanMessage(
                content=augmented_prompt
            ))

        answer = self.chat(self.messages).content

        self.messages.append(
            AIMessage(
                content=answer
            ))

        return answer
