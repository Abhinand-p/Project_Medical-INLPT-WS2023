from fastapi import Body, APIRouter
from .pipeline_modules import azure_config, chatGPT_config, llama7b_config, openSearchClient, embedding_config
router = APIRouter()

#------------Initialize Pipeline Modules------------

# Generation
gpt3 = chatGPT_config.GPTManager()
#llama7b = llama7b_config.LlamaManager()
azure = azure_config.AzureManager()

# Retrieval
openSearch = openSearchClient.OpenSearchManager()

# Embedding
embed = embedding_config.EmbeddingManager()


#------------Configuration Options------------
llm_list = ["GPT 3.5 Turbo 0125", "LLAMA-2-7b-chat-hf", "Azure-QA-Conversational"]
retrieval_list = ["Dense Retrieval", "Sparse Retrieval", "Hybrid Search"]


#------------Routes------------
@router.post("/healthcheck")
async def mirror(text: str = Body(..., embed= True)):
  return text


@router.get("/getOpenSearchIndices")
def getIndices():
  #Filter out default Indices that are always present
  defaultIndices = set( [".plugins-ml-config",".opensearch-observability",".opensearch-sap-log-types-config",".opendistro_security"])
  allIndices = openSearch.getAllIndices()
  filtered_list = [item for item in allIndices if item not in defaultIndices]
  #Filter out security logs
  filtered_list = [string for string in filtered_list if "security" not in string]
  return filtered_list

@router.get("/getLLMs")
def getLLM():
  return llm_list

@router.get("/getRetrievalStrategy")
def getRetrieval():
  return retrieval_list

@router.post("/pipeline")
def get_answer_from_pipeline(question: str= Body(..., embed=True), retrieval_strategy:str= Body(..., embed=True),
                 index:str= Body(..., embed=True),llm:str= Body(..., embed=True), citation:str= Body(..., embed=True)):

  #Embed query
  embedded_query = embed.controller(question, retrieval_strategy, index) #Index corresponds to embedding model since we have one index per mbedding model

  #Retrieve Data
  context, source = openSearch.controller(retrieval_strategy, embedded_query, question, index)

  #Generate Answer based on requested LLM
  if llm == llm_list[0]:
    answer = gpt3.query(question, context)

 # elif llm == llm_list[1]:
 #   answer = llama7b.query(question, context)

  elif llm == llm_list[2]:
    answer = azure.query(question, context)

  # Send Citation
  if citation == "true":
    answer = f"{answer} (Citation: {source})"

  return answer


