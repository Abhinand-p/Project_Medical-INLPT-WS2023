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
        #If more than two different prompt msg is needed, implement dictionary
        system_prompt1 = "You are a researcher on Medical Intelligence, that can answer questions based on the provided articles."
        system_prompt2 = "You are a friendly Assistant that will answer Questions based on given Contexts."
        user_prompt1 = f"1- Answer the question with the regarding all chunked Contexts.2- If there are more than one answer provide all of them with resources.\n 3- If it is not possible to answer based on given contexts, Explicitly say that and answer based on your knowledge.\n4- provide the resources for each chunk at the end of your message.\n 5- If there is previous answers from you use them as well with reference \nQuestion:\n{question} \nContexts:\n{context}"
        user_prompt2 = f"Answer the following question: {question} based on the following chunked texts: {context}. 1- If there is no answer based on provided texts, just say 'I cannot provide an answer based on the provided text.'"

        # Check if the question or context is empty
        if len(question) == 0 or len(context) == 0:
            pass
        else:
            self.messages  = [
            SystemMessage(content=system_prompt1),
        ]
            # Augment the prompt with the question and context
            augmented_prompt = user_prompt1
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
