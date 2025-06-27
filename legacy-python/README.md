# Customer Profile Service

A Python 3.8 customer profile service using Python's built-in `http.server` module for maximum compatibility.

## Features

- **GET /customers/{id}** - Fetch a customer's profile by ID
- **GET /customers/{id}/risk-profile** - Get customer risk assessment for insurance underwriting
- **PATCH /customers/{id}** - Update customer fields (phone number, address, email)
- Hardcoded test data for 3 customers:
  - Julia Kordick (ID: 1)
  - Dr. Alexander Wachtel (ID: 2)
  - Igor Rykhlevskyi (ID: 3)
- No external dependencies (except for testing)
- Uses only Python standard library for maximum compatibility

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Service

Start the development server:
```bash
python main.py
```

The service will be available at `http://localhost:8000`

## Usage Examples

### Get a customer profile
```bash
curl -X GET "http://localhost:8000/customers/1"
```

### Get customer risk assessment
```bash
curl -X GET "http://localhost:8000/customers/1/risk-profile"
```

### Update customer phone number
```bash
curl -X PATCH "http://localhost:8000/customers/1" \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+1-555-9999"}'
```

### Update customer address and email
```bash
curl -X PATCH "http://localhost:8000/customers/2" \
  -H "Content-Type: application/json" \
  -d '{"address": "New Address St 123", "email": "new.email@example.com"}'
```

## Testing

Run the test suite:
```bash
pip install pytest
pytest test_main.py -v
```

## Project Structure

```
legacy-python/
├── main.py           # HTTP server application entry point
├── models.py         # Customer model and validation functions
├── database.py       # In-memory database simulation
├── risk_calculator.py # Risk assessment calculation logic
├── test_main.py      # Test suite for main application
├── test_risk_calculator.py # Test suite for risk calculator
├── requirements.txt  # Python dependencies (minimal)
└── README.md         # This file
```

## API Endpoints

### GET /customers/{id}
Fetch a customer's complete profile.

**Response Example:**
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

### PATCH /customers/{id}
Update customer fields. Only provided fields will be updated.

**Request Body Example:**
```json
{
  "phone_number": "+1-555-9999",
  "address": "456 New Street, Updated City, UC 12345"
}
```

**Updatable Fields:**
- `phone_number` (string)
- `address` (string)
- `email` (string)

### GET /customers/{id}/risk-profile
Calculate and return insurance risk assessment for a customer.

**Response Example:**
```json
{
  "customer_id": 1,
  "risk_score": 82,
  "risk_level": "MODERATE",
  "risk_factors": {
    "age_factor": {
      "score": 85,
      "description": "Age 40 - lower risk demographic"
    },
    "location_factor": {
      "score": 70,
      "description": "Urban area - moderate crime rates"
    },
    "profile_completeness": {
      "score": 95,
      "description": "Complete profile with verified contact info"
    }
  },
  "recommendations": [
    "Standard coverage recommended",
    "Monitor profile for improvements"
  ],
  "calculated_at": "2025-06-27T09:52:06.839127Z",
  "expires_at": "2025-07-04T09:52:06.839127Z"
}
```

**Risk Calculation Logic:**
- **Age Factor (30% weight)**: Based on customer's age from date_of_birth
- **Location Factor (40% weight)**: Based on address zip code analysis  
- **Profile Completeness (30% weight)**: Based on data quality and completeness

**Risk Levels:**
- **LOW** (85-100): Preferred rates eligible
- **MODERATE** (70-84): Standard coverage
- **HIGH** (0-69): Enhanced screening recommended

## Test Data

The service includes three hardcoded customers:

1. **Julia Kordick** (ID: 1)
   - Email: julia.kordick@example.com
   - Phone: +1-555-0123
   - Address: 123 Main St, New York, NY 10001

2. **Alexander Wachtel** (ID: 2) 
   - Email: alexander.wachtel@example.com
   - Phone: +1-555-0456
   - Address: 456 Oak Ave, Boston, MA 02101

3. **Igor Rykhlevskyi** (ID: 3)
   - Email: igor.rykhlevskyi@example.com
   - Phone: +1-555-0789
   - Address: 789 Pine Rd, San Francisco, CA 94102
