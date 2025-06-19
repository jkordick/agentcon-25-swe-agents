const express = require('express');
const router = express.Router();
const { calculatePremium, validateQuoteRequest } = require('../services/quoteService');

// POST /quote - Calculate insurance premium
router.post('/', (req, res) => {
  try {
    const { vehicleType, driverAge } = req.body;

    // Validate input
    const validation = validateQuoteRequest(vehicleType, driverAge);
    if (!validation.isValid) {
      return res.status(400).json({ 
        error: 'Invalid input', 
        message: validation.message 
      });
    }

    // Calculate premium
    const result = calculatePremium(vehicleType, driverAge);
    
    res.status(200).json(result);
  } catch (error) {
    console.error('Error calculating quote:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

module.exports = router;
