from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Dict, Optional
    
class LambdaResponse(BaseModel):
    status_code: Optional[int] = Field(..., serialization_alias="statusCode")
    body: Optional[str] = None
    headers: Dict[str, str] = {"Content-Type": "application/json"}
    
    def to_dict(self) -> dict:
        return self.model_dump(by_alias=True)