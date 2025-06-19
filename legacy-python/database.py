from typing import Dict, Optional
from datetime import datetime
from models import Customer


class CustomerDatabase:
    def __init__(self):
        # Initialize with hardcoded test data
        self.customers: Dict[int, Customer] = {
            1: Customer(
                id=1,
                first_name="Julia",
                last_name="Kordick",
                email="julia.kordick@example.com",
                phone_number="+1-555-0123",
                address="123 Main St, New York, NY 10001",
                date_of_birth="1985-03-15",
                created_at=datetime(2025, 1, 1, 10, 0, 0),
                updated_at=datetime(2025, 1, 1, 10, 0, 0)
            ),
            2: Customer(
                id=2,
                first_name="Alexander",
                last_name="Wachtel",
                email="alexander.wachtel@example.com",
                phone_number="+1-555-0456",
                address="456 Oak Ave, Boston, MA 02101",
                date_of_birth="1978-11-22",
                created_at=datetime(2025, 1, 1, 10, 0, 0),
                updated_at=datetime(2025, 1, 1, 10, 0, 0)
            ),
            3: Customer(
                id=3,
                first_name="Igor",
                last_name="Rykhlevskyi",
                email="igor.rykhlevskyi@example.com",
                phone_number="+1-555-0789",
                address="789 Pine Rd, San Francisco, CA 94102",
                date_of_birth="1990-07-08",
                created_at=datetime(2025, 1, 1, 10, 0, 0),
                updated_at=datetime(2025, 1, 1, 10, 0, 0)
            )
        }

    def get_customer(self, customer_id: int) -> Optional[Customer]:
        """Retrieve a customer by ID"""
        return self.customers.get(customer_id)

    def update_customer(self, customer_id: int, update_data: dict) -> Optional[Customer]:
        """Update a customer's information"""
        if customer_id not in self.customers:
            return None
        
        customer = self.customers[customer_id]
        
        # Update only the provided fields
        for field, value in update_data.items():
            if value is not None and hasattr(customer, field):
                setattr(customer, field, value)
        
        # Update the timestamp
        customer.updated_at = datetime.now()
        
        return customer

    def get_all_customers(self) -> Dict[int, Customer]:
        """Get all customers (for debugging/testing purposes)"""
        return self.customers


# Global database instance
customer_db = CustomerDatabase()
