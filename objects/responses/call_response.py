from pydantic import BaseModel

class CallResponse(BaseModel):
    host: str
    recipient: str
    voice: str
    date_created: str
    body: str