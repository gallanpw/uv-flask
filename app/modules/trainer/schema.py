from pydantic import BaseModel, ConfigDict


class TrainerBase(BaseModel):
    name: str
    specialty: str


class TrainerCreate(TrainerBase):
    pass


class TrainerResponse(TrainerBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TrainerPath(BaseModel):
    id: int
