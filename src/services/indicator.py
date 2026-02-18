"""技術指標計算模組。

使用 pandas 計算各種技術指標：MA、RSI、MACD、KD、布林通道。
"""

import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def calculate_ma(close: pd.Series, periods: list[int] | None = None) -> pd.DataFrame:
    """計算移動平均線。

    Args:
        close: 收盤價序列。
        periods: 計算週期列表，預設為 [5, 10, 20, 60]。

    Returns:
        包含各週期 MA 的 DataFrame。
    """
    if periods is None:
        periods = [5, 10, 20, 60]
    result = pd.DataFrame(index=close.index)
    for period in periods:
        result[f"ma{period}"] = close.rolling(window=period).mean()
    return result


def calculate_rsi(close: pd.Series, period: int = 14) -> pd.Series:
    """計算相對強弱指標 (RSI)。

    Args:
        close: 收盤價序列。
        period: 計算週期，預設為 14。

    Returns:
        RSI 值序列。
    """
    delta = close.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = (-delta).where(delta < 0, 0.0)

    avg_gain = gain.ewm(alpha=1 / period, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1 / period, min_periods=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    # avg_loss 為 0 時（全部上漲），RSI 應為 100
    rsi = rsi.fillna(100.0)
    return rsi


def calculate_macd(
    close: pd.Series,
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
) -> pd.DataFrame:
    """計算 MACD 指標。

    Args:
        close: 收盤價序列。
        fast: 快線週期，預設為 12。
        slow: 慢線週期，預設為 26。
        signal: 訊號線週期，預設為 9。

    Returns:
        包含 macd、macd_signal、macd_hist 的 DataFrame。
    """
    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line

    return pd.DataFrame({
        "macd": macd_line,
        "macd_signal": signal_line,
        "macd_hist": histogram,
    })


def calculate_kd(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    n: int = 9,
    k_smooth: int = 3,
    d_smooth: int = 3,
) -> pd.DataFrame:
    """計算 KD 隨機指標。

    Args:
        high: 最高價序列。
        low: 最低價序列。
        close: 收盤價序列。
        n: RSV 計算週期，預設為 9。
        k_smooth: K 值平滑週期，預設為 3。
        d_smooth: D 值平滑週期，預設為 3。

    Returns:
        包含 k、d 的 DataFrame。
    """
    lowest_low = low.rolling(window=n).min()
    highest_high = high.rolling(window=n).max()

    rsv = (close - lowest_low) / (highest_high - lowest_low).replace(0, np.nan) * 100

    k = rsv.ewm(com=k_smooth - 1, adjust=False).mean()
    d = k.ewm(com=d_smooth - 1, adjust=False).mean()

    return pd.DataFrame({"k": k, "d": d})


def calculate_bollinger_bands(
    close: pd.Series,
    period: int = 20,
    std_dev: float = 2.0,
) -> pd.DataFrame:
    """計算布林通道。

    Args:
        close: 收盤價序列。
        period: 計算週期，預設為 20。
        std_dev: 標準差倍數，預設為 2.0。

    Returns:
        包含 bb_upper、bb_middle、bb_lower 的 DataFrame。
    """
    middle = close.rolling(window=period).mean()
    std = close.rolling(window=period).std()

    return pd.DataFrame({
        "bb_upper": middle + std_dev * std,
        "bb_middle": middle,
        "bb_lower": middle - std_dev * std,
    })


def calculate_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """計算所有技術指標。

    Args:
        df: 包含 date、open、high、low、close 欄位的 DataFrame。

    Returns:
        包含所有技術指標的 DataFrame。
    """
    close = df["close"].astype(float)
    high = df["high"].astype(float)
    low = df["low"].astype(float)

    ma = calculate_ma(close)
    rsi = calculate_rsi(close)
    macd = calculate_macd(close)
    kd = calculate_kd(high, low, close)
    bb = calculate_bollinger_bands(close)

    result = pd.DataFrame({"date": df["date"]})
    result = pd.concat([result, ma, bb], axis=1)
    result["rsi"] = rsi
    result = pd.concat([result, macd, kd], axis=1)

    return result
