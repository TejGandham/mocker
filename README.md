[![codecov](https://codecov.io/github/TejGandham/mocker/branch/main/graph/badge.svg?token=MJV2T634F4)](https://codecov.io/github/TejGandham/mocker)
# Mocker

A simple **mock API server** built with **Python FastAPI** that logs incoming API requests. Useful for QA environments to verify that your service under test is correctly interacting with external APIs, especially when those external services might not be reliably available.

## Features

- **Logs all incoming HTTP requests**: Method, URL, headers, and body.
- **Supports all HTTP methods**: GET, POST, PUT, DELETE, PATCH, OPTIONS.
- **Dynamic Mock Responses**: Configure custom responses for specific path templates.
- **Dockerized**: Easy deployment using Docker and Docker Compose.
- **Configurable**: Modify settings via environment variables or code.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
    - [Using Docker Compose (Recommended)](#using-docker-compose-recommended)
    - [Running Locally Without Docker](#running-locally-without-docker)
- [Usage](#usage)
  - [Example Request](#example-request)
  - [Setting a Mock Response](#setting-a-mock-response)
  - [Testing the Mock Response](#testing-the-mock-response)
  - [Configuring Your Service Under Test](#configuring-your-service-under-test)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Getting Started

### Prerequisites

- **Docker** and **Docker Compose** installed on your machine.
- **Python 3.7+** (if you wish to run without Docker).

### Installation

#### Using Docker Compose (Recommended)

1. **Clone the Repository**

   ```bash
   git clone https://github.com/TejGandham/mocker.git
   cd mocker
   ```

2. **Build and Run the Docker Container**

   ```bash
   docker-compose up --build
   ```

   This command builds the Docker image and starts the mock API server on port `8000`.

#### Running Locally Without Docker

1. **Clone the Repository**

   ```bash
   git clone https://github.com/TejGandham/mocker.git
   cd mocker
   ```

2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Server**

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

## Usage

### Example Request

**Send a Request Using `curl`:**

```bash
curl -X POST "http://localhost:8000/test/endpoint" \
     -H "Content-Type: application/json" \
     -d '{"name": "John Doe", "age": 30}'
```

**Expected Response:**

```
Request received and logged.
```

**Server Logs:**

```
Received POST request for URL: http://localhost:8000/test/endpoint
Headers: {'host': 'localhost:8000', 'user-agent': 'curl/7.68.0', 'accept': '*/*', 'content-type': 'application/json', 'content-length': '34'}
Body:
{
    "name": "John Doe",
    "age": 30
}
Responding with status code: 200
```

### Setting a Mock Response

You can configure the server to return custom responses for specific path templates.

**Send a POST Request to `/mock-response`:**

```bash
curl -X POST "http://localhost:8000/mock-response" \
     -H "Content-Type: application/json" \
     -d '{
           "path_template": "/user/{}/details",
           "response": {
             "status": "success"
           }
         }'
```

**Request Body Explanation:**

- `path_template`: The URL pattern you want to match. The `{}` acts as a wildcard.
- `response`: The JSON response you want the server to return for the matched path.

### Testing the Mock Response

After setting the mock response, any requests matching the `path_template` will return the configured response.

**Send a Request to a Matching Path:**

```bash
curl -X GET "http://localhost:8000/user/123/details"
```

**Expected Response:**

```json
{
  "status": "success"
}
```

**Send Another Request with a Different Parameter:**

```bash
curl -X GET "http://localhost:8000/user/XYZ/details"
```

**Expected Response:**

```json
{
  "status": "success"
}
```

### Configuring Your Service Under Test

Point your service under test to the mock API server by changing the API endpoints to `http://localhost:8000` (or the appropriate network address if running in a containerized environment).

## Configuration

- **Port Configuration**: Modify the `docker-compose.yml` or `uvicorn` command to change the port.
- **Logging**: By default, the server logs requests to the console. You can modify `app/main.py` to log to a file or adjust the log format.
- **Response Customization**: Use the `/mock-response` endpoint to configure custom responses for specific path templates.

## Project Structure

```
mocker/
├── app/
│   └── main.py          # FastAPI application
├── Dockerfile           # Docker image definition
├── docker-compose.yml   # Docker Compose configuration
└── requirements.txt     # Python dependencies
```

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**
2. **Create a Feature Branch**

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Commit Your Changes**

   ```bash
   git commit -am 'Add a new feature'
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/YourFeature
   ```

5. **Open a Pull Request**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework for building APIs with Python 3.7+.
- [Uvicorn](https://www.uvicorn.org/) - A lightning-fast ASGI server implementation.
- [Docker](https://www.docker.com/) - Platform for developing, shipping, and running applications in containers.
