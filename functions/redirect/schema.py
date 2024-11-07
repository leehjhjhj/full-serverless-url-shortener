from pydantic import BaseModel, Field

class RedirectRequest(BaseModel):
    hash_value: str

class DataDto(BaseModel):
    hash_value: str = Field(..., serialization_alias='hash', alias='hash')
    id: int
    origin_url: str = Field(..., serialization_alias='ou', alias='ou')
    on: bool
    count: int = Field(..., serialization_alias='ct', alias='ct')