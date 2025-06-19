const request = require('supertest');
const app = require('../index');

describe('Insurance Quote API', () => {
  describe('POST /quote', () => {
    test('should calculate premium for valid car and adult driver', async () => {
      const response = await request(app)
        .post('/quote')
        .send({
          vehicleType: 'car',
          driverAge: 35
        });

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('finalPremium');
      expect(response.body).toHaveProperty('status');
      expect(response.body.vehicleType).toBe('car');
      expect(response.body.driverAge).toBe(35);
      expect(response.body.ageCategory).toBe('adult');
    });

    test('should calculate premium for motorcycle and young driver', async () => {
      const response = await request(app)
        .post('/quote')
        .send({
          vehicleType: 'motorcycle',
          driverAge: 20
        });

      expect(response.status).toBe(200);
      expect(response.body.ageCategory).toBe('young');
      expect(response.body.finalPremium).toBeGreaterThan(800); // Should be higher due to age and motorcycle risk
    });

    test('should return peasant status for high-risk profiles', async () => {
      const response = await request(app)
        .post('/quote')
        .send({
          vehicleType: 'truck',
          driverAge: 18
        });

      expect(response.status).toBe(200);
      expect(response.body.status).toBe('peasant');
      expect(response.body.finalPremium).toBeGreaterThan(2500);
    });

    test('should return 400 for invalid vehicle type', async () => {
      const response = await request(app)
        .post('/quote')
        .send({
          vehicleType: 'spaceship',
          driverAge: 30
        });

      expect(response.status).toBe(400);
      expect(response.body).toHaveProperty('error');
    });

    test('should return 400 for invalid driver age', async () => {
      const response = await request(app)
        .post('/quote')
        .send({
          vehicleType: 'car',
          driverAge: 15
        });

      expect(response.status).toBe(400);
      expect(response.body).toHaveProperty('error');
    });

    test('should return 400 for missing fields', async () => {
      const response = await request(app)
        .post('/quote')
        .send({
          vehicleType: 'car'
        });

      expect(response.status).toBe(400);
      expect(response.body).toHaveProperty('error');
    });
  });

  describe('GET /health', () => {
    test('should return health status', async () => {
      const response = await request(app).get('/health');
      
      expect(response.status).toBe(200);
      expect(response.body.status).toBe('OK');
    });
  });

  describe('404 handler', () => {
    test('should return 404 for unknown routes', async () => {
      const response = await request(app).get('/unknown');
      
      expect(response.status).toBe(404);
      expect(response.body).toHaveProperty('error');
    });
  });
});
