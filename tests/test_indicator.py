"""技術指標計算模組的單元測試。"""

import unittest

import numpy as np
import pandas as pd

from src.services.indicator import (
    calculate_all_indicators,
    calculate_bollinger_bands,
    calculate_kd,
    calculate_ma,
    calculate_macd,
    calculate_rsi,
)


class TestCalculateMA(unittest.TestCase):
    """測試移動平均線計算。"""

    def setUp(self):
        """建立測試資料。"""
        self.close = pd.Series(range(1, 61), dtype=float)

    def test_default_periods(self):
        """測試預設週期 (5, 10, 20, 60)。"""
        result = calculate_ma(self.close)
        self.assertIn("ma5", result.columns)
        self.assertIn("ma10", result.columns)
        self.assertIn("ma20", result.columns)
        self.assertIn("ma60", result.columns)

    def test_ma5_values(self):
        """測試 MA5 計算值正確。"""
        result = calculate_ma(self.close, periods=[5])
        # 第 5 筆（index=4）的 MA5 應為 (1+2+3+4+5)/5 = 3.0
        self.assertAlmostEqual(result["ma5"].iloc[4], 3.0)
        # 前 4 筆應為 NaN
        self.assertTrue(pd.isna(result["ma5"].iloc[3]))

    def test_custom_periods(self):
        """測試自訂週期。"""
        result = calculate_ma(self.close, periods=[3, 7])
        self.assertIn("ma3", result.columns)
        self.assertIn("ma7", result.columns)
        self.assertNotIn("ma5", result.columns)


class TestCalculateRSI(unittest.TestCase):
    """測試 RSI 計算。"""

    def test_all_up(self):
        """測試全部上漲的情況，RSI 應接近 100。"""
        close = pd.Series(range(1, 30), dtype=float)
        rsi = calculate_rsi(close, period=14)
        # 全部上漲，RSI 應接近 100
        self.assertGreater(rsi.iloc[-1], 90)

    def test_all_down(self):
        """測試全部下跌的情況，RSI 應接近 0。"""
        close = pd.Series(range(30, 1, -1), dtype=float)
        rsi = calculate_rsi(close, period=14)
        # 全部下跌，RSI 應接近 0
        self.assertLess(rsi.iloc[-1], 10)

    def test_rsi_range(self):
        """測試 RSI 值範圍在 0-100 之間。"""
        np.random.seed(42)
        close = pd.Series(np.random.uniform(90, 110, 100))
        rsi = calculate_rsi(close, period=14)
        valid = rsi.dropna()
        self.assertTrue((valid >= 0).all())
        self.assertTrue((valid <= 100).all())


class TestCalculateMACD(unittest.TestCase):
    """測試 MACD 計算。"""

    def setUp(self):
        """建立測試資料。"""
        np.random.seed(42)
        self.close = pd.Series(np.cumsum(np.random.randn(100)) + 100)

    def test_output_columns(self):
        """測試輸出欄位正確。"""
        result = calculate_macd(self.close)
        self.assertIn("macd", result.columns)
        self.assertIn("macd_signal", result.columns)
        self.assertIn("macd_hist", result.columns)

    def test_histogram_equals_diff(self):
        """測試柱狀圖等於 MACD 減去訊號線。"""
        result = calculate_macd(self.close)
        diff = result["macd"] - result["macd_signal"]
        pd.testing.assert_series_equal(
            result["macd_hist"], diff, check_names=False
        )


class TestCalculateKD(unittest.TestCase):
    """測試 KD 計算。"""

    def setUp(self):
        """建立測試資料。"""
        np.random.seed(42)
        base = np.cumsum(np.random.randn(50)) + 100
        self.high = pd.Series(base + np.abs(np.random.randn(50)))
        self.low = pd.Series(base - np.abs(np.random.randn(50)))
        self.close = pd.Series(base)

    def test_output_columns(self):
        """測試輸出欄位正確。"""
        result = calculate_kd(self.high, self.low, self.close)
        self.assertIn("k", result.columns)
        self.assertIn("d", result.columns)

    def test_kd_range(self):
        """測試 KD 值範圍在 0-100 之間。"""
        result = calculate_kd(self.high, self.low, self.close)
        valid_k = result["k"].dropna()
        valid_d = result["d"].dropna()
        self.assertTrue((valid_k >= 0).all() and (valid_k <= 100).all())
        self.assertTrue((valid_d >= 0).all() and (valid_d <= 100).all())


class TestCalculateBollingerBands(unittest.TestCase):
    """測試布林通道計算。"""

    def setUp(self):
        """建立測試資料。"""
        np.random.seed(42)
        self.close = pd.Series(np.random.uniform(95, 105, 50))

    def test_output_columns(self):
        """測試輸出欄位正確。"""
        result = calculate_bollinger_bands(self.close)
        self.assertIn("bb_upper", result.columns)
        self.assertIn("bb_middle", result.columns)
        self.assertIn("bb_lower", result.columns)

    def test_upper_greater_than_lower(self):
        """測試上軌大於下軌。"""
        result = calculate_bollinger_bands(self.close)
        valid = result.dropna()
        self.assertTrue((valid["bb_upper"] >= valid["bb_lower"]).all())

    def test_middle_is_ma(self):
        """測試中軌等於移動平均線。"""
        result = calculate_bollinger_bands(self.close, period=20)
        ma20 = self.close.rolling(window=20).mean()
        pd.testing.assert_series_equal(
            result["bb_middle"], ma20, check_names=False
        )


class TestCalculateAllIndicators(unittest.TestCase):
    """測試計算所有技術指標的整合函式。"""

    def setUp(self):
        """建立測試資料。"""
        np.random.seed(42)
        dates = pd.date_range("2026-01-01", periods=60, freq="B")
        base = np.cumsum(np.random.randn(60)) + 100
        self.df = pd.DataFrame({
            "date": dates.strftime("%Y-%m-%d"),
            "open": base + np.random.randn(60) * 0.5,
            "high": base + np.abs(np.random.randn(60)),
            "low": base - np.abs(np.random.randn(60)),
            "close": base,
        })

    def test_output_has_all_indicators(self):
        """測試輸出包含所有技術指標欄位。"""
        result = calculate_all_indicators(self.df)
        expected_cols = [
            "date", "ma5", "ma10", "ma20", "ma60",
            "rsi", "macd", "macd_signal", "macd_hist",
            "k", "d", "bb_upper", "bb_middle", "bb_lower",
        ]
        for col in expected_cols:
            self.assertIn(col, result.columns, f"缺少欄位: {col}")

    def test_output_length(self):
        """測試輸出長度與輸入相同。"""
        result = calculate_all_indicators(self.df)
        self.assertEqual(len(result), len(self.df))


if __name__ == "__main__":
    unittest.main()
