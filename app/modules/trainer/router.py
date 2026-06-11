from flask_openapi3 import APIBlueprint, Tag
from app.core.database import get_db
from .repository import TrainerRepository
from .service import TrainerService
from .schema import TrainerCreate, TrainerResponse, TrainerPath

# Tag digunakan untuk mengelompokkan API di UI Scalar
tag = Tag(name="Trainer", description="Manajemen Trainer")

# Gunakan APIBlueprint sebagai pengganti Blueprint standar
trainer_bp = APIBlueprint("trainer", __name__, url_prefix="/trainers")


@trainer_bp.get("/", tags=[tag], responses={"200": TrainerResponse})
def get_trainers():
    db = next(get_db())  # Gunakan dependency injection untuk mendapatkan session DB
    try:
        repo = TrainerRepository(db)
        service = TrainerService(repo)
        trainers = service.list_trainers()
        # return jsonify([{"id": t.id, "name": t.name} for t in trainers])
        # Pydantic support: flask-openapi3 akan otomatis validasi jika diinginkan
        return [TrainerResponse.model_validate(t).model_dump() for t in trainers]
    finally:
        db.close()


@trainer_bp.post("/", tags=[tag], responses={"201": TrainerResponse})
def create_trainer(
    body: TrainerCreate,
):  # Body otomatis di-parsing & divalidasi dari Pydantic
    # data = TrainerCreate(**request.json)
    db = next(get_db())
    try:
        repo = TrainerRepository(db)
        service = TrainerService(repo)

        new_trainer = service.register_trainer(body)
        # return jsonify({"id": new_trainer.id, "status": "created"}), 201
        return TrainerResponse.model_validate(new_trainer).model_dump(), 201
    finally:
        db.close()


@trainer_bp.get("/<int:id>", tags=[tag], responses={"200": TrainerResponse})
def get_trainer_by_id(path: TrainerPath):
    db = next(get_db())
    try:
        repo = TrainerRepository(db)
        service = TrainerService(repo)
        trainer = service.get_trainer_by_id(path.id)
        return TrainerResponse.model_validate(trainer).model_dump()
    finally:
        db.close()
