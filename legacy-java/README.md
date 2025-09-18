# Insurance Claims API

A Spring Boot REST API for managing insurance claims with Java 11 and Maven.

## Features

- Submit new insurance claims via REST API
- Retrieve claim status and details
- In-memory storage using HashMap
- Basic validation for request data
- Global exception handling
- Unit tests included

## API Endpoints

### Submit a New Claim
```
POST /api/claims
Content-Type: application/json

{
    "customerId": 12345,
    "claimType": "Auto",
    "description": "Car accident on highway"
}
```

**Response (201 Created):**
```json
{
    "id": 1,
    "customerId": 12345,
    "claimType": "Auto",
    "description": "Car accident on highway",
    "status": "SUBMITTED",
    "createdAt": "2025-06-19T10:30:00",
    "updatedAt": "2025-06-19T10:30:00"
}
```

### Retrieve Claim Status
```
GET /api/claims/{id}
```

**Response (200 OK):**
```json
{
    "id": 1,
    "customerId": 12345,
    "claimType": "Auto",
    "description": "Car accident on highway",
    "status": "SUBMITTED",
    "createdAt": "2025-06-19T10:30:00",
    "updatedAt": "2025-06-19T10:30:00"
}
```

**Response (404 Not Found):** When claim ID doesn't exist

### Health Check
```
GET /api/claims/health
```

## Claim Statuses

- `SUBMITTED` - Initial status when claim is created
- `UNDER_REVIEW` - Claim is being reviewed
- `APPROVED` - Claim has been approved
- `DENIED` - Claim has been denied
- `CLOSED` - Claim processing is complete

## Validation Rules

- `customerId`: Required, must be a valid Long
- `claimType`: Required, cannot be blank
- `description`: Required, cannot be blank

## Building and Running

### Prerequisites
- Java 11
- Maven 3.6+

### Build the application
```bash
mvn clean compile
```

### Run tests
```bash
mvn test
```

### Run the application
```bash
mvn spring-boot:run
```

The application will start on `http://localhost:8080/api`

### Package as JAR
```bash
mvn clean package
java -jar target/claims-api-1.0.0.jar
```

## Project Structure

```
src/
├── main/
│   ├── java/com/insurance/claims/
│   │   ├── ClaimsApiApplication.java       # Main Spring Boot application
│   │   ├── controller/
│   │   │   └── ClaimController.java        # REST endpoints
│   │   ├── service/
│   │   │   └── ClaimService.java          # Business logic
│   │   ├── model/
│   │   │   ├── Claim.java                 # Claim entity
│   │   │   └── ClaimStatus.java           # Status enum
│   │   ├── dto/
│   │   │   └── ClaimRequest.java          # Request DTO
│   │   └── exception/
│   │       └── GlobalExceptionHandler.java # Error handling
│   └── resources/
│       └── application.properties          # Configuration
└── test/
    └── java/com/insurance/claims/
        ├── controller/
        │   └── ClaimControllerTest.java    # Controller tests
        └── service/
            └── ClaimServiceTest.java       # Service tests
```

## Notes

- Data is stored in-memory using HashMap and will be lost when the application stops
- The application includes 3 hardcoded claims for testing:
  - **Claim ID 1**: Auto claim (Customer 12345) - Status: UNDER_REVIEW
  - **Claim ID 2**: Home claim (Customer 67890) - Status: APPROVED  
  - **Claim ID 3**: Health claim (Customer 11111) - Status: SUBMITTED

- Auto-incrementing IDs continue from 4 for new claims
- All timestamps are in UTC format
- Global exception handler provides consistent error responses with validation details
