from pydantic import BaseModel

class RedirectRequest(BaseModel):
    hash_value: str

class OriginUrlData(BaseModel):
    origin_url: str
    on: bool