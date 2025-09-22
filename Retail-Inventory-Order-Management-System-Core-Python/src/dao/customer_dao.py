from typing import Optional, List, Dict
from src.config import get_supabase


class CustomerDAO:
    def __init__(self):
        self._sb = get_supabase()

    def create_customer(self, name: str, email: str, phone: Optional[str], city: Optional[str]) -> Optional[Dict]:
        payload = {"name": name, "email": email, "phone": phone, "city": city}

        # Insert new customer
        self._sb.table("customers").insert(payload).execute()

        # Fetch inserted row by unique email
        resp = self._sb.table("customers").select("*").eq("email", email).limit(1).execute()
        return resp.data[0] if resp.data else None

    def delete_customer(self, email: str) -> Optional[Dict]:
        # Fetch row before delete
        resp_before = self._sb.table("customers").select("*").eq("email", email).limit(1).execute()
        row = resp_before.data[0] if resp_before.data else None

        if not row:
            return None

        # Delete by email
        self._sb.table("customers").delete().eq("email", email).execute()
        return row

    def get_customer_by_email(self, email: str) -> Optional[Dict]:
        resp = self._sb.table("customers").select("*").eq("email", email).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_customer_by_city(self, city: str) -> List[Dict]:
        resp = self._sb.table("customers").select("*").eq("city", city).execute()
        return resp.data or []

    def list_customer(self, limit: int = 100) -> List[Dict]:
        resp = self._sb.table("customers").select("*").order("cust_id", desc=False).limit(limit).execute()
        if resp.error:
            raise Exception(resp.error)
        return resp.data or []
