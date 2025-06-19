# Technical Documentation - Insurance Quote API

## Overview

The Insurance Quote API is a Node.js 16 REST service designed to calculate insurance premium quotes based on vehicle type and driver age. The system implements a modular architecture with clear separation of concerns, comprehensive input validation, and business logic encapsulation.

## Architecture

### System Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Express App   │───▶│   Route Layer   │───▶│  Service Layer  │
│    (index.js)   │    │  (routes/*)     │    │ (services/*)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Middleware    │    │   Controllers   │    │ Business Logic  │
│ (CORS, JSON)    │    │ (HTTP Handling) │    │ (Calculations)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Layer Responsibilities

1. **Express Application Layer** (`index.js`)
   - Server initialization and configuration
   - Middleware setup (CORS, JSON parsing)
   - Route registration
   - Global error handling
   - Health check endpoint

2. **Route Layer** (`routes/quote.js`)
   - HTTP request/response handling
   - Input validation coordination
   - Service layer invocation
   - Error response formatting

3. **Service Layer** (`services/quoteService.js`)
   - Core business logic implementation
   - Premium calculation algorithms
   - Input validation logic
   - Data transformation

## Core Implementation Details

### Premium Calculation Algorithm

The premium calculation follows a multi-step process:

```javascript
Premium = BaseRate × AgeMultiplier × ConditionalAdjustments
```

#### Step 1: Base Rate Determination
```javascript
const VEHICLE_BASE_RATES = {
  'car': 1200,        // Standard passenger vehicle
  'truck': 1800,      // Commercial/heavy vehicle
  'motorcycle': 800,  // Two-wheeled vehicle
  'suv': 1500,        // Sport utility vehicle
  'van': 1400         // Multi-purpose vehicle
};
```

#### Step 2: Age-Based Risk Assessment
```javascript
const AGE_MULTIPLIERS = {
  'young': 1.8,    // Ages 16-25 (high risk)
  'adult': 1.0,    // Ages 26-65 (standard risk)
  'senior': 1.3    // Ages 66+ (moderate risk)
};
```

#### Step 3: Conditional Adjustments
The system applies additional risk factors based on specific combinations:

1. **Young Motorcycle Riders** (age < 21 + motorcycle)
   - Additional 50% penalty (×1.5)
   - Rationale: Statistical high-risk combination

2. **Senior Truck Drivers** (age > 70 + truck)
   - Additional 20% penalty (×1.2)
   - Rationale: Physical demands and vehicle size

3. **Prime Age Car Drivers** (age 30-50 + car)
   - 10% discount (×0.9)
   - Rationale: Experienced, responsible demographic

### Input Validation Strategy

The service implements comprehensive input validation with multiple layers:

#### Vehicle Type Validation
```javascript
function validateVehicleType(vehicleType) {
  // Check presence and type
  if (!vehicleType || typeof vehicleType !== 'string') {
    return false;
  }
  
  // Normalize and validate against supported types
  const normalized = vehicleType.toLowerCase();
  return VEHICLE_BASE_RATES.hasOwnProperty(normalized);
}
```

#### Driver Age Validation
```javascript
function validateDriverAge(driverAge) {
  // Type checking
  if (!driverAge || typeof driverAge !== 'number') {
    return false;
  }
  
  // Range validation (legal driving age to reasonable maximum)
  return driverAge >= 16 && driverAge <= 100;
}
```

### Business Logic Implementation

#### Age Categorization Logic
```javascript
function getAgeCategory(age) {
  if (age >= 16 && age <= 25) return 'young';
  if (age >= 26 && age <= 65) return 'adult';
  return 'senior'; // 66+
}
```

#### Premium Classification
The system categorizes premiums into two tiers:
- **Premium**: Standard rates (≤ $2,500)
- **Peasant**: High-risk rates (> $2,500)

This classification helps identify policies that may require additional underwriting or special handling.

## Data Flow

### Request Processing Flow

```
1. HTTP POST /quote
   ↓
2. Express middleware (JSON parsing, CORS)
   ↓
3. Route handler (routes/quote.js)
   ↓
4. Input validation (validateQuoteRequest)
   ↓
5. Premium calculation (calculatePremium)
   ↓
6. Response formatting
   ↓
7. HTTP response (JSON)
```

### Error Handling Flow

```
Error Detected
   ↓
Error Type Classification
   ├── Validation Error (400 Bad Request)
   ├── Server Error (500 Internal Server Error)
   └── Not Found (404 Not Found)
   ↓
Error Response Formatting
   ↓
Client Response
```

## API Response Schema

### Successful Quote Response
```json
{
  "vehicleType": "string",      // Original input
  "driverAge": "number",        // Original input
  "ageCategory": "string",      // Computed: young|adult|senior
  "basePremium": "number",      // Base rate for vehicle type
  "ageMultiplier": "number",    // Age-based multiplier applied
  "finalPremium": "number",     // Calculated final premium
  "currency": "string",         // Always "USD"
  "status": "string",           // premium|peasant
  "message": "string"           // Status description
}
```

### Error Response Schema
```json
{
  "error": "string",           // Error category
  "message": "string"          // Detailed error description
}
```

## Performance Considerations

### Computational Complexity
- **Time Complexity**: O(1) - All operations are constant time
- **Space Complexity**: O(1) - Fixed memory footprint
- **Throughput**: Limited primarily by HTTP overhead, not calculation time

### Optimization Strategies
1. **In-Memory Lookups**: All rate tables stored in memory
2. **Minimal Computation**: Simple arithmetic operations only
3. **Early Validation**: Fail fast on invalid inputs
4. **Response Caching**: Identical requests could be cached (future enhancement)

## Security Considerations

### Input Sanitization
- Type checking for all inputs
- Range validation for numeric inputs
- String normalization (lowercase) for consistent processing

### Denial of Service Prevention
- Input size limits (handled by Express body parser defaults)
- Request rate limiting (not implemented - would be handled at infrastructure level)

### Data Privacy
- No sensitive data storage
- Stateless operation (no session management)
- No logging of personal information

## Testing Strategy

### Test Coverage Areas

1. **Unit Tests** (`tests/quoteService.test.js`)
   - Premium calculation accuracy
   - Input validation logic
   - Edge case handling
   - Business rule verification

2. **Integration Tests** (`tests/quote.test.js`)
   - HTTP endpoint functionality
   - Request/response flow
   - Error handling
   - Content-type validation

### Test Data Strategy
- **Valid Inputs**: Cover all vehicle types and age ranges
- **Edge Cases**: Boundary values (age 16, 25, 65, 100)
- **Invalid Inputs**: Type mismatches, out-of-range values
- **Business Scenarios**: High-risk combinations, discount eligibility

## Configuration Management

### Environment Variables
```bash
PORT=3000                    # Server port (default: 3000)
NODE_ENV=production|development  # Runtime environment
```

### Rate Configuration
All rates are hardcoded constants for simplicity. In a production system, these would typically be:
- Stored in a configuration database
- Loaded from environment-specific config files
- Managed through an admin interface

## Deployment Considerations

### Node.js Version
- **Target Version**: Node.js 16.x
- **Compatibility**: ES6+ features used throughout
- **Dependencies**: Minimal external dependencies for stability

### Resource Requirements
- **Memory**: ~50MB baseline (Express + dependencies)
- **CPU**: Minimal (simple arithmetic operations)
- **Storage**: Stateless (no persistent storage required)

### Monitoring Points
1. **Response Times**: Should be < 100ms for calculation
2. **Error Rates**: Track validation failures vs. server errors
3. **Request Volume**: Monitor for usage patterns
4. **Health Check**: `/health` endpoint for load balancer monitoring

## Future Enhancement Opportunities

### Functional Enhancements
1. **Additional Risk Factors**: Location, driving history, vehicle year
2. **Dynamic Pricing**: Real-time rate adjustments
3. **Quote Persistence**: Save and retrieve quotes
4. **Multi-Vehicle Discounts**: Family/fleet pricing

### Technical Improvements
1. **Database Integration**: Persistent storage for rates and quotes
2. **Caching Layer**: Redis for frequently requested combinations
3. **Rate Limiting**: Prevent API abuse
4. **Authentication**: API key or OAuth2 integration
5. **Logging**: Structured logging with correlation IDs
6. **Metrics**: Prometheus/StatsD integration

### Scalability Considerations
1. **Horizontal Scaling**: Stateless design supports load balancing
2. **Microservice Architecture**: Separate rating engine from API layer
3. **Event-Driven Updates**: Real-time rate updates via message queues
4. **CDN Integration**: Geographic distribution of API endpoints

## Maintenance Guidelines

### Code Quality Standards
- **Linting**: ESLint configuration recommended
- **Testing**: Maintain >90% code coverage
- **Documentation**: Keep JSDoc comments current
- **Dependencies**: Regular security updates

### Operational Procedures
1. **Deployment**: Zero-downtime rolling deployments
2. **Rollback**: Quick revert capability for rate changes
3. **Monitoring**: Alert on error rate thresholds
4. **Backup**: Configuration and rate data backup procedures
