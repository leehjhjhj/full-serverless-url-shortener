from functions.redirect.adapter import RedirectPort
from functions.common.response import LambdaResponse
from functions.redirect.schema import RedirectRequest

class RedirectService:
    def __init__(self, adapter: RedirectPort):
        self._adapter = adapter

    def connect_url(self, request: RedirectRequest) -> str:
        hash_value = request.hash_value
        result = self._adapter.find(hash_value)
        return result.origin_url