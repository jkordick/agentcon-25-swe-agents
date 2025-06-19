# User Handbook - Insurance Quote API

## Welcome to the Insurance Quote API

This handbook provides everything you need to know to successfully integrate and use the Insurance Quote API in your applications. Whether you're a developer building a web application, a mobile app, or a backend service, this guide will help you get started quickly and use the API effectively.

## Table of Contents

1. [Quick Start Guide](#quick-start-guide)
2. [API Overview](#api-overview)
3. [Getting Your First Quote](#getting-your-first-quote)
4. [Understanding Responses](#understanding-responses)
5. [Supported Vehicle Types](#supported-vehicle-types)
6. [Age Categories and Pricing](#age-categories-and-pricing)
7. [Special Pricing Rules](#special-pricing-rules)
8. [Error Handling](#error-handling)
9. [Best Practices](#best-practices)
10. [Code Examples](#code-examples)
11. [Troubleshooting](#troubleshooting)
12. [FAQ](#frequently-asked-questions)

## Quick Start Guide

### Step 1: Start the API Server
```bash
cd legacy-node
npm install
npm start
```
The API will be available at `http://localhost:3000`

### Step 2: Test the Health Endpoint
```bash
curl http://localhost:3000/health
```
You should receive: `{"status":"OK","message":"Insurance Quote API is running"}`

### Step 3: Get Your First Quote
```bash
curl -X POST http://localhost:3000/quote \
  -H "Content-Type: application/json" \
  -d '{"vehicleType": "car", "driverAge": 30}'
```

## API Overview

The Insurance Quote API provides a simple way to calculate insurance premiums based on two key factors:
- **Vehicle Type**: The type of vehicle being insured
- **Driver Age**: The age of the primary driver

### Base URL
```
http://localhost:3000
```

### Available Endpoints
- `POST /quote` - Calculate insurance premium
- `GET /health` - Check API health status

## Getting Your First Quote

### Basic Request Format
```json
POST /quote
Content-Type: application/json

{
  "vehicleType": "car",
  "driverAge": 30
}
```

### Sample Response
```json
{
  "vehicleType": "car",
  "driverAge": 30,
  "ageCategory": "adult",
  "basePremium": 1200,
  "ageMultiplier": 1.0,
  "finalPremium": 1080,
  "currency": "USD",
  "status": "premium",
  "message": "Standard premium calculated successfully"
}
```

## Understanding Responses

### Response Fields Explained

| Field | Type | Description |
|-------|------|-------------|
| `vehicleType` | string | The vehicle type you submitted |
| `driverAge` | number | The driver age you submitted |
| `ageCategory` | string | Risk category: "young", "adult", or "senior" |
| `basePremium` | number | Base rate for the vehicle type |
| `ageMultiplier` | number | Age-based risk multiplier applied |
| `finalPremium` | number | Final calculated premium amount |
| `currency` | string | Always "USD" |
| `status` | string | "premium" (≤$2,500) or "peasant" (>$2,500) |
| `message` | string | Human-readable status description |

### Status Types

#### "premium" Status
- Premium amount is $2,500 or less
- Considered standard risk pricing
- Most customers will receive this status

#### "peasant" Status  
- Premium amount exceeds $2,500
- Indicates high-risk profile
- May require additional underwriting or special handling

## Supported Vehicle Types

| Vehicle Type | Base Premium | Typical Use Case |
|--------------|--------------|------------------|
| `car` | $1,200 | Standard passenger vehicles |
| `truck` | $1,800 | Pickup trucks and commercial vehicles |
| `motorcycle` | $800 | Two-wheeled motor vehicles |
| `suv` | $1,500 | Sport utility vehicles |
| `van` | $1,400 | Multi-purpose and cargo vehicles |

### Important Notes:
- Vehicle types are **case-insensitive** ("Car", "CAR", "car" all work)
- Only the five types listed above are currently supported
- Submitting an unsupported type will return a 400 error

## Age Categories and Pricing

### Age Ranges and Risk Multipliers

#### Young Drivers (Ages 16-25)
- **Risk Multiplier**: 1.8x
- **Reasoning**: Statistical higher accident rates
- **Example**: $1,200 base → $2,160 premium

#### Adult Drivers (Ages 26-65)  
- **Risk Multiplier**: 1.0x (baseline)
- **Reasoning**: Most experienced, stable risk group
- **Example**: $1,200 base → $1,200 premium

#### Senior Drivers (Ages 66+)
- **Risk Multiplier**: 1.3x
- **Reasoning**: Age-related factors increase risk
- **Example**: $1,200 base → $1,560 premium

## Special Pricing Rules

The API applies additional adjustments based on specific combinations of age and vehicle type:

### 🏍️ Young Motorcycle Riders (Age < 21 + Motorcycle)
- **Additional Penalty**: +50% (×1.5)
- **Example**: 18-year-old with motorcycle
  - Base: $800 × 1.8 (young) × 1.5 (penalty) = $2,160

### 🚛 Senior Truck Drivers (Age > 70 + Truck)
- **Additional Penalty**: +20% (×1.2)  
- **Example**: 75-year-old with truck
  - Base: $1,800 × 1.3 (senior) × 1.2 (penalty) = $2,808

### 🚗 Prime Age Car Drivers (Age 30-50 + Car)
- **Discount**: -10% (×0.9)
- **Example**: 35-year-old with car
  - Base: $1,200 × 1.0 (adult) × 0.9 (discount) = $1,080

## Error Handling

### Common Error Scenarios

#### Invalid Vehicle Type (400 Bad Request)
```json
{
  "error": "Invalid input",
  "message": "Unsupported vehicle type. Supported types: car, truck, motorcycle, suv, van"
}
```

#### Invalid Driver Age (400 Bad Request)
```json
{
  "error": "Invalid input", 
  "message": "Driver age is required and must be between 16 and 100"
}
```

#### Missing Required Fields (400 Bad Request)
```json
{
  "error": "Invalid input",
  "message": "Vehicle type is required and must be a string"
}
```

#### Server Error (500 Internal Server Error)
```json
{
  "error": "Internal server error"
}
```

## Best Practices

### 1. Input Validation
Always validate inputs on your client side before sending requests:
```javascript
function validateQuoteInput(vehicleType, driverAge) {
  const validVehicles = ['car', 'truck', 'motorcycle', 'suv', 'van'];
  
  if (!vehicleType || !validVehicles.includes(vehicleType.toLowerCase())) {
    return { valid: false, error: 'Invalid vehicle type' };
  }
  
  if (!driverAge || driverAge < 16 || driverAge > 100) {
    return { valid: false, error: 'Driver age must be between 16 and 100' };
  }
  
  return { valid: true };
}
```

### 2. Error Handling
Implement proper error handling for all possible scenarios:
```javascript
try {
  const response = await fetch('/quote', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ vehicleType, driverAge })
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message);
  }
  
  const quote = await response.json();
  return quote;
} catch (error) {
  console.error('Quote request failed:', error.message);
  // Handle error appropriately
}
```

### 3. User Experience Tips
- **Clear Messaging**: Display the status and message fields to users
- **Format Currency**: Always display premiums with proper currency formatting
- **Explain Categories**: Help users understand age categories and their impact
- **Handle High Premiums**: Provide guidance for "peasant" status quotes

### 4. Performance Considerations
- **Caching**: Cache quotes for identical inputs to reduce API calls
- **Debouncing**: For real-time calculators, debounce user input
- **Timeout Handling**: Set reasonable request timeouts (API responds quickly)

## Code Examples

### JavaScript (Frontend)
```javascript
class InsuranceQuoteCalculator {
  constructor(apiBase = 'http://localhost:3000') {
    this.apiBase = apiBase;
  }

  async getQuote(vehicleType, driverAge) {
    try {
      const response = await fetch(`${this.apiBase}/quote`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          vehicleType: vehicleType,
          driverAge: parseInt(driverAge)
        })
      });

      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.message || 'Quote calculation failed');
      }

      return {
        success: true,
        quote: data
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  formatPremium(amount) {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  }
}

// Usage example
const calculator = new InsuranceQuoteCalculator();

calculator.getQuote('car', 35).then(result => {
  if (result.success) {
    console.log(`Premium: ${calculator.formatPremium(result.quote.finalPremium)}`);
    console.log(`Status: ${result.quote.status}`);
  } else {
    console.error('Error:', result.error);
  }
});
```

### Python
```python
import requests
import json

class InsuranceQuoteAPI:
    def __init__(self, base_url="http://localhost:3000"):
        self.base_url = base_url
    
    def get_quote(self, vehicle_type, driver_age):
        """Get insurance quote for given vehicle type and driver age."""
        try:
            response = requests.post(
                f"{self.base_url}/quote",
                json={
                    "vehicleType": vehicle_type,
                    "driverAge": driver_age
                },
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "quote": response.json()
                }
            else:
                error_data = response.json()
                return {
                    "success": False,
                    "error": error_data.get("message", "Unknown error")
                }
                
        except requests.RequestException as e:
            return {
                "success": False,
                "error": f"Network error: {str(e)}"
            }
    
    def format_premium(self, amount):
        """Format premium amount as currency."""
        return f"${amount:,.2f}"

# Usage example
api = InsuranceQuoteAPI()
result = api.get_quote("motorcycle", 22)

if result["success"]:
    quote = result["quote"]
    print(f"Premium: {api.format_premium(quote['finalPremium'])}")
    print(f"Status: {quote['status']}")
    print(f"Message: {quote['message']}")
else:
    print(f"Error: {result['error']}")
```

### cURL Examples
```bash
# Standard car quote
curl -X POST http://localhost:3000/quote \
  -H "Content-Type: application/json" \
  -d '{"vehicleType": "car", "driverAge": 35}'

# High-risk motorcycle quote
curl -X POST http://localhost:3000/quote \
  -H "Content-Type: application/json" \
  -d '{"vehicleType": "motorcycle", "driverAge": 18}'

# Senior truck driver
curl -X POST http://localhost:3000/quote \
  -H "Content-Type: application/json" \
  -d '{"vehicleType": "truck", "driverAge": 75}'

# Invalid vehicle type (error example)
curl -X POST http://localhost:3000/quote \
  -H "Content-Type: application/json" \
  -d '{"vehicleType": "spaceship", "driverAge": 30}'
```

## Troubleshooting

### Common Issues and Solutions

#### Problem: "Connection refused" or "Network error"
**Solution**: Ensure the API server is running
```bash
cd legacy-node
npm start
```

#### Problem: "Unsupported vehicle type" error
**Solution**: Check that you're using one of the supported types:
- car, truck, motorcycle, suv, van (case-insensitive)

#### Problem: "Driver age is required" error
**Solution**: Ensure age is:
- A number (not a string)
- Between 16 and 100 (inclusive)

#### Problem: Quotes seem too high
**Solution**: Check for special conditions:
- Young motorcycle riders get +50% penalty
- Senior truck drivers get +20% penalty
- Some combinations result in "peasant" status (>$2,500)

#### Problem: Missing response fields
**Solution**: Ensure you're sending POST request with proper JSON:
```bash
# Correct
curl -X POST http://localhost:3000/quote \
  -H "Content-Type: application/json" \
  -d '{"vehicleType": "car", "driverAge": 30}'

# Incorrect (missing Content-Type header)
curl -X POST http://localhost:3000/quote \
  -d '{"vehicleType": "car", "driverAge": 30}'
```

### Debug Checklist
1. ✅ API server is running (`npm start`)
2. ✅ Using correct endpoint (`POST /quote`)
3. ✅ Sending JSON with Content-Type header
4. ✅ Valid vehicle type (car, truck, motorcycle, suv, van)
5. ✅ Valid driver age (16-100)
6. ✅ Numeric age (not string)

## Frequently Asked Questions

### Q: What vehicle types are supported?
A: Currently five types: car, truck, motorcycle, suv, and van. Vehicle types are case-insensitive.

### Q: What's the difference between "premium" and "peasant" status?
A: "Premium" status indicates standard pricing (≤$2,500), while "peasant" status indicates high-risk pricing (>$2,500) that may require special handling.

### Q: Why is my motorcycle quote so expensive?
A: Motorcycles have a lower base rate ($800), but young riders (under 21) receive an additional 50% penalty due to higher risk factors.

### Q: Can I get quotes for drivers under 16?
A: No, the minimum age is 16 (legal driving age). Requests with ages below 16 will return a validation error.

### Q: Are there discounts available?
A: Yes! Drivers aged 30-50 with cars receive a 10% discount as they're considered experienced and low-risk.

### Q: How often do rates change?
A: Currently, rates are fixed. In a production system, rates might be updated periodically based on actuarial data.

### Q: Can I get quotes for multiple drivers?
A: Currently, the API supports single-driver quotes only. For multiple drivers, you would need to make separate API calls.

### Q: Is there rate limiting?
A: No rate limiting is currently implemented. However, the API is designed to handle reasonable request volumes.

### Q: Can I cache quote results?
A: Yes! Since quotes are deterministic (same inputs always produce same outputs), caching is safe and recommended for performance.

### Q: What happens if I send a decimal age?
A: The API expects integer ages. Decimal values may cause validation errors or unexpected behavior.

## Support and Resources

### Getting Help
- Check this handbook first for common scenarios
- Review the technical documentation for implementation details
- Use the health endpoint to verify API availability
- Test with simple examples before complex integrations

### Best Practices Summary
1. Always validate inputs client-side
2. Handle all possible error responses
3. Cache results when appropriate  
4. Use proper error messaging for users
5. Format currency values consistently
6. Test edge cases (young/senior ages, different vehicle types)

### Example Integration Checklist
- [ ] Input validation implemented
- [ ] Error handling for all scenarios
- [ ] Currency formatting
- [ ] User-friendly status messages
- [ ] Proper request headers (Content-Type)
- [ ] Network timeout handling
- [ ] Testing with all vehicle types
- [ ] Testing with edge case ages (16, 25, 65, 100)

---

This handbook should provide everything you need to successfully integrate and use the Insurance Quote API. For technical implementation details, refer to the technical documentation and README files.
