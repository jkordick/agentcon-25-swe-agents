import json
import re
from typing import Optional
from datetime import datetime, timedelta


class Customer:
    def __init__(self, id, first_name, last_name, email, phone_number, address, 
                 date_of_birth, created_at, updated_at):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.address = address
        self.date_of_birth = date_of_birth
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'address': self.address,
            'date_of_birth': self.date_of_birth,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)


def validate_customer_update(data):
    """Simple validation for customer update data"""
    errors = []
    
    if 'phone_number' in data:
        phone = data['phone_number']
        if not isinstance(phone, str) or len(phone) < 10 or len(phone) > 20:
            errors.append("phone_number must be a string between 10 and 20 characters")
    
    if 'address' in data:
        address = data['address']
        if not isinstance(address, str) or len(address) < 5 or len(address) > 200:
            errors.append("address must be a string between 5 and 200 characters")
    
    if 'email' in data:
        email = data['email']
        if not isinstance(email, str) or '@' not in email:
            errors.append("email must be a valid email address")
    
    return errors


def calculate_age(date_of_birth_str):
    """Calculate age from date of birth string (YYYY-MM-DD)"""
    try:
        birth_date = datetime.strptime(date_of_birth_str, '%Y-%m-%d')
        today = datetime.now()
        age = today.year - birth_date.year
        if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
            age -= 1
        return age
    except ValueError:
        return None


def calculate_age_factor(age):
    """Calculate age risk factor and description"""
    if age is None:
        return {"score": 50, "description": "Unknown age - default risk"}
    elif 18 <= age <= 25:
        return {"score": 65, "description": f"Age {age} - higher risk demographic"}
    elif 26 <= age <= 45:
        return {"score": 85, "description": f"Age {age} - lower risk demographic"}
    elif 46 <= age <= 65:
        return {"score": 75, "description": f"Age {age} - moderate risk demographic"}
    elif age >= 66:
        return {"score": 67, "description": f"Age {age} - higher risk demographic"}
    else:
        return {"score": 50, "description": f"Age {age} - outside typical range"}


def calculate_location_factor(address):
    """Calculate location risk factor based on address"""
    if not address or not isinstance(address, str):
        return {"score": 60, "description": "No address information - default risk"}
    
    address_lower = address.lower()
    
    # Simple heuristics based on common patterns
    if any(word in address_lower for word in ['new york', 'boston', 'san francisco', 'chicago', 'los angeles']):
        return {"score": 70, "description": "Urban area - moderate crime rates"}
    elif any(word in address_lower for word in ['ave', 'avenue', 'street', 'st', 'blvd', 'boulevard']):
        # Urban-ish based on street naming
        return {"score": 72, "description": "Urban area - moderate crime rates"}
    elif any(word in address_lower for word in ['rd', 'road', 'lane', 'ln', 'drive', 'dr']):
        # Suburban-ish based on road naming
        return {"score": 82, "description": "Suburban area - lower risk"}
    else:
        # Default to moderate risk
        return {"score": 75, "description": "Area risk assessment - moderate"}


def calculate_profile_completeness(customer):
    """Calculate profile completeness factor"""
    required_fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'date_of_birth']
    missing_count = 0
    
    for field in required_fields:
        value = getattr(customer, field, None)
        if not value or (isinstance(value, str) and len(value.strip()) == 0):
            missing_count += 1
    
    if missing_count == 0:
        return {"score": 95, "description": "Complete profile with verified contact info"}
    elif missing_count <= 2:
        return {"score": 77, "description": f"Missing {missing_count} field(s) - moderate risk"}
    else:
        return {"score": 60, "description": f"Missing {missing_count} field(s) - higher risk"}


def calculate_risk_level(risk_score):
    """Determine risk level based on risk score"""
    if risk_score >= 85:
        return "LOW"
    elif risk_score >= 70:
        return "MODERATE"
    else:
        return "HIGH"


def generate_recommendations(risk_level, age, customer):
    """Generate recommendations based on risk assessment"""
    recommendations = []
    
    if risk_level == "LOW":
        recommendations.append("Standard coverage recommended")
        recommendations.append("Consider loyalty discount eligibility")
    elif risk_level == "MODERATE":
        recommendations.append("Standard coverage recommended")
        recommendations.append("Review coverage options annually")
    else:  # HIGH
        recommendations.append("Enhanced coverage evaluation recommended")
        recommendations.append("Consider additional risk mitigation measures")
    
    # Age-specific recommendations
    if age and 26 <= age <= 45:
        recommendations.append("Eligible for good driver discount programs")
    
    return recommendations


def calculate_customer_risk_profile(customer):
    """Calculate comprehensive risk profile for a customer"""
    # Calculate age
    age = calculate_age(customer.date_of_birth)
    
    # Check for insufficient data
    if age is None:
        raise ValueError("Invalid date_of_birth format - cannot calculate age")
    
    # Calculate individual risk factors
    age_factor = calculate_age_factor(age)
    location_factor = calculate_location_factor(customer.address)
    profile_completeness = calculate_profile_completeness(customer)
    
    # Calculate weighted risk score
    # Age Factor: 30% weight, Location Factor: 40% weight, Profile Completeness: 30% weight
    risk_score = int(
        (age_factor["score"] * 0.30) +
        (location_factor["score"] * 0.40) +
        (profile_completeness["score"] * 0.30)
    )
    
    risk_level = calculate_risk_level(risk_score)
    recommendations = generate_recommendations(risk_level, age, customer)
    
    # Calculate expiration time (7 days from now)
    calculated_at = datetime.now()
    expires_at = calculated_at + timedelta(days=7)
    
    return {
        "customer_id": customer.id,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_factors": {
            "age_factor": age_factor,
            "location_factor": location_factor,
            "profile_completeness": profile_completeness
        },
        "recommendations": recommendations,
        "calculated_at": calculated_at.isoformat() + "Z",
        "expires_at": expires_at.isoformat() + "Z"
    }
