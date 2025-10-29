# Customer Profile Service - Technical Documentation

## Overview

The Customer Profile Service is a lightweight HTTP API built using Python's standard library `http.server` module. It provides RESTful endpoints for managing customer profile data with an in-memory database simulation.

## Architecture

### High-Level Design

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   HTTP Client   │───▶│  HTTP Server    │───▶│   Database      │
│   (curl, web)   │    │  (main.py)      │    │  (database.py)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │     Models      │
                       │   (models.py)   │
                       └─────────────────┘
```

### Components

#### 1. HTTP Server (`main.py`)
- **Framework**: Python's built-in `http.server.HTTPServer`
- **Handler**: Custom `CustomerProfileHandler` extending `BaseHTTPRequestHandler`
- **Port**: 8000 (configurable)
- **Protocol**: HTTP/1.1
- **CORS**: Enabled for cross-origin requests

#### 2. Data Models (`models.py`)
- **Customer Class**: Core data structure with serialization methods
- **Validation**: Simple field validation for updates
- **Serialization**: JSON conversion with proper datetime formatting

#### 3. Database Layer (`database.py`)
- **Type**: In-memory dictionary-based storage
- **Persistence**: Data exists only during runtime
- **Operations**: GET, UPDATE (no CREATE/DELETE for this demo)
- **Concurrency**: Single-threaded (no locking required)

## API Specification

### Base URL
```
http://localhost:8000
```

### Endpoints

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| GET | `/` | Service information | 200 |
| GET | `/health` | Health check | 200 |
| GET | `/customers/{id}` | Get customer profile | 200, 400, 404 |
| PATCH | `/customers/{id}` | Update customer | 200, 400, 404, 422 |

### Request/Response Format

#### Content-Type
- **Request**: `application/json` (for PATCH)
- **Response**: `application/json`

#### Error Response Structure
```json
{
  "error": "Error message description"
}
```

## Data Model

### Customer Entity

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | Integer | Yes | Unique customer identifier |
| `first_name` | String | Yes | Customer's first name |
| `last_name` | String | Yes | Customer's last name |
| `email` | String | Yes | Email address |
| `phone_number` | String | Yes | Phone number |
| `address` | String | Yes | Physical address |
| `date_of_birth` | String | Yes | Birth date (YYYY-MM-DD) |
| `created_at` | DateTime | Yes | Record creation timestamp |
| `updated_at` | DateTime | Yes | Last modification timestamp |

### Updatable Fields
Only the following fields can be modified via PATCH:
- `phone_number` (10-20 characters)
- `address` (5-200 characters)  
- `email` (must contain '@')

## Implementation Details

### Request Processing Flow

1. **Request Reception**: HTTP server receives request
2. **Route Matching**: URL pattern matching using regex
3. **Validation**: Input validation and sanitization
4. **Business Logic**: Customer lookup/update operations
5. **Response Generation**: JSON serialization and HTTP response

### Error Handling

#### Client Errors (4xx)
- **400 Bad Request**: Invalid customer ID, malformed JSON
- **404 Not Found**: Customer not found, invalid endpoint
- **422 Unprocessable Entity**: Validation failures

#### Server Errors (5xx)
- **500 Internal Server Error**: Unexpected server-side errors

### Validation Rules

#### Customer ID
- Must be a positive integer
- Range: 1 to N (where N is the maximum customer ID)

#### Phone Number
- Length: 10-20 characters
- Format: Any string (no specific format enforced)

#### Address
- Length: 5-200 characters
- Format: Free text

#### Email
- Must contain '@' character
- Basic format validation only

## Configuration

### Environment Variables
None required - all configuration is hardcoded for simplicity.

### Dependencies
- **Runtime**: Python 3.12+ standard library only
- **Testing**: pytest, requests

## Performance Characteristics

### Scalability
- **Concurrent Users**: Limited by Python GIL and single-threaded server
- **Memory Usage**: O(n) where n = number of customers
- **Response Time**: Sub-millisecond for in-memory operations

### Limitations
- No persistent storage
- No authentication/authorization
- No rate limiting
- Single-threaded request handling
- No logging to files

## Security Considerations

### Current State
- **Authentication**: None
- **Authorization**: None
- **Input Validation**: Basic
- **CORS**: Permissive (allows all origins)

### Recommendations for Production
1. Add authentication (API keys, JWT)
2. Implement proper input sanitization
3. Add rate limiting
4. Use HTTPS
5. Implement proper logging
6. Add database persistence
7. Use a production-grade WSGI server

## Testing Strategy

### Test Coverage Areas
- Endpoint functionality (GET, PATCH)
- Error handling (404, 400, 422)
- Data validation
- Business logic
- Response formatting

### Test Approach
- Unit tests for individual components
- Integration tests for API endpoints
- Manual testing with curl commands

## Deployment

### Local Development
```bash
python main.py
```

### Production Considerations
- Use reverse proxy (nginx)
- Implement process management (systemd, supervisor)
- Add monitoring and alerting
- Implement proper logging
- Use environment-based configuration

## Monitoring and Observability

### Current Logging
- Console logging for requests
- Timestamp-based log format
- Basic request/response logging

### Metrics (Not Implemented)
- Request count
- Response times
- Error rates
- Customer access patterns

## Future Enhancements

### Short Term
1. Add CREATE and DELETE operations
2. Implement proper logging to files
3. Add configuration file support
4. Improve error messages

### Long Term
1. Database persistence (SQLite, PostgreSQL)
2. Authentication and authorization
3. API versioning
4. Swagger/OpenAPI documentation
5. Containerization (Docker)
6. Microservice architecture

## Development Guidelines

### Code Style
- Follow PEP 8 Python style guide
- Use type hints where applicable
- Maintain clear separation of concerns
- Add docstrings for all public methods

### Git Workflow
- Feature branches for new functionality
- Code review before merging
- Semantic versioning for releases

### Testing
- Minimum 80% test coverage
- Test all error conditions
- Integration tests for API endpoints
