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
        unique_id: Optional[Union[int, str]] = request.unique_id
        if not unique_id:
            return base_url
        
        full_type: str | None = self._get_url_path_by_type(request.type, unique_id, request.event_url)
    
        if not full_type:
            return base_url

        return base_url + full_type

    def _get_url_path_by_type(
        self,
        type: str,
        unique_id: Optional[str] = None,
        event_url: Optional[str] = None
    ):
        if type in ("l", "b"):
            if not event_url:
                return None
    
        mapping = {
            "p": f"/prod/view/{unique_id}",
            "t": f"/ticket/view/{unique_id}",
            "e": f"/event/@{unique_id}",
            "d": f"/demand/view/{unique_id}",
            "r": f"/paper/view/{unique_id}",
            "l": f"/event/@{event_url}/timeline/{unique_id}",
            "br": f"/event/@{event_url}/booth/ready/{unique_id}",
            "bf": f"/event/@{event_url}/booth/{unique_id}"
        }
        return mapping.get(type)
    
    def _check_forbidden(self, on: bool):
        if not on:
            raise ForbiddenException