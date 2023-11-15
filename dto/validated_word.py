from pydantic import BaseModel


class ValidatedWordBase(BaseModel):
    uuid: str
    word: str
    result_word: str
    is_valid: bool
    path: str


class ValidatedWordCreate(ValidatedWordBase):
    pass


class ValidatedWord(ValidatedWordBase):
    id: int
    created_at: str

    class Config:
        orm_mode = True
