from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from settings import Settings
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
    service_name="api_exponentiation",
    os_version="1.0.0",
    cluster="cluster_4",
    datacentre="datacentre_1"
)
RequestsInstrumentor().instrument()
app = FastAPI()
settings = Settings()
FastAPIInstrumentor().instrument_app(app)


# Schema
# --------------------------------------------------------------

class RequestExponentiation(BaseModel):
    base : float
    exponent : float

class ResponseExponentiation(BaseModel):
    result: float


# Endpoints
# --------------------------------------------------------------

@app.post("/exponentiation", response_model=ResponseExponentiation)
def exponentiation_numbers(request: RequestExponentiation):
    return ResponseExponentiation(result=request.base ** request.exponent)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST_API_EXPONENTIATION, port=settings.PORT_API_EXPONENTIATION)