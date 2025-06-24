import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple


def calculate_age(date_of_birth: str) -> int:
    """Calculate age from date of birth string (YYYY-MM-DD format)"""
    try:
        birth_date = datetime.strptime(date_of_birth, "%Y-%m-%d")
        today = datetime.now()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    except ValueError:
        raise ValueError(f"Invalid date format: {date_of_birth}")


def extract_zip_code(address: str) -> Optional[str]:
    """Extract ZIP code from address string"""
    # Look for 5-digit ZIP code pattern at the end of address
    zip_match = re.search(r'\b(\d{5})\b', address)
    return zip_match.group(1) if zip_match else None


def get_location_type(zip_code: str) -> str:
    """Determine location type based on ZIP code"""
    # Simple mapping for known ZIP codes
    urban_zips = {
        '10001', '10002', '10003', '10004', '10005',  # NYC Manhattan
        '02101', '02102', '02103', '02104', '02105',  # Boston
        '94102', '94103', '94104', '94105', '94107',  # San Francisco
        '90210', '90211', '90212',  # Beverly Hills
        '60601', '60602', '60603', '60604'   # Chicago
    }
    
    suburban_zips = {
        '10801', '10802', '10803',  # Westchester County, NY
        '02138', '02139', '02140',  # Cambridge, MA
        '94301', '94302', '94303',  # Palo Alto, CA
        '60614', '60615', '60616'   # Chicago suburbs
    }
    
    if zip_code in urban_zips:
        return 'urban'
    elif zip_code in suburban_zips:
        return 'suburban'
    else:
        return 'rural'  # Default for unknown ZIP codes


def calculate_age_factor(age: int) -> Tuple[int, str]:
    """Calculate age-based risk factor"""
    if 18 <= age <= 25:
        score = 65  # Higher risk
        description = f"Age {age} - higher risk demographic"
    elif 26 <= age <= 45:
        score = 85  # Lower risk
        description = f"Age {age} - lower risk demographic"
    elif 46 <= age <= 65:
        score = 75  # Moderate risk
        description = f"Age {age} - moderate risk demographic"
    else:  # 65+
        score = 68  # Higher risk
        description = f"Age {age} - senior demographic with elevated risk"
    
    return score, description


def calculate_location_factor(address: str) -> Tuple[int, str]:
    """Calculate location-based risk factor"""
    zip_code = extract_zip_code(address)
    
    if not zip_code:
        return 70, "Unable to determine location risk - ZIP code not found"
    
    location_type = get_location_type(zip_code)
    
    if location_type == 'urban':
        score = 70  # Moderate risk
        description = f"Urban area (ZIP {zip_code}) - moderate crime rates"
    elif location_type == 'suburban':
        score = 82  # Lower risk
        description = f"Suburban area (ZIP {zip_code}) - lower crime rates"
    else:  # rural
        score = 75  # Variable risk
        description = f"Rural area (ZIP {zip_code}) - variable risk factors"
    
    return score, description


def calculate_profile_completeness(customer_data: dict) -> Tuple[int, str]:
    """Calculate profile completeness factor"""
    required_fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'date_of_birth']
    missing_fields = []
    
    for field in required_fields:
        value = customer_data.get(field)
        if not value or (isinstance(value, str) and not value.strip()):
            missing_fields.append(field)
    
    missing_count = len(missing_fields)
    
    if missing_count == 0:
        score = 95  # Low risk
        description = "Complete profile with verified contact info"
    elif missing_count <= 2:
        score = 78  # Moderate risk
        description = f"Profile missing {missing_count} field(s): {', '.join(missing_fields)}"
    else:
        score = 60  # Higher risk
        description = f"Incomplete profile missing {missing_count} fields: {', '.join(missing_fields)}"
    
    return score, description


def determine_risk_level(risk_score: int) -> str:
    """Determine risk level based on overall score"""
    if risk_score >= 85:
        return "LOW"
    elif risk_score >= 70:
        return "MODERATE"
    else:
        return "HIGH"


def generate_recommendations(risk_score: int, risk_level: str, age: int, location_type: str) -> List[str]:
    """Generate insurance recommendations based on risk assessment"""
    recommendations = []
    
    if risk_level == "LOW":
        recommendations.append("Standard coverage recommended")
        recommendations.append("Consider loyalty discount eligibility")
        if age >= 26 and age <= 45:
            recommendations.append("Prime demographic - consider premium package options")
    elif risk_level == "MODERATE":
        recommendations.append("Standard coverage recommended")
        if age >= 65:
            recommendations.append("Consider senior-specific coverage options")
        if location_type == 'urban':
            recommendations.append("Urban area - consider comprehensive theft protection")
    else:  # HIGH
        recommendations.append("Enhanced coverage recommended")
        recommendations.append("Additional underwriting review required")
        if age <= 25:
            recommendations.append("Young driver - consider defensive driving course discount")
    
    return recommendations


def calculate_customer_risk_profile(customer_data: dict) -> dict:
    """Calculate complete risk profile for a customer"""
    try:
        # Extract customer data
        customer_id = customer_data.get('id')
        date_of_birth = customer_data.get('date_of_birth')
        address = customer_data.get('address', '')
        
        # Validate required data
        if not date_of_birth:
            raise ValueError("Customer date_of_birth is required for risk assessment")
        
        if not address:
            raise ValueError("Customer address is required for risk assessment")
        
        # Calculate age
        age = calculate_age(date_of_birth)
        
        # Calculate individual risk factors
        age_score, age_description = calculate_age_factor(age)
        location_score, location_description = calculate_location_factor(address)
        profile_score, profile_description = calculate_profile_completeness(customer_data)
        
        # Calculate weighted overall risk score
        # Age: 30%, Location: 40%, Profile: 30%
        overall_risk_score = round(
            (age_score * 0.3) + 
            (location_score * 0.4) + 
            (profile_score * 0.3)
        )
        
        risk_level = determine_risk_level(overall_risk_score)
        
        # Generate recommendations
        zip_code = extract_zip_code(address)
        location_type = get_location_type(zip_code) if zip_code else 'unknown'
        recommendations = generate_recommendations(overall_risk_score, risk_level, age, location_type)
        
        # Create timestamps
        calculated_at = datetime.now()
        expires_at = calculated_at + timedelta(days=7)  # Risk assessment valid for 7 days
        
        return {
            "customer_id": customer_id,
            "risk_score": overall_risk_score,
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
                    "score": profile_score,
                    "description": profile_description
                }
            },
            "recommendations": recommendations,
            "calculated_at": calculated_at.isoformat() + "Z",
            "expires_at": expires_at.isoformat() + "Z"
        }
        
    except ValueError as e:
        raise ValueError(f"Risk assessment failed: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error during risk assessment: {str(e)}")