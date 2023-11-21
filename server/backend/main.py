from typing import Union
from fastapi import FastAPI
from fastapi import Body
from fastapi.middleware.cors import CORSMiddleware
#from transformers import pipeline

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/convert")
def convert_text(text: str = Body(..., embed=True)):
    return {text.lower()}