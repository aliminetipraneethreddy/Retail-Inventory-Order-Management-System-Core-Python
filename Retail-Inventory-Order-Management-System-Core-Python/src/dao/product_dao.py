from typing import Optional, List, Dict, Any
from src.config import get_supabase

class ProductDAO:
    def __init__(self):
        self._sb = get_supabase()

    def create_product(self, name: str, sku: str, price: float, stock: int = 0, category: Optional[str] = None) -> Optional[Dict]:
        payload = {"name": name, "sku": sku, "price": price, "stock": stock}
        if category is not None:
            payload["category"] = category

        self._sb.table("products").insert(payload).execute()
        resp = self._sb.table("products").select("*").eq("sku", sku).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_product_by_id(self, prod_id: int) -> Optional[Dict]:
        resp = self._sb.table("products").select("*").eq("prod_id", prod_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_product_by_sku(self, sku: str) -> Optional[Dict]:
        resp = self._sb.table("products").select("*").eq("sku", sku).limit(1).execute()
        return resp.data[0] if resp.data else None

    def update_product(self, prod_id: int, fields: Dict) -> Optional[Dict]:
        self._sb.table("products").update(fields).eq("prod_id", prod_id).execute()
        resp = self._sb.table("products").select("*").eq("prod_id", prod_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def delete_product(self, prod_id: int) -> Optional[Dict]:
        resp_before = self._sb.table("products").select("*").eq("prod_id", prod_id).limit(1).execute()
        row = resp_before.data[0] if resp_before.data else None
        self._sb.table("products").delete().eq("prod_id", prod_id).execute()
        return row

    def list_products(self, limit: int = 100, category: Optional[str] = None) -> List[Dict]:
        q = self._sb.table("products").select("*").order("prod_id", desc=False).limit(limit)
        if category:
            q = q.eq("category", category)
        resp = q.execute()
        return resp.data or []


class CustomerDAO:
    def __init__(self):
        self._sb = get_supabase()

    def update_customer(self, cust_id: int, phone: Optional[str] = None, city: Optional[str] = None) -> Optional[Dict[str, Any]]:
        updates: Dict[str, Any] = {}
        if phone:
            updates["phone"] = phone
        if city:
            updates["city"] = city

        if not updates:
            raise ValueError("No updates provided (phone or city required).")

        resp = (
            self._sb.table("customer")
            .update(updates)
            .eq("cust_id", cust_id)
            .execute()
        )

        if resp.error:
            raise Exception(f"Error updating customer {cust_id}: {resp.error}")

        return resp.data[0] if resp.data else None
