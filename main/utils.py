def calculate_round_up(transactions):
    """Calculate the total round-up amount for outgoing transactions."""
    total_round_up = 0
    for transaction in transactions:
        if transaction["direction"] == "OUT":
            amount = transaction["amount"]["minorUnits"]
            round_up = (100 - (amount % 100)) % 100
            total_round_up += round_up
    return total_round_up / 100  # Convert to major units
