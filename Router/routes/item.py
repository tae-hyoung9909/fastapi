from fastapi import APIRouter
from schemas import ItemCreate, ItemResponse

router = APIRouter(
    prefix="/items",
    tags=["Items"]
)

fake_items_db = [
    {
    "name": "macbook",
    "price": 3000
    }
]

@router.post("/", response_model=ItemResponse)
def create_item(item: ItemCreate, owner_id: int):
    new_item = {
        "id": len(fake_items_db) + 1,
        "owner_id": owner_id,
        **item.dict()
    }
    fake_items_db.append(new_item)
    return new_item


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int):
    return fake_items_db[item_id - 1]
