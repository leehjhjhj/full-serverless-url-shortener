from pydantic import BaseModel, Field
from typing import Optional

class CreateRequest(BaseModel):
    origin_url: str = Field(..., serialization_alias='ou', alias='originUrl')
    hoping_hash: Optional[str] = Field(default=None, alias='hopingHash')
    title: Optional[str] = Field(default=None)