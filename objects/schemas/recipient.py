from pydantic import BaseModel

class Recipient(BaseModel):
    phone: str
    message: str