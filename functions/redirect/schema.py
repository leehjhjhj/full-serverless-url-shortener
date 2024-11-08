from pydantic import BaseModel

class RedirectRequest(BaseModel):
    hash_value: str