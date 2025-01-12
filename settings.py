from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    
    HTTP_PROTOCOL: str = "http"
    
    # API AVERAGE
    # --------------------------------------------------------------
    PORT_API_AVERAGE: int = 9001
    HOST_API_AVERAGE: str = "localhost"
    
    
    # API ADD
    # --------------------------------------------------------------
    PORT_API_ADD: int = 9002
    HOST_API_ADD: str = "localhost"
    
    
    # API DIVIDE
    # --------------------------------------------------------------
    PORT_API_DIVIDE: int = 9003
    HOST_API_DIVIDE: str = "localhost"

    
    # API EXPONENTIATION
    # --------------------------------------------------------------
    PORT_API_EXPONENTIATION: int = 9004
    HOST_API_EXPONENTIATION: str = "localhost"
    
    
    # API STANDART DEVIATION
    # --------------------------------------------------------------
    PORT_API_STANDART_DEVIATION: int = 9005
    HOST_API_STANDART_DEVIATION: str = "localhost"
    
