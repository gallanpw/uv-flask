from pydantic import BaseModel


class TrainerBase(BaseModel):
    name: str
    specialty: str


class TrainerCreate(TrainerBase):
    pass


class TrainerResponse(TrainerBase):
    id: int

    class Config:
        from_attributes = True
