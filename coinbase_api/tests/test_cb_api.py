from django.test import TestCase
from unittest.mock import MagicMock
from coinbase_api.cb_api import CBApi


class CoinbaseClientTest(TestCase):
    def setUp(self):
        # Mock client
        self.mock_client = MagicMock()
        self.client = CBApi()

    def test_get_prices(self):
        # Mock data_dd
        mock_candles = [
            [1638316800, 50000.0, 51000.0, 49000.0, 50500.0, 100.0],
            [1638403200, 50500.0, 51500.0, 49500.0, 51000.0, 150.0],
        ]

        # Set up mock return valuebab
        self.mock_client.get_candles.return_value = mock_candles

        # Run function
        result = self.client.get_prices(granularity="ONE_DAY", token="BTC-USD")
        result2 = self.client.get_prices(granularity="ONE_DAY", token="ETH-USD")
        print(result.head())

        # Verify the function was called with correct parameters
        # self.mock_client.get_candles.assert_called_once_with(
        #     product_id='BTC-USD',
        #     start=(datetime.now() - timedelta(days=365)).isoformat(),
        #     end=datetime.now().isoformat(),
        #     granularity="ONE_DAY"
        # )
        #
        # # Check the result
        # self.assertEqual(result, mock_candles)

    def test_get_volume(self):
        res = self.client.get_volume(granularity="ONE_DAY", token="BTC-USD")
        print(res)

