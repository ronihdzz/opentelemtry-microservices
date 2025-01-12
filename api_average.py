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
    service_name="api_average",
    os_version="1.0.0",
    cluster="cluster_1",
    datacentre="datacentre_1"
)
RequestsInstrumentor().instrument()
app = FastAPI()
settings = Settings()
FastAPIInstrumentor().instrument_app(app)


# Schema
# --------------------------------------------------------------
class RequestAverage(BaseModel):
    numbers: list[float]

class ResponseAverage(BaseModel):
    result: float


# Endpoints
# --------------------------------------------------------------

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
