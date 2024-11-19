from abc import ABC, abstractmethod
import boto3
from typing import Optional
from functions.crud.schema import UpdateRequest

class CrudPort(ABC):

    @abstractmethod
    def find_hash(self, hash: str):
        pass

    @abstractmethod
    def find_hash_by_origin_url(self, origin_url: str):
        pass

    @abstractmethod
    def find_all(self, last_evaluated_key: dict = None):
        pass

    @abstractmethod
    def save(self):
        pass

class CrudDynamoDBPort(CrudPort):
    def __init__(self, table_name: str):
        self._dynamo_client = boto3.resource('dynamodb')
        self._table_name = table_name
        self._table = self._dynamo_client.Table(self._table_name)

    def find_hash(self, hash: str) -> dict:
        response: dict = self._table.get_item(
            Key={
                'hash': hash
            }
        )
        item: dict = response.get('Item')
        return item

    def find_hash_by_origin_url(self, origin_url: str) -> list[Optional[dict]]:
        response = self._table.query(
            IndexName='url-index',
            KeyConditionExpression='ou = :url',
            ExpressionAttributeValues={
                ':url': origin_url
            }
        )
        items: dict = response.get('Items', [])
        return items
    
    def find_all(self, last_evaluated_key: dict = None) -> tuple[list[Optional[dict]], dict]:
        limit: int = 20
        scan_kwargs = {
            'Limit': limit
        }
        
        if last_evaluated_key:
            scan_kwargs['ExclusiveStartKey'] = last_evaluated_key
        response = self._table.scan(**scan_kwargs)
        
        return response.get('Items', []), response.get('LastEvaluatedKey')
    
    def save(self, data: UpdateRequest) -> None:
        item = {
            **data.model_dump(by_alias=True)
        }
        self._table.put_item(Item=item)