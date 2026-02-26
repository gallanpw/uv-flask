from sqlalchemy.orm import Session
from .entity import TrainerEntity
from .schema import TrainerCreate


class TrainerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(TrainerEntity).all()

    def create(self, trainer: TrainerCreate):
        db_trainer = TrainerEntity(**trainer.model_dump())
        self.db.add(db_trainer)
        self.db.commit()
        self.db.refresh(db_trainer)
        return db_trainer
