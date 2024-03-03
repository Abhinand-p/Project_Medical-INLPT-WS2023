""" This module is responsible for the configuration of the GPT-3.5 model. It is used to query the model with a question and a context.
 The model will then return an answer to the question. """

import string
from langchain_openai import ChatOpenAI
from langchain.chat_models import ChatOpenAI as chatAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.retrievers.multi_query import MultiQueryRetriever
from utils import LineList, LineListOutputParser
from langchain.schema import (SystemMessage, HumanMessage, AIMessage)
from dotenv import load_dotenv
import os
from utils import Utils
import logging
import numpy as np
from langchain.chains import RetrievalQA
from .vector_store import VectorStoreManager
import urllib.request
import zipfile

systemPrompts = {
    "system_prompt1" : "You are a researcher on Medical Intelligence, that can answer questions based on the provided articles.",
    "system_prompt2" : "You are a friendly Assistant that will answer Questions based on given Contexts."
}

class GPTManager:

    def __init__(self):
        try:
            load_dotenv()
            self.utils = Utils()
            api_key = os.getenv("OPENAI_API_KEY") # "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"

            if api_key is None:
                raise ValueError("OPENAI_API_KEY is not set in the environment variables. Please set it and restart the server.")
            else:
                self.chat = ChatOpenAI(api_key=api_key, model='gpt-3.5-turbo-0125')

                # Using chatOpenAI model for query transformation
                self.chatAIBot = chatAI(api_key=api_key, model='gpt-3.5-turbo-0125')

                # Using the Glove model for semantic similarity computation of the queries
                self.word_to_vec = self.load_glove_model("glove.6B.50d.txt")

                self.messages  = [SystemMessage(systemPrompts["system_prompt1"])]
                self.history = []

                # Set logging for the queries
                logging.basicConfig()
                self.logger  = logging.getLogger("langchain.retrievers.multi_query")
                self.logger.setLevel(logging.INFO)
                file_handler = logging.FileHandler('logfile.log')
                self.logger.addHandler(file_handler)
        except Exception as varname:
            print(varname)


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

            self.messages.append(AIMessage(content=answer))

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

    # Query Transformation
    def queryTransformation(self, query, vector: VectorStoreManager):
        list_questions = []

        output_parser = LineListOutputParser()

        # Other inputs
        question = "simplify the question"

        QUERY_PROMPT = PromptTemplate(
                input_variables=["question"],
                template="""Can you simplify user question so a ten year old can understand it?
                You are an AI language model assistant. Your task is to generate five
                different versions of the given user question to retrieve relevant documents from a vector
                database. By generating multiple perspectives on the user question, your goal is to help
                the user overcome some of the limitations of the distance-based similarity search.
                Provide these alternative questions separated by newlines.
                Original question: {question}""")

        # Chain
        llm_chain = LLMChain(llm=self.chatAIBot, prompt=QUERY_PROMPT, output_parser=output_parser)

        # Run
        retriever = MultiQueryRetriever(retriever=vector.db.as_retriever(), llm_chain=llm_chain, parser_key="lines")

        # Results
        retriever.get_relevant_documents(query=query)

        # List of questions returned by the LLM
        list_questions = self.query_list()

        # Compute the semantic similarity between the original question and the transformed questions
        selected_questions = []
        for transformed_query in list_questions:
            semantic_similarity_score = self.compute_semantic_similarity(question, transformed_query, self.word_to_vec)
            if(semantic_similarity_score >= 0.7):
                selected_questions.append(transformed_query)

        # Handling the case where no question is returned
        if len(selected_questions) == 0:
            return query

        # Retrive the top 2 questions
        selected_questions = selected_questions[:2]

        return selected_questions

    def query_list(self):
        logfilename = "logfile.log"

        with open(logfilename, "r") as file:
            lines = file.readlines()
            line = lines[-1]
            log_parts = line.split(':')
            message = log_parts[1]
            start_index = message.index("['")
            end_index = message.index("']") + 2
            queries_str = message[start_index:end_index]
            queries_list = eval(queries_str)
        return queries_list

    def load_glove_model(self, glove_file):
        if not os.path.exists(glove_file): # Check if the GloVe embeddings are already downloaded
            # Downloading GloVe embeddings
            print("Downloading GloVe Model")
            self.download_glove_embedding("http://nlp.stanford.edu/data/glove.6B.zip", "glove.6B.zip")

            # Unzip GloVe embeddings
            print("Unzipping GloVe Model")
            self.unzip_file("glove.6B.zip", "./")

        # Load GloVe embeddings
        print("Loading GloVe Model")
        with open(glove_file, 'r', encoding='utf-8') as f:
            word_to_vec = {}
            for line in f:
                values = line.split()
                word = values[0]
                vec = np.array(values[1:], dtype='float32')
                word_to_vec[word] = vec
        print("Done.", len(word_to_vec), " words loaded!")
        return word_to_vec

    def compute_semantic_similarity(self, query, transformed_query, word_to_vec):
        query_embedding = np.mean([word_to_vec[word] for word in query.lower().split() if word in word_to_vec], axis=0)
        transformed_query_embedding = np.mean([word_to_vec[word] for word in transformed_query.lower().split() if word in word_to_vec], axis=0)

        if np.all(np.isnan(query_embedding)) or np.all(np.isnan(transformed_query_embedding)):
            return 0.0

        similarity_score = np.dot(query_embedding, transformed_query_embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(transformed_query_embedding))
        return similarity_score

    # Download GloVe embeddings
    def download_glove_embedding(self, glove_url, glove_file):
        urllib.request.urlretrieve(glove_url, glove_file)

    def unzip_file(self, zip_path, extract_path):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
