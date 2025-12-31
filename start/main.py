from fastapi import FastAPI

app = FastAPI()

@app.get("/", summary="simple api",
         description="A simple API endpoint")
async def root():
    '''
    A simple endpoint that returns a greeting message.
    '''
    return {"message": "Hello World"}

