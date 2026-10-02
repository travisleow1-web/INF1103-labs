import json
import os

FILENAME = "inventory.json"


def load_inventory():
    """Loads inventory from inventory.json if present, otherwise returns an empty dictionary."""
    if os.path.exists(FILENAME):
        print(f"{FILENAME} found.")
        try:
            with open(FILENAME, "r") as file:
                inventory = json.load(file)
            print("Inventory loaded successfully.")
            return inventory
        except json.JSONDecodeError:
            print("Error parsing inventory.json. Starting with empty inventory.")
            return {}
    else:
        print(f"{FILENAME} not found. Starting with empty inventory.")
        return {}


def save_inventory(inventory, is_exit=False):
    """Saves inventory data to inventory.json."""
    if is_exit:
        print("Saving inventory before exit...")
    else:
        print("Saving inventory...")

    with open(FILENAME, "w") as file:
        json.dump(inventory, file, indent=4)

    if is_exit:
        print("Inventory saved successfully.")
    else:
        print(f"Inventory saved successfully to {FILENAME}.")


def display_all(inventory):
    """Displays all products in formatted structure."""
    print("Current Inventory")
    print("-" * 48)
    if not inventory:
        print("Inventory is currently empty.")
    else:
        for p_id, item in inventory.items():
            price = float(item["price"])
            stock = int(item["stock"])
            print(
                f"ID: {p_id} | Name: {item['name']} | Price: ${price:.2f} | Stock: {stock}"
            )
    print("-" * 48)


def add_product(inventory):
    """Adds a new product item to the inventory dictionary."""
    print("Add New Product")
    p_id = input("Product ID: ").strip()

    if p_id in inventory:
        print("Product ID already exists!")
        return

    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("Invalid input for price or stock. Addition canceled.")
        return

    inventory[p_id] = {"name": name, "price": price, "stock": stock}
    print("Product added successfully!")


def update_stock(inventory):
    """Updates stock quantity for an existing product."""
    print("Update Stock")
    p_id = input("Enter Product ID: ").strip()

    if p_id not in inventory:
        print("Product not found.")
        return

    item = inventory[p_id]
    print("Product Found:")
    print(f"Name: {item['name']}")
    print(f"Current Stock: {item['stock']}")

    try:
        new_stock = int(input("New Stock Quantity: "))
        inventory[p_id]["stock"] = new_stock
        print("Stock updated successfully!")
    except ValueError:
        print("Invalid stock number. Update canceled.")


def search_product(inventory):
    """Searches for a specific product by ID."""
    print("Search Product")
    p_id = input("Enter Product ID: ").strip()

    if p_id in inventory:
        item = inventory[p_id]
        price = float(item["price"])
        print("Product Found")
        print("-" * 48)
        print(f"ID: {p_id}")
        print(f"Name: {item['name']}")
        print(f"Price: ${price:.2f}")
        print(f"Stock: {item['stock']}")
        print("-" * 48)
    else:
        print("Product not found.")


def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    inventory = load_inventory()

    while True:
        print("----------- MENU -----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")
        print("----------------------------")

        option = input("Enter option: ").strip()

        if option == "1":
            display_all(inventory)
        elif option == "2":
            add_product(inventory)
        elif option == "3":
            update_stock(inventory)
        elif option == "4":
            search_product(inventory)
        elif option == "5":
            save_inventory(inventory, is_exit=False)
        elif option == "6":
            save_inventory(inventory, is_exit=True)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()