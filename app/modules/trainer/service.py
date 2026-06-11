# from .repository import TrainerRepository
from flask import abort
from .schema import TrainerCreate
from .interface import ITrainerRepository


class TrainerService:
    def __init__(self, repository: ITrainerRepository):
        self.repository = repository

    def list_trainers(self):
        return self.repository.get_all()

    def register_trainer(self, trainer_data: TrainerCreate):
        # Tambahkan logika bisnis di sini (misal: validasi unik)
        return self.repository.create(trainer_data)

    def get_trainer_by_id(self, id: int):
        trainer = self.repository.get_by_id(id)
        if not trainer:
            abort(404, description="Trainer not found")
        return trainer
