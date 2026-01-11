from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(UserCreate):
    id: int


class ItemCreate(BaseModel):
    name: str
    price: int

class ItemResponse(ItemCreate):
    id: int
    owner_id: int
