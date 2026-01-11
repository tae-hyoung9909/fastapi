from fastapi import FastAPI
from routes import user, item

app = FastAPI()

app.include_router(user.router)
app.include_router(item.router)
