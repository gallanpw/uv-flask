from contextlib import contextmanager

from app.core.database import SessionLocal

from .repository import TrainerRepository
from .service import TrainerService


# Tempat merakit TrainerService: session DB -> repository -> service.
# Router cukup memakai `with trainer_service() as service:`, session ditutup otomatis.
@contextmanager
def trainer_service():
    db = SessionLocal()
    try:
        yield TrainerService(TrainerRepository(db))
    finally:
        db.close()
