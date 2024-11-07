from __future__ import annotations
from functions.redirect.service import RedirectService
from functions.redirect.adapter import RedirectDynamoDBPort
from functions.redirect.environments import env
from typing import Optional

class RedirectContainer:
    _instance: Optional[RedirectContainer] = None
    
    def __init__(self):
        self._adapter = RedirectDynamoDBPort(table_name=env.TABLE_NAME, region=env.REGION)
        self.service = RedirectService(self._adapter)
    
    @classmethod
    def get_instance(cls) -> RedirectContainer:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance