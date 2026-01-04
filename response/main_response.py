from fastapi import FastAPI, Form, status
from fastapi.responses import (
    JSONResponse, 
    HTMLResponse,
    RedirectResponse
)
from pydantic import BaseModel

app = FastAPI()

# response_class의 default가 JSONResponse이므로 명시적으로 지정하지 않아도 됨
@app.get("/resp_json/{item_id}", response_class=JSONResponse)
async def resp_json(item_id: int, q: str | None = None):
    return JSONResponse(
        content={
            "message": "This is a JSON response",
            "item_id": item_id,
            "q": q
        },
        status_code = status.HTTP_200_OK
    )

# HTML Response
@app.get('/resp_html/{item_id}', response_class=HTMLResponse)
async def resp_html(item_id: int, name: str | None = None):
    content = f"""
    <html>
        <head>
            <title>HTML Response</title>
        </head>
        <body>
            <h1>This is an HTML response</h1>
            <p>Item ID: {item_id}</p>
            <p>Name: {name}</p>
        </body>
    </html>
    """
    return HTMLResponse(content=content, status_code=status.HTTP_200_OK)


# Redirect(GET -> GET)
@app.get('/redirect')
def redirect_only(comment: str | None = None):
    print(f"Comment: {comment}")
    return RedirectResponse(
        url=f"/resp_html/3?name={comment}",
    )

# Redirect(POST -> GET)
@app.post('/redirect_post')
async def redirect_post(item_id: int = Form(...), item_name: str = Form(...)):
    print(f"Item ID: {item_id}, Item Name: {item_name}")
    return RedirectResponse(
        url=f"/resp_html/{item_id}?name={item_name}",
        status_code=status.HTTP_303_SEE_OTHER
        # satus_code를 default(307)로 하면 url를 GET로 바꾸지 않고 POST로 전송하여 에러가 난다.
        # 때문에 satuse_code를 303로 변경해주어야 한다.
    )


class Item(BaseModel):
    name: str
    description: str
    price: float
    tax: float | None = None

# pydantic model 
class ItemResp(BaseModel):
    name: str
    description: str
    price_with_tax: float

# response model
@app.post('/create_item', response_model=ItemResp,
                 status_code=status.HTTP_201_CREATED)
async def create_item_model(item: Item):
    price_with_tax = item.price + item.tax if item.tax else item.price
    resp_item = ItemResp(
        name=item.name,
        description=item.description,
        price_with_tax=price_with_tax
    )
    return resp_item
    #response_model을 지정해주면 pydantic model에 정의된 필드만 응답으로 보내진다.
    # 때문에 item를 리턴하면 안됨 