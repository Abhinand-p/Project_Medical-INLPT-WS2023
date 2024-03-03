from fastapi import Body, APIRouter
from .pipeline_modules import azure_config, chatGPT_config, llama7b_config, openSearchClient, embedding_config, vector_store, retrievalqa
router = APIRouter()

#------------Initialize Pipeline Modules------------

# Generation
gpt3 = chatGPT_config.GPTManager()
# llama7b = llama7b_config.LlamaManager()
azure = azure_config.AzureManager()
retrievalQA = retrievalqa.RetrievalQAManager()

# Vector Store
vector = vector_store.VectorStoreManager()

# Retrieval
openSearch = openSearchClient.OpenSearchManager()

# Embedding
embed = embedding_config.EmbeddingManager()

#------------Configuration Options------------
llm_list = ["GPT 3.5 Turbo 0125", "LLAMA-2-7b-chat-hf", "Azure-Biobert-Pubmed-QA", "Conversational GPT 3.5 Turbo 0125"]
retrieval_list = ["Dense Retrieval", "Sparse Retrieval", "Hybrid Search"]
chain_types = ["stuff", "refine", "map_reduce", "map_re_rank"]


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

@router.get("/getChainTypes")
def getChainTypes():
  return chain_types

@router.post("/pipeline")
def get_answer_from_pipeline(question: str= Body(..., embed=True), retrieval_strategy:str= Body(..., embed=True),
                             index:str= Body(..., embed=True),llm:str= Body(..., embed=True), citation:str= Body(..., embed=True),
                             qt:str= Body(..., embed=True), chain_type:str= Body(..., embed=True)):

  checking_availability, err = vector.update_index_model(index)
  if checking_availability == False:
    return err

  # Query Transformation
  if qt == "true":
    # Perform Query Transformation
    query_transform_questions = gpt3.queryTransformation(question, vector)

    for generated_query in query_transform_questions:
      # Embed the query transformed question
      embedded_query = embed.controller(generated_query, retrieval_strategy, index)

      # Retrieve the data for the query transformed question with a retrieval strategy
      context += openSearch.controller(retrieval_strategy, embedded_query, question, index) + ". " # Concatenate the context for each query transformed question
  else:
    #Embed query
    embedded_query = embed.controller(question, retrieval_strategy, index) # Index corresponds to the vector space in opensearch since we have one index per embedding model

    #Retrieve Data
    context, source = openSearch.controller(retrieval_strategy, embedded_query, question, index)

  #Generate Answer based on requested LLM
  if llm == llm_list[0]:
    answer = gpt3.query(question, context)

  # elif llm == llm_list[1]:
  #   answer = llama7b.query(question, context)

  elif llm == llm_list[2]:
    answer = azure.query(question, context)

  elif llm == llm_list[3]:
    answer = retrievalQA.conversationalRetrievalChain(question, vector, chain_type=chain_type)

  # Send Citation
  if citation == "true":
    answer = f"{answer} (Citation: {source})"

  return answer

