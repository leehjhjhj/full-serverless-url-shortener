from __future__ import annotations
from functions.create.service import CreatetService
from functions.create.adapter import CreateDynamoDBPort
from functions.create.environments import env
from typing import Optional

class CreateContainer:
    _instance: Optional[CreateContainer] = None
    
    def __init__(self):
        self._adapter = CreateDynamoDBPort(table_name=env.TABLE_NAME)
        self.service = CreatetService(self._adapter)
    
    @classmethod
    def get_instance(cls) -> CreateContainer:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance