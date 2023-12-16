from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body
'''couldnt find the install for this so i commented it out for now'''
#from backend.api.router import router
from sentence_transformers import SentenceTransformer
from api import pineconeClient
from typing import List, Tuple, Any
from pydantic.main import BaseModel

app = FastAPI()

origins = ["*"]

#app.include_router(router)

#Initialize FaunaDB
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient

client = FaunaClient(
  secret="fnAFVGT2DnAAzKCbNx04jSXn6UGEmjU2xheJIW9e",
)


#embed data
model = SentenceTransformer('pritamdeka/S-PubMedBert-MS-MARCO')

pineconeOps = pineconeClient.PineconeOperations()

@app.get("/api/v1/health")
async def root():
    return {"message": "OK"}

@app.get("/api/v1/index/stats")
async def stats():
    return pineconeOps.fetch_stats()

text: str = Body(..., embed=True)
@app.post("/api/v1/search-vector")
async def create_index(text: str = Body(..., embed=True)):
    #Embedd query into vector
    test = model.encode(text).tolist()
    #Get id of nearest vector from VectorDB
    abstractId = pineconeOps.query(query_vector=test)["matches"][0]["id"]
    #Query abstract with resective id
    result = client.query(
        q.paginate(q.match(q.index("metadata"), abstractId)))
    
    return result["data"][0]

