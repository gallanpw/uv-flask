from sqlalchemy import Column, Integer, String
from app.core.database import Base


class TrainerEntity(Base):
    __tablename__ = "trainers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    specialty = Column(String)
