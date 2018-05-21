from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from common.db import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    hash = Column(String(128), nullable=False)
    created_date = Column(Date, default=datetime.now(), nullable=False)
    highscore = relationship("Highscore", uselist=False, back_populates="user")

    def __repr__(self):
        return '<User %r>' % self.username