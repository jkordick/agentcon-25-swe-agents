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

    def test_get_customer_risk_profile_existing_customer(self):
        """Test getting risk profile for an existing customer"""
        response = requests.get(f"{BASE_URL}/customers/1/risk-profile")
        assert response.status_code == 200
        data = response.json()
        
        # Check required fields are present
        assert "customer_id" in data
        assert "risk_score" in data
        assert "risk_level" in data
        assert "risk_factors" in data
        assert "recommendations" in data
        assert "calculated_at" in data
        assert "expires_at" in data
        
        # Check data types and values
        assert data["customer_id"] == 1
        assert isinstance(data["risk_score"], int)
        assert data["risk_level"] in ["LOW", "MODERATE", "HIGH"]
        assert isinstance(data["recommendations"], list)
        assert len(data["recommendations"]) > 0
        
        # Check risk factors structure
        risk_factors = data["risk_factors"]
        assert "age_factor" in risk_factors
        assert "location_factor" in risk_factors
        assert "profile_completeness" in risk_factors
        
        for factor in risk_factors.values():
            assert "score" in factor
            assert "description" in factor
            assert isinstance(factor["score"], int)
            assert isinstance(factor["description"], str)

    def test_get_customer_risk_profile_all_customers(self):
        """Test getting risk profiles for all customers"""
        for customer_id in [1, 2, 3]:
            response = requests.get(f"{BASE_URL}/customers/{customer_id}/risk-profile")
            assert response.status_code == 200
            data = response.json()
            assert data["customer_id"] == customer_id
            assert isinstance(data["risk_score"], int)
            assert 0 <= data["risk_score"] <= 100

    def test_get_customer_risk_profile_nonexistent_customer(self):
        """Test getting risk profile for non-existent customer"""
        response = requests.get(f"{BASE_URL}/customers/999/risk-profile")
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["error"].lower()

    def test_get_customer_risk_profile_invalid_customer_id(self):
        """Test getting risk profile with invalid customer ID"""
        # Test zero ID
        response = requests.get(f"{BASE_URL}/customers/0/risk-profile")
        assert response.status_code == 400
        
        # Test negative ID
        response = requests.get(f"{BASE_URL}/customers/-1/risk-profile")
        assert response.status_code == 400

    def test_risk_profile_response_format(self):
        """Test that risk profile response matches expected format"""
        response = requests.get(f"{BASE_URL}/customers/1/risk-profile")
        assert response.status_code == 200
        data = response.json()
        
        # Check timestamp format (should be ISO format with Z suffix)
        assert data["calculated_at"].endswith("Z")
        assert data["expires_at"].endswith("Z")
        
        # Check that expires_at is after calculated_at
        from datetime import datetime
        calculated = datetime.fromisoformat(data["calculated_at"].replace("Z", ""))
        expires = datetime.fromisoformat(data["expires_at"].replace("Z", ""))
        assert expires > calculated

    def test_root_endpoint_includes_risk_profile(self):
        """Test that root endpoint lists the new risk profile endpoint"""
        response = requests.get(f"{BASE_URL}/")
        assert response.status_code == 200
        data = response.json()
        assert "endpoints" in data
        
        # Check that risk profile endpoint is listed
        endpoint_found = False
        for endpoint in data["endpoints"]:
            if "risk-profile" in endpoint:
                endpoint_found = True
                break
        assert endpoint_found, "Risk profile endpoint not found in root endpoint list"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
