import unittest
from unittest.mock import patch, MagicMock
from starling_bank_client import StarlingBankClient
import os


class TestStarlingBankClient(unittest.TestCase):

    def setUp(self):
        # Retrieve the access token from the environment variable
        self.access_token = os.getenv('STARLING_ACCESS_TOKEN')
        self.client = StarlingBankClient(self.access_token)

    @patch('starling_bank_client.requests.get')
    def test_get_accounts(self, mock_get):
        # Set up the mock to return a response with a status code of 200 and a specific JSON response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "accounts": [{
                "accountUid": "account-uid",
                "defaultCategory": "category-uid",
                "createdAt": "2020-01-01T00:00:00Z"
            }]
        }
        mock_get.return_value = mock_response
        accounts = self.client.get_accounts()

        # Verify that the response is as expected
        self.assertEqual(accounts, mock_response.json.return_value)

    @patch('starling_bank_client.requests.get')
    def test_get_account_identifiers(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'iban': 'GB123456789',
            'bic': 'ABCDGB2A'
        }
        mock_get.return_value = mock_response
        identifiers = self.client.get_account_identifiers()
        self.assertEqual(identifiers, mock_response.json.return_value)

    @patch('starling_bank_client.requests.get')
    def test_get_balance(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'clearedBalance': {'currency': 'GBP', 'minorUnits': 1000},
            'effectiveBalance': {'currency': 'GBP', 'minorUnits': 1000},
            'pendingTransactions': {'currency': 'GBP', 'minorUnits': 0}
        }
        mock_get.return_value = mock_response
        balance = self.client.get_balance()
        self.assertEqual(balance, mock_response.json.return_value)

    @patch('starling_bank_client.requests.get')
    def test_get_feed(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'feedItems': [
                {
                    'feedItemUid': '789',
                    'categoryUid': '456',
                    'amount': {'currency': 'GBP', 'minorUnits': -500},
                    'direction': 'OUT',
                    'updatedAt': '2021-01-02T00:00:00Z'
                }
            ]
        }
        mock_get.return_value = mock_response
        feed = self.client.get_feed()
        self.assertEqual(feed, mock_response.json.return_value)

    @patch('starling_bank_client.requests.get')
    def test_get_transactions(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'feedItems': [
                {
                    'feedItemUid': '789',
                    'categoryUid': '456',
                    'amount': {'currency': 'GBP', 'minorUnits': -500},
                    'direction': 'OUT',
                    'updatedAt': '2021-01-02T00:00:00Z'
                }
            ]
        }
        mock_get.return_value = mock_response
        transactions = self.client.get_transactions('2021-01-01', '2021-01-02')
        self.assertEqual(transactions, mock_response.json.return_value)

    @patch('starling_bank_client.requests.put')
    def test_create_savings_goal(self, mock_put):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'savingsGoalUid': 'abc123',
            'success': True
        }
        mock_put.return_value = mock_response
        savings_goal = self.client.create_savings_goal('Vacation', 'GBP', 10000)
        self.assertEqual(savings_goal, mock_response.json.return_value)

    @patch('starling_bank_client.requests.get')
    def test_get_savings_goal(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'name': 'Vacation',
            'target': {'currency': 'GBP', 'minorUnits': 10000},
            'totalSaved': {'currency': 'GBP', 'minorUnits': 5000},
            'savedPercentage': 50
        }
        mock_get.return_value = mock_response
        savings_goal = self.client.get_savings_goal('abc123')
        self.assertEqual(savings_goal, mock_response.json.return_value)

    @patch('starling_bank_client.requests.put')
    def test_transfer_to_savings_goal(self, mock_put):
        mock_put.return_value.status_code = 200
        success = self.client.transfer_to_savings_goal('abc123', 'transfer123', 500, 'GBP')
        self.assertTrue(success)


if __name__ == '__main__':
    unittest.main()
