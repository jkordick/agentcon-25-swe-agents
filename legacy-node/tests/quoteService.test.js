const { calculatePremium, validateQuoteRequest, VEHICLE_BASE_RATES, AGE_MULTIPLIERS } = require('../services/quoteService');

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
  });

  describe('calculatePremium', () => {
    test('should calculate correct premium for car and adult driver', () => {
      const result = calculatePremium('car', 35);
      
      expect(result.vehicleType).toBe('car');
      expect(result.driverAge).toBe(35);
      expect(result.ageCategory).toBe('adult');
      expect(result.basePremium).toBe(VEHICLE_BASE_RATES.car);
      expect(result.ageMultiplier).toBe(AGE_MULTIPLIERS.adult);
      expect(result.finalPremium).toBe(1080); // 1200 * 1.0 * 0.9 (discount for prime age car drivers)
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
  });
});
