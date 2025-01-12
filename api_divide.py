from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from settings import Settings

app = FastAPI()
settings = Settings()

class RequestDivide(BaseModel):
    divide : float
    divindend : float

class ResponseDivide(BaseModel):
    result: float


@app.post("/divide", response_model=ResponseDivide)
def divide_numbers(request: RequestDivide):
    return ResponseDivide(result=request.divide / request.divindend)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST_API_DIVIDE, port=settings.PORT_API_DIVIDE)