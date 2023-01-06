
from fastapi import APIRouter
import task_spacy


text_model_router = APIRouter(
    prefix='/text',
    tags=['text_model']
)


@text_model_router.get("/posTagging")
def pos_tagging(str):
    return task_spacy.performPOS(str)


@text_model_router.get("/ner")
def ner(str):
    return task_spacy.ner(str)
