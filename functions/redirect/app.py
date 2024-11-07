from functions.redirect.container import RedirectContainer
from functions.redirect.schema import RedirectRequest
from functions.common.response import LambdaResponse

def lambda_handler(event, context):
    try:
        container = RedirectContainer.get_instance()
        hash_value = event['pathParameters']['hash']
        request = RedirectRequest(hash_value=hash_value)
        response = container.service.connect_url(request)
        return response
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