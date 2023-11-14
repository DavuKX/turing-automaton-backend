from fastapi import FastAPI
from repositories.validated_words_repository import ValidatedWordsRepository
from database.schemas.validated_word import ValidatedWordCreate
from database.database import engine
from database.models.validated_word import Base
from database.schemas import validated_word

Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/validated_words/{uuid}")
async def read_item(uuid: str):
    repository = ValidatedWordsRepository()
    by_uuid = repository.get_by_uuid(uuid)
    return by_uuid


@app.post("/validated_words/")
async def create_item(validated_word_create: ValidatedWordCreate) -> validated_word.ValidatedWord:
    repository = ValidatedWordsRepository()
    return repository.create(validated_word_create)
