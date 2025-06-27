"""
Test module for risk_calculator.py
"""

import pytest
from datetime import datetime, date
from risk_calculator import (
    calculate_age_from_dob,
    calculate_age_factor,
    calculate_location_factor,
    calculate_profile_completeness,
    calculate_overall_risk_score,
    determine_risk_level,
    generate_recommendations,
    calculate_customer_risk_profile
)


class TestRiskCalculator:
    
    def test_calculate_age_from_dob(self):
        """Test age calculation from date of birth"""
        # Test with a known date
        today = date.today()
        birth_year = today.year - 30
        dob = f"{birth_year}-{today.month:02d}-{today.day:02d}"
        age = calculate_age_from_dob(dob)
        assert age == 30
        
        # Test with invalid format
        with pytest.raises(ValueError):
            calculate_age_from_dob("invalid-date")

    def test_calculate_age_factor(self):
        """Test age factor calculation"""
        # Test different age ranges
        score, desc = calculate_age_factor(22)  # 18-25 range
        assert 60 <= score <= 70
        assert "higher risk" in desc.lower()
        
        score, desc = calculate_age_factor(35)  # 26-45 range
        assert 80 <= score <= 90
        assert "lower risk" in desc.lower()
        
        score, desc = calculate_age_factor(55)  # 46-65 range
        assert 70 <= score <= 80
        assert "moderate risk" in desc.lower()
        
        score, desc = calculate_age_factor(70)  # 65+ range
        assert 60 <= score <= 75
        assert "higher risk" in desc.lower()

    def test_calculate_location_factor(self):
        """Test location factor calculation"""
        # Test New York address
        score, desc = calculate_location_factor("123 Main St, New York, NY 10001")
        assert 60 <= score <= 80
        assert "urban" in desc.lower()
        
        # Test empty address
        score, desc = calculate_location_factor("")
        assert score == 60
        assert "insufficient" in desc.lower()

    def test_calculate_profile_completeness(self):
        """Test profile completeness calculation"""
        # Complete profile
        complete_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'phone_number': '+1-555-0123',
            'address': '123 Main St',
            'date_of_birth': '1985-01-01'
        }
        score, desc = calculate_profile_completeness(complete_data)
        assert score >= 90
        assert "complete" in desc.lower()
        
        # Incomplete profile
        incomplete_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': '',  # Missing email
            'phone_number': '',  # Missing phone
            'address': '123 Main St',
            'date_of_birth': '1985-01-01'
        }
        score, desc = calculate_profile_completeness(incomplete_data)
        assert score < 90

    def test_calculate_overall_risk_score(self):
        """Test overall risk score calculation"""
        score = calculate_overall_risk_score(80, 70, 90)
        # Expected: (80 * 0.3) + (70 * 0.4) + (90 * 0.3) = 24 + 28 + 27 = 79
        assert score == 79

    def test_determine_risk_level(self):
        """Test risk level determination"""
        assert determine_risk_level(90) == "LOW"
        assert determine_risk_level(75) == "MODERATE"
        assert determine_risk_level(60) == "HIGH"

    def test_generate_recommendations(self):
        """Test recommendation generation"""
        # Low risk
        recommendations = generate_recommendations(90, "LOW", 30)
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        assert any("standard coverage" in rec.lower() for rec in recommendations)
        
        # High risk
        recommendations = generate_recommendations(60, "HIGH", 30)
        assert any("enhanced screening" in rec.lower() for rec in recommendations)

    def test_calculate_customer_risk_profile_complete(self):
        """Test complete customer risk profile calculation"""
        customer_data = {
            'id': 1,
            'first_name': 'Julia',
            'last_name': 'Kordick',
            'email': 'julia.kordick@example.com',
            'phone_number': '+1-555-0123',
            'address': '123 Main St, New York, NY 10001',
            'date_of_birth': '1985-03-15'
        }
        
        result = calculate_customer_risk_profile(customer_data)
        
        # Check all required fields are present
        assert result["customer_id"] == 1
        assert isinstance(result["risk_score"], int)
        assert result["risk_level"] in ["LOW", "MODERATE", "HIGH"]
        assert "risk_factors" in result
        assert "recommendations" in result
        assert "calculated_at" in result
        assert "expires_at" in result
        
        # Check risk factors structure
        factors = result["risk_factors"]
        assert "age_factor" in factors
        assert "location_factor" in factors
        assert "profile_completeness" in factors
        
        for factor in factors.values():
            assert "score" in factor
            assert "description" in factor

    def test_calculate_customer_risk_profile_missing_dob(self):
        """Test risk profile calculation with missing date of birth"""
        customer_data = {
            'id': 1,
            'first_name': 'Julia',
            'last_name': 'Kordick',
            'email': 'julia.kordick@example.com',
            'phone_number': '+1-555-0123',
            'address': '123 Main St, New York, NY 10001'
            # Missing date_of_birth
        }
        
        with pytest.raises(ValueError, match="date_of_birth is required"):
            calculate_customer_risk_profile(customer_data)

    def test_calculate_customer_risk_profile_invalid_dob(self):
        """Test risk profile calculation with invalid date of birth"""
        customer_data = {
            'id': 1,
            'first_name': 'Julia',
            'last_name': 'Kordick',
            'email': 'julia.kordick@example.com',
            'phone_number': '+1-555-0123',
            'address': '123 Main St, New York, NY 10001',
            'date_of_birth': 'invalid-date'
        }
        
        with pytest.raises(ValueError, match="Invalid date_of_birth format"):
            calculate_customer_risk_profile(customer_data)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])