from functions.redirect.container import RedirectContainer
from functions.redirect.schema import RedirectRequest
from functions.common.response import LambdaResponse
from functions.common.exceptions import NotFoundException

def lambda_handler(event, context):
    try:
        container = RedirectContainer.get_instance()
        hash_value = event['pathParameters']['hash']
        request = RedirectRequest(hash_value=hash_value)
        response = container.service.connect_url(request)
        return response
    except NotFoundException as e:
        return LambdaResponse(
                status_code=404,
                body={'error': e.message}
            ).to_dict()
    except Exception as e:
        print(e)
        return LambdaResponse(
            status_code=500,
            message="Internal server error"
        ).to_dict()

event = {
    "pathParameters": {
        "hash": "1"
    }
}
print(lambda_handler(event, ""))