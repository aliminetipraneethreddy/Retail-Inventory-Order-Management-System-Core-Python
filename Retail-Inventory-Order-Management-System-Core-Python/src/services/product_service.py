from typing import List, Dict, Optional
from src.dao.product_dao import ProductDAO

class ProductError(Exception):
    pass

class ProductService:
    def __init__(self, dao: Optional[ProductDAO] = None):
        # Allow dependency injection for easier testing/mock
        self.dao = dao if dao else ProductDAO()

    def add_product(self, name: str, sku: str, price: float, stock: int = 0, category: Optional[str] = None) -> Dict:
        """
        Validate and insert a new product.
        Raises ProductError on validation failure.
        """
        if price <= 0:
            raise ProductError("Price must be greater than 0")
        
        existing = self.dao.get_product_by_sku(sku)
        if existing:
            raise ProductError(f"SKU already exists: {sku}")
        
        return self.dao.create_product(name, sku, price, stock, category)

    def restock_product(self, prod_id: int, delta: int) -> Dict:
        if delta <= 0:
            raise ProductError("Delta must be positive")
        
        product = self.dao.get_product_by_id(prod_id)
        if not product:
            raise ProductError("Product not found")
        
        new_stock = (product.get("stock") or 0) + delta
        return self.dao.update_product(prod_id, {"stock": new_stock})

    def get_low_stock(self, threshold: int = 5) -> List[Dict]:
        all_products = self.dao.list_products(limit=1000)
        return [p for p in all_products if (p.get("stock") or 0) <= threshold]
