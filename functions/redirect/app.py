from functions.redirect.container import RedirectContainer
from functions.redirect.schema import RedirectRequest
from functions.common.response import LambdaResponse
from functions.common.exceptions import NotFoundException, ForbiddenException

def lambda_handler(event, context):
    try:
        container = RedirectContainer.get_instance()
        hash_value = event['pathParameters']['hash']
        request = RedirectRequest(hash_value=hash_value)
        url = container.service.connect_url(request)
        return LambdaResponse(
            status_code=302,
            headers={
                'Location': url,
                'Cache-Control': 'public, max-age=86400'
            }
        ).to_dict()
    except NotFoundException as e:
        return LambdaResponse(
                status_code=404,
                body={'error': e.message}
            ).to_dict()
    except ForbiddenException as e:
        return LambdaResponse(
                status_code=403,
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
        "hash": "test"
    }
}
print(lambda_handler(event, ""))