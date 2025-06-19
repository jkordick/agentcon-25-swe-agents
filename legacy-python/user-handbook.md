# Customer Profile Service - User Handbook

## Introduction

Welcome to the Customer Profile Service! This handbook provides everything you need to know to effectively use our customer management API. Whether you're a developer integrating with our service or testing the API manually, this guide will help you get started quickly.

## Getting Started

### Service Information

- **Base URL**: `http://localhost:8000`
- **Protocol**: HTTP/1.1
- **Data Format**: JSON
- **Authentication**: None required (demo service)

### Quick Health Check

Before using the API, verify the service is running:

```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "customer-profile-service",
  "timestamp": "2025-06-19T19:15:30.123456"
}
```

## Available Customers

The service comes pre-loaded with three test customers:

| ID | Name | Email | Phone | Location |
|----|------|-------|-------|----------|
| 1 | Julia Kordick | julia.kordick@example.com | +1-555-0123 | New York, NY |
| 2 | Alexander Wachtel | alexander.wachtel@example.com | +1-555-0456 | Boston, MA |
| 3 | Igor Rykhlevskyi | igor.rykhlevskyi@example.com | +1-555-0789 | San Francisco, CA |

## API Operations

### 1. Retrieve Customer Profile

Get complete information about a specific customer.

**Endpoint:** `GET /customers/{id}`

**Example:**
```bash
curl -X GET "http://localhost:8000/customers/1"
```

**Response:**
```json
{
  "id": 1,
  "first_name": "Julia",
  "last_name": "Kordick",
  "email": "julia.kordick@example.com",
  "phone_number": "+1-555-0123",
  "address": "123 Main St, New York, NY 10001",
  "date_of_birth": "1985-03-15",
  "created_at": "2025-01-01T10:00:00",
  "updated_at": "2025-01-01T10:00:00"
}
```

### 2. Update Customer Information

Modify specific fields in a customer's profile. You can update one or more fields in a single request.

**Endpoint:** `PATCH /customers/{id}`

**Updatable Fields:**
- `phone_number`: Customer's phone number
- `address`: Customer's physical address  
- `email`: Customer's email address

#### Update Phone Number

```bash
curl -X PATCH "http://localhost:8000/customers/1" \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+1-555-9999"}'
```

#### Update Address

```bash
curl -X PATCH "http://localhost:8000/customers/2" \
  -H "Content-Type: application/json" \
  -d '{"address": "456 New Street, Boston, MA 02102"}'
```

#### Update Email

```bash
curl -X PATCH "http://localhost:8000/customers/3" \
  -H "Content-Type: application/json" \
  -d '{"email": "igor.new@example.com"}'
```

#### Update Multiple Fields

```bash
curl -X PATCH "http://localhost:8000/customers/1" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+1-555-8888",
    "address": "789 Updated Ave, New York, NY 10002",
    "email": "julia.updated@example.com"
  }'
```

**Response Example:**
```json
{
  "id": 1,
  "first_name": "Julia",
  "last_name": "Kordick",
  "email": "julia.updated@example.com",
  "phone_number": "+1-555-8888",
  "address": "789 Updated Ave, New York, NY 10002",
  "date_of_birth": "1985-03-15",
  "created_at": "2025-01-01T10:00:00",
  "updated_at": "2025-06-19T19:15:30.123456"
}
```

## Using Different Tools

### cURL Examples

#### Windows Command Prompt
```cmd
curl -X GET "http://localhost:8000/customers/1"

curl -X PATCH "http://localhost:8000/customers/1" ^
  -H "Content-Type: application/json" ^
  -d "{\"phone_number\": \"+1-555-9999\"}"
```

#### PowerShell
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/customers/1" -Method Get

