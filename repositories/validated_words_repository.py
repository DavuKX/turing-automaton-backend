from typing import List, Type

from sqlalchemy.orm import Session

from database.database import get_db
from database.models.validated_word import ValidatedWord
from database.schemas.validated_word import ValidatedWordCreate


class ValidatedWordsRepository:
    def __init__(self):
        self.db: Session = get_db().__next__()

    def get_all(self) -> list[Type[ValidatedWord]]:
        return self.db.query(ValidatedWord).all()

    def get_by_uuid(self, uuid: str):
        uuid__all = self.db.query(ValidatedWord).filter(ValidatedWord.uuid == uuid).all()
        print(uuid__all)
        return uuid__all

    def create(self, validated_word: ValidatedWordCreate) -> ValidatedWord:
        db_validated_word = ValidatedWord(
            uuid=validated_word.uuid,
            word=validated_word.word,
            is_valid=validated_word.is_valid,
            path=validated_word.path
        )
        self.db.add(db_validated_word)
        self.db.commit()
        self.db.refresh(db_validated_word)
        return db_validated_word
