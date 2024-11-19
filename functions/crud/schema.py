from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class UrlDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    hash_value: str = Field(..., serialization_alias='hash', alias='hash')
    origin_url: str = Field(..., serialization_alias='originUrl', alias='ou')
    created_at: int = Field(..., serialization_alias='createdAt', alias='ca')
    count: int = Field(default=0, serialization_alias='count', alias='ct')
    on: bool = Field(default=True)
    title: Optional[str] = Field(default=None, serialization_alias='title', alias='ti')

class SearchAllResult(BaseModel):
    result: list[UrlDto]
    last_key: Optional[dict] = Field(..., serialization_alias='lastKey')

class SearchResult(BaseModel):
    result: list[UrlDto]

class UpdateRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    hash_value: str = Field(..., serialization_alias='hash', alias='hash')
    origin_url: str = Field(..., serialization_alias='ou', alias='originUrl')
    created_at: int = Field(..., serialization_alias='ca', alias='createdAt')
    count: int = Field(default=0)
    on: bool = Field(default=True)
    title: Optional[str] = Field(default=None, serialization_alias='ti')

class DeleteRequest(BaseModel):
    hash_value: str = Field(..., serialization_alias='hash', alias='hash')