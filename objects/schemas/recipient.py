from pydantic import BaseModel

class Recipient(BaseModel):
    phone: str
    voice: str
    message: str