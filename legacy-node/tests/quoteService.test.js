const { calculatePremium, validateQuoteRequest, VEHICLE_BASE_RATES, AGE_MULTIPLIERS, COVERAGE_OPTIONS } = require('../services/quoteService');

describe('Quote Service', () => {
  describe('validateQuoteRequest', () => {
    test('should validate correct input', () => {
      const result = validateQuoteRequest('car', 30);
      expect(result.isValid).toBe(true);
    });

    test('should reject invalid vehicle type', () => {
      const result = validateQuoteRequest('plane', 30);
      expect(result.isValid).toBe(false);
      expect(result.message).toContain('Unsupported vehicle type');
    });

    test('should reject invalid age', () => {
      const result = validateQuoteRequest('car', 15);
      expect(result.isValid).toBe(false);
      expect(result.message).toContain('Driver age is required');
    });

    test('should validate coverage options', () => {
      const result = validateQuoteRequest('car', 30, { roadsideAssistance: true });
      expect(result.isValid).toBe(true);
    });

    test('should reject invalid coverage option', () => {
      const result = validateQuoteRequest('car', 30, { invalidOption: true });
      expect(result.isValid).toBe(false);
      expect(result.message).toContain('Unsupported coverage option');
    });

    test('should reject non-boolean coverage option value', () => {
      const result = validateQuoteRequest('car', 30, { roadsideAssistance: 'yes' });
      expect(result.isValid).toBe(false);
      expect(result.message).toContain('must be a boolean value');
    });

    test('should reject array as coverage options', () => {
      const result = validateQuoteRequest('car', 30, ['roadsideAssistance']);
      expect(result.isValid).toBe(false);
      expect(result.message).toContain('must be an object, not an array');
    });

    test('should handle null coverage options', () => {
      const result = validateQuoteRequest('car', 30, null);
      expect(result.isValid).toBe(true);
    });
  });

  describe('calculatePremium', () => {
    test('should calculate correct premium for car and adult driver', () => {
      const result = calculatePremium('car', 35);
      
      expect(result.vehicleType).toBe('car');
      expect(result.driverAge).toBe(35);
      expect(result.ageCategory).toBe('adult');
      expect(result.basePremium).toBe(VEHICLE_BASE_RATES.car);
      expect(result.ageMultiplier).toBe(AGE_MULTIPLIERS.adult);
      expect(result.calculatedPremium).toBe(1080); // 1200 * 1.0 * 0.9 (discount for prime age car drivers)
      expect(result.finalPremium).toBe(1080); // No coverage options
    });

    test('should apply young driver penalty for motorcycle', () => {
      const result = calculatePremium('motorcycle', 20);
      
      expect(result.ageCategory).toBe('young');
      expect(result.finalPremium).toBe(2160); // 800 * 1.8 * 1.5 (young motorcycle penalty)
      expect(result.status).toBe('premium'); // 2160 is below 2500 threshold
    });

    test('should apply senior truck driver penalty', () => {
      const result = calculatePremium('truck', 75);
      
      expect(result.ageCategory).toBe('senior');
      expect(result.finalPremium).toBe(2808); // 1800 * 1.3 * 1.2 (senior truck penalty)
      expect(result.status).toBe('peasant');
    });

    test('should return premium status for reasonable rates', () => {
      const result = calculatePremium('car', 40);
      
      expect(result.finalPremium).toBeLessThan(2500);
      expect(result.status).toBe('premium');
    });

    test('should return peasant status for very young motorcycle rider', () => {
      const result = calculatePremium('truck', 18);
      
      expect(result.finalPremium).toBeGreaterThan(2500);
      expect(result.status).toBe('peasant');
    });

    test('should calculate premium with roadside assistance', () => {
      const result = calculatePremium('car', 35, { roadsideAssistance: true });
      
      expect(result.calculatedPremium).toBe(1080);
      expect(result.coverageOptions.roadsideAssistance).toBe(COVERAGE_OPTIONS.roadsideAssistance);
      expect(result.totalCoverageCost).toBe(120);
      expect(result.finalPremium).toBe(1200); // 1080 + 120
    });

    test('should calculate premium with multiple coverage options', () => {
      const result = calculatePremium('car', 35, { 
        roadsideAssistance: true,
        rentalCar: true,
        glassCoverage: true
      });
      
      expect(result.calculatedPremium).toBe(1080);
      expect(result.coverageOptions.roadsideAssistance).toBe(120);
      expect(result.coverageOptions.rentalCar).toBe(180);
      expect(result.coverageOptions.glassCoverage).toBe(90);
      expect(result.totalCoverageCost).toBe(390); // 120 + 180 + 90
      expect(result.finalPremium).toBe(1470); // 1080 + 390
    });

    test('should not add cost for disabled coverage options', () => {
      const result = calculatePremium('car', 35, { 
        roadsideAssistance: true,
        rentalCar: false,
        glassCoverage: true
      });
      
      expect(result.coverageOptions.roadsideAssistance).toBe(120);
      expect(result.coverageOptions.glassCoverage).toBe(90);
      expect(result.coverageOptions.rentalCar).toBeUndefined();
      expect(result.totalCoverageCost).toBe(210); // 120 + 90
      expect(result.finalPremium).toBe(1290); // 1080 + 210
    });

    test('should handle empty coverage options object', () => {
      const result = calculatePremium('car', 35, {});
      
      expect(result.coverageOptions).toEqual({});
      expect(result.totalCoverageCost).toBe(0);
      expect(result.finalPremium).toBe(1080);
    });

    test('should handle null coverage options', () => {
      const result = calculatePremium('car', 35, null);
      
      expect(result.coverageOptions).toEqual({});
      expect(result.totalCoverageCost).toBe(0);
      expect(result.finalPremium).toBe(1080);
    });

    test('should handle undefined coverage options', () => {
      const result = calculatePremium('car', 35, undefined);
      
      expect(result.coverageOptions).toEqual({});
      expect(result.totalCoverageCost).toBe(0);
      expect(result.finalPremium).toBe(1080);
    });
  });
});
