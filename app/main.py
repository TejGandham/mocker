from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
import uvicorn
import json
import re
from typing import Optional, Dict, Any

app = FastAPI()

# Dictionary to store mock responses: path_pattern -> {method -> ResponseData_object}
mock_responses: Dict[str, Dict[str, 'ResponseData']] = {}

# Pydantic models for mock response configuration
class ResponseData(BaseModel):
    body: Dict[str, Any]
    status_code: int = 200
    custom_headers: Optional[Dict[str, str]] = None

class MockConfigRequest(BaseModel):
    path_template: str
    method: str  # e.g., GET, POST, PUT. Case-insensitive on input, stored as UPPER.
    response: ResponseData

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Received {request.method} request for URL: {request.url}")
    print(f"Headers: {dict(request.headers)}")

    body_bytes = await request.body()
    body_str = body_bytes.decode('utf-8')

    try:
        # Attempt to parse as JSON for pretty printing, otherwise use raw string
        if body_str:
            body_json = json.loads(body_str)
            pretty_body = json.dumps(body_json, indent=4)
        else:
            pretty_body = "[No Body]"
    except json.JSONDecodeError:
        pretty_body = body_str
    
    print(f"Body:\n{pretty_body}")

    response_from_route = await call_next(request)

    print(f"Responding with status code: {response_from_route.status_code}")
    # Headers are part of the response_from_route object, will be sent by FastAPI

    return response_from_route

@app.post("/mock-response", status_code=201)
async def create_mock_response(config: MockConfigRequest):
    regex_pattern = re.escape(config.path_template).replace(r'\{\}', r'.*')
    if not regex_pattern.startswith('^'):
        regex_pattern = '^' + regex_pattern
    regex_pattern += r'$'

    method_upper = config.method.upper()

    if regex_pattern not in mock_responses:
        mock_responses[regex_pattern] = {}

    # Store the ResponseData object directly (Pydantic model instance)
    mock_responses[regex_pattern][method_upper] = config.response
    
    print(f"Registered mock response for METHOD: {method_upper}, PATTERN: {regex_pattern} with status {config.response.status_code}")
    return {"message": f"Mock response set for METHOD: {method_upper}, PATH: {config.path_template}"}

@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def catch_all(request: Request, path_name: str):
    normalized_path = path_name
    if not normalized_path.startswith('/'):
        normalized_path = '/' + normalized_path
    
    current_method = request.method.upper()

    print(f"Attempting to match: {current_method} {normalized_path}")

    for pattern, methods_map in mock_responses.items():
        if re.match(pattern, normalized_path):
            if current_method in methods_map:
                mock_data = methods_map[current_method]
                print(f"Found mock for {current_method} {normalized_path} (Pattern: {pattern}) -> Status: {mock_data.status_code}")
                return Response(
                    content=json.dumps(mock_data.body),
                    status_code=mock_data.status_code,
                    headers=mock_data.custom_headers, # FastAPI handles None headers correctly
                    media_type="application/json"
                )
            else:
                print(f"Path pattern {pattern} matched, but no mock for METHOD: {current_method}. Configured methods: {list(methods_map.keys())}")
    
    default_body = {"message": f"Request for {current_method} {normalized_path} received and logged. No specific mock found."}
    print(f"No specific mock found for {current_method} {normalized_path}. Returning default 404.")
    return Response(
        content=json.dumps(default_body),
        status_code=404, # Changed default to 404 when no mock is found
        media_type="application/json"
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
