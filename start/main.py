# FastAPI Import
from fastapi import FastAPI

# Create FastAPI instance
app = FastAPI()

# Define a simple GET endpoint
# Opertaion은 get, post, put, delete 등의 http method를 의미
@app.get("/", summary="simple api",
         tags=["Root Endpoint"],
         description="A simple API endpoint")
async def root():
    '''
    A simple endpoint that returns a greeting message.
    '''
    return {"message": "Hello World"} # application/json으로 반환
