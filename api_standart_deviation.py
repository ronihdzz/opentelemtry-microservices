from fastapi import FastAPI
from settings import Settings
from pydantic import BaseModel
import requests
from fastapi import status, HTTPException
from fastapi.responses import RedirectResponse
from loguru import logger
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor


# Telemetry
# --------------------------------------------------------------

def initialize_telemetry(collector_endpoint, collector_port, service_name, os_version, cluster, datacentre):
    
    resource = Resource(attributes={
        "service.name": service_name,
        "os-version": os_version,
        "cluster": cluster,
        "datacentre": datacentre
    })
    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=f"http://{collector_endpoint}:{collector_port}/v1/traces"))
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)
    tracer = trace.get_tracer(service_name)
    return tracer



# Initialize
# --------------------------------------------------------------

initialize_telemetry(
    collector_endpoint="localhost",
    collector_port="4318",
    service_name="api_standart_deviation",
    os_version="1.0.0",
    cluster="cluster_5",
    datacentre="datacentre_1"
)
RequestsInstrumentor().instrument()
app = FastAPI()
settings = Settings()
FastAPIInstrumentor().instrument_app(app)


# Schema
# --------------------------------------------------------------
class RequestStandartDeviation(BaseModel):
    numbers: list[float]

class ResponseStandartDeviation(BaseModel):
    result: float


# Endpoints
# --------------------------------------------------------------

@app.get("/", include_in_schema=False)
def index():
    return RedirectResponse(url="/docs")

@app.post("/standart_deviation", response_model=ResponseStandartDeviation)
def standart_deviation_numbers(request: RequestStandartDeviation):
    list_numbers = request.numbers
    
    # List services:
    # --------------------------------------------------------------
    service_add = f"{settings.HTTP_PROTOCOL}://{settings.HOST_API_ADD}:{settings.PORT_API_ADD}/add"
    service_divide = f"{settings.HTTP_PROTOCOL}://{settings.HOST_API_DIVIDE}:{settings.PORT_API_DIVIDE}/divide"
    service_exponentiation = f"{settings.HTTP_PROTOCOL}://{settings.HOST_API_EXPONENTIATION}:{settings.PORT_API_EXPONENTIATION}/exponentiation"
    service_average = f"{settings.HTTP_PROTOCOL}://{settings.HOST_API_AVERAGE}:{settings.PORT_API_AVERAGE}/average"
    
    
    # Step 1 get average
    # --------------------------------------------------------------
    
    # Request to get the average
    request = {"numbers": list_numbers}
    logger.info(f"Request to {service_average} with {request}")
    response_average = requests.post(service_average, json=request)
    average = None
    if response_average.status_code == status.HTTP_200_OK:
        average = response_average.json()["result"]
        logger.info(f"Response from {service_average} with {response_average.json()}")
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al obtener el promedio de los números")
    
    
    # Step 2 obtener sumatoria total de 
    # la resta de cada numero con el promedio elevado al cuadrado
    # --------------------------------------------------------------
    
    sum_total = 0
    for number in list_numbers:
        # Request to get the difference
        request = {"numbers": [number, -average]}
        logger.info(f"Request to {service_add} with {request}")
        response_add = requests.post(service_add, json=request)
        logger.info(f"Response from {service_add} with {response_add.json()}")
        if response_add.status_code == status.HTTP_200_OK:
            difference = response_add.json()["result"]
            
            # Request to get the square of the difference
            request_exponentiation = {"base": difference, "exponent": 2}
            logger.info(f"Request to {service_exponentiation} with {request_exponentiation}")
            response_exponentiation = requests.post(service_exponentiation, json=request_exponentiation)
            logger.info(f"Response from {service_exponentiation} with {response_exponentiation.json()}")
            if response_exponentiation.status_code == status.HTTP_200_OK:
                difference_square = response_exponentiation.json()["result"]
                sum_total += difference_square
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al obtener el cuadrado de la diferencia")
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al obtener la diferencia de cada numero con el promedio")
        

    # Step 3 obtener la divicion de la sumatoria total entre la cantidad de numeros menos 1
    # --------------------------------------------------------------
    
    result_divide = 0
    n_less_one = len(list_numbers) - 1
    
    # Request to get the divide
    request = {"divide": sum_total, "divindend": n_less_one }
    logger.info(f"Request to {service_divide} with {request}")
    response_divide = requests.post(service_divide, json=request)
    if response_divide.status_code == status.HTTP_200_OK:
        result_divide = response_divide.json()["result"]
        logger.info(f"Response from {service_divide} with {response_divide.json()}")
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al obtener el promedio de los números")
    

    # Step 4 obtener la raiz cuadrada del resultado de la divicion 
    # --------------------------------------------------------------
    
    standart_deviation = 0
    
    # Request to exponentiation
    request_exponentiation = {"base": result_divide, "exponent": 0.5}
    logger.info(f"Request to {service_exponentiation} with {request_exponentiation}")
    response_exponentiation = requests.post(service_exponentiation, json=request_exponentiation)
    logger.info(f"Response from {service_exponentiation} with {response_exponentiation.json()}")
    if response_exponentiation.status_code == status.HTTP_200_OK:
        standart_deviation = response_exponentiation.json()["result"]
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al obtener la raiz cuadrada del resultado de la divicion")
    
    return ResponseStandartDeviation(result=standart_deviation)
