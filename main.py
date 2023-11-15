from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from dto.validate_word_request import ValidateWordRequest
from repositories.validated_words_repository import ValidatedWordsRepository
from dto.validated_word import ValidatedWordCreate
from database.database import engine
from database.models.validated_word import Base
from dto import validated_word
from services.validation_service import ValidationService

Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/validated-words/")
async def get_validated_words_by_uuid(uuid: str):
    repository = ValidatedWordsRepository()
    by_uuid = repository.get_by_uuid(uuid)
    return by_uuid


@app.post("/api/validated-words/")
async def create_validated_word(validated_word_create: ValidatedWordCreate) -> validated_word.ValidatedWord:
    repository = ValidatedWordsRepository()
    return repository.create(validated_word_create)


@app.post("/api/validate-word/")
async def validate_word(validate_word_request: ValidateWordRequest):
    service = ValidationService(
        automaton_data=validate_word_request.automaton_data,
        word=validate_word_request.word,
        uuid=validate_word_request.uuid
    )
    return service.validate()
