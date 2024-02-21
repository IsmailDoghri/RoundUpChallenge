from starling_bank_client import StarlingBankClient
from utils import calculate_round_up
from datetime import datetime, timedelta
import uuid
import os

# Usage example:
# Retrieve the access token from the environment variable
access_token = os.getenv('STARLING_ACCESS_TOKEN')
client = StarlingBankClient(access_token)

# Get transactions for the last week
today = datetime.utcnow().date()
start_date = (today - timedelta(days=today.weekday() + 7)).isoformat()
end_date = (today - timedelta(days=today.weekday())).isoformat()
transactions = client.get_transactions(start_date, end_date)

# Calculate the round-up amount
round_up_amount = calculate_round_up(transactions["feedItems"])
print(f"Round-up amount for the week: £{round_up_amount}")

# Create a savings goal (if it doesn't exist) and transfer the round-up amount
savings_goal_name = "Future Adventures"
savings_goal = client.create_savings_goal(savings_goal_name)
savings_goal_uid = savings_goal["savingsGoalUid"]
transfer_uid = str(uuid.uuid4())
client.transfer_to_savings_goal(savings_goal_uid, transfer_uid, int(round_up_amount * 100))  # Convert amount to minor

savings_goal_uid = savings_goal_uid
savings_goal_details = client.get_savings_goal(savings_goal_uid)
print("Savings Goal Details:")
print(f"- Name: {savings_goal_details['name']}")

# Handle possible absence of 'target' key
target = savings_goal_details.get('target', {})
target_currency = target.get('currency', 'N/A')
target_minor_units = target.get('minorUnits', 0) / 100
print(f"- Target Amount: {target_currency} {target_minor_units}")

# Print total saved and goal percentage
print(
    f"- Total Saved: {savings_goal_details['totalSaved']['currency']} {savings_goal_details['totalSaved']['minorUnits'] / 100}")

# Handle possible absence of 'savedPercentage' key
goal_percentage = savings_goal_details.get('savedPercentage', 'N/A')
print(f"- Goal Percentage: {goal_percentage}%")
