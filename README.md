# URL Shortener Service

A simple URL shortening service implemented with AWS SAM (Serverless Application Model).

## Architecture

![alt text](https://velog.velcdn.com/images/leehjhjhj/post/2b8e64c7-2409-46c5-8ef7-8181802cb377/image.png)

This service utilizes the following AWS services:
- AWS Lambda: URL creation and redirection handling
- Amazon API Gateway: HTTP endpoint provisioning
- Amazon DynamoDB: URL information storage

## Features

1. URL Creation (`POST /url`)
   - Receives original URL and generates shortened hash
   - Checks for duplicate URLs
   - Returns hash value in response

2. URL Redirection (`GET /redirect/{hash}`)
   - Retrieves original URL using hash value
   - Returns 301/302 redirection response

## Prerequisites

- Python 3.9 or higher
- AWS SAM CLI
- AWS CLI (configured with credentials)

## Installation

1. Clone repository
```bash
git clone [repository-url]
cd [repository-name]
```

2. Set up virtual environment and install dependencies
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure .env file
```env
TABLE_NAME=your-table-name
REGION=ap-northeast-2
```

4. Deploy with SAM
```bash
sam build
sam deploy --guided  # First deployment
sam deploy  # Subsequent deployments
```

## API Usage

### Create URL
```bash
curl -X POST https://your-api-endpoint/url \
  -H "Content-Type: application/json" \
  -d '{"originUrl": "https://example.com"}'
```

Response:
```json
{
  "hashValue": "abc123"
}
```

### URL Redirection
```bash
curl -L https://your-api-endpoint/redirect/abc123
```

## Project Structure
```
.
├── functions/
│   ├── common/           # Common modules
│   │   ├── exceptions.py
│   │   └── response.py
│   ├── create/          # URL creation Lambda
│   │   ├── app.py
│   │   └── service.py
│   └── redirect/        # URL redirection Lambda
│       ├── app.py
│       └── service.py
├── template.yaml        # SAM template
└── samconfig.toml      # SAM configuration
```

## Error Handling

- 404: URL not found
- 400: Invalid request or duplicate URL
- 500: Internal server error

## Local Testing

```bash
# Test Lambda function locally
sam local invoke RedirectFunction -e events/event.json

# Test API locally
sam local start-api
```

## DynamoDB Table Structure

- Partition Key: `hash_value` (String)
- Attributes:
  - `origin_url`: Original URL
  - `created_at`: Creation timestamp

## Environment Variables

- `TABLE_NAME`: DynamoDB table name
- `REGION`: AWS region

## Troubleshooting

1. 502 Bad Gateway
   - Verify response body is in string format
   - Check Lambda response format is correct

2. Import Errors
   - Verify PYTHONPATH environment variable
   - Check for necessary `__init__.py` files

## Development Notes

- The service uses Pydantic for request/response validation
- Common modules are shared between Lambda functions
- Responses are standardized using LambdaResponse class

## API Endpoints

### Create URL
- **Endpoint**: POST /url
- **Request Body**:
```json
{
  "originUrl": "https://example.com"
}
```
- **Response**: 201 Created
```json
{
  "hashValue": "abc123"
}
```

### Redirect
- **Endpoint**: GET /redirect/{hash}
- **Response**: 302 Found with Location header

## Security Considerations

- Input validation for URLs
- Rate limiting implemented at API Gateway
- DynamoDB access restricted by IAM roles

## Monitoring and Logging

- CloudWatch Logs enabled for Lambda functions
- API Gateway metrics available
- Custom error tracking implemented

## License

This project is licensed under the MIT License.