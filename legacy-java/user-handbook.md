# Insurance Claims API - User Handbook

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [API Endpoints](#api-endpoints)
4. [Request Examples](#request-examples)
5. [Response Formats](#response-formats)
6. [Error Handling](#error-handling)
7. [Best Practices](#best-practices)
8. [Deprecated Endpoints](#deprecated-endpoints)
9. [Troubleshooting](#troubleshooting)

## Introduction

Welcome to the Insurance Claims API User Handbook. This guide will help you understand how to interact with our REST API for managing insurance claims. The API allows you to submit new claims, retrieve claim information, and monitor claim status updates.

### What You Can Do
- Submit new insurance claims with detailed information
- Retrieve complete claim details including current status
- Monitor the processing progress of your claims
- Access claim history and timestamps

### Base URL
All API requests should be made to: `http://localhost:8080/api`

## Getting Started

### Prerequisites
- API access credentials (if authentication is enabled)
- HTTP client (curl, Postman, or programming language HTTP library)
- Basic understanding of REST APIs and JSON format

### Quick Start
1. Ensure the API server is running on port 8080
2. Test connectivity with the health check endpoint
3. Try retrieving an existing claim (IDs 1-3 are pre-loaded)
4. Submit your first claim

### Authentication
Currently, the API does not require authentication. Future versions will implement JWT-based authentication.

## API Endpoints

### 1. Health Check
**Purpose**: Verify API availability and get basic statistics

```
GET /api/claims/health
```

**Response**: Simple text message with claim count

---

### 2. Submit New Claim
**Purpose**: Create a new insurance claim

```
POST /api/claims
Content-Type: application/json
```

**Required Fields**:
- `customerId` (number): Unique customer identifier
- `claimType` (string): Type of insurance claim
- `description` (string): Detailed description of the claim

---

### 3. Retrieve Claim Details
**Purpose**: Get complete information about a specific claim

```
GET /api/claims/{id}
```

**Parameters**:
- `id` (number): Unique claim identifier

---

---

## Request Examples

### Submitting a New Auto Insurance Claim

```bash
curl -X POST http://localhost:8080/api/claims \
  -H "Content-Type: application/json" \
  -d '{
    "customerId": 12345,
    "claimType": "Auto",
    "description": "Vehicle collision at intersection of Main St and Oak Ave"
  }'
```

### Submitting a Home Insurance Claim

```bash
curl -X POST http://localhost:8080/api/claims \
  -H "Content-Type: application/json" \
  -d '{
    "customerId": 67890,
    "claimType": "Home",
    "description": "Storm damage to roof and windows from hurricane"
  }'
```

### Submitting a Health Insurance Claim

```bash
curl -X POST http://localhost:8080/api/claims \
  -H "Content-Type: application/json" \
  -d '{
    "customerId": 11111,
    "claimType": "Health",
    "description": "Emergency surgery for appendicitis at City General Hospital"
  }'
```

### Retrieving Claim Information

```bash
# Get full details for claim ID 1
curl http://localhost:8080/api/claims/1

# Get full details for claim ID 2
curl http://localhost:8080/api/claims/2

# Check API health and claim count
curl http://localhost:8080/api/claims/health
```

## Response Formats

### Successful Claim Submission (HTTP 201)

```json
{
  "id": 4,
  "customerId": 12345,
  "claimType": "Auto",
  "description": "Vehicle collision at intersection of Main St and Oak Ave",
  "status": "SUBMITTED",
  "createdAt": "2025-06-19T14:30:00",
  "updatedAt": "2025-06-19T14:30:00"
}
```

### Successful Claim Retrieval (HTTP 200)

```json
{
  "id": 1,
  "customerId": 12345,
  "claimType": "Auto",
  "description": "Car accident on highway - rear-end collision",
  "status": "UNDER_REVIEW",
  "createdAt": "2025-06-19T10:00:00",
  "updatedAt": "2025-06-19T12:30:00"
}
```



### Claim Status Values

| Status | Description |
|--------|-------------|
| `SUBMITTED` | Claim has been received and is queued for review |
| `UNDER_REVIEW` | Claim is being actively processed by our team |
| `APPROVED` | Claim has been approved for payment |
| `DENIED` | Claim has been rejected (reason provided separately) |
| `CLOSED` | Claim processing is complete |

## Error Handling

### Validation Errors (HTTP 400)

```json
{
  "error": "Validation failed",
  "message": "One or more fields have validation errors",
  "timestamp": "2025-06-19T14:30:00",
  "validationErrors": {
    "customerId": "Customer ID is required",
    "claimType": "Claim type is required",
    "description": "Description is required"
  }
}
```

### Claim Not Found (HTTP 404)

When requesting a claim that doesn't exist, you'll receive an HTTP 404 status with an empty response body.

### Server Error (HTTP 500)

```json
{
  "error": "Internal server error",
  "message": "An unexpected error occurred",
  "timestamp": "2025-06-19T14:30:00",
  "validationErrors": null
}
```

## Best Practices

### 1. Request Formatting
- Always include the `Content-Type: application/json` header for POST requests
- Ensure JSON is properly formatted and valid
- Use meaningful descriptions (minimum 10 characters recommended)

### 2. Error Handling
- Always check HTTP status codes before processing responses
- Implement retry logic for 5xx server errors
- Handle validation errors gracefully in your application

### 3. Performance
- Cache claim data when appropriate to reduce API calls
- Use the health check endpoint to verify API availability
- Use the full claim details endpoint to get complete claim information including status
- Implement timeouts for your HTTP requests (recommended: 30 seconds)

### 4. Data Validation
- Validate customer IDs exist in your system before submitting claims
- Use standardized claim types (Auto, Home, Health, Life, etc.)
- Provide detailed, accurate descriptions to speed up processing

### 5. Monitoring
- Log all API interactions for debugging purposes
- Monitor response times and implement alerting
- Track claim submission success rates

## Deprecated Endpoints

*Currently, there are no deprecated endpoints in this API version.*

## Troubleshooting

### Common Issues

#### 1. Connection Refused
**Problem**: Cannot connect to the API
**Solution**: 
- Verify the server is running on port 8080
- Check if the context path `/api` is included in your URL
- Ensure no firewall is blocking the connection

#### 2. 400 Bad Request
**Problem**: Request validation failed
**Solutions**:
- Check that all required fields are included
- Verify JSON format is valid
- Ensure data types match requirements (numbers for IDs)
- Confirm Content-Type header is set to `application/json`

#### 3. 404 Not Found
**Problem**: Claim ID doesn't exist
**Solutions**:
- Verify the claim ID is correct
- Check if the claim was successfully created
- Ensure you're using the correct endpoint URL

#### 4. Slow Response Times
**Problem**: API responses are delayed
**Solutions**:
- Check server resources and memory usage
- Verify network connectivity
- Consider the number of claims in memory (affects performance)

### Getting Help

If you encounter issues not covered in this handbook:

1. **Check the API Health**: Use `GET /api/claims/health` to verify the service is running
2. **Review Error Messages**: Pay attention to validation error details
3. **Verify Request Format**: Ensure JSON syntax and required fields are correct
4. **Check Server Logs**: Look for error messages in the application logs
5. **Contact Support**: Reach out to the development team with specific error details

### Sample Test Data

The API comes pre-loaded with three test claims you can use for testing:

| Claim ID | Customer ID | Type | Status | Description |
|----------|-------------|------|--------|-------------|
| 1 | 12345 | Auto | UNDER_REVIEW | Car accident on highway - rear-end collision |
| 2 | 67890 | Home | APPROVED | Water damage from burst pipe in basement |
| 3 | 11111 | Health | SUBMITTED | Emergency room visit for broken arm |

### API Limits

**Current Limitations**:
- No rate limiting implemented
- Claims are stored in memory (lost on restart)
- No authentication required
- Maximum description length: 1000 characters (recommended)

**Future Enhancements**:
- Database persistence
- User authentication and authorization
- Rate limiting and quotas
- Claim attachment support
- Email notifications for status updates

---

**Last Updated**: June 19, 2025  
**API Version**: 1.0.0  
**Support Contact**: development-team@insurance-company.com
