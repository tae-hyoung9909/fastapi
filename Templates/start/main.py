from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

templates = Jinja2Templates(directory="templates")

class Item(BaseModel):
    name: str
    price: float

# reponse_class를 HTMLResponse로 지정해주면 swagger ui에서 인식
@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str, q: str | None = None):
    # 내부에서 pydantic 객체 생성
    item = Item(
        name="Sample Item",
        price=10
    )
    
    # pydantic model값을 dict 변환
    item_dict = item.model_dump()

    return templates.TemplateResponse(
        request=request,
        name="item.html",
        context={
            "id": id,
            "q_str": q,
            "item": item,
            "item_dict": item_dict
    })

@app.get("/item_gubun")
async def read_item_by_gubun(request: Request, gubun: str):
    item = Item(
        name="Gubun Item",
        price=20
    )
    
    return templates.TemplateResponse(
        request=request,
        name="item_gubun.html",
        context={
            "gubun": gubun,
            "item": item
        })

@app.get("/all_items", response_class=HTMLResponse)
async def read_all_items(request: Request):
    items = [
        Item(name="Item 1", price=10),
        Item(name="Item 2", price=20),
        Item(name="Item 3", price=30)
    ]
    
    return templates.TemplateResponse(
        request=request,
        name="all_items.html",
        context={
            "items": items
        })

@app.get("/read_safe", response_class=HTMLResponse)
async def read_safe(request: Request):
    # 이렇게 태그가 포함된 문자열을 넘기면 XSS 공격이 될 수 있다.
    dangerous_str = '<h1>This is an XSS attack!</h1>'
    
    return templates.TemplateResponse(
        request=request,
        name="safe.html",
        context={
            "dangerous_str": dangerous_str
        })