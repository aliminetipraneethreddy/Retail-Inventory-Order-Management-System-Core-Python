import argparse
import json
from src.services.product_service import ProductService
from src.dao.product_dao import ProductDAO
from src.dao.customer_dao import CustomerDAO
from src.services.customer_service import CustomerService

class RetailCLI:
    def __init__(self):
        self.product_service = ProductService()
        self.product_dao = ProductDAO()
        
        self.customer_service = CustomerService()   # ✅ use service, not DAO directly

        # Initialize other DAOs or services here if needed
        # e.g., self.customer_dao = CustomerDAO()

    def cmd_product_add(self, args):
        try:
            p = self.product_service.add_product(args.name, args.sku, args.price, args.stock, args.category)
            print("Created product:")
            print(json.dumps(p, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

    def cmd_product_list(self, args):
        ps = self.product_dao.list_products(limit=100)
        print(json.dumps(ps, indent=2, default=str))

    def cmd_customer_add(self, args):
        try:
            # Assuming you have a customer_dao similar to product_dao
            c = self.customer_dao.create_customer(args.name, args.email, args.phone, args.city)
            print("Created customer:")
            print(json.dumps(c, indent=2, default=str))
        except Exception as e:
            print("Error:", e)
    def cmd_customer_add(self, args):
        try:
            c = self.customer_dao.delete_customer(args.email)
            print("Delted customer:")
            print(json.dumps(c, indent=2, default=str))
        except Exception as e:
            print("Error:", e)




    
    def build_parser(self):
        parser = argparse.ArgumentParser(prog="retail-cli")
        sub = parser.add_subparsers(dest="cmd")

        # product add/list
        p_prod = sub.add_parser("product", help="product commands")
        pprod_sub = p_prod.add_subparsers(dest="action")
        addp = pprod_sub.add_parser("add")
        addp.add_argument("--name", required=True)
        addp.add_argument("--sku", required=True)
        addp.add_argument("--price", type=float, required=True)
        addp.add_argument("--stock", type=int, default=0)
        addp.add_argument("--category", default=None)
        addp.set_defaults(func=self.cmd_product_add)

        listp = pprod_sub.add_parser("list")
        listp.set_defaults(func=self.cmd_product_list)

        # customer add
        pcust = sub.add_parser("customers")
        pcust_sub = pcust.add_subparsers(dest="action")
        addc = pcust_sub.add_parser("add")
        addc.add_argument("--name", required=True)
        addc.add_argument("--email", required=True)
        addc.add_argument("--phone", required=True)
        addc.add_argument("--city", default=None)
        addc.set_defaults(func=self.cmd_customer_add)

        #delete customer
        pcust = sub.add_parser("customers")
        pcust_sub = pcust.add_subparsers(dest="action")
        addc = pcust_sub.add_parser("delete")
        addc.add_argument("--email", required=True)
        addc.set_defaults(func=self.cmd_customer_delete)





        # order
        porder = sub.add_parser("order")
        porder_sub = porder.add_subparsers(dest="action")

        createo = porder_sub.add_parser("create")
        createo.add_argument("--customer", type=int, required=True)
        createo.add_argument("--item", required=True, nargs="+", help="prod_id:qty (repeatable)")
        createo.set_defaults(func=self.cmd_order_create)

        showo = porder_sub.add_parser("show")
        showo.add_argument("--order", type=int, required=True)
        showo.set_defaults(func=self.cmd_order_show)

        cano = porder_sub.add_parser("cancel")
        cano.add_argument("--order", type=int, required=True)
        cano.set_defaults(func=self.cmd_order_cancel)

        return parser

    def run(self):
        parser = self.build_parser()
        args = parser.parse_args()
        if not hasattr(args, "func"):
            parser.print_help()
            return
        args.func(args)


if __name__ == "__main__":
    cli = RetailCLI()
    cli.run()
