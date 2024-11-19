from __future__ import annotations
from functions.crud.service import CrudService
from functions.crud.adapter import CrudDynamoDBPort
from functions.crud.environments import env
from typing import Optional

class CrudContainer:
    _instance: Optional[CrudContainer] = None
    
    def __init__(self):
        self._adapter = CrudDynamoDBPort(table_name=env.TABLE_NAME)
        self.service = CrudService(self._adapter)
    
    @classmethod
    def get_instance(cls) -> CrudContainer:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance