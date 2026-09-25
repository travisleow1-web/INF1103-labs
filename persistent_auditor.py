import os

FILENAME = "orders.txt"

# Standard item catalog (IDs 1001 to 1003)
DEFAULT_CATALOG = [
    {"id": 1001, "name": "Wireless Mouse", "quantity": 0},
    {"id": 1002, "name": "Keyboard", "quantity": 0},
    {"id": 1003, "name": "USB Cable", "quantity": 0}
]

def load_orders(filename=FILENAME):
    """
    Loads existing orders from disk. If no file exists,
    initializes the standard catalog (1001-1003) with 0 quantities[cite: 7].
    """
    orders = []
    if os.path.exists(filename):
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(",")
                    if len(parts) == 3:
                        orders.append({
                            "id": int(parts[0].strip()),
                            "name": parts[1].strip(),
                            "quantity": int(parts[2].strip())
                        })
    
    # Fallback if file is missing or empty
    if not orders:
        orders = [dict(item) for item in DEFAULT_CATALOG]
        
    return orders


def display_orders(orders):
    """
    Prints current active order totals[cite: 7].
    """
    print("Current Orders:\n")
    for item in orders:
        print(f"{item['id']}, {item['name']}, {item['quantity']}")
    print()


def save_orders(orders, filename=FILENAME):
    """
    Writes updated order totals back to orders.txt[cite: 7].
    """
    with open(filename, "w") as file:
        for item in orders:
            file.write(f"{item['id']},{item['name']},{item['quantity']}\n")
            
    print(f"\nOrder successfully saved to {filename}")


def main():
    # 1. Load initial state
    orders = load_orders(FILENAME)
    display_orders(orders)

    print("--- Enter order quantities for each product ---")
    
    # 2. Cycle automatically through each item (1001 -> 1002 -> 1003)
    for item in orders:
        user_input = input(f"Enter Quantity for {item['name']} (ID {item['id']}): ").strip()
        
        # Safely convert input to int; default to 0 if empty/invalid
        added_quantity = int(user_input) if user_input.isdigit() else 0
        
        # Update running quantity for this item
        item["quantity"] += added_quantity

    # 3. Display updated totals
    print("\nUpdated Summary:")
    display_orders(orders)

    # 4. Persist to file
    save_orders(orders, FILENAME)


if __name__ == "__main__":
    main()