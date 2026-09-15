# auditor.py

def main():
    # 1. Initialize the inventory to zero in the start
    inventory = 0
    failed_entries = 0

    # 2. Run in a continuous loop
    while True:
        user_input = input("Enter stock quantity (or 'quit' to stop): ").strip()

        # Check for quit condition
        if user_input.lower() == 'quit':
            break

        # 5. Enforce business rules: Reject negative numbers
        if user_input.startswith('-') and user_input[1:].isdigit():
            print("Error: Stock values cannot be negative.")
            failed_entries += 1
            continue

        # 4. Handle invalid input using .isdigit()
        if not user_input.isdigit():
            print("Error: Invalid input. Please enter a valid number.")
            failed_entries += 1
            continue

        # 3. Accept stock values as integers
        stock = int(user_input)
        
        # 6. Keep a running total of the inventory
        inventory += stock
        print(f"Accepted {stock} units. Current inventory: {inventory}")

        # 7. Trigger Overstock Alert
        if inventory > 500:
            print("OVERSTOCK ALERT: Total inventory exceeds 500 units! Halting deliveries.")
            break

    # 8. Reporting
    print("\n--- End of Day Report ---")
    print(f"Total Units Processed: {inventory}")
    print(f"Number of Failed/Rejected Entries: {failed_entries}")


if __name__ == "__main__":
    main()


#step 8