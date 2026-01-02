# path parameter
from fastapi import FastAPI
from enum import Enum

app = FastAPI()

@app.get("/items/all")
async def read_all_items():
    return {"items": "all items"} # content-type: application/json


#Path Parameter Example
# http://localhost:8081/items/3
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id} # content-type: application/json


# 위에 경로(type:int)로 매핑 하기때문에 에러가 난다.
# 해결방법: ("/items/{item_id}") 보다 위에 위치해야한다.
# @app.get("/items/all")
# async def read_all_items():
#     return {"items": "all items"} # content-type: application/json
