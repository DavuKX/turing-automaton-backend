from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP

from database.database import Base


class ValidatedWord(Base):
    __tablename__ = "validated_words"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String)
    word = Column(String)
    result_word = Column(String)
    is_valid = Column(Boolean)
    path = Column(String)

    created_at = Column(TIMESTAMP, default=datetime.utcnow)
