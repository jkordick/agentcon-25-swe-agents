import pytest
import json
import requests
import time
import threading
from main import run_server
from database import customer_db


# Global test server variables
test_server = None
server_thread = None
BASE_URL = "http://localhost:8001"


def start_test_server():
    """Start the test server in a separate thread"""
    global test_server, server_thread
    from http.server import HTTPServer
    from main import CustomerProfileHandler
    
    def run_test_server():
        server_address = ('', 8001)
        test_server = HTTPServer(server_address, CustomerProfileHandler)
        test_server.serve_forever()
    
    server_thread = threading.Thread(target=run_test_server, daemon=True)
    server_thread.start()
    time.sleep(1)  # Give server time to start


@pytest.fixture(scope="session", autouse=True)
def setup_test_server():
    """Setup test server for the entire test session"""
    start_test_server()
    yield
    # Server will be automatically cleaned up when thread dies


class TestCustomerProfileService:
    
    def test_root_endpoint(self):
        """Test the root endpoint"""
        response = requests.get(f"{BASE_URL}/")
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert data["service"] == "Customer Profile Service"

    def test_health_check(self):
        """Test the health check endpoint"""
        response = requests.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_get_existing_customer(self):
        """Test fetching an existing customer"""
        response = requests.get(f"{BASE_URL}/customers/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["first_name"] == "Julia"
        assert data["last_name"] == "Kordick"
        assert data["email"] == "julia.kordick@example.com"

    def test_get_nonexistent_customer(self):
        """Test fetching a non-existent customer"""
        response = requests.get(f"{BASE_URL}/customers/999")
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["error"].lower()

    def test_get_invalid_customer_id(self):
        """Test fetching with invalid customer ID"""
        response = requests.get(f"{BASE_URL}/customers/0")
        assert response.status_code == 400

    def test_update_customer_phone(self):
        """Test updating customer phone number"""
        update_data = {"phone_number": "+1-555-9999"}
        response = requests.patch(f"{BASE_URL}/customers/1", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["phone_number"] == "+1-555-9999"
        assert data["id"] == 1

    def test_update_customer_address(self):
        """Test updating customer address"""
        update_data = {"address": "999 New Street, Updated City, UC 12345"}
        response = requests.patch(f"{BASE_URL}/customers/2", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["address"] == "999 New Street, Updated City, UC 12345"
        assert data["first_name"] == "Alexander"  # Other fields unchanged

    def test_update_customer_multiple_fields(self):
        """Test updating multiple customer fields"""
        update_data = {
            "phone_number": "+1-555-7777",
            "address": "777 Multi Update Ave, Test City, TC 77777",
            "email": "igor.updated@example.com"
        }
        response = requests.patch(f"{BASE_URL}/customers/3", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["phone_number"] == "+1-555-7777"
        assert data["address"] == "777 Multi Update Ave, Test City, TC 77777"
        assert data["email"] == "igor.updated@example.com"
        assert data["first_name"] == "Igor"  # Unchanged field

    def test_update_nonexistent_customer(self):
        """Test updating a non-existent customer"""
        update_data = {"phone_number": "+1-555-0000"}
        response = requests.patch(f"{BASE_URL}/customers/999", json=update_data)
        assert response.status_code == 404

    def test_update_customer_empty_data(self):
        """Test updating customer with no updatable data"""
        response = requests.patch(f"{BASE_URL}/customers/1", json={})
        assert response.status_code == 400
        data = response.json()
        assert "at least one" in data["error"].lower()

    def test_all_hardcoded_customers_exist(self):
        """Test that all three hardcoded customers exist"""
        # Julia Kordick
        response = requests.get(f"{BASE_URL}/customers/1")
        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == "Julia"
        assert data["last_name"] == "Kordick"

        # Dr. Alexander Wachtel
        response = requests.get(f"{BASE_URL}/customers/2")
        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == "Alexander"
        assert data["last_name"] == "Wachtel"

        # Igor Rykhlevskyi
        response = requests.get(f"{BASE_URL}/customers/3")
        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == "Igor"
        assert data["last_name"] == "Rykhlevskyi"


class TestRiskAssessment:
    
    def test_risk_assessment_young_adult(self):
        """Test risk assessment for young adult (18-24)"""
        response = requests.get(f"{BASE_URL}/risk-assessment/age-range?age=22")
        assert response.status_code == 200
        data = response.json()
        assert data["age"] == 22
        assert data["age_range"] == "18-24"
        assert data["risk_level"] == "High"
        assert "risk_factors" in data
        assert "premium_modifier" in data
    
    def test_risk_assessment_middle_age(self):
        """Test risk assessment for middle age (40-59)"""
        response = requests.get(f"{BASE_URL}/risk-assessment/age-range?age=45")
        assert response.status_code == 200
        data = response.json()
        assert data["age"] == 45
        assert data["age_range"] == "40-59"
        assert data["risk_level"] == "Low"
        assert "risk_factors" in data
    
    def test_risk_assessment_senior(self):
        """Test risk assessment for senior (75+)"""
        response = requests.get(f"{BASE_URL}/risk-assessment/age-range?age=80")
        assert response.status_code == 200
        data = response.json()
        assert data["age"] == 80
        assert data["age_range"] == "75+"
        assert data["risk_level"] == "High"
    
    def test_risk_assessment_minor(self):
        """Test risk assessment for minor (under 18)"""
        response = requests.get(f"{BASE_URL}/risk-assessment/age-range?age=16")
        assert response.status_code == 200
        data = response.json()
        assert data["age"] == 16
        assert data["age_range"] == "Under 18"
        assert data["risk_level"] == "Low"
    
    def test_risk_assessment_easter_egg(self):
        """Test easter egg for age 1337"""
        response = requests.get(f"{BASE_URL}/risk-assessment/age-range?age=1337")
        assert response.status_code == 200
        data = response.json()
        assert data["age"] == 1337
        assert "joke" in data
        assert "elite_status" in data
        assert "1337" in data["elite_status"]
    
    def test_risk_assessment_missing_age(self):
        """Test risk assessment without age parameter"""
        response = requests.get(f"{BASE_URL}/risk-assessment/age-range")
        assert response.status_code == 400
        data = response.json()
        assert "missing" in data["error"].lower()
    
    def test_risk_assessment_invalid_age(self):
        """Test risk assessment with invalid age"""
        response = requests.get(f"{BASE_URL}/risk-assessment/age-range?age=abc")
        assert response.status_code == 400
        data = response.json()
        assert "integer" in data["error"].lower()
    
    def test_risk_assessment_negative_age(self):
        """Test risk assessment with negative age"""
        response = requests.get(f"{BASE_URL}/risk-assessment/age-range?age=-5")
        assert response.status_code == 400
        data = response.json()
        assert "non-negative" in data["error"].lower()
    
    def test_risk_assessment_age_too_high(self):
        """Test risk assessment with age over 150"""
        response = requests.get(f"{BASE_URL}/risk-assessment/age-range?age=200")
        assert response.status_code == 400
        data = response.json()
        assert "150" in data["error"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
