# query parameter
from fastapi import FastAPI
from typing import Optional

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# http://localhost:8081/items?skip=0&limit=2
@app.get("/items")
# 함수에 개별 인자값이 들어가 있는 경우 path parameter가 아닌 모든 인자는 query parameter
# query parameter의 타입과 default값 설정
# 여긴 skip, limit 둘다 default 값이 주어져 있기 때문에 query parameter로 제공되지 않아도 됨.
async def read_item(skip: int = 0, limit: int = 2):
    return fake_items_db[skip: skip + limit]


@app.get("/items_nd/")
# 함수 인자값에 default 값이 주어지지 않으면 반드시 query parameter에 해당 인자가 주어져야 함.
# http://localhost:8081/items_nd?skip=0&limit=2 여기서 skip, limit 둘다 반드시 제공되어야 함.
async def read_item_nd(skip: int, limit: int):
    return fake_items_db[skip : skip + limit]



@app.get("/items_op/")
# 함수 인자값에 default 값이 주어지지 않으면 None으로 설정. 
# limit: Optional[int] = None 또는 limit: int | None = None 과 같이 Type Hint 부여  
async def read_item_op(skip: int, limit: int = None ):
    # return fake_items_db[skip : skip + limit]
    if limit:
        return fake_items_db[skip : skip + limit]
    else:
        return {"limit is not provided"}
    
# Path와 Query Parameter를 함께 사용.
# q: str | None = None  == q: Optional[str] = None
# Optional[str]만 쓰면 안됨 . 반드시 기본값 None을 지정해줘야 함.
# None을 안주면 필수값이 되어버림.(required)
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}   