$body = @{
    phone_number = "+1-555-9999"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/customers/1" -Method Patch -Body $body -ContentType "application/json"
```

### Programming Language Examples

#### Python
```python
import requests

# Get customer
response = requests.get('http://localhost:8000/customers/1')
customer = response.json()
print(customer)

# Update customer
update_data = {
    'phone_number': '+1-555-9999',
    'email': 'new.email@example.com'
}
response = requests.patch('http://localhost:8000/customers/1', json=update_data)
updated_customer = response.json()
print(updated_customer)
```

#### JavaScript (Node.js)
```javascript
const fetch = require('node-fetch');

// Get customer
async function getCustomer(id) {
    const response = await fetch(`http://localhost:8000/customers/${id}`);
    const customer = await response.json();
    console.log(customer);
    return customer;
}

// Update customer
async function updateCustomer(id, updates) {
    const response = await fetch(`http://localhost:8000/customers/${id}`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(updates)
    });
    const updatedCustomer = await response.json();
    console.log(updatedCustomer);
    return updatedCustomer;
}

// Usage
getCustomer(1);
updateCustomer(1, { phone_number: '+1-555-9999' });
```

#### Java
```java
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URI;

// Get customer
HttpClient client = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("http://localhost:8000/customers/1"))
    .GET()
    .build();

HttpResponse<String> response = client.send(request, 
    HttpResponse.BodyHandlers.ofString());
System.out.println(response.body());

// Update customer
String jsonBody = "{\"phone_number\": \"+1-555-9999\"}";
HttpRequest updateRequest = HttpRequest.newBuilder()
    .uri(URI.create("http://localhost:8000/customers/1"))
    .header("Content-Type", "application/json")
    .method("PATCH", HttpRequest.BodyPublishers.ofString(jsonBody))
    .build();

HttpResponse<String> updateResponse = client.send(updateRequest,
    HttpResponse.BodyHandlers.ofString());
System.out.println(updateResponse.body());
```

## Error Handling

### Common Error Responses

#### Customer Not Found (404)
```bash
curl -X GET "http://localhost:8000/customers/999"
```
```json
{
  "error": "Customer with ID 999 not found"
}
```

#### Invalid Customer ID (400)
```bash
curl -X GET "http://localhost:8000/customers/0"
```
```json
{
  "error": "Customer ID must be a positive integer"
}
```

#### No Update Data Provided (400)
```bash
curl -X PATCH "http://localhost:8000/customers/1" \
  -H "Content-Type: application/json" \
  -d '{}'
```
```json
{
  "error": "At least one updatable field must be provided (phone_number, address, email)"
}
```

#### Validation Error (422)
```bash
curl -X PATCH "http://localhost:8000/customers/1" \
  -H "Content-Type: application/json" \
  -d '{"email": "invalid-email"}'
```
```json
{
  "error": "Validation error: email must be a valid email address"
}
```

#### Malformed JSON (400)
```bash
curl -X PATCH "http://localhost:8000/customers/1" \
  -H "Content-Type: application/json" \
  -d '{"phone_number": +1-555-9999}'
```
```json
{
  "error": "Invalid JSON data"
}
```

## Validation Rules

### Phone Number
- **Length**: 10-20 characters
- **Format**: Any string (flexible format)
- **Examples**: 
  - ✅ `"+1-555-1234"`
  - ✅ `"555.123.4567"`
  - ✅ `"(555) 123-4567"`
  - ❌ `"123"` (too short)

### Address
- **Length**: 5-200 characters
- **Format**: Free text
- **Examples**:
  - ✅ `"123 Main St, City, State 12345"`
  - ✅ `"Apt 4B, 456 Oak Avenue"`
  - ❌ `"123"` (too short)

### Email
- **Format**: Must contain '@' character
- **Examples**:
  - ✅ `"user@example.com"`
  - ✅ `"test.email+tag@domain.co.uk"`
  - ❌ `"invalid-email"` (missing @)

## Best Practices

### 1. Always Check Status Codes
```python
response = requests.get('http://localhost:8000/customers/1')
if response.status_code == 200:
    customer = response.json()
    # Process customer data
