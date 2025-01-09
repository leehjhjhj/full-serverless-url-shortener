from functions.redirect.adapter import RedirectPort
from functions.redirect.schema import RedirectRequest, RedirectUrlRequest
from functions.common.exceptions import ForbiddenException
from typing import Optional, Union

class RedirectService:
    def __init__(self, adapter: RedirectPort):
        self._adapter = adapter

    def connect_hash_url(self, request: RedirectRequest) -> str:
        hash_value = request.hash_value
        if not hash_value:
            return "https://takemm.com"
        data = self._adapter.find(hash_value)
        self._check_forbidden(data.on)
        data.count += 1
        self._adapter.save(data)
        return data.origin_url
    
    def connect_type_unique_url(self, request: RedirectUrlRequest):
        base_url = "https://takemm.com"
        full_type: str | None = self._get_url_path_by_type(request.type)
        unique_id: Optional[Union[int, str]] = request.unique_id
        if not full_type or not unique_id:
            return base_url
        return base_url + full_type + str(unique_id)

    def _get_url_path_by_type(self, type: str):
        mapping = {
            "p": "/prod/view/",
            "t": "/ticket/view/",
            "e": "/event/@",
            "d": "/demand/view/",
            "r": "/paper/view/"
        }
        return mapping.get(type)
    
    def _check_forbidden(self, on: bool):
        if not on:
            raise ForbiddenException