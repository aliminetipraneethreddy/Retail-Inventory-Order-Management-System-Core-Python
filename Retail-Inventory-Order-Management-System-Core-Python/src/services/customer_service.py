from typing import List, Dict, Optional, Any
from src.dao.customer_dao import CustomerDAO


class CustomerService:
    def __init__(self):
        self.dao = CustomerDAO()

    def create_customer(
        self,
        name: str,
        email: str,
        phone: Optional[str] = None,
        city: Optional[str] = None
    ) -> Dict[str, Any]:
        # Basic validation
        if not name or not email:
            raise ValueError("Name and email are required")

        # Check if email already exists
        existing = self.dao.get_customer_by_email(email)
        if existing:
            raise Exception(f"Customer with email {email} already exists")

        return self.dao.create_customer(name, email, phone, city)

    def delete_customer(self, email: str) -> Optional[Dict[str, Any]]:
        if not email:
            raise ValueError("Email is required")
        return self.dao.delete_customer(email)

    def get_customer_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        return self.dao.get_customer_by_email(email)

    def get_customers_by_city(self, city: str) -> List[Dict[str, Any]]:
        return self.dao.get_customer_by_city(city)

    def list_customers(self, limit: int = 100) -> List[Dict[str, Any]]:
        return self.dao.list_customer(limit)
