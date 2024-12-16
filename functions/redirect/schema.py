from pydantic import BaseModel
from typing import Optional

class RedirectRequest(BaseModel):
    hash_value: Optional[str] = None