# Insurance Quote API

A Node.js 16 REST API for calculating insurance premium quotes based on vehicle type and driver age.

## Features

- Calculate insurance premiums based on vehicle type and driver age
- Support for multiple vehicle types (car, truck, motorcycle, SUV, van)
- Age-based risk assessment with different multipliers
- Special conditions and discounts for specific scenarios
- Returns either "premium" or "peasant" status based on quote amount
- Input validation and error handling
- Comprehensive test suite

## API Endpoints

### POST /quote

Calculate an insurance premium quote.

**Request Body:**
```json
{
  "vehicleType": "car",
  "driverAge": 35
}
```

**Response:**
```json
{
  "vehicleType": "car",
  "driverAge": 35,
  "ageCategory": "adult",
  "basePremium": 1200,
  "ageMultiplier": 1.0,
  "finalPremium": 1080,
  "currency": "USD",
  "status": "premium",
  "message": "Standard premium calculated successfully"
}
```

**Supported Vehicle Types:**
- `car` - Base rate: $1,200
- `truck` - Base rate: $1,800
- `motorcycle` - Base rate: $800
- `suv` - Base rate: $1,500
- `van` - Base rate: $1,400

**Age Categories:**
- `young` (16-25): 1.8x multiplier
- `adult` (26-65): 1.0x multiplier
- `senior` (66+): 1.3x multiplier

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "OK",
  "message": "Insurance Quote API is running"
}
```

## Premium Calculation Logic

The API uses simple if-else logic to calculate premiums:

1. **Base Rate**: Determined by vehicle type
2. **Age Multiplier**: Applied based on driver age category
3. **Special Conditions**:
   - Young motorcycle riders (under 21): +50% premium
   - Senior truck drivers (over 70): +20% premium
   - Prime age car drivers (30-50): -10% discount
4. **Status Classification**:
   - Premium > $2,500: "peasant" status
   - Premium ≤ $2,500: "premium" status

## Installation

1. Install dependencies:
```bash
npm install
```

2. Start the server:
```bash
npm start
```

3. For development with auto-reload:
```bash
npm run dev
```

## Testing

Run the test suite:
```bash
npm test
```

## Examples

### Standard Car Insurance for Adult
```bash
curl -X POST http://localhost:3000/quote \
  -H "Content-Type: application/json" \
  -d '{"vehicleType": "car", "driverAge": 35}'
```

### High-Risk Motorcycle for Young Driver
```bash
curl -X POST http://localhost:3000/quote \
  -H "Content-Type: application/json" \
  -d '{"vehicleType": "motorcycle", "driverAge": 18}'
```

### Truck Insurance for Senior Driver
```bash
curl -X POST http://localhost:3000/quote \
  -H "Content-Type: application/json" \
  -d '{"vehicleType": "truck", "driverAge": 75}'
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- `400 Bad Request`: Invalid input (missing fields, invalid vehicle type, invalid age)
- `404 Not Found`: Route not found
- `500 Internal Server Error`: Server errors

Example error response:
```json
{
  "error": "Invalid input",
  "message": "Unsupported vehicle type. Supported types: car, truck, motorcycle, suv, van"
}
```

## Requirements

- Node.js 16.x
- Express.js 4.x
- CORS support enabled
