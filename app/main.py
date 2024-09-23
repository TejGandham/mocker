from fastapi import FastAPI, Request, Response
import uvicorn
import json
app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Log request details
    print(f"Received {request.method} request for URL: {request.url}")
    print(f"Headers: {dict(request.headers)}")

    # Read and decode the request body
    body = await request.body()
    body_str = body.decode('utf-8')

    # Try to parse the body as JSON for pretty printing
    try:
        body_json = json.loads(body_str)
        pretty_body = json.dumps(body_json, indent=4)
    except json.JSONDecodeError:
        # If it's not JSON, just print the raw body
        pretty_body = body_str

    print(f"Body:\n{pretty_body}")

    # Process the request
    response = await call_next(request)

    print(f"Responding with status code: {response.status_code}")

    return response

@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def catch_all(request: Request, path_name: str):
    response = {"message":"Request received and logged."}
    return response

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)