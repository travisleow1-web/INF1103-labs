import os

FILENAME = "inventory.txt"
OVERSTOCK_LIMIT = 500

def load_inventory(filename=FILENAME):
    """
    Reads transaction amounts from the inventory file.
    If the file does not exist, returns an empty list.
    """
    history = []
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                for line in file:
                    line = line.strip()
                    if line.isdigit():
                        history.append(int(line))
        except Exception as e:
            print(f"Error reading {filename}: {e}")
    else:
        print(f"No existing {filename} found. Starting with empty inventory.")
    
    return history


def save_inventory(history, filename=FILENAME):
    """
    Saves the list of transaction history entries to disk.
    """
    try:
        with open(filename, "w") as file:
            for item in history:
                file.write(f"{item}\n")
        print(f"\nOrder/inventory successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving to {filename}: {e}")


def main():
    # 1. Load history (starts at [] and count 0 if file is missing)[cite: 5]
    history = load_inventory(FILENAME)
    failed_entries = 0
    
    running_total = sum(history)
    print(f"Current Inventory Count: {running_total}\n")

    # 2. Input loop
    while True:
        user_input = input("Enter stock quantity (or 'quit' to exit): ").strip()
        
        if user_input.lower() == "quit":
            break
            
        if not user_input.isdigit():
            print("Invalid input! Please enter a valid non-negative integer.")
            failed_entries += 1
            continue
            
        amount = int(user_input)
        history.append(amount)
        running_total += amount
        print(f"Added {amount} units. Current Total: {running_total}")
        
        if running_total > OVERSTOCK_LIMIT:
            print(f"\nALERT: Overstock limit of {OVERSTOCK_LIMIT} reached!")
            break

    # 3. Save to file on exit[cite: 5]
    save_inventory(history, FILENAME)
    
    # 4. Final summary
    print("\n--- FINAL REPORT ---")
    print(f"Total Transactions Processed: {len(history)}")
    print(f"Total Units in Inventory:    {sum(history)}")
    print(f"Failed Entries:              {failed_entries}")


if __name__ == "__main__":
    main()

#commit 5, Realligned the functions to match lesson materials instead of previous lessons. 
