from fastapi import Body, APIRouter
from .pipeline_modules import azure_config, chatGPT_config, llama7b_config, openSearchClient, embedding_config, vector_store, retrievalqa
from opensearchpy import OpenSearch

router = APIRouter()

#------------Initialize Pipeline Modules------------

# Generation
gpt3 = chatGPT_config.GPTManager()
#llama7b = llama7b_config.LlamaManager()
azure = azure_config.AzureManager()
retrievalQA = retrievalqa.RetrievalQAManager()

# Vector Store
vector = vector_store.VectorStoreManager()

# Retrieval
openSearch = openSearchClient.OpenSearchManager()

# Embedding
embed = embedding_config.EmbeddingManager()

#------------Configuration Options------------
llm_list = ["GPT 3.5 Turbo 0125", "GPT 3.5 Turbo 0125 (Langchain)", "LLAMA-2-7b-chat-hf", "Azure-Biobert-Pubmed-QA"]
retrieval_list = ["Dense Retrieval", "Sparse Retrieval", "Hybrid Search"]
chain_types = ["stuff", "refine", "map_reduce", "map_rerank"]


#------------Routes------------
@router.post("/healthcheck")
async def mirror(text: str = Body(..., embed= True)):
  return text

@router.get("/getOpenSearchIndices")
def getIndices():
  #Filter out default Indices that are always present
  defaultIndices = set( [".plugins-ml-config",".opensearch-observability",".opensearch-sap-log-types-config",".opendistro_security", ".kibana_1", "sophiaqho-boolq_finetuned_on_pubmed"])
  allIndices = openSearch.getAllIndices()

  filtered_list = [item for item in allIndices if item not in defaultIndices]

  #Filter out security logs
  filtered_list = [string for string in filtered_list if "security" not in string]
  return filtered_list

@router.get("/status")
def status():
  #Initialize connection to opensearch
  host = 'opensearch-node1'
  # port = 9200
  auth = ('admin', '!akjdaDsdoij!oijadSsajd123120938')

  client = OpenSearch(
      hosts = [{'host': host}],
      http_auth = auth,
      use_ssl = True,
      verify_certs = False,
      timeout=100
  )
  #check status
  print(client.info())
  return client.info()

@router.get("/getLLMs")
def getLLM():
  return llm_list

@router.get("/getRetrievalStrategy")
def getRetrieval():
  return retrieval_list

@router.get("/getChainTypes")
def getChainTypes():
  return chain_types

@router.get("/testAzure")
def testAzure():
  return azure.azure_status()

@router.post("/pipeline")
def get_answer_from_pipeline(question: str= Body(..., embed=True), retrieval_strategy:str= Body(..., embed=True),
                             index:str= Body(..., embed=True),llm:str= Body(..., embed=True), QueryTransformation:str= Body(..., embed=True),chainType:str= Body(..., embed=True)):

  #Check Config
  print(f"##### \n Configuration: \n Retrieval:{retrieval_strategy} \n LLM:{llm} \n Embedding: {index} \n QueryTransformation: {QueryTransformation} \n ChainType: {chainType}\n#####" )

  checking_availability, err = vector.update_index_model(index)
  if checking_availability == False:
    return err

  # Query Transformatio
  if QueryTransformation == "true":
    # Perform Query Transformation
    query_transform_questions = gpt3.queryTransformation(question, vector)
    context = ""
    embedded_query = ""
    for generated_query in query_transform_questions:
      # Embed the query transformed question (but not if we chose sparse retrieval)
      
      if(retrieval_strategy != "Sparse Retrieval"):
        embedded_query = embed.controller(generated_query, retrieval_strategy, index)

      # Retrieve the data for the query transformed question with a retrieval strategy
        res = openSearch.controller(retrieval_strategy, embedded_query, question, index)[0]["context"]
        print(res)
      context +=res + ". " # Concatenate the context for each query transformed question
  else:
    #Embed query
    embedded_query = embed.controller(question, retrieval_strategy, index) # Index corresponds to the vector space in opensearch since we have one index per embedding model

    #Retrieve Data
    context = openSearch.controller(retrieval_strategy, embedded_query, question, index)

  #Generate Answer based on requested LLM
  if llm == llm_list[0]:
    answer = gpt3.query(question, context)

  elif llm == llm_list[1]:
    answer = retrievalQA.query(question, vector, chainType)

  # elif llm == llm_list[2]:
  #   answer = llama7b.query(question, context)

  elif llm == llm_list[3]:
    answer = azure.query(question, context)

  return answer

