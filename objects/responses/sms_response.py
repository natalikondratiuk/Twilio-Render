from pydantic import BaseModel

class SmsResponse(BaseModel):
    host: str
    recipient: str
    date_created: str
    body: str