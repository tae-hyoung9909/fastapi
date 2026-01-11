from fastapi import APIRouter
from schemas import UserCreate, UserResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

fake_users_db = [
    {
        "name": "kim",
        "email": "kim@test.com"
    }
]

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):
    new_user = {
        "id": len(fake_users_db) + 1,
        **user.dict()
    }
    fake_users_db.append(new_user)
    return new_user


@router.get("/{user_id}")
def get_user(user_id: int):
    return fake_users_db[user_id - 1]
