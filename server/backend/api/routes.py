from typing import Union
from opensearchpy import OpenSearch
from fastapi import Body, APIRouter, HTTPException
#from api import db_manager
from faunadb import query as q
from faunadb.client import FaunaClient
from api import pineconeClient
from sentence_transformers import SentenceTransformer
import os
from .model import get_data
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

#DOWNLOAD embedding model
embedding_model = SentenceTransformer('intfloat/e5-large-v2')

#Initialize FaunaDB
client = FaunaClient(
  secret="fnAFXCXwtRAAzbZaH3YURuEnoGu7Np6vhjhnl5Tp",
)

#Initialize pinecone manager
pineconeOps = pineconeClient.PineconeOperations()

@router.post("/healthcheck")
async def mirror(text: str = Body(..., embed= True)):
  return text

"""0. Attempt for prototype: Azure Endpoint approach"""

# Embedding model: Local intfloat/e5-large-v2
# IR: Cloud Pinecone + FaunaDB
# LLM: Cloud biobert-pubmed-qa
@router.post("/get-answer-from-model")
def get_answer_1(question: str= Body(..., embed=True)):
  """ Workflow:
  1. Embedd question which is the text attribute
  2. Query most relevant abstract with Pinecone + FaunaDB
  3. Create the prompt, put together context (abstract_text), prompt command (SystemMessage) and User query (HumanMessage)
  4. Query prompt to LLM and return the answer
  """
  # 1. Embedding the retrieved question from frontend
  embedded_question = embedding_model.encode(question).tolist()
  # 2. Query most relevant abstract with Pinecone
  abstracts = pineconeOps.query(query_vector=embedded_question)
  context = ""
  check_prompt_size = 0
  #Query metadata of top 3 chunks, check if returned chunks exceed input limit or not
  def queryMetaData(abstractId, check_prompt_size):
    abstract_data = client.query(q.paginate(q.match(q.index("metadata"), abstractId)))
    chunk_with_local_context = abstract_data["data"][0][1] + abstract_data["data"][0][0] +abstract_data["data"][0][2]
    check_prompt_size += len(chunk_with_local_context.split())
    if(check_prompt_size < model_max_input + len(question.split())):
      return (chunk_with_local_context,check_prompt_size )
    else:
      print("Prompt exceeded models max input size!")
      return "","" # in case of prompt size exceeded, return empty string

  for id, abstract in enumerate(abstracts["matches"]):
    data = queryMetaData(abstract["id"],check_prompt_size)
    check_prompt_size += data[1]
    print(check_prompt_size)

    context = context + f"""Chunk {id}: {data[0]}"""

  print(context)
  res = get_data(question, context)

  return res

"""1. Attempt for prototype: local approach"""

chat = ChatOpenAI(
    openai_api_key= "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",
    model='gpt-3.5-turbo'
)
model_max_input = 4096

# Embedding model: Local intfloat/e5-large-v2
# IR: Cloud Pinecone + FaunaDB
# LLM: Cloud GPT 3.5 Turbo
@router.post("/get-answer-from-local")
def get_answer_2(question: str= Body(..., embed=True)):
  """ Workflow:
  1. Embedd question which is the question attribute
  2. Query most relevant abstract with Pinecone + FaunaDB
  3. Create the prompt, put together context (abstract_text), prompt command (SystemMessage) and User query (HumanMessage)
  4. Query prompt to LLM and return the answer
  """
  embedded_question = embedding_model.encode(question).tolist()
  abstracts = pineconeOps.query(query_vector=embedded_question)
  context = ""
  check_prompt_size = 0
  #Query metadata of top 3 chunks, check if returned chunks exceed input limit or not
  def queryMetaData(abstractId, check_prompt_size):
    abstract_data = client.query(
    q.paginate(q.match(q.index("metadata"), abstractId)))
    chunk_with_local_context = abstract_data["data"][0][1] + abstract_data["data"][0][0] +abstract_data["data"][0][2]
    check_prompt_size += len(chunk_with_local_context.split())
    if(check_prompt_size < model_max_input + len(question.split())):
      return (chunk_with_local_context,check_prompt_size )
    else:
      print("Prompt exceeded models max input size!")
      return ""

  # check if returned chunks exceed input limit or not
  for id, abstract in enumerate(abstracts["matches"]):
    data = queryMetaData(abstract["id"],check_prompt_size)
    check_prompt_size += data[1]

    context = context + f"""Chunk {id}: {data[0]}"""

  print(context)

  #Use GPT 3.5 Turbo to generate the answer
  messages = [
    SystemMessage(content="You are a friendly assistant that will answer questions"),
    ]

  augmented_prompt = f"""Try to to answer the question with the Chunks. The the chunks dont provide information to answer explictily say so. Answer the question with your own knowledge.
  Contexts:
  {context}
  Query: {question}"""
  prompt = HumanMessage(
    content=augmented_prompt
  )
  messages.append(prompt)
  res = chat(messages)

  return res.content


"""2. Attempt for prototype: local approach"""

#Initialize connection to opensearch
host = 'localhost'
port = 9200
auth = ('admin', 'admin')

client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_auth = auth,
    use_ssl = True,
    verify_certs = False,
    timeout=100
)
#check status
print(client.info())

# Embedding model: Local intfloat/e5-large-v2
# IR: Local openSearch
# LLM: Cloud GPT 3.5 Turbo
@router.post("/get-answer-from-local-openSearch")
def get_answer_3(question: str= Body(..., embed=True)):
  """ Workflow:
  1. Embedd question which is the question attribute
  2. Query most relevant abstract from open Search
  3. Create the prompt, put together context (abstract_text), prompt command (SystemMessage) and User query (HumanMessage)
  4. Query prompt to LLM and return the answer
  """
  # First thing is to use Query Transformation to create better queries from the LLM
  
  
  embedded_question = embedding_model.encode(question).tolist()

  knn_search_body = {
    "size": 5,  # Number of nearest neighbors to retrieve
    "query": {
        "knn": {
            "vector": {
                "vector": embedded_question,
                "k": 3  # Number of nearest neighbors to retrieve
                }
            }
          }
        }
  # Execute the search
  response = client.search(index="med_data", body=knn_search_body)

  # Extract the relevant information from the response
  context = ""
  hits = response['hits']['hits']
  for id, hit in enumerate(hits): # fixing the id from built-in to retrieve it back from the enumerate
    source = hit['_source']
    context = context + f"""Chunk {id}: {source['text'][0]}"""
    print(f"Score: {hit['_score']}, Text: {source['text']}")

  #Use GPT 3.5 Turbo to generate the answer
  messages = [
    SystemMessage(content="You are a friendly assistant that will answer questions"),
    ]

  augmented_prompt = f"""Try to to answer the question with the Chunks. The the chunks dont provide information to answer explictily say so. Answer the question with your own knowledge.
  Contexts:
  {context}
  Query: {question}"""
  prompt = HumanMessage(
    content=augmented_prompt
  )
  messages.append(prompt)
  res = chat(messages)

  return res.content


