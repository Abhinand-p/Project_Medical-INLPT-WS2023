""" This module is responsible for the configuration of the GPT-3.5 model. It is used to query the model with a question and a context.
 The model will then return an answer to the question. """

from langchain_openai import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
from dotenv import load_dotenv
import os
from utils import Utils

class GPTManager:

    def __init__(self): 
        load_dotenv()
        self.utils = Utils()
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key is None:
            raise ValueError("OPENAI_API_KEY is not set")
        else:
            self.chat = ChatOpenAI(
                openai_api_key= api_key,
                model='gpt-3.5-turbo-0125'
            )

        self.messages  = []
        self.history = []

    def query(self, question, context):
        print("###########  LLM: GPT")
        # Check if the question or context is empty
        if len(question) == 0 or len(context) == 0:
            pass
        else:
            self.messages  = [
            SystemMessage(content="You are a friendly Assistant that will answer Questions based on given Contexts."),
        ]
            # Augment the prompt with the question and context
            augmented_prompt = f"1- Answer the question with the given Contexts.2- If it is not possible to answer based on given contexts, use the the following template and answer based on your knowledge.\n ``` There is no such data on provided Articles, However, based on my knowledge, I can say that... \n 3- If there are previous conversations use them as well. ``` \nQuestion:\n{question} \nContexts:\n{context}"
            self.history.append(question)
        #ToDo: Check Size of messages so we dont exceed conext window of 16835 tokens
        #Naive approach; keep mesages in memory shorter than 3
        #if(len(self.messages) > 4):
        #    self.messages.pop(1)

            self.messages.append(
                HumanMessage(
                    content=augmented_prompt
                ))
            #Check if GPT-3.5 cannot find any data on the given context, then do not add it to the history
            answer = self.chat(self.messages).content
            if not self.utils.extract_context(AIMessage(content=answer)):
                self.history.append(AIMessage(content=answer))
                self.utils.save_conversation(self.history)
                # self.messages.append(
                #     SystemMessage(
                #         content = answer
                #     ))
                self.messages.append(
                AIMessage(
                    content=answer
                ))
                return answer
            else:
                pass
