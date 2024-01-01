from typing import Union
from fastapi import Body
from fastapi import Header, APIRouter
#from api import db_manager
from faunadb import query as q
from faunadb.client import FaunaClient
from api import pineconeClient
from sentence_transformers import SentenceTransformer

router = APIRouter()


# @router.get('')
# async def get_text(lang: str, section: str, key: str):
# return await dm_manager.get_language(lang, section, key)


# @router.post('', status_code=201)
# async def set_text(lang: str, section: str, key: str, value: str):
#    return await dm_manager.set_language(lang, section, key, value)


#Initialize FaunaDB
client = FaunaClient(
  secret="fnAFVGT2DnAAzKCbNx04jSXn6UGEmjU2xheJIW9e",
)

#DOWNLOAD embedding model
embedding_model = SentenceTransformer('pritamdeka/S-PubMedBert-MS-MARCO')

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