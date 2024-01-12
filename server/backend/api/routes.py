from typing import Union
from fastapi import Body, APIRouter
from opensearchpy import OpenSearch
#from api import db_manager
from faunadb import query as q
from faunadb.client import FaunaClient

from sentence_transformers import SentenceTransformer
import os
#from model import get_data
from langchain.chat_models import ChatOpenAI
router = APIRouter()


# @router.get('')
# async def get_text(lang: str, section: str, key: str):
# return await dm_manager.get_language(lang, section, key)


# @router.post('', status_code=201)
# async def set_text(lang: str, section: str, key: str, value: str):
#    return await dm_manager.set_language(lang, section, key, value)

@router.post("/healthcheck")
async def mirror(text: str = Body(..., embed= True)):
  return text

#DOWNLOAD embedding model
embedding_model = SentenceTransformer('intfloat/e5-small-v2')

@router.post("/questions-answering")
def get_answer_1(question: str= Body(..., embed=True)):
  """ Workflow:
  1. Embedd question which is the text attribute
  2. Query most relevant abstract with Pinecone + FaunaDB
  3. Create the prompt, put together context (abstract_text), prompt command (SystemMessage) and User query (HumanMessage)
  4. Query prompt to LLM and return the answer
  """ 
    
  return question
  
"""1. Attempt for prototype: local approach"""

#Initialize connection to opensearch
host = 'localhost'
port = 9200
auth = ('admin', 'admin') 

openSearch_client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_auth = auth,
    use_ssl = True,
    verify_certs = False
)
#check status
info = openSearch_client.info()

chat = ChatOpenAI(
    openai_api_key= "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",
    model='gpt-3.5-turbo'
)

model_max_input = 4096

@router.post("/get-answer-from-local")
def get_answer(question: str= Body(..., embed=True)):
  """ Workflow:
  1. Embedd question which is the text attribute
  2. Query most relevant abstract with Pinecone + FaunaDB
  3. Create the prompt, put together context (abstract_text), prompt command (SystemMessage) and User query (HumanMessage)
  4. Query prompt to LLM and return the answer
  """ 
  embedded_question = embedding_model.encode(question).tolist()
  
  query={"size": 1, "query":{"knn":{"vector":{"vector": embedded_question, "k": 1}}}}
  
  response = openSearch_client.search(
    body = query,
    index = "med_data"
  )
  
  print(response["hits"]["hits"][0]["_source"]["txt"])
  
  return response["hits"]["hits"][0]["_source"]["txt"]
