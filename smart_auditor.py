
import json
import os

class Product:
    def __init__(self, product_id, name, price, stock):
        self._product_id = product_id
        self.name = name
        self._price = float(price)
        self._stock = int(stock)

    def update_stock(self, quantity):
        self._stock = quantity

    def display_information(self):
        print(f"ID: {self._product_id} | Name: {self.name} | Price: ${self._price:.2f} | Stock: {self._stock}")

    def to_dict(self):
        return {
            "product_id": self._product_id,
            "name": self.name,
            "price": self._price,
            "stock": self._stock
        }

class Inventory:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def search_product(self, product_id):
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



def load_inventory(filename="inventory.json"):
    inventory = Inventory()
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            try:
                data = json.load(file)
                for item in data:
                    prod = Product(item['product_id'], item['name'], item['price'], item['stock'])
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