from typing import Protocol, List
from .schema import TrainerCreate
from .entity import TrainerEntity


class ITrainerRepository(Protocol):
    def get_all(self) -> List[TrainerEntity]: ...
    def create(self, trainer: TrainerCreate) -> TrainerEntity: ...
