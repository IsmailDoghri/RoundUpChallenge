from starling_bank_client import StarlingBankClient
from utils import calculate_round_up
from datetime import datetime, timedelta
import uuid

# Usage example:
access_token = "eyJhbGciOiJQUzI1NiIsInppcCI6IkdaSVAifQ.H4sIAAAAAAAA_21Ty5KcMAz8lRTn1RYPMzxuueUH8gGyLc-4FmzKNrPZSuXfYzAMw9Te6G6pJVnib6a9z_oMJw2SRvvuA7pBmytH8_Eu7Ji9ZX7mMaIqLuqSFxVUxAtgknHgRZ5DXmLV5IgCqzoG058p64smb-uq7VjxlmkMiWB1WS8ECmFnE37ZQZL7reXmrZhqoOikAlYVBXCZcyDJ2zIKijoVvYP9IJMyGn4puGIFdCxvgamyBC7aGnhOjKSI1RTGjDjWTyHI-6OOuDAFCkkC45eYUBMDbLDo2gbLpmPLwMJOtDxK6hRua6tgcKTeEcofL0L4ml4ELckErTS5Mz9oH07MBqR0scmepA4PkJQQUNxGekTO4Wad9nFDoI3Udy1nHJLGcUAjtk4EOgnCmuDskHwXZtOsUdqNGLQ1YONrzEZu9cTsgx33tmlEvWWPaCQG6iUNFOgB17CRAkaEvYhwEXe8Zk74RbRLCWwmCRxBoEe8bp5JOz4hODQexdLzg4bBijj94Z0IsMszvLJblrNKD3upVPtErVGOBOkpnIA_S59OR3eP97gKD1d79HHitlFP3OrzzKThVHz2bywO8RuvQ0ym4kZyHuJxx7GPq_EUQhxwnjY44X4m8XePVxSPyTr5VP7M7nXP7Df5YD_Ngw-0NADC31-pSapEPe90XcXrkrN__wE6D0O_oQQAAA.MOCEJRin_exTsRfyLw-fuPUjz4EeR66pavIv4ApKaLemokogldkq0SsGsFOBRcZlFayIAGsXulET7oSbR3QyHJUnPnpBCu9x733St-l9DM1m8B9q93YhdrPK2qV5CbkLUK_LLTtGuoKCSi55BbjmoJoCkicqAswEv0Fa08IX32Fwdl1SnDKq-e0QKIpbd2MIwakvzhzGRJGDT_MSWYrdyQh0oFeVdjc-CMAzpwAiUMrAv8VD0T7-ukmE66heqlb8ZkhvWxCFsuKk_nC__0GKyXeXClPEa18r6zILcIpeTodovFcukccggqueTYVW_4UO9jwLLaEBe9PFAHyeNViEhwYzv2a9KlnJkWfc_Fk4g2TG6qQyqwKK1EUtHn-hMOvC7HnHDXOvN-l9Mbs0JWuGc89NckEv0SipaYbbdOy7k4ZDMWY6Ca7k0GB3qvsZsLYPsW0hLdWhAWtVu6q-NQxdVm4J6ZwXjgTiF-mOm6KzAQs5H-jXl8sJhdXL1EInLVDNWWheebTj31MaF1NNSM4Q7hCc99Waww6qezPw4eyL9jzvxXQmr2-RaFHDOImU33QlybWxFf2oEDmyfPPtQUpJFzIqZnS1oaTFenqny850FzBh0Y55KUl0wZmz1ff5J4BmcMF-cTDwGs3V651kjixUl4KJmsFqyDEPMBJguxynayY"
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
