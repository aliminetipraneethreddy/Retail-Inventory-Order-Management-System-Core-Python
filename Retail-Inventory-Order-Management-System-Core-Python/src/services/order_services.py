from typing import List, Dict
from src.dao.order_dao import OrderDAO
from src.dao.customer_dao import CustomerDAO
from src.dao.product_dao import ProductDAO



class OrderService:
    def __init__(self):
        self.order_dao = OrderDAO()
        self.customer_dao = CustomerDAO()
        self.product_dao = ProductDAO()

    def create_order(self, cust_id: int, items: List[Dict]) -> Dict:
        cust = self.customer_dao.get_customer_by_id(cust_id)
        if not cust:
            raise Exception(f"Customer {cust_id} not found")

        total_amount = 0
        validated_items = []

        # 2. Validate products + stock
        for item in items:
            prod = self.product_dao.get_product_by_id(item["prod_id"])
            if not prod:
                raise Exception(f"Product {item['prod_id']} not found")
            if prod["stock"] < item["quantity"]:
                raise Exception(f"Not enough stock for product {prod['name']}")

            subtotal = prod["price"] * item["quantity"]
            total_amount += subtotal

            validated_items.append({
                "prod_id": prod["prod_id"],
                "quantity": item["quantity"],
                "price": prod["price"],
                "subtotal": subtotal
            })

        # 3. Create order
        order = self.order_dao.insert_order(customer_id, total_amount)

        # 4. Insert order_items + deduct stock
        for vi in validated_items:
            self.order_dao.insert_order_item(
                order["order_id"], vi["prod_id"], vi["quantity"], vi["price"]
            )
            self.product_dao.update_stock(vi["prod_id"], -vi["quantity"])

        return self.get_order_details(order["order_id"])

    # ---------------- FETCH DETAILS ----------------
    def get_order_details(self, order_id: int) -> Dict:
        """
        Fetch full details: order + customer + items
        """
        order = self.order_dao.get_order(order_id)
        if not order:
            raise Exception(f"Order {order_id} not found")

        customer = self.customer_dao.get_customer_by_id(order["customer_id"])
        items = self.order_dao.get_order_items(order_id)

        order["customer"] = customer
        order["items"] = items
        return order

    # ---------------- CANCEL ORDER ----------------
    def cancel_order(self, order_id: int) -> Dict:
        """
        Cancel only if status = PLACED.
        Restore product stock.
        Update status = CANCELLED.
        """
        order = self.order_dao.get_order(order_id)
        if not order:
            raise Exception(f"Order {order_id} not found")

        if order["status"] != "PLACED":
            raise Exception(f"Order {order_id} cannot be cancelled (status = {order['status']})")

        items = self.order_dao.get_order_items(order_id)

        # restore stock
        for item in items:
            self.product_dao.update_stock(item["prod_id"], item["quantity"])

        # update status
        self.order_dao.update_order_status(order_id, "CANCELLED")

        return self.get_order_details(order_id)

    # ---------------- COMPLETE ORDER ----------------
    def complete_order(self, order_id: int) -> Dict:
        """
        Mark order as COMPLETED after payment success.
        """
        order = self.order_dao.get_order(order_id)
        if not order:
            raise Exception(f"Order {order_id} not found")

        if order["status"] != "PLACED":
            raise Exception(f"Order {order_id} cannot be completed (status = {order['status']})")

        self.order_dao.update_order_status(order_id, "COMPLETED")
        return self.get_order_details(order_id)
