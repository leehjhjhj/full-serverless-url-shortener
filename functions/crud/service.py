from functions.crud.adapter import CrudPort
from functions.crud.schema import SearchAllResult, SearchResult, UrlDto, UpdateRequest, DeleteRequest
from functions.common.exceptions import NotFoundException
from typing import Optional

class CrudService:
    def __init__(self, adapter: CrudPort):
        self._adapter = adapter

    def get_all_urls(self, last_evaluated_key: Optional[dict]) -> SearchAllResult:
        results, last_key = self._adapter.find_all(last_evaluated_key)
        return SearchAllResult(
            result=[UrlDto(**result) for result in results],
            last_key=last_key
        )
        
    def get_url(self, query_params: dict) -> list[SearchResult]:
        if query_params:
            hash = query_params.get('hash')
            origin_url = query_params.get('ou')
            if hash is not None:
                result = self._adapter.find_hash(hash)
                return SearchResult(
                    result=[UrlDto(**result)] 
                )
            elif origin_url is not None:
                results = self._adapter.find_hash_by_origin_url(hash)
                if not results:
                    raise NotFoundException
                return SearchResult(
                    [UrlDto(**result) for result in results] 
                )
            else:
                raise NotFoundException
        else:
            raise NotFoundException
        
    def update_url(self, update_request: UpdateRequest) -> None:
        self._adapter.save(update_request)

    def delete_url(self, delete_request: DeleteRequest) -> None:
        self._adapter.delete(delete_request)