from opensearchpy import OpenSearch
from fastapi import Body, APIRouter
from sentence_transformers import SentenceTransformer
#from .model import get_data
from langchain_openai import ChatOpenAI, OpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
)
import voyageai
import openai
router = APIRouter()
from torch import bfloat16 
import transformers
from transformers import LlamaTokenizer
import os
from langchain.llms import HuggingFacePipeline 
from openai import OpenAI

##################LLM#######################
model_id = 'meta-llama/Llama-2-7b-chat-hf' #'HuggingFaceH4/zephyr-7b-alpha' 
hf_auth = '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' 
os.environ['OPENAI_API_KEY'] = "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"

bnb_config = transformers.BitsAndBytesConfig( load_in_4bit=True, 
                                             bnb_4bit_quant_type='nf4',
                                             bnb_4bit_use_double_quant=True, 
                                             bnb_4bit_compute_dtype=bfloat16 ) # begin initializing HF items, need auth token for these 

model_config = transformers.AutoConfig.from_pretrained( model_id, token=hf_auth )

model = transformers.AutoModelForCausalLM.from_pretrained(model_id, 
                                                          trust_remote_code=True,
                                                          config=model_config,
                                                          quantization_config=bnb_config,
                                                          device_map="auto",
                                                          token=hf_auth ) 

tokenizer = LlamaTokenizer.from_pretrained("meta-llama/Llama-2-13b-chat-hf",token=hf_auth)

generate_text = transformers.pipeline( model=model, tokenizer=tokenizer,
                                      return_full_text=True, # langchain expects the full text
                                      task='text-generation', # we pass model parameters here too 
                                      max_new_tokens=512,
                                      repetition_penalty=1.1, # without this output begins repeating
                                      use_cache=True,
                                     )

llama2_7b = HuggingFacePipeline(pipeline=generate_text)

chat = ChatOpenAI(
    openai_api_key= "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",
    model='gpt-3.5-turbo-0125'
)

#####################EMBEDDING###########################
openAIClient = OpenAI()

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
retrieval_list = ["Dense Retrieval", "Sparse Retrieval", "Hybrid Search"]

@router.post("/healthcheck")
async def mirror(text: str = Body(..., embed= True)):
  return text

@router.get("/getOpenSearchIndices")
def getIndices():
  filterOut = [".plugins-ml-config",".opensearch-observability",".opensearch-sap-log-types-config",
               ".opendistro_security"]
  
  res = client.indices.get_alias().keys()
  indices = []
  for index in res:
    indices.append(index)

  set2 = set(filterOut)
  filtered_list1 = [item for item in indices if item not in set2]

  return filtered_list1

@router.get("/getLLMs")
def getLLM():
  return llm_list

@router.get("/getRetrievalStrategy")
def getRetrieval():
  return retrieval_list


@router.post("/pipeline")
def get_answer_from_pipeline(question: str= Body(..., embed=True), retrieval_strategy:str= Body(..., embed=True), 
                 index:str= Body(..., embed=True),llm:str= Body(..., embed=True), citation:str= Body(..., embed=True)):

  
  #Select correct embedding
  if retrieval_strategy != "Sparse Retrieval" : 
    if index == "voyage-2-large":
      embedding =  vo.embed(question, model="voyage-large-2", input_type="document").embeddings[0]
      print("---------------------------voyage-2-large:", embedding)
    elif index == "text-embedding-3-large":
      response = openAIClient.embeddings.create(
          model="text-embedding-3-large",
          input=question,
          dimensions = 1024
      )
      embedding = response.data[0].embedding
      print("---------------------------text-embedding-3-large:", embedding)

  
  
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
    response = client.search(index=index, body=knn_search_body)

  elif retrieval_strategy == "Sparse Retrieval":
    text_search_body = {
      "query": {
          "match": {
              "text": question  
          }
      }
    }

    response = client.search(index=index, body=text_search_body)
  
  elif retrieval_strategy == "Hybrid Search":
    print("######HYBRIDHYBRIDHYBRID")
    
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
  cite = ""
  hits = response['hits']['hits']
  for id, hit in enumerate(hits[:3]): # fixing the id from built-in to retrieve it back from the enumerate
    source = hit['_source']
    context = context + f"""Chunk {id}: {source['text']}"""
    print(f"Score: {hit['_score']}, Text: {source['text']}")

  #Select correct LLM
  if llm == "GPT 3.5 Turbo 0125":
    messages = [
      SystemMessage(content="You are a friendly assistant that will answer questions"),
      ]

    augmented_prompt = f"""Try to to answer the question with the Chunks. Dont say you tok the information from the chunks unless they dont provide information to answer, in that case explictily say so and answer the question with your own knowledge.
    Contexts:
    {context}
    Query: {question}"""
    prompt = HumanMessage(
      content=augmented_prompt
    )
    messages.append(prompt)
    res = chat(messages)
    res = res.content
  elif llm ==  "LLAMA-2-7b-chat-hf":
    print("### LLAMA 2 Answer:")
    prompt = f"""Try to to answer the question with the Chunks. If the chunks dont provide information to answer explictily say so and answer the question with your own knowledge.
    Contexts:
    {context}
    Query: {question}"""
    res = llama2_7b(prompt)

  if citation == "true":
    cite = f" (Citation:{response['hits']['hits'][0]['_source']['cite']})"

  return f"{res} \n \n {cite}"


