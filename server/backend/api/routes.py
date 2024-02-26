from opensearchpy import OpenSearch
from fastapi import Body, APIRouter
from sentence_transformers import SentenceTransformer
#from .model import get_data
from langchain_openai import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
)
import voyageai
import openai
router = APIRouter()

#####################EMBEDDING###########################
chat = ChatOpenAI(
    openai_api_key= "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",
    model='gpt-3.5-turbo'
)

voyageai.api_key =  "pa-3xpcuUhVVgmOQPDBiG7ObYUA58rGn1eB1ZMaowr5xy0" 
vo = voyageai.Client()

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

llm_list = ["GPT 3.5 Turbo 0125", "LLAMA-2-7b-chat-hf"]
index_list = ["voyage-2-large", "text-embedding-3-large"]
retrieval_list = ["Dense Retrieval", "Sparse Retrieval" "Hybrid Search"]

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


@router.post("/get-answer-from-local-openSearch")
def get_answer_3(question: str= Body(..., embed=True), retrieval_strategy:str= Body(..., embed=True), 
                 index:str= Body(..., embed=True),llm:str= Body(..., embed=True)):

  
  #Select correct embedding
  if index == "voyage-2-large":
    embedding =  vo.embed(question, model="voyage-large-2", input_type="document").embeddings
  elif index == "text-embedding-3-large":
    response = openai.Embedding.create(
        engine="text-embedding-3-large",
        input=question,
        dimensions = 1024
    )
    embedding = response["data"]["embedding"]

  
  
  #Select correct retrieval strategy
  if retrieval_strategy == "Dense Retrieval":
    knn_search_body = {
      "size": 5,  # Number of nearest neighbors to retrieve
      "query": {
          "knn": {
              "vector": {
                  "vector": embedding,
                  "k": 3  # Number of nearest neighbors to retrieve
                  }
              }
            }
          }
    # Execute the search
    response = client.search(index="index", body=knn_search_body)

  elif retrieval_strategy == "Sparse Retrieval":
    text_search_body = {
      "size": 53, 
      "explain": True,
      "query": {
          "match": {
              "text": question  
          }
      }
    }

    response = client.search(index="index", body=text_search_body)
  
  elif retrieval_strategy == "Hybrid Search":
    
    route = f"/{index}/_search?search_pipeline=nlp_search-pipeline"
    hybrid_search_body = {
      "_source": {
        "exclude": [
          "vector"
        ]
      },
      "query": {
        "hybrid": {
          "queries": [
            {
              "match": {
                "text": {
                  "query": question
                }
              }
            },
            {
              "knn": {                 
                "vector": {
                  "vector": embedding,
                  "k": 5
                }
              }
            }
          ]
        }
      }
    }

    response  = client.transport.perform_request(method = "GET", url = route, body = hybrid_search_body) 

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


