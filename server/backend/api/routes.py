from opensearchpy import OpenSearch
from fastapi import Body, APIRouter
from sentence_transformers import SentenceTransformer
#from .model import get_data
from langchain_openai import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
)
router = APIRouter()

#DOWNLOAD embedding model
embedding_model = SentenceTransformer('intfloat/e5-large-v2')

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

#openai config

chat = ChatOpenAI(
    openai_api_key= "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",
    model='gpt-3.5-turbo'
)

@router.post("/healthcheck")
async def mirror(text: str = Body(..., embed= True)):
  return text

@router.get("/getOpenSearchIndices")
def getIndices():
  filterOut = [".kibana_1",".opendistro_security","security-auditlog-2024.02.17",
               ".opensearch-observability", ".plugins-ml-config", "security-auditlog-2024.02.25",
               ".opensearch-sap-log-types-config",
               "security-auditlog-2024.02.19",
               "wmt_voyage-large-2-paragraph",
               "security-auditlog-2024.02.18"]
  
  res = client.indices.get_alias().keys()
  indices = []
  for index in res:
    indices.append(index)

  set2 = set(filterOut)
  filtered_list1 = [item for item in indices if item not in set2]

  return filtered_list1

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


