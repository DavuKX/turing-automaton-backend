from pydantic import BaseModel


class ValidateWordRequest(BaseModel):
    automaton_data: dict
    word: str
    uuid: str
