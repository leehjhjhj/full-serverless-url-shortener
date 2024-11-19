from functions.crud.container import CrudContainer
from functions.common.response import LambdaResponse
from functions.common.exceptions import (
    NotFoundException
)
from functions.crud.schema import UpdateRequest
import json
from typing import Optional

def lambda_handler(event, context):
    try:
        http_method = event['httpMethod']
        path = event['path']
        container = CrudContainer.get_instance()

        if http_method == 'GET' and path == '/get':
            query_params: dict = event.get('queryStringParameters', {}) or {}
            result = container.service.get_url(query_params)
            return LambdaResponse(
                status_code=200,
                body=json.dumps(result.model_dump(by_alias=True))
            ).to_dict()
        elif http_method == 'POST' and path == '/get-all':
            last_evaluated_key: Optional[dict] = event.get('body')
            result = container.service.get_all_urls(last_evaluated_key)
            return LambdaResponse(
                status_code=200,
                body=json.dumps(result.model_dump(by_alias=True))
            ).to_dict()
        elif http_method == 'PUT' and path == '/update':
            body = json.loads(event['body'])
            request = UpdateRequest(**body)
            container.service.update_url(request)
            return LambdaResponse(
                status_code=200
            ).to_dict()
        else:
            return LambdaResponse(
                status_code=405,
                body=json.dumps({'error': 'Invalid endpoint'})
            ).to_dict()

    except ValueError as e:
        return LambdaResponse(
            status_code=400,
            body=json.dumps({'error': f'Invalid parameter value: {str(e)}'})
        ).to_dict()
    except NotFoundException as e:
        return LambdaResponse(
            status_code=404,
            body=json.dumps({'error': e.message})
        ).to_dict()
    except Exception as e:
        print(e)
        return LambdaResponse(
            status_code=500
        ).to_dict()