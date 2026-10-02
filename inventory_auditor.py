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
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error reading {FILENAME}: {e}. Starting with empty inventory.")
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

    try:
        with open(FILENAME, "w") as file:
            json.dump(inventory, file, indent=4)

        if is_exit:
            print("Inventory saved successfully.")
        else:
            print(f"Inventory saved successfully to {FILENAME}.")
    except Exception as e:
        print(f"Failed to save inventory: {e}")


def display_all(inventory):
    """Displays all products in formatted structure with validation."""
    print("Current Inventory")
    print("-" * 48)
    if not inventory:
        print("No products currently in inventory.")
        print("Use Option 2 (Add Product) to add items to your inventory.")
    else:
        for p_id, item in inventory.items():
            try:
                price = float(item.get("price", 0))
                stock = int(item.get("stock", 0))
                name = item.get("name", "Unknown")
                print(
                    f"ID: {p_id} | Name: {name} | Price: ${price:.2f} | Stock: {stock}"
                )
            except (ValueError, TypeError):
                print(f"ID: {p_id} | [Error: Corrupted product data format]")
    print("-" * 48)


def get_non_empty_string(prompt):
    """Ensures user enters a non-empty string."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")


def get_valid_float(prompt):
    """Validates numeric price input."""
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Price cannot be negative. Please try again.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid decimal number (e.g. 29.99).")


def get_valid_int(prompt):
    """Validates integer stock input."""
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Stock quantity cannot be negative. Please try again.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid whole number (e.g. 10).")


def add_product(inventory):
    """Adds a new product item with input validation."""
    print("Add New Product")
    p_id = get_non_empty_string("Product ID: ")

    if p_id in inventory:
        print("Error: Product ID already exists!")
        return

    name = get_non_empty_string("Product Name: ")
    price = get_valid_float("Price: ")
    stock = get_valid_int("Stock Quantity: ")

    inventory[p_id] = {"name": name, "price": price, "stock": stock}
    print("Product added successfully!")


def update_stock(inventory):
    """Updates stock quantity for an existing product with validation."""
    print("Update Stock")
    p_id = get_non_empty_string("Enter Product ID: ")

    if p_id not in inventory:
        print("Product not found.")
        return

    item = inventory[p_id]
    print("Product Found:")
    print(f"Name: {item['name']}")
    print(f"Current Stock: {item['stock']}")

    new_stock = get_valid_int("New Stock Quantity: ")
    inventory[p_id]["stock"] = new_stock
    print("Stock updated successfully!")


def search_product(inventory):
    """Searches for a specific product by ID."""
    print("Search Product")
    p_id = get_non_empty_string("Enter Product ID: ")

    if p_id in inventory:
        item = inventory[p_id]
        try:
            price = float(item["price"])
            stock = int(item["stock"])
            print("Product Found")
            print("-" * 48)
            print(f"ID: {p_id}")
            print(f"Name: {item['name']}")
            print(f"Price: ${price:.2f}")
            print(f"Stock: {stock}")
            print("-" * 48)
        except (ValueError, TypeError):
            print("Error: Product data is corrupted.")
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


#Product not found issue has been rectified by ensuring that the product ID is checked against the inventory dictionary. The search_product function now correctly verifies if the product ID exists and handles cases where the product data may be corrupted.
