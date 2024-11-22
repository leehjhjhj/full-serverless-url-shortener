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
        origin_hash = self._adapter.find_origin(request.origin_url)
        if origin_hash:
            return origin_hash[0].get('hash')
        if hoping_hash is not None:
            self._check_hoping_hash(hoping_hash)
            hash_value = hoping_hash
        else:
            hash_value = self._make_hash()
        dto = self._make_record(hash_value, request.origin_url, request.url_type, request.title)
        self._adapter.save(dto)
        return hash_value

    def _make_hash(self) -> str:
        CHARSET = '23456789' + 'ABCDEFGHJKLMNPQRSTUVWXYZ' + 'abcdefghjkmnpqrstuvwxyz'
        timestamp = self._get_epoch_milliseconds()
        
        timestamp_part = timestamp % (10 ** 7)
        random_part = random.randint(0, 9999)
        
        combined = (timestamp_part * 10000) + random_part
        result = []
        
        while combined:
            combined, remainder = divmod(combined, len(CHARSET))
            result.append(CHARSET[remainder])
        
        base62_str = ''.join(reversed(result))[-7:].rjust(7, CHARSET[0])
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
            url_type: str,
            title: str = None
        ) -> UrlSchema:
        created_at = int(time.time())
        return UrlSchema(
            hash=hash_value,
            origin_url=origin_url,
            created_at=created_at,
            title=title,
            url_type=url_type
        )