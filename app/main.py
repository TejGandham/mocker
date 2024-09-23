from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
import uvicorn
import json
import re

app = FastAPI()

# Dictionary to store mock responses with regex patterns as keys
mock_responses = {}

# Pydantic model for mock response creation
class MockResponse(BaseModel):
    path_template: str
    response: dict

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Received {request.method} request for URL: {request.url}")
    print(f"Headers: {dict(request.headers)}")

    body = await request.body()
    body_str = body.decode('utf-8')

    try:
        body_json = json.loads(body_str)
        pretty_body = json.dumps(body_json, indent=4)
    except json.JSONDecodeError:
        pretty_body = body_str

    print(f"Body:\n{pretty_body}")

    response = await call_next(request)

    print(f"Responding with status code: {response.status_code}")

    return response

@app.post("/mock-response")
async def create_mock_response(mock_response: MockResponse):
    # Use raw paths without escaping that start with a slash
    regex_pattern = re.escape(mock_response.path_template).replace(r'\{\}', r'.*') 
    if not regex_pattern.startswith('^'):
        regex_pattern = '^' + regex_pattern  # Ensure it matches the start
    regex_pattern += r'$'  # Ensure it matches the end

    mock_responses[regex_pattern] = json.dumps(mock_response.response)
    print(f"Registered mock response for pattern: {regex_pattern}")
    return {"message": f"Mock response set for path: {mock_response.path_template}"}



@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def catch_all(request: Request, path_name: str):
    print(f"Checking path: {path_name} against registered patterns")
    
    # Handle leading slash if necessary
    if not path_name.startswith('/'):
        path_name = '/' + path_name  

    for pattern, mock_response in mock_responses.items():
        print(f"Trying pattern: {pattern}")
        if re.match(pattern, path_name):
            print(f"Found: {path_name}")
            return Response(content=mock_response, media_type="application/json", status_code=200)

    response = {"message": "Request received and logged."}
    return response

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
