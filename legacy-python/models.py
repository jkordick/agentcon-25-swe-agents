import json
from typing import Optional
from datetime import datetime


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
