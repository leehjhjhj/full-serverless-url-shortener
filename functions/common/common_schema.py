from pydantic import BaseModel, Field
from typing import Optional

class UrlSchema(BaseModel):
    hash_value: str = Field(..., serialization_alias='hash', alias='hash')
    origin_url: str = Field(..., serialization_alias='ou', alias='ou')
    # user_id: Optional[str] = Field(default=None, serialization_alias='ui', alias='ui')
    created_at: int = Field(..., serialization_alias='ca', alias='ca')
    count: int = Field(default=0, serialization_alias='ct', alias='ct')
    on: bool = Field(default=True)
    title: Optional[str] = Field(default=None, serialization_alias='ti', alias='ti')