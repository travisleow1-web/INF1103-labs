from abc import ABC, abstractmethod
import json
import os
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
    def __init__(self, product_id: str, name: str, price: float, stock: int, weight: float = 0.0, supplier: Supplier = None):
        self._product_id = product_id
        self.name = name
        self._price = float(price)
        self._stock = int(stock)
        self.supplier: Supplier = supplier

    def update_stock(self, quantity: int) -> None:
        self._stock = quantity

    def display_information(self) -> None:
        print(f"ID: {self._product_id} | Name: {self.name} | Price: ${self._price:.2f} | Stock: {self._stock} | Supplier: {self.supplier.name if self.supplier else 'N/A'}", end=" ")

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
        super().__init__(product_id, name, price, stocks, supplier)
        self._weight = float(weight)  # Default weight in kg

    def update_stock(self, quantity: int) -> None:
        self._stock = quantity

    def display_information(self):
        print(f"ID: {self._product_id} | Name: {self.name} | Price: ${self._price:.2f} | Stock: {self._stock} | Supplier: {self.supplier.name if self.supplier else 'N/A'}", end=" ")

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
            "weight": self._weight
        }


class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int, download_size: float):
        super().__init__(product_id, name, price, stock)
        self.download_size = float(download_size)  # Size in MB

    def display_information(self) -> None:
        print(f" | Download Size: {self.download_size}MB", end=" ")

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
            "download_size": self.download_size
        }

class Inventory:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def search_product(self, product_id:str):
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



def load_inventory(filename="inventory.json")-> Inventory:
    inventory = Inventory()
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            try:
                data = json.load(file)
                for item in data:
                    if item['type'] == 'physical':
                        prod = PhysicalProduct(item['product_id'], item['name'], item['price'], item['stock'], item.get('weight', 0.0))
                    elif item['type'] == 'digital':
                        prod = DigitalProduct(item['product_id'], item['name'], item['price'], item['stock'], item.get('download_size', 0.0))
                    inventory.add_product(prod)
                print("Inventory loaded successfully.")
            except json.JSONDecodeError:
                print("Error reading the JSON file. Starting with an empty inventory.")
    else:
        print("No existing inventory file found. Starting fresh.")
    return inventory

def save_inventory(inventory, filename="inventory.json"):
    data = [p.to_dict() for p in inventory.products]
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    print("Inventory saved successfully.")


# main.py (Append this to the bottom of your file)

def main():
    inventory = load_inventory()

    while True:
        print("\n--- Inventory Management System ---")
        print("1. Display all products")
        print("2. Add a product")
        print("3. Update stock")
        print("4. Search for a product")
        print("5. Save inventory")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            inventory.display_all()
            
        elif choice == '2':
            p_type = input("Enter product type (1. Physical / 2. Digital): ").strip()
            pid = input("Enter Product ID: ").strip()
            name = input("Enter Product Name: ").strip()
            price = float(input("Enter Price: "))
            stock = int(input("Enter Stock Quantity: "))

            if p_type == '1':
                weight = float(input("Enter Weight (kg): "))
                new_product = PhysicalProduct(pid, name, price, stock, weight)
            elif p_type == '2':
                download_size = float(input("Enter Download Size (MB): "))
                new_product = DigitalProduct(pid, name, price, stock, download_size)
            else:
                print("Invalid product type.")
                continue

            inventory.add_product(new_product)
            print(f"Product {name} added successfully.")
            
        elif choice == '3':
            pid = input("Enter Product ID to update: ")
            product = inventory.search_product(pid)
            if product:
                new_stock = int(input("Enter the new stock quantity: "))
                product.update_stock(new_stock)
                print("Stock updated successfully.")
            else:
                print("Product not found.")
                
        elif choice == '4':
            pid = input("Enter Product ID to search: ").strip()
            product = inventory.search_product(pid)
            if product:
                product.display_information()
                print(f"Fulfilment: {product.get_fulfilment_info()}")
                if isinstance(product, CanBeShipped):
                    print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")
            else:
                print("Product not found.")
                
        elif choice == '5':
            save_inventory(inventory)
            
        elif choice == '6':
            print("Exiting system...")
            break
            
        else:
            print("Invalid input. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()