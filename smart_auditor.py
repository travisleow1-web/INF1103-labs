from abc import ABC, abstractmethod
import json
import os
import csv

class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        pass

class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total

class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float):
        if percentage < 0 or percentage > 100:
            raise ValueError("Percentage must be between 0 and 100.")
        self.percentage: float = float(percentage)

    def apply(self, total: float) -> float:
        return total * (1 - self.percentage / 100.0)

class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float, amount: float):
        self.threshold: float = float(threshold)
        self.amount: float = float(amount)

    def apply(self, total: float) -> float:
        return max(0.0, total - self.amount) if total >= self.threshold else total

class StudentDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total * 0.95  # 5% student discount   

class Supplier:
    def __init__(self, supplier_id: str,name: str, contact_email: str):
        self.supplier_id:str = supplier_id
        self.name: str = name
        self.contact_email: str = contact_email

    def display_supplier_info(self) -> None:
        print(f"Supplier Name: {self.name} , ID: {self.supplier_id} | Contact Email: {self.contact_email}")

class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass


class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, weight: float = 0.0):
        price_val = float(price)
        stock_val = int(stock)
        if price_val < 0:
           raise ValueError("Price cannot be negative.")
        if stock_val < 0:
           raise ValueError("Stock cannot be negative.")

        self._product_id = product_id
        self.name = name
        self._price = float(price)
        self._stock = int(stock)
        self._weight = float(weight)  # Default weight in kg
        self.supplier: Supplier = supplier

    @property
    def product_id(self) -> str:
        return self._product_id

    @property
    def price(self) -> float:
        return self._price

    def update_stock(self, quantity: int) -> None:
        self._stock = quantity

    def display_information(self) -> None:
        print(f"ID: {self._product_id} | Name: {self.name} | Price: ${self._price:.2f} | Stock: {self._stock} | Supplier: {self.supplier.name if self.supplier else 'N/A'}", end="")

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Abstract method forcing subclasses to define fulfilment behavior."""
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """Abstract method to ensure subclasses export full attributes for JSON persistence."""
        pass


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, weight: float):
        super().__init__(product_id, name, price, stock, supplier)
        weight_val = float(weight)
        if weight_val < 0:
            raise ValueError("Weight cannot be negative.")
        self._weight = float(weight)  # Default weight in kg

    def update_stock(self, quantity: int) -> None:
        self._stock = quantity

    def display_information(self):
        super().display_information()
        print(f"ID: {self._product_id} | Name: {self.name} | Price: ${self._price:.2f} | Stock: {self._stock} | Supplier: {self.supplier.name if self.supplier else 'N/A'}")

    def get_fulfilment_info(self) -> str:
        return f"Product requires physical shipping. Weight: {self._weight} kg"

    def get_fulfillment_info(self) -> str:
        return self.get_fulfilment_info()

    def calculate_shipping_cost(self) -> float:
        base_cost = 5.0  # Base shipping cost
        cost_per_kg = 2.0  # Cost per kg
        return base_cost + (cost_per_kg * self._weight)

    def to_dict(self) -> dict:
        return {
            "type": "physical",
            "product_id": self._product_id,
            "name": self.name,
            "price": self._price,
            "stock": self._stock,
            "weight": self._weight,
            "supplier": {
                "supplier_id": self.supplier.supplier_id if self.supplier else None,
                "name": self.supplier.name if self.supplier else None,
                "contact_email": self.supplier.contact_email if self.supplier else None
        }
        }


class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, download_size: float):
        super().__init__(product_id, name, price, stock, supplier)
        size_val = float(download_size)
        if size_val < 0:    
            raise ValueError("Download size cannot be negative.")
        self.download_size = float(download_size)  # Size in MB

    def display_information(self) -> None:
        super().display_information()
        print(f" | Download Size: {self.download_size}MB")

    def get_fulfilment_info(self) -> str:
        return f"Product is digital and can be delivered electronically. No shipping required, download size: {self.download_size} MB"

    def get_fulfillment_info(self) -> str:
        return self.get_fulfilment_info()

    def to_dict(self) -> dict:
        return {
            "type": "digital",
            "product_id": self._product_id,
            "name": self.name,
            "price": self._price,
            "stock": self._stock,
            "download_size": self.download_size,
            "supplier": {
                "supplier_id": self.supplier.supplier_id if self.supplier else None,
                "name": self.supplier.name if self.supplier else None,
                "contact_email": self.supplier.contact_email if self.supplier else None
            }
        }
        
class ProductFactory:
    @staticmethod
    def create(
        product_type: str,
        product_id: str,
        name: str,
        price: float,
        stock_quantity: int,
        supplier: Supplier | None = None,
        extra_attr: float = 1.0,
    ) -> Product:
        p_type = product_type.strip().lower()
        if p_type == "physical":
            return PhysicalProduct(product_id, name, price, stock_quantity, supplier, extra_attr)
        elif p_type == "digital":
            return DigitalProduct(product_id, name, price, stock_quantity, supplier, extra_attr)
        else:
            raise ValueError(f"Unknown product type: {product_type}")
        
class Inventory:
    def __init__(self):
        self.products : list[Product] = []

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def remove_product(self, product_id: str) -> bool:
        product = self.search_product(product_id)
        if product:
            self.products.remove(product)
            return True
        return False

    def search_product(self, product_id:str) -> Product | None:
        for p in self.products:
            if p._product_id == product_id:
                return p
        return None

    def display_all(self):
        if not self.products:
            print("The inventory is currently empty.")
        else:
            for p in self.products:
                p.display_information()

class OrderLine:
    def __init__(self, product: Product, quantity: int):
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        self.product: Product = product
        self.quantity: int = int(quantity)
        

    def calculate_line_total(self) -> float:
        return self.product._price * self.quantity 

    def display_order_line(self):
        print(f"Product ID: {self.product._product_id} | Name: {self.product.name} | Quantity: {self.quantity} | Price per unit: ${self.product._price:.2f}")

class Order:
    def __init__(self, order_id: str, discount: DiscountStrategy | None = None):
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = [] 
        self.discount: DiscountStrategy = discount if discount is not None else NoDiscount()

    def set_discount(self, discount: DiscountStrategy) -> None:
        self.discount = discount
        
    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        for line in self.order_lines:
            if line.product._product_id == product_id:
                self.order_lines.remove(line)
                return True
        return False

    def calculate_order_total(self) -> float:
        total = sum(line.calculate_line_total() for line in self.order_lines)
        return self.discount.get_discounted_total(total)

    def display_order(self) -> None:
        print(f"Order ID: {self.order_id}")
        for line in self.order_lines:
            print(f" - {line.product.name} x {line.quantity} = ${line.calculate_line_total():.2f}")
        print(f"Total Order Cost: ${self.calculate_order_total():.2f}")

def get_positive_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                raise ValueError("Value must be non-negative.")
            return value
        except ValueError as e:
            print(f"Invalid input: {e}. Please enter a valid number.")

def get_positive_int(prompt: str) -> int:
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                raise ValueError("Value must be a positive integer.")
            return value
        except ValueError as e:
            print(f"Invalid input: {e}. Please enter a valid integer.")

def get_non_negative_int(prompt: str) -> int:
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                raise ValueError("Value must be a non-negative integer.")
            return value
        except ValueError as e:
            print(f"Invalid input: {e}. Please enter a valid integer.")

            
def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> int:
    loaded = 0
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header row
            for row_num, row in enumerate(reader, start=2):
                if len(row) < 5:
                    print(f"Row {row_num} skipped: incomplete data.")
                    continue
                try:
                    p_type, pid, name, price_str, stock_str = [col.strip() for col in row[:5]]
                    prod = ProductFactory.create(p_type, pid, name, float(price_str), int(stock_str), supplier)
                    inventory.add_product(prod)
                    loaded += 1
                except ValueError as err:
                    print(f"Row {row_num} skipped ({row}): {err}")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")
    return loaded


def load_inventory(filename="inventory.json")-> Inventory:
    inventory = Inventory()
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            try:
                data = json.load(file)
                for item in data:
                    sup_data = item.get("supplier") or {"supplier_id": "S000", "name": "Default Supplier", "contact_email": "support@example.com"}
                    supplier = Supplier(sup_data["supplier_id"], sup_data["name"], sup_data["contact_email"])
                    extra = item.get("weight", 1.0) if item.get("type") == "physical" else item.get("download_size", 10.0)
                    prod = ProductFactory.create(item["type"], item["product_id"], item["name"], item["price"], item["stock"], supplier, extra)
                    inventory.add_product(prod)
                print("Inventory loaded successfully.")
            except json.JSONDecodeError:
                print("Error reading the JSON file. Starting with an empty inventory.")
    else:
        print("No existing inventory file found. Starting fresh.")
    return inventory

def save_inventory(inventory: Inventory, filename: str ="inventory.json"):
    data = [p.to_dict() for p in inventory.products]
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    print("Inventory saved successfully.")


def relationship_demo():
    print ("=== Lab 8 Relationship Demonstration ===")
    sup = supplier = Supplier("S001", "Tech Supplies Inc.", "contact@techsupplies.com")
    p1 = PhysicalProduct("1001", "Laptop", 999.99, 10, supplier, 2.5)
    p2 = DigitalProduct("2001", "E-Book", 19.99, 100, supplier, 5.0)
    del sup  # Explicitly delete the supplier reference to demonstrate relationship handling
    show_product_details(p1)
    show_product_details(p2)

    #2 Aggregation tests 
    inv_1 = Inventory()
    inv_2 = Inventory()
    inv_1.add_product(p1)
    inv_1 .remove_product("1001")
    inv_2.add_product(p1)
    print("Product transferred from inv_1 to inv_2. Current inventories:")
    inv_1.display_all()
    inv_2.display_all()

    #3 Composition tests
    order1 = Order("ORD001")
    order2 = Order("ORD002")
    order1.add_order_line(p1, 2)
    order2.add_order_line(p2, 1)
    order2.add_order_line(p1, 1)
    print(f"Are the products the same for both orders?{order1.order_lines[0].product is order2.order_lines[0].product}")
    print(f"Are the products different for the respective orders? {order1.order_lines[0].product is not order2.order_lines[1].product}")
    order1.display_order()
    order2.display_order()
# main.py (Append this to the bottom of your file)

def main():
    inventory = load_inventory()

    while True:
        print("\n--- Inventory Management System ---")
        print("1. Display all products")
        print("2. Add a product (with supplier details)")
        print("3. Remove a product")
        print("4. Update stock quantity for a product")
        print("5. Create & Calculate Sample Order")
        print("6. Search for a product & view details")
        print("7. Save inventory")
        print("8. Run Lab 8 Relationship Demonstration")
        print("9. Import products from CSV file")
        print("10. Exit")

        choice = input("Enter your choice (1-10): ")

        if choice == '1':
            inventory.display_all()
            
        elif choice == '2':
            p_type = input("Enter product type (1. Physical / 2. Digital): ").strip()
            pid = input("Enter Product ID: ").strip()
            name = input("Enter Product Name: ").strip()
            price = get_positive_float(input("Enter Price: "))
            stock = get_non_negative_int(input("Enter Stock Quantity: "))
            s_id = input("Enter Supplier ID: ").strip()
            s_name = input("Enter Supplier Name: ").strip()
            s_email = input("Enter Supplier Contact Email: ").strip()
            supplier = Supplier(s_id, s_name, s_email)
            extra_prompt = "Enter Weight (kg): " if p_type == 'physical' else "Enter Download Size (MB): "
            extra = get_positive_float(extra_prompt)

            try:
                new_product = ProductFactory.create(p_type, pid, name, price, stock, supplier, extra)
                inventory.add_product(new_product)
                print(f"Product {name} added successfully.")
            except ValueError as err:
                print(f"Could not create product: {err}")

        elif choice == '3':
            pid = input("Enter Product ID to remove: ").strip()
            if inventory.remove_product(pid):
                print("Product removed successfully.")
                continue
            else:
                print("Product not found.")
                continue
            
        elif choice == '4':
            pid = input("Enter Product ID to update: ")
            product = inventory.search_product(pid)
            if product:
                new_stock = get_non_negative_int(input("Enter the new stock quantity: "))
                product.update_stock(new_stock)
                print("Stock updated successfully.")
                continue
            else:
                print("Product not found.")
                continue

        elif choice == '5':
            order_id = input("Enter Order ID: ").strip()
            order = Order(order_id)
            while True:
                pid = input("Enter Product ID to add to order (or 'done' to finish): ").strip()
                if pid.lower() == 'done':
                    break
                product = inventory.search_product(pid)
                if product:
                    quantity = get_positive_int(input(f"Enter quantity for {product.name}: "))
                    order.add_order_line(product, quantity)
                else:
                    print("Product not found.")

            print("Select Discount Strategy: 1. None | 2. 10% Off | 3. Bulk ($20 off $200+) | 4. Student (5% Off)")
            d_choice = input("Choice: ").strip()
            if d_choice == "2":
                order.set_discount(PercentageDiscount(10))
            elif d_choice == "3":
                order.set_discount(BulkDiscount(200, 20))
            elif d_choice == "4":
                order.set_discount(StudentDiscount())

            print("\nOrder Summary:")
            order.display_order()

        elif choice == '6':
            pid = input("Enter Product ID to search: ").strip()
            product = inventory.search_product(pid)
            if product:
                product.display_information()
                print(f"Fulfilment: {product.get_fulfilment_info()}")
                if isinstance(product, CanBeShipped):
                    print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")
            else:
                print("Product not found.")

        elif choice == '7':
            save_inventory(inventory)
            continue

        elif choice == '8':
            relationship_demo()
            continue

        elif choice == "9":
            path = input("Enter CSV filename (default 'products.csv'): ").strip() or "products.csv"
            default_sup = Supplier("S001", "CSV Import Supplier", "import@supplier.com")
            load_products(path, inventory, default_sup)
            
        elif choice == '10':
            print("Exiting system...")
            break
            
        else:
            print("Invalid input. Please enter a number between 1 and 9.")

if __name__ == "__main__":
    main()