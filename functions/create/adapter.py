from abc import ABC, abstractmethod
import boto3
from functions.common.common_schema import UrlSchema
from boto3.dynamodb.conditions import Key
from typing import List, Optional

class CreatePort(ABC):

    @abstractmethod
    def find_hash(self, hoping_hash: str):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def find_origin(self, origin_url: str):
        pass

class CreateDynamoDBPort(CreatePort):
    def __init__(self, table_name: str):
        self._dynamo_client = boto3.resource('dynamodb')
        self._table_name = table_name
        self._table = self._dynamo_client.Table(self._table_name)

    def find_hash(self, hoping_hash: str) -> dict:
        response: dict = self._table.get_item(
            Key={
                'hash': hoping_hash
            }
        )
        item: dict = response.get('Item')
        return item

    def save(self, data: UrlSchema) -> None:
        item = {
            **data.model_dump(by_alias=True)
        }
        response = self._table.put_item(Item=item)

    def find_origin(self, origin_url: str) -> List[Optional[dict]]:
        response = self._table.query(
            IndexName='url-index',
            KeyConditionExpression='ou = :url',
            ExpressionAttributeValues={
                ':url': origin_url
            }
        )
        items: dict = response.get('Items', [])
        return items