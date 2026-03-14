# Callback Debug Server

A FastAPI-based callback debugging server that captures and logs all incoming HTTP requests for debugging webhooks, callbacks, and other HTTP integrations.

## Features

- **Capture All Paths**: Accepts requests to any path (`/{path:path}`)
- **All HTTP Methods**: GET, POST, PUT, DELETE, PATCH, OPTIONS, HEAD
- **Detailed Logging**:
  - Request timestamp, method, and URL
  - Request headers
  - Query parameters
  - Request body (automatically tries to format JSON)
  - Client IP and port
  - Response status code and processing time
- **Dual Output**: Logs to both console and file
- **Log Rotation**: Automatic rotation, max 10MB per file, keeps 10 backups

## Quick Start

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Server

```bash
python main.py
```

The server starts at `http://localhost:8000`.

### Send Test Requests

```bash
# GET request
curl http://localhost:8000/test

# POST request (JSON)
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{"event": "payment", "data": {"id": 123, "amount": 99.99}}'

# POST request (form data)
curl -X POST http://localhost:8000/callback \
  -d "name=test&value=hello"

# Request with query parameters
curl "http://localhost:8000/api?token=abc123&version=2"
```

### View Logs

All request logs are saved to `callback.log` and also printed to the console.

## Project Structure

```
callback-printer/
├── main.py           # Main application entry point
├── requirements.txt  # Python dependencies
└── callback.log      # Log file (generated at runtime)
```

## Configuration

To modify server settings, edit the following parameters in `main.py`:

- **Port**: Change `port=8000` in `uvicorn.run()`
- **Log file size**: Change `maxBytes=10*1024*1024` (default 10MB)
- **Backup count**: Change `backupCount=10`

## API Response Format

All requests return the following response format:

```json
{
  "status": "success",
  "message": "Path /xxx POST request received",
  "received_at": "2026-03-14T12:00:00",
  "path": "xxx",
  "method": "POST"
}
```

## Use Cases

- Debug third-party API callback notifications
- Test webhook integrations
- Capture and analyze HTTP request data
- API integration testing
- Inspect request headers and body content

## Docker Deployment

### Run Container

```bash
docker run -d -p 8000:8000 --name callback-printer ghcr.io/tursom/callback-printer:latest
```

## License

MIT License - see [LICENSE](LICENSE) file for details.
