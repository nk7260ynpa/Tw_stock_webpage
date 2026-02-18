"""股票資料查詢服務的單元測試。"""

import unittest
from unittest.mock import patch

from src.services.stock_service import _to_float, _to_int


class TestToFloat(unittest.TestCase):
    """測試 _to_float 轉換函式。"""

    def test_normal_float(self):
        """測試一般浮點數轉換。"""
        self.assertAlmostEqual(_to_float(123.45), 123.45)

    def test_string_float(self):
        """測試字串浮點數轉換。"""
        self.assertAlmostEqual(_to_float("123.45"), 123.45)

    def test_comma_separated(self):
        """測試含逗號的數字轉換。"""
        self.assertAlmostEqual(_to_float("1,234,567.89"), 1234567.89)

    def test_none(self):
        """測試 None 值。"""
        self.assertIsNone(_to_float(None))

    def test_empty_string(self):
        """測試空字串。"""
        self.assertIsNone(_to_float(""))

    def test_dash(self):
        """測試 -- 符號。"""
        self.assertIsNone(_to_float("--"))

    def test_na(self):
        """測試 N/A 字串。"""
        self.assertIsNone(_to_float("N/A"))

    def test_invalid_string(self):
        """測試無效字串。"""
        self.assertIsNone(_to_float("abc"))

    def test_integer(self):
        """測試整數轉換。"""
        self.assertAlmostEqual(_to_float(100), 100.0)

    def test_negative(self):
        """測試負數轉換。"""
        self.assertAlmostEqual(_to_float("-5.23"), -5.23)


class TestToInt(unittest.TestCase):
    """測試 _to_int 轉換函式。"""

    def test_normal_int(self):
        """測試一般整數轉換。"""
        self.assertEqual(_to_int(100), 100)

    def test_float_to_int(self):
        """測試浮點數轉整數。"""
        self.assertEqual(_to_int(100.7), 100)

    def test_string_int(self):
        """測試字串整數轉換。"""
        self.assertEqual(_to_int("1,234"), 1234)

    def test_none(self):
        """測試 None 值。"""
        self.assertIsNone(_to_int(None))

    def test_dash(self):
        """測試 -- 符號。"""
        self.assertIsNone(_to_int("--"))


class TestGetAllStocks(unittest.TestCase):
    """測試取得所有股票清單。"""

    @patch("src.services.stock_service.execute_query")
    def test_merges_twse_and_tpex(self, mock_query):
        """測試合併上市和上櫃股票。"""
        mock_query.side_effect = [
            [{"code": "2330", "name": "台積電"}],
            [{"code": "6510", "name": "精測"}],
        ]

        from src.services.stock_service import get_all_stocks

        result = get_all_stocks()

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["code"], "2330")
        self.assertEqual(result[0]["market"], "TWSE")
        self.assertEqual(result[1]["code"], "6510")
        self.assertEqual(result[1]["market"], "TPEX")

    @patch("src.services.stock_service.execute_query")
    def test_empty_databases(self, mock_query):
        """測試資料庫為空的情況。"""
        mock_query.side_effect = [[], []]

        from src.services.stock_service import get_all_stocks

        result = get_all_stocks()
        self.assertEqual(len(result), 0)


class TestGetMarket(unittest.TestCase):
    """測試判斷股票市場別。"""

    @patch("src.services.stock_service.execute_query")
    @patch("src.services.stock_service._stock_market_cache", None)
    def test_twse_stock(self, mock_query):
        """測試上市股票判斷。"""
        mock_query.side_effect = [
            [{"code": "2330"}],
            [],
        ]

        from src.services.stock_service import get_market

        result = get_market("2330")
        self.assertEqual(result, "TWSE")

    @patch("src.services.stock_service.execute_query")
    @patch("src.services.stock_service._stock_market_cache", None)
    def test_unknown_stock(self, mock_query):
        """測試不存在的股票。"""
        mock_query.side_effect = [[], []]

        from src.services.stock_service import get_market

        result = get_market("9999")
        self.assertIsNone(result)


class TestGetPriceHistory(unittest.TestCase):
    """測試取得股價歷史。"""

    @patch("src.services.stock_service.get_stock_name", return_value="台積電")
    @patch("src.services.stock_service.get_market", return_value="TWSE")
    @patch("src.services.stock_service.execute_query")
    def test_returns_prices_and_indicators(self, mock_query, mock_market, mock_name):
        """測試回傳包含價格和指標。"""
        mock_query.return_value = [
            {
                "Date": "2026-01-02",
                "OpeningPrice": "100",
                "HighestPrice": "105",
                "LowestPrice": "99",
                "ClosingPrice": "103",
                "Change": "3",
                "TradeVolume": "10000",
                "TradeValue": "1030000",
                "Transaction": "500",
            }
        ]

        from src.services.stock_service import get_price_history

        result = get_price_history("2330")

        self.assertEqual(result["code"], "2330")
        self.assertEqual(result["name"], "台積電")
        self.assertEqual(result["market"], "TWSE")
        self.assertEqual(len(result["prices"]), 1)
        self.assertAlmostEqual(result["prices"][0]["close"], 103.0)

    @patch("src.services.stock_service.get_market", return_value=None)
    def test_unknown_stock_returns_empty(self, mock_market):
        """測試不存在的股票回傳空資料。"""
        from src.services.stock_service import get_price_history

        result = get_price_history("9999")
        self.assertEqual(result["prices"], [])
        self.assertEqual(result["indicators"], [])


if __name__ == "__main__":
    unittest.main()
