from pydantic import BaseModel

class FailedResponse(BaseModel):
    error_code: int = -1
    error_message: str = "Unhandled exception"