""" This module is responsible for the configuration of the GPT-3.5 model. It is used to query the model with a question and a context.
 The model will then return an answer to the question. """

import string
from langchain_openai import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
from dotenv import load_dotenv
import os
from utils import Utils

systemPrompts = {
    "system_prompt1" : "You are a researcher on Medical Intelligence, that can answer questions based on the provided articles.",
    "system_prompt2" : "You are a friendly Assistant that will answer Questions based on given Contexts."
}

class GPTManager:

    def __init__(self):
        load_dotenv()
        self.utils = Utils()
        api_key = "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" # os.getenv("OPENAI_API_KEY")
        if api_key is None:
            raise ValueError("OPENAI_API_KEY is not set")
        else:
            self.chat = ChatOpenAI(
                api_key=api_key,
                model='gpt-3.5-turbo-0125'
            )

            # self.chain = RetrievalQA.from_chain_type(self.chat, retriever=vectorstore.as_retriever(), chain_type_kwargs={"prompt": prompt})

        self.messages  = [SystemMessage(systemPrompts["system_prompt1"])]
        self.history = []

    def query(self, question, context):
        print("###########  LLM: GPT")
        #If more than two different prompt msg is needed, implement dictionary
        user_prompt1 = f"1- Answer the question with the regarding all chunked Contexts.2- If there are more than one answer provide all of them with resources.\n 3- If it is not possible to answer based on given contexts, Explicitly say that and answer based on your knowledge.\n4- provide the resources for each chunk at the end of your message.\n 5- If there is previous answers from you use them as well with reference \nQuestion:\n{question} \nContexts:\n{context}"
        user_prompt2 = f"Answer the following question: {question} based on the following chunked texts: {context}. 1- If there is no answer based on provided texts, just say 'I cannot provide an answer based on the provided text.'"
        user_prompt3 = f"1- Answer the question with the given Contexts 2. If there is no Context try to answer the question with the previous messages 3. For each Context that you used for the answer, get its source and append it to your answer  3. If the user specifically asks something about a answer you gave in the past, do so and ignore the context 3. \n If it is not possible to answer based on given texts, Explicitly say that and answer based on your knowledge. \nQuestion:\n{question} \n Contexts:\n{context}"

        # Augment the prompt with the question and contexty

        self.history.append(question)

        self.messages.append(
            HumanMessage(
                content=user_prompt3
            ))
        #Check if GPT-3.5 cannot find any data on the given context, then do not add it to the history
        answer = self.chat(self.messages).content
        if not self.utils.extract_context(answer):
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
            print(self.messages)
            #Make sure Hat history wont get too big
            self.chatHistoryHousekeeping()
            return answer
        else:
            pass

            #Make sure chat history wont ge too big
    def chatHistoryHousekeeping(self):
        if len(self.messages) == 5:
            self.messages.pop(1)
            self.messages.pop(1)

        for id ,message in enumerate(self.messages):
            if type(message) == HumanMessage:
                message_content =message.content
                last_contexts_index = message_content.rfind("Contexts")

                if last_contexts_index != -1:
                    result = message_content[:last_contexts_index]
                    cut_off = message_content[last_contexts_index:]
                else:
                    result = message_content
                    cut_off = ""

                answer = self.chat([HumanMessage(f"Summarize each Context into a few sentences: {cut_off}")]).content #tldr

                newHumanMessage = result + " " + answer

                self.messages[id] = HumanMessage(newHumanMessage)
