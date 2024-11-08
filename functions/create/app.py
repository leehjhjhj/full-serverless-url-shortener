from functions.create.container import CreateContainer
from functions.create.schema import CreateRequest
from functions.common.response import LambdaResponse
from functions.common.exceptions import NotFoundException, AlreadyExistException
import json

def lambda_handler(event, context):
    try:
        # body = json.loads(event['body'])
        body = event['body']
        request = CreateRequest(**body)
        container = CreateContainer.get_instance()
        hash_value = container.service.create_hash(request)
        return LambdaResponse(
            status_code=201,
            message="success",
            body={'hashValue': hash_value}
        ).to_dict()
    except NotFoundException as e:
        return LambdaResponse(
                status_code=404,
                body={'error': e.message}
            ).to_dict()
    except AlreadyExistException as e:
        return LambdaResponse(
                status_code=400,
                body={'error': e.message}
            ).to_dict()
    except Exception as e:
        print(e)
        return LambdaResponse(
            status_code=500,
            message="Internal server error"
        ).to_dict()