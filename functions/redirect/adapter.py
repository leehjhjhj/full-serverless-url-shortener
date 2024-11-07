from abc import ABC, abstractmethod
import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime, timedelta
from functions.redirect.schema import OriginUrlData

class RedirectPort(ABC):
    @abstractmethod
    def find(self, hash_value: str):
        pass
    
    @abstractmethod
    def save(self):
        pass

class RedirectDynamoDBPort(RedirectPort):
    def __init__(self, table_name: str, region: str) -> OriginUrlData:
        self._dynamo_client = boto3.resource('dynamodb')
        self._table_name = table_name
        self._table = self._dynamo_client.Table(self._table_name) 

    def find(self, hash_value: str):
        response = self._table.query(
            KeyConditionExpression=Key('hash').eq(hash_value)
        )
        
        items = response.get('Items', [])
        return OriginUrlData(
            origin_url=items[0].get('ou')
        )
    
    def save(self):
        pass
