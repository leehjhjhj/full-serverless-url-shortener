from functions.redirect.container import RedirectContainer
from functions.redirect.schema import RedirectRequest, RedirectUrlRequest
from functions.common.response import LambdaResponse
from functions.common.exceptions import NotFoundException, ForbiddenException
import json

def lambda_handler(event, context):
    try:
        container = RedirectContainer.get_instance()
        parameters = event.get('pathParameters')
        url = "https://takemm.com"
        if parameters:
            if parameters.get('hash') and parameters.get('unique_id'):
                request = RedirectUrlRequest(
                    type=parameters.get('hash'),
                    unique_id=parameters.get('unique_id'),
                    event_url=parameters.get('event_url')
                )
                url = container.service.connect_type_unique_url(request)
            else:
                hash_value = parameters.get('hash')
                request = RedirectRequest(hash_value=hash_value)
                url = container.service.connect_hash_url(request)
        return LambdaResponse(
            status_code=302,
            headers={
                'Location': url,
                'Cache-Control': 'no-store, no-cache'
            }
        ).to_dict()
    except NotFoundException as e:
        print(e)
        return LambdaResponse(
            status_code=302,
            headers={
                'Location': "https://takemm.com",
                'Cache-Control': 'no-store, no-cache'
            }
        ).to_dict()
    except ForbiddenException as e:
        print(e)
        return LambdaResponse(
            status_code=302,
            headers={
                'Location': "https://takemm.com",
                'Cache-Control': 'no-store, no-cache'
            }
        ).to_dict()
    except Exception as e:
        print(e)
        return LambdaResponse(
            status_code=500
        ).to_dict()