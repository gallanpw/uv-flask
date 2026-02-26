from .repository import TrainerRepository
from .schema import TrainerCreate


class TrainerService:
    def __init__(self, repository: TrainerRepository):
        self.repository = repository

    def list_trainers(self):
        return self.repository.get_all()

    def register_trainer(self, trainer_data: TrainerCreate):
        # Tambahkan logika bisnis di sini (misal: validasi unik)
        return self.repository.create(trainer_data)
