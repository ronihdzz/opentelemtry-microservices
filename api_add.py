from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from settings import Settings

app = FastAPI()
settings = Settings()

class RequestAdd(BaseModel):
    numbers : list[float]

class ResponseAdd(BaseModel):
    result: float

@app.post("/add", response_model=ResponseAdd)
def add_numbers(request: RequestAdd):
    return ResponseAdd(result=sum(request.numbers))

if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST_API_ADD, port=settings.PORT_API_ADD)