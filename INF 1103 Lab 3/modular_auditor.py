def get_valid_input():
    """Prompts the user, validates input, and returns an int or 'quit'."""
    user_input = input("Enter stock quantity (or 'quit' to stop): ").strip()

    if user_input.lower() == 'quit':
        return 'quit'

    # Check for negative numbers
    if user_input.startswith('-') and user_input[1:].isdigit():
        print("Error: Stock values cannot be negative.")
        return None

    # Check for non-numeric input
    if not user_input.isdigit():
        print("Error: Invalid input. Please enter a valid number.")
        return None

    return int(user_input)


def process_delivery(current_total, new_value):
    """Calculates and returns the updated total inventory."""
    return current_total + new_value


def calculate_tax(amount):
    """Calculates 10% tax for a given delivery amount."""
    return amount * 0.10


def generate_report(total_units, failed_attempts):
    """Prints the final summary report."""
    print("\n--- End of Day Report ---")
    print(f"Total Units Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")


def main():
    inventory = 0
    failed_entries = 0

    while True:
        stock = get_valid_input()

        if stock == 'quit':
            break

        if stock is None:
            failed_entries += 1
            continue

        # Process tax and inventory update using functions
        tax = calculate_tax(stock)
        inventory = process_delivery(inventory, stock)

        print(f"Accepted {stock} units (Tax: ${tax:.2f}). Current inventory: {inventory}")

        # Overstock check
        if inventory > 500:
            print("OVERSTOCK ALERT: Total inventory exceeds 500 units! Halting deliveries.")
            break

    # Generate final report
    generate_report(inventory, failed_entries)


if __name__ == "__main__":
    main()

#Step 3 