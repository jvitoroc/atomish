from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from common.db import Base

class Highscore(Base):
    __tablename__ = 'highscores'
    score = Column(Integer, default=0)
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", uselist=False, back_populates="highscore")
    updated_date = Column(Date, default=datetime.now(), nullable=False)

    def __repr__(self):
        return '<Highscore %r>' % self.score