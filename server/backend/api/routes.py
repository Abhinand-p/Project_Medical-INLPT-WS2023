from typing import Union
from fastapi import Body, APIRouter, HTTPException
#from api import db_manager
from faunadb import query as q
from faunadb.client import FaunaClient
from api import pineconeClient
from sentence_transformers import SentenceTransformer
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
router = APIRouter()


# @router.get('')
# async def get_text(lang: str, section: str, key: str):
# return await dm_manager.get_language(lang, section, key)


# @router.post('', status_code=201)
# async def set_text(lang: str, section: str, key: str, value: str):
#    return await dm_manager.set_language(lang, section, key, value)


#Initialize FaunaDB
client = FaunaClient(
  secret="fnAFXCXwtRAAzbZaH3YURuEnoGu7Np6vhjhnl5Tp",
)

#DOWNLOAD embedding model
embedding_model = SentenceTransformer('intfloat/e5-large-v2')

#Initialize pinecone manager
pineconeOps = pineconeClient.PineconeOperations()

@router.post("/questions-answering")
async def create_index(text: str = Body(..., embed=True)):
    """ Workflow:
    1. Embedd question which is the text attribute
    2. Query most relevant abstract with Pinecone + FaunaDB
    ------ToDo------
    3. Put abstract_text into model function
    """
    
    embedded_question = embedding_model.encode(text).tolist()
    
    abstractId = pineconeOps.query(query_vector=embedded_question)["matches"][0]["id"]
    abstract_text = client.query(
        q.paginate(q.match(q.index("metadata"), abstractId)))
    
    """ToDo: """
    
    
    return abstract_text["data"][0]
  
@router.post("/healthcheck")
async def mirror(text: str = Body(..., embed= True)):
  return text
  
  
  
"""1. Attempt for prototype: local approach"""


chat = ChatOpenAI(
    openai_api_key= "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",
    model='gpt-3.5-turbo'
)

@router.post("/get-answer-from-local")
def get_answer(question: str= Body(..., embed=True)):
  """ Workflow:
  1. Embedd question which is the text attribute
  2. Query most relevant abstract with Pinecone + FaunaDB
  3. Create the prompt, put together context (abstract_text), prompt command (SystemMessage) and User query (HumanMessage)
  4. Query prompt to LLM and return the answer
  """ 
  embedded_question = embedding_model.encode(question).tolist()
  abstractId = pineconeOps.query(query_vector=embedded_question)["matches"][0]["id"]
  abstract_data = client.query(
    q.paginate(q.match(q.index("metadata"), abstractId))) 
  abstract_text = abstract_data["data"][0][1] + abstract_data["data"][0][0] + abstract_data["data"][0][2]
  print(abstract_text)
  messages = [
    SystemMessage(content="Try to answer the question with the given context, if the answer lies not in the context say so but still try to answer the question"),
    ]
  augmented_prompt = f"""Using the contexts below, answer the query.
  Contexts:
  {abstract_text}
  Query: {question}"""
  prompt = HumanMessage(
    content=augmented_prompt
  )
  messages.append(prompt)
  res = chat(messages)
    
  return res.content
  