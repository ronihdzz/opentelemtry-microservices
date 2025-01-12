from fastapi import FastAPI
import uvicorn
from settings import Settings
from pydantic import BaseModel
import requests
from fastapi import status, HTTPException
from fastapi.responses import RedirectResponse
from loguru import logger

app = FastAPI()
settings = Settings()

class RequestAverage(BaseModel):
    numbers: list[float]

class ResponseAverage(BaseModel):
    result: float


@app.get("/", include_in_schema=False)
def index():
    return RedirectResponse(url="/docs")

@app.post("/average", response_model=ResponseAverage)
def average_numbers(request: RequestAverage):
    numbers = request.numbers
    
    # Request to post the sum of the numbers
    # --------------------------------------------------------------
    service_add = f"{settings.HTTP_PROTOCOL}://{settings.HOST_API_ADD}:{settings.PORT_API_ADD}/add"
    request = {"numbers": numbers}
    logger.info(f"Request to {service_add} with {request}")
    response_add = requests.post(service_add, json=request)
    if response_add.status_code == status.HTTP_200_OK:
        sum_numbers = response_add.json()["result"]
        logger.info(f"Response from {service_add} with {response_add.json()}")
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al obtener la suma de los números")
    
    
    # Request to post the divide
    # --------------------------------------------------------------
    service_divide = f"{settings.HTTP_PROTOCOL}://{settings.HOST_API_DIVIDE}:{settings.PORT_API_DIVIDE}/divide"
    request = {"divide": sum_numbers, "divindend": len(numbers)}
    logger.info(f"Request to {service_divide} with {request}")
    response_divide = requests.post(service_divide, json=request)
    if response_divide.status_code == status.HTTP_200_OK:
        average = response_divide.json()["result"]
        logger.info(f"Response from {service_divide} with {response_divide.json()}")
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al obtener el promedio de los números")
    

    # Return the average
    # --------------------------------------------------------------
    return ResponseAverage(result=average)

if __name__ == "__main__":
    uvicorn.run("api_average:app", host="localhost", port=settings.PORT_API_AVERAGE)