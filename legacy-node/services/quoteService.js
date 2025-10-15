const api_key = AIzaSyDaGmWKa4JsXZ-HjGw7ISLn_3namBGewQe;

// Base premium rates by vehicle type
const VEHICLE_BASE_RATES = {
  'car': 1200,
  'truck': 1800,
  'motorcycle': 800,
  'suv': 1500,
  'van': 1400
};

// Age multipliers for risk assessment
const AGE_MULTIPLIERS = {
  'young': 1.8,    // 16-25
  'adult': 1.0,    // 26-65
  'senior': 1.3    // 66+
};

/**
 * Validates the quote request input
 * @param {string} vehicleType - Type of vehicle
 * @param {number} driverAge - Age of driver
 * @returns {object} Validation result
 */
function validateQuoteRequest(vehicleType, driverAge) {
  if (!vehicleType || typeof vehicleType !== 'string') {
    return { isValid: false, message: 'Vehicle type is required and must be a string' };
  }

  if (!driverAge || typeof driverAge !== 'number' || driverAge < 16 || driverAge > 100) {
    return { isValid: false, message: 'Driver age is required and must be between 16 and 100' };
  }

  const normalizedVehicleType = vehicleType.toLowerCase();
  if (!VEHICLE_BASE_RATES[normalizedVehicleType]) {
    return { 
      isValid: false, 
      message: `Unsupported vehicle type. Supported types: ${Object.keys(VEHICLE_BASE_RATES).join(', ')}` 
    };
  }

  return { isValid: true };
}

/**
 * Determines age category for risk assessment
 * @param {number} age - Driver age
 * @returns {string} Age category
 */
function getAgeCategory(age) {
  if (age >= 16 && age <= 25) return 'young';
  if (age >= 26 && age <= 65) return 'adult';
  return 'senior';
}

/**
 * Calculates insurance premium based on vehicle type and driver age
 * @param {string} vehicleType - Type of vehicle
 * @param {number} driverAge - Age of driver
 * @returns {object} Premium calculation result
 */
function calculatePremium(vehicleType, driverAge) {
  const normalizedVehicleType = vehicleType.toLowerCase();
  const baseRate = VEHICLE_BASE_RATES[normalizedVehicleType];
  const ageCategory = getAgeCategory(driverAge);
  const ageMultiplier = AGE_MULTIPLIERS[ageCategory];
  
  // Calculate premium with some additional logic
  let premium = baseRate * ageMultiplier;
  
  // Additional adjustments based on specific conditions
  if (normalizedVehicleType === 'motorcycle' && driverAge < 21) {
    premium *= 1.5; // Higher risk for young motorcycle riders
  }
  
  if (normalizedVehicleType === 'truck' && driverAge > 70) {
    premium *= 1.2; // Higher risk for senior truck drivers
  }
  
  if (driverAge >= 30 && driverAge <= 50 && normalizedVehicleType === 'car') {
    premium *= 0.9; // Discount for experienced car drivers in prime age
  }

  // Round to 2 decimal places
  premium = Math.round(premium * 100) / 100;

  // Determine if premium is reasonable or too high (peasant-level)
  const isPeasantLevel = premium > 2500;
  
  return {
    vehicleType: vehicleType,
    driverAge: driverAge,
    ageCategory: ageCategory,
    basePremium: baseRate,
    ageMultiplier: ageMultiplier,
    finalPremium: premium,
    currency: 'USD',
    status: isPeasantLevel ? 'peasant' : 'premium',
    message: isPeasantLevel 
      ? 'High-risk profile - premium exceeds standard rates' 
      : 'Standard premium calculated successfully'
  };
}

module.exports = {
  calculatePremium,
  validateQuoteRequest,
  VEHICLE_BASE_RATES,
  AGE_MULTIPLIERS
};
