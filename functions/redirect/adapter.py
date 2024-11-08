from abc import ABC, abstractmethod
import boto3
from boto3.dynamodb.conditions import Key
from functions.common.common_schema import DataDto
from functions.common.exceptions import NotFoundException

class RedirectPort(ABC):
    @abstractmethod
    def find(self, hash_value: str):
        pass
    
    @abstractmethod
    def save(self):
        pass

class RedirectDynamoDBPort(RedirectPort):
    def __init__(self, table_name: str, region: str):
        self._dynamo_client = boto3.resource('dynamodb')
        self._table_name = table_name
        self._table = self._dynamo_client.Table(self._table_name) 

    def find(self, hash_value: str) -> DataDto:
        response: dict = self._table.get_item(
            Key={
                'hash': hash_value
            }
        )
        item: dict = response.get('Item')
        if not item:
            raise NotFoundException
        return DataDto(**item)
    
    def save(self, data: DataDto):
        item = {
            **data.model_dump(by_alias=True)
        }
        response = self._table.put_item(Item=item)
