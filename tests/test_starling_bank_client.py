import unittest
from unittest.mock import patch, MagicMock
from starling_bank_client import StarlingBankClient


class TestStarlingBankClient(unittest.TestCase):

    def setUp(self):
        self.access_token = "eyJhbGciOiJQUzI1NiIsInppcCI6IkdaSVAifQ.H4sIAAAAAAAA_21Ty5KcMAz8lRTn1RYPMzxuueUH8gGyLc-4FmzKNrPZSuXfYzAMw9Te6G6pJVnib6a9z_oMJw2SRvvuA7pBmytH8_Eu7Ji9ZX7mMaIqLuqSFxVUxAtgknHgRZ5DXmLV5IgCqzoG058p64smb-uq7VjxlmkMiWB1WS8ECmFnE37ZQZL7reXmrZhqoOikAlYVBXCZcyDJ2zIKijoVvYP9IJMyGn4puGIFdCxvgamyBC7aGnhOjKSI1RTGjDjWTyHI-6OOuDAFCkkC45eYUBMDbLDo2gbLpmPLwMJOtDxK6hRua6tgcKTeEcofL0L4ml4ELckErTS5Mz9oH07MBqR0scmepA4PkJQQUNxGekTO4Wad9nFDoI3Udy1nHJLGcUAjtk4EOgnCmuDskHwXZtOsUdqNGLQ1YONrzEZu9cTsgx33tmlEvWWPaCQG6iUNFOgB17CRAkaEvYhwEXe8Zk74RbRLCWwmCRxBoEe8bp5JOz4hODQexdLzg4bBijj94Z0IsMszvLJblrNKD3upVPtErVGOBOkpnIA_S59OR3eP97gKD1d79HHitlFP3OrzzKThVHz2bywO8RuvQ0ym4kZyHuJxx7GPq_EUQhxwnjY44X4m8XePVxSPyTr5VP7M7nXP7Df5YD_Ngw-0NADC31-pSapEPe90XcXrkrN__wE6D0O_oQQAAA.MOCEJRin_exTsRfyLw-fuPUjz4EeR66pavIv4ApKaLemokogldkq0SsGsFOBRcZlFayIAGsXulET7oSbR3QyHJUnPnpBCu9x733St-l9DM1m8B9q93YhdrPK2qV5CbkLUK_LLTtGuoKCSi55BbjmoJoCkicqAswEv0Fa08IX32Fwdl1SnDKq-e0QKIpbd2MIwakvzhzGRJGDT_MSWYrdyQh0oFeVdjc-CMAzpwAiUMrAv8VD0T7-ukmE66heqlb8ZkhvWxCFsuKk_nC__0GKyXeXClPEa18r6zILcIpeTodovFcukccggqueTYVW_4UO9jwLLaEBe9PFAHyeNViEhwYzv2a9KlnJkWfc_Fk4g2TG6qQyqwKK1EUtHn-hMOvC7HnHDXOvN-l9Mbs0JWuGc89NckEv0SipaYbbdOy7k4ZDMWY6Ca7k0GB3qvsZsLYPsW0hLdWhAWtVu6q-NQxdVm4J6ZwXjgTiF-mOm6KzAQs5H-jXl8sJhdXL1EInLVDNWWheebTj31MaF1NNSM4Q7hCc99Waww6qezPw4eyL9jzvxXQmr2-RaFHDOImU33QlybWxFf2oEDmyfPPtQUpJFzIqZnS1oaTFenqny850FzBh0Y55KUl0wZmz1ff5J4BmcMF-cTDwGs3V651kjixUl4KJmsFqyDEPMBJguxynayY"
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
