
import os

FILENAME = "inventory.txt"
OVERSTOCK_LIMIT = 500

def load_inventory(filename=FILENAME):
    """
    Loads transaction history from the inventory file if it exists.
    Returns a list of transaction integers.
    """
    history = []
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                for line in file:
                    line = line.strip()
                    if line.isdigit():
                        history.append(int(line))
            print(f"Successfully loaded {len(history)} previous transaction(s) from {filename}.")
        except Exception as e:
            print(f"Warning: Could not read {filename} ({e}). Starting with empty inventory.")
    else:
        print(f"No existing {filename} found. Starting with a fresh inventory.")
    
    return history


def save_inventory(history, filename=FILENAME):
    """
    Saves all transaction history amounts to the inventory file.
    """
    try:
        with open(filename, "w") as file:
            for item in history:
                file.write(f"{item}\n")
        print(f"\nInventory history successfully saved to {filename}")
    except Exception as e:
        print(f"Error: Failed to write to {filename}: {e}")


def get_valid_input():
    """
    Prompts the user for a stock quantity or 'quit'.
    Returns the lowercased string 'quit', an integer value, or None if invalid.
    """
    user_input = input("Enter stock quantity (or 'quit' to exit): ").strip()
    
    if user_input.lower() == "quit":
        return "quit"
    
    if user_input.isdigit():
        value = int(user_input)
        if value >= 0:
            return value
    
    return None


def main():
    print("=== Modular Inventory Auditor (Persistent) ===")
    
    # 1. Load existing transaction history from file
    history = load_inventory(FILENAME)
    failed_entries = 0
    
    # Calculate current starting total from existing history
    running_total = sum(history)
    print(f"Current Starting Total: {running_total} units\n")
    
    # 2. Main execution loop
    while True:
        entry = get_valid_input()
        
        if entry == "quit":
            print("\nExiting audit routine...")
            break
        
        if entry is None:
            print("Invalid entry! Please enter a non-negative integer.")
            failed_entries += 1
            continue
        
        # Track valid transaction in history list and update running total
        history.append(entry)
        running_total += entry
        print(f"Added {entry} units. Current Total: {running_total}")
        
        # Enforce business rule: Overstock alert at 500 units
        if running_total > OVERSTOCK_LIMIT:
            print(f"\nALERT: Overstock limit reached ({running_total} > {OVERSTOCK_LIMIT} units)!")
            break

    # 3. Save updated history to disk
    save_inventory(history, FILENAME)
    
    # 4. Final Reporting
    print("\n--- FINAL AUDIT REPORT ---")
    print(f"Total Transactions Recorded: {len(history)}")
    print(f"Total Units Processed:      {sum(history)}")
    print(f"Failed/Rejected Entries:   {failed_entries}")
    print("---------------------------")


if __name__ == "__main__":
    main()

# Commit 1