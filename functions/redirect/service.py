from functions.redirect.adapter import RedirectPort
from functions.redirect.schema import RedirectRequest
from functions.common.exceptions import ForbiddenException

class RedirectService:
    def __init__(self, adapter: RedirectPort):
        self._adapter = adapter

    def connect_url(self, request: RedirectRequest) -> str:
        hash_value = request.hash_value
        data = self._adapter.find(hash_value)
        self._check_forbidden(data.on)
        data.count += 1
        self._adapter.save(data)
        return data.origin_url
    
    def _check_forbidden(self, on: bool):
        if not on:
            raise ForbiddenException