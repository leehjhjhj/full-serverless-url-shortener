from functions.redirect.container import RedirectContainer
from functions.redirect.schema import RedirectRequest
from functions.common.response import LambdaResponse
from functions.common.exceptions import NotFoundException, ForbiddenException
import json

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
                'Cache-Control': 'no-store, no-cache'
            }
        ).to_dict()
    except NotFoundException as e:
        return LambdaResponse(
                status_code=404,
                body=json.dumps({'error': e.message})
            ).to_dict()
    except ForbiddenException as e:
        return LambdaResponse(
                status_code=403,
                body=json.dumps({'error': e.message})
            ).to_dict()
    except Exception as e:
        print(e)
        return LambdaResponse(
            status_code=500
        ).to_dict()