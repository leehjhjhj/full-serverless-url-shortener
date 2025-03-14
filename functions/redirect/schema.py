from pydantic import BaseModel
from typing import Optional, Union

class RedirectRequest(BaseModel):
    hash_value: Optional[str] = None

class RedirectUrlRequest(BaseModel):
    type: Optional[str] = None
    unique_id: Optional[Union[int, str]] = None
    event_url: Optional[str] = None