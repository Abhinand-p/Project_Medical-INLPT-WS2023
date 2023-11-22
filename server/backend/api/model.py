from fastapi import Header, APIRouter


model = APIRouter(prefix="/model")


@model.get('')
async def get_data():
    return {}