elif response.status_code == 404:
    print("Customer not found")
else:
    print(f"Error: {response.status_code}")
```

### 2. Handle Errors Gracefully
```javascript
async function safeGetCustomer(id) {
    try {
        const response = await fetch(`http://localhost:8000/customers/${id}`);
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error);
        }
        return await response.json();
    } catch (error) {
        console.error('Failed to get customer:', error.message);
        return null;
    }
}
```

### 3. Validate Data Before Sending
```python
def update_customer(customer_id, updates):
    # Validate phone number
    if 'phone_number' in updates:
        phone = updates['phone_number']
        if len(phone) < 10 or len(phone) > 20:
            raise ValueError("Phone number must be 10-20 characters")
    
    # Validate email
    if 'email' in updates:
        email = updates['email']
        if '@' not in email:
            raise ValueError("Email must contain @ character")
    
    # Send update
    return requests.patch(f'http://localhost:8000/customers/{customer_id}', 
                         json=updates)
```

## Testing Scenarios

### Scenario 1: Customer Onboarding Update
```bash
# Customer Julia just moved and changed her phone
curl -X PATCH "http://localhost:8000/customers/1" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+1-555-NEW1",
    "address": "789 New Apartment, Brooklyn, NY 11201"
  }'
```

### Scenario 2: Email Migration
```bash
# Company email migration - update all customers
curl -X PATCH "http://localhost:8000/customers/1" \
  -H "Content-Type: application/json" \
  -d '{"email": "julia.kordick@newdomain.com"}'

curl -X PATCH "http://localhost:8000/customers/2" \
  -H "Content-Type: application/json" \
  -d '{"email": "alexander.wachtel@newdomain.com"}'

curl -X PATCH "http://localhost:8000/customers/3" \
  -H "Content-Type: application/json" \
  -d '{"email": "igor.rykhlevskyi@newdomain.com"}'
```

### Scenario 3: Data Verification
```bash
# Get all customers to verify current state
for id in 1 2 3; do
  echo "Customer $id:"
  curl -X GET "http://localhost:8000/customers/$id" | jq '.'
  echo ""
done
```

## Troubleshooting

### Service Not Responding
1. **Check if service is running**: `curl http://localhost:8000/health`
2. **Verify port**: Ensure port 8000 is not blocked
3. **Check logs**: Look at server console output for errors

### Invalid JSON Errors
1. **Validate JSON**: Use online JSON validators
2. **Check quotes**: Ensure all strings are properly quoted
3. **Escape characters**: Properly escape quotes in command line

### Validation Failures
1. **Check field lengths**: Verify phone (10-20 chars), address (5-200 chars)
2. **Email format**: Ensure email contains '@'
3. **Required fields**: Only update allowed fields (phone_number, address, email)

## Limitations

### Current Service Limitations
- **No user authentication** - Anyone can access any customer
- **No data persistence** - Data resets when service restarts
- **Limited customers** - Only 3 predefined customers (IDs 1, 2, 3)
- **No customer creation** - Cannot add new customers
- **No customer deletion** - Cannot remove customers
- **Single-threaded** - May be slow under high load

### Working Within Limitations
- **Test with existing customers** - Use IDs 1, 2, or 3 only
- **Save important changes** - Document any critical updates elsewhere
- **Plan for resets** - Service data returns to original state on restart

## Support

For questions or issues with this API:

1. **Check the health endpoint** first: `/health`
2. **Review error messages** - they provide specific guidance
3. **Verify request format** - ensure proper JSON and headers
4. **Test with simple examples** - start with basic GET requests
5. **Check technical documentation** for implementation details

## Changelog

### Version 1.0.0
- Initial release with GET and PATCH operations
- Support for 3 predefined customers
- Basic validation for phone, email, and address fields
- CORS support for web applications
