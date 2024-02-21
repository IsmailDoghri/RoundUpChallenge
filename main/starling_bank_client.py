import requests


class StarlingBankClient:
    def __init__(self, access_token):
        """Initialize the Starling Bank client with an access token."""
        self.base_url = "https://api-sandbox.starlingbank.com"
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
            "User-Agent": "Ismail Doghri"
        }
        self.accounts = self.get_accounts()
        self.account_uid = self.accounts["accounts"][0]["accountUid"]
        self.category_uid = self.accounts["accounts"][0]["defaultCategory"]
        self.changes_since = self.accounts["accounts"][0]["createdAt"]

    def get_accounts(self):
        """Retrieve the list of accounts for the authenticated user."""
        url = f"{self.base_url}/api/v2/accounts"
        response = self._make_request("GET", url)
        return response.json()

    def get_account_identifiers(self):
        """Retrieve the account identifiers (e.g., IBAN, BIC) for the primary account."""
        url = f"{self.base_url}/api/v2/accounts/{self.account_uid}/identifiers"
        response = self._make_request("GET", url)
        return response.json()

    def get_balance(self):
        """Retrieve the current balance of the primary account."""
        url = f"{self.base_url}/api/v2/accounts/{self.account_uid}/balance"
        response = self._make_request("GET", url)
        return response.json()

    def get_feed(self):
        """Retrieve the transaction feed for the primary account since account creation."""
        url = f"{self.base_url}/api/v2/feed/account/{self.account_uid}/category/{self.category_uid}?changesSince={self.changes_since}"
        response = self._make_request("GET", url)
        return response.json()

    def get_transactions(self, start_date, end_date):
        """Retrieve transactions for the primary account within a specified date range."""
        url = f"{self.base_url}/api/v2/feed/account/{self.account_uid}/category/{self.category_uid}?changesSince={start_date}T00:00:00Z&changesBefore={end_date}T23:59:59Z"
        response = self._make_request("GET", url)
        return response.json()

    def create_savings_goal(self, name, currency="GBP", target_amount=None):
        """Create a new savings goal for the primary account."""
        url = f"{self.base_url}/api/v2/account/{self.account_uid}/savings-goals"
        data = {
            "name": name,
            "currency": currency
        }
        if target_amount is not None:
            data["target"] = {"currency": currency, "minorUnits": target_amount}
        response = self._make_request("PUT", url, json=data)
        return response.json()

    def get_savings_goal(self, savings_goal_uid):
        """Retrieve details of a specific savings goal."""
        url = f"{self.base_url}/api/v2/account/{self.account_uid}/savings-goals/{savings_goal_uid}"
        response = self._make_request("GET", url)
        return response.json()

    def transfer_to_savings_goal(self, savings_goal_uid, transfer_uid, amount, currency="GBP"):
        """Transfer funds to a savings goal."""
        url = f"{self.base_url}/api/v2/account/{self.account_uid}/savings-goals/{savings_goal_uid}/add-money/{transfer_uid}"
        data = {
            "amount": {"currency": currency, "minorUnits": amount}
        }
        response = self._make_request("PUT", url, json=data)
        return response.status_code == 200

    def _make_request(self, method, url, json=None):
        """Helper method to make API requests and handle errors."""
        if method == "GET":
            response = requests.get(url, headers=self.headers)
        elif method == "PUT":
            response = requests.put(url, headers=self.headers, json=json)
        else:
            raise ValueError("Unsupported HTTP method")

        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

        return response
