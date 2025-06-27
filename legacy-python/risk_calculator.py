"""
Risk Assessment Calculator for Customer Profile Service
Calculates insurance risk scores based on customer data
"""

import re
from datetime import datetime, date
from typing import Dict, Tuple, Optional


def calculate_age_from_dob(date_of_birth: str) -> int:
    """Calculate age from date of birth string in YYYY-MM-DD format"""
    try:
        birth_date = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    except (ValueError, TypeError):
        raise ValueError(f"Invalid date of birth format: {date_of_birth}")


def calculate_age_factor(age: int) -> Tuple[int, str]:
    """
    Calculate age risk factor based on age ranges
    Returns (score, description)
    """
    if 18 <= age <= 25:
        return 65, f"Age {age} - higher risk demographic"
    elif 26 <= age <= 45:
        return 85, f"Age {age} - lower risk demographic"
    elif 46 <= age <= 65:
        return 75, f"Age {age} - moderate risk demographic"
    elif age > 65:
        return 67, f"Age {age} - higher risk demographic"
    else:
        return 50, f"Age {age} - insufficient data for assessment"


def extract_zip_code(address: str) -> Optional[str]:
    """Extract ZIP code from address string"""
    # Look for 5-digit ZIP code pattern
    zip_match = re.search(r'\b(\d{5})\b', address)
    if zip_match:
        return zip_match.group(1)
    return None


def calculate_location_factor(address: str) -> Tuple[int, str]:
    """
    Calculate location risk factor based on address analysis
    Returns (score, description)
    """
    if not address or len(address.strip()) < 5:
        return 60, "Insufficient address data for assessment"
    
    address_lower = address.lower()
    zip_code = extract_zip_code(address)
    
    # Simple heuristic based on common location indicators
    if any(indicator in address_lower for indicator in ['ny', 'new york', 'brooklyn', 'manhattan', 'bronx', 'queens']):
        return 70, "Urban area - moderate crime rates"
    elif any(indicator in address_lower for indicator in ['boston', 'ma', 'massachusetts']):
        return 75, "Urban area - moderate crime rates"
    elif any(indicator in address_lower for indicator in ['san francisco', 'ca', 'california']):
        return 65, "Urban area - higher cost of living"
    elif any(indicator in address_lower for indicator in ['suburb', 'avenue', 'ave', 'lane', 'ln']):
        return 82, "Suburban area - lower risk"
    elif any(indicator in address_lower for indicator in ['rural', 'county', 'farm', 'ranch']):
        return 75, "Rural area - variable risk"
    else:
        return 70, "Area analysis - moderate risk assessment"


def calculate_profile_completeness(customer_data: Dict) -> Tuple[int, str]:
    """
    Calculate profile completeness factor based on data quality
    Returns (score, description)
    """
    required_fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'date_of_birth']
    missing_count = 0
    
    for field in required_fields:
        value = customer_data.get(field)
        if not value or (isinstance(value, str) and len(value.strip()) == 0):
            missing_count += 1
    
    if missing_count == 0:
        return 95, "Complete profile with verified contact info"
    elif missing_count <= 2:
        return 77, f"Profile missing {missing_count} field(s) - moderate completeness"
    else:
        return 60, f"Profile missing {missing_count} field(s) - low completeness"


def calculate_overall_risk_score(age_score: int, location_score: int, completeness_score: int) -> int:
    """
    Calculate weighted overall risk score
    Age Factor: 30%, Location Factor: 40%, Profile Completeness: 30%
    """
    weighted_score = (age_score * 0.3) + (location_score * 0.4) + (completeness_score * 0.3)
    return round(weighted_score)


def determine_risk_level(risk_score: int) -> str:
    """Determine risk level category based on score"""
    if risk_score >= 85:
        return "LOW"
    elif risk_score >= 70:
        return "MODERATE"
    else:
        return "HIGH"


def generate_recommendations(risk_score: int, risk_level: str, age: int) -> list:
    """Generate recommendations based on risk assessment"""
    recommendations = []
    
    if risk_level == "LOW":
        recommendations.append("Standard coverage recommended")
        recommendations.append("Consider loyalty discount eligibility")
        if age >= 26 and age <= 45:
            recommendations.append("Eligible for preferred rates")
    elif risk_level == "MODERATE":
        recommendations.append("Standard coverage recommended")
        recommendations.append("Monitor profile for improvements")
    else:  # HIGH
        recommendations.append("Enhanced screening recommended")
        recommendations.append("Consider additional documentation")
        
    return recommendations


def calculate_customer_risk_profile(customer_data: Dict) -> Dict:
    """
    Calculate complete risk profile for a customer
    Returns the full risk assessment response
    """
    customer_id = customer_data.get('id')
    date_of_birth = customer_data.get('date_of_birth')
    address = customer_data.get('address', '')
    
    # Validate required data
    if not date_of_birth:
        raise ValueError("Customer date_of_birth is required for risk assessment")
    
    try:
        age = calculate_age_from_dob(date_of_birth)
    except ValueError as e:
        raise ValueError(f"Invalid date_of_birth format: {e}")
    
    # Calculate individual risk factors
    age_score, age_description = calculate_age_factor(age)
    location_score, location_description = calculate_location_factor(address)
    completeness_score, completeness_description = calculate_profile_completeness(customer_data)
    
    # Calculate overall score and level
    overall_score = calculate_overall_risk_score(age_score, location_score, completeness_score)
    risk_level = determine_risk_level(overall_score)
    recommendations = generate_recommendations(overall_score, risk_level, age)
    
    # Generate timestamps
    calculated_at = datetime.now()
    expires_at = datetime(calculated_at.year, calculated_at.month, calculated_at.day, 
                         calculated_at.hour, calculated_at.minute, calculated_at.second)
    # Add 7 days using timedelta
    from datetime import timedelta
    expires_at = calculated_at + timedelta(days=7)
    
    return {
        "customer_id": customer_id,
        "risk_score": overall_score,
        "risk_level": risk_level,
        "risk_factors": {
            "age_factor": {
                "score": age_score,
                "description": age_description
            },
            "location_factor": {
                "score": location_score,
                "description": location_description
            },
            "profile_completeness": {
                "score": completeness_score,
                "description": completeness_description
            }
        },
        "recommendations": recommendations,
        "calculated_at": calculated_at.isoformat() + "Z",
        "expires_at": expires_at.isoformat() + "Z"
    }