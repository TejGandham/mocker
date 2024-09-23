## Usage

### Setting a Mock Response

Send a POST request to `/mock-response` with a JSON body like:

```json
{
  "path_template": "/user/{}/details",
  "response": {
    "status": "success"
  }
}
```

### Testing the Mock Response

Requesting paths like `/user/123/details` or `/user/XYZ/details` will both respond with the configured response:

```json
{
  "status": "success"
}
```
