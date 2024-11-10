from functions.create.adapter import CreatePort
from functions.create.schema import CreateRequest
from functions.common.exceptions import AlreadyExistException, TooLongExceiption
from functions.common.common_schema import UrlSchema
from datetime import datetime
import time
import random
import string

class CreatetService:
    def __init__(self, adapter: CreatePort):
        self._adapter = adapter

    def create_hash(self, request: CreateRequest) -> None:
        hoping_hash = request.hoping_hash
        if self._adapter.find_origin(request.origin_url):
            raise AlreadyExistException
        if hoping_hash is not None:
            self._check_hoping_hash(hoping_hash)
            hash_value = hoping_hash
        else:
            hash_value = self._make_hash()
        dto = self._make_record(hash_value, request.origin_url, request.title)
        self._adapter.save(dto)
        return hash_value

    def _make_hash(self) -> str:
        CHARSET = string.digits + string.ascii_uppercase + string.ascii_lowercase
        timestamp = self._get_epoch_milliseconds()
        random_bits = random.randint(0, 999)
        combined = (timestamp * 1000) + random_bits
        result = []
        while combined:
            combined, remainder = divmod(combined, 62)
            result.append(CHARSET[remainder])
        
        base62_str = ''.join(reversed(result))[-7:].rjust(7, '0')
        return base62_str
    
    def _check_hoping_hash(self, hoping_hash: str) -> bool:
        if len(hoping_hash) > 7 :
            raise TooLongExceiption
        if self._adapter.find_hash(hoping_hash):
            raise AlreadyExistException
    def _get_epoch_milliseconds(self) -> int:
        return int(time.time() * 1000)
    
    def _make_record(
            self,
            hash_value: str,
            origin_url: str,
            title: str = None
        ) -> UrlSchema:
        created_at = int(time.time())
        return UrlSchema(
            hash=hash_value,
            origin_url=origin_url,
            created_at=created_at,
            title=title
        )