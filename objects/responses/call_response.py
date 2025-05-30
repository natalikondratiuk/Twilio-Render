from pydantic import BaseModel

class CallResponse(BaseModel):
    host: str
    recipient: str
    date_created: str | None
    body: str