"""股票資料查詢服務模組。

提供股票清單、股價歷史、法人買賣超、融資融券等資料查詢功能。
"""

import logging

import pandas as pd

from src.database import execute_query
from src.services.indicator import calculate_all_indicators

logger = logging.getLogger(__name__)

# 快取股票清單與市場對照
_stock_market_cache: dict[str, str] | None = None


def _get_stock_market_map() -> dict[str, str]:
    """取得股票代號與市場別的對照表。

    Returns:
        股票代號到市場別（"TWSE" 或 "TPEX"）的對照字典。
    """
    global _stock_market_cache
    if _stock_market_cache is not None:
        return _stock_market_cache

    twse_stocks = execute_query(
        "TWSE",
        "SELECT SecurityCode AS code FROM StockName",
    )
    tpex_stocks = execute_query(
        "TPEX",
        "SELECT Code AS code FROM StockName",
    )

    market_map = {}
    for row in twse_stocks:
        market_map[str(row["code"]).strip()] = "TWSE"
    for row in tpex_stocks:
        market_map[str(row["code"]).strip()] = "TPEX"

    _stock_market_cache = market_map
    logger.info("已載入股票市場對照表，共 %d 檔", len(market_map))
    return market_map


def get_market(code: str) -> str | None:
    """判斷股票屬於上市或上櫃。

    Args:
        code: 股票代號。

    Returns:
        "TWSE" 或 "TPEX"，找不到則回傳 None。
    """
    market_map = _get_stock_market_map()
    return market_map.get(code.strip())


def get_all_stocks() -> list[dict]:
    """取得所有股票清單（合併上市+上櫃）。

    Returns:
        股票清單，每筆包含 code、name、market。
    """
    twse_stocks = execute_query(
        "TWSE",
        "SELECT SecurityCode AS code, StockName AS name FROM StockName ORDER BY SecurityCode",
    )
    tpex_stocks = execute_query(
        "TPEX",
        "SELECT Code AS code, Name AS name FROM StockName ORDER BY Code",
    )

    result = []
    for row in twse_stocks:
        result.append({
            "code": str(row["code"]).strip(),
            "name": str(row["name"]).strip(),
            "market": "TWSE",
        })
    for row in tpex_stocks:
        result.append({
            "code": str(row["code"]).strip(),
            "name": str(row["name"]).strip(),
            "market": "TPEX",
        })

    return result


def get_stock_name(code: str, market: str) -> str:
    """查詢股票名稱。

    Args:
        code: 股票代號。
        market: 市場別（"TWSE" 或 "TPEX"）。

    Returns:
        股票名稱，找不到則回傳空字串。
    """
    if market == "TWSE":
        rows = execute_query(
            "TWSE",
            "SELECT StockName AS name FROM StockName WHERE SecurityCode = :code",
            {"code": code},
        )
    else:
        rows = execute_query(
            "TPEX",
            "SELECT Name AS name FROM StockName WHERE Code = :code",
            {"code": code},
        )

    if rows:
        return str(rows[0]["name"]).strip()
    return ""


def get_price_history(
    code: str,
    start: str | None = None,
    end: str | None = None,
) -> dict:
    """取得股價歷史資料與技術指標。

    Args:
        code: 股票代號。
        start: 開始日期（YYYY-MM-DD）。
        end: 結束日期（YYYY-MM-DD）。

    Returns:
        包含 code、name、market、prices、indicators 的字典。
    """
    market = get_market(code)
    if not market:
        return {"code": code, "name": "", "market": "", "prices": [], "indicators": []}

    name = get_stock_name(code, market)

    if market == "TWSE":
        query = """
            SELECT Date, OpeningPrice, HighestPrice, LowestPrice,
                   ClosingPrice, `Change`, TradeVolume, TradeValue, Transaction
            FROM DailyPrice
            WHERE SecurityCode = :code
        """
    else:
        query = """
            SELECT Date, Open, High, Low, Close, `Change`,
                   TradeVolume, TradeAmount, NumberOfTransactions
            FROM DailyPrice
            WHERE Code = :code
        """

    params: dict = {"code": code}
    if start:
        query += " AND Date >= :start"
        params["start"] = start
    if end:
        query += " AND Date <= :end"
        params["end"] = end
    query += " ORDER BY Date"

    rows = execute_query(market, query, params)

    if market == "TWSE":
        prices = []
        for row in rows:
            prices.append({
                "date": str(row["Date"]),
                "open": _to_float(row.get("OpeningPrice")),
                "high": _to_float(row.get("HighestPrice")),
                "low": _to_float(row.get("LowestPrice")),
                "close": _to_float(row.get("ClosingPrice")),
                "change": _to_float(row.get("Change")),
                "volume": _to_int(row.get("TradeVolume")),
                "trade_value": _to_float(row.get("TradeValue")),
                "transaction": _to_int(row.get("Transaction")),
            })
    else:
        prices = []
        for row in rows:
            prices.append({
                "date": str(row["Date"]),
                "open": _to_float(row.get("Open")),
                "high": _to_float(row.get("High")),
                "low": _to_float(row.get("Low")),
                "close": _to_float(row.get("Close")),
                "change": _to_float(row.get("Change")),
                "volume": _to_int(row.get("TradeVolume")),
                "trade_value": _to_float(row.get("TradeAmount")),
                "transaction": _to_int(row.get("NumberOfTransactions")),
            })

    # 計算技術指標
    indicators = []
    if prices:
        df = pd.DataFrame(prices)
        ind_df = calculate_all_indicators(df)
        # 將 NaN 替換為 None 以確保 JSON 序列化正常
        records = ind_df.to_dict(orient="records")
        for record in records:
            for key, val in record.items():
                if isinstance(val, float) and (pd.isna(val) or val != val):
                    record[key] = None
        indicators = records

    return {
        "code": code,
        "name": name,
        "market": market,
        "prices": prices,
        "indicators": indicators,
    }


def get_latest_info(code: str) -> dict:
    """取得最新一日完整資訊。

    Args:
        code: 股票代號。

    Returns:
        包含最新一日所有資訊的字典。
    """
    market = get_market(code)
    if not market:
        return {"code": code, "name": "", "market": ""}

    name = get_stock_name(code, market)

    if market == "TWSE":
        query = """
            SELECT Date, OpeningPrice, HighestPrice, LowestPrice,
                   ClosingPrice, `Change`, TradeVolume, TradeValue,
                   Transaction, PriceEarningratio
            FROM DailyPrice
            WHERE SecurityCode = :code
            ORDER BY Date DESC LIMIT 1
        """
    else:
        query = """
            SELECT Date, Open, High, Low, Close, `Change`,
                   TradeVolume, TradeAmount, NumberOfTransactions
            FROM DailyPrice
            WHERE Code = :code
            ORDER BY Date DESC LIMIT 1
        """

    rows = execute_query(market, query, {"code": code})
    if not rows:
        return {"code": code, "name": name, "market": market}

    row = rows[0]
    if market == "TWSE":
        return {
            "code": code,
            "name": name,
            "market": market,
            "date": str(row["Date"]),
            "close": _to_float(row.get("ClosingPrice")),
            "change": _to_float(row.get("Change")),
            "open": _to_float(row.get("OpeningPrice")),
            "high": _to_float(row.get("HighestPrice")),
            "low": _to_float(row.get("LowestPrice")),
            "volume": _to_int(row.get("TradeVolume")),
            "trade_value": _to_float(row.get("TradeValue")),
            "transaction": _to_int(row.get("Transaction")),
            "pe_ratio": _to_float(row.get("PriceEarningratio")),
        }
    return {
        "code": code,
        "name": name,
        "market": market,
        "date": str(row["Date"]),
        "close": _to_float(row.get("Close")),
        "change": _to_float(row.get("Change")),
        "open": _to_float(row.get("Open")),
        "high": _to_float(row.get("High")),
        "low": _to_float(row.get("Low")),
        "volume": _to_int(row.get("TradeVolume")),
        "trade_value": _to_float(row.get("TradeAmount")),
        "transaction": _to_int(row.get("NumberOfTransactions")),
        "pe_ratio": None,
    }


def get_institutional(
    code: str,
    start: str | None = None,
    end: str | None = None,
) -> dict:
    """取得三大法人買賣超資料。

    Args:
        code: 股票代號。
        start: 開始日期（YYYY-MM-DD）。
        end: 結束日期（YYYY-MM-DD）。

    Returns:
        包含 code、name、records 的字典。
    """
    market = get_market(code)
    name = get_stock_name(code, market) if market else ""

    query = """
        SELECT Date, SecurityCode,
               ForeignInvestorsDifference,
               SecuritiesInvestmentDifference,
               DealersDifference,
               TotalDifference
        FROM DailyPrice
        WHERE SecurityCode = :code
    """
    params: dict = {"code": code}
    if start:
        query += " AND Date >= :start"
        params["start"] = start
    if end:
        query += " AND Date <= :end"
        params["end"] = end
    query += " ORDER BY Date"

    rows = execute_query("FAOI", query, params)

    records = []
    for row in rows:
        records.append({
            "date": str(row["Date"]),
            "foreign_buy_sell": _to_float(row.get("ForeignInvestorsDifference")),
            "investment_trust_buy_sell": _to_float(
                row.get("SecuritiesInvestmentDifference")
            ),
            "dealer_buy_sell": _to_float(row.get("DealersDifference")),
            "total_buy_sell": _to_float(row.get("TotalDifference")),
        })

    return {"code": code, "name": name, "records": records}


def get_margin(
    code: str,
    start: str | None = None,
    end: str | None = None,
) -> dict:
    """取得融資融券資料。

    Args:
        code: 股票代號。
        start: 開始日期（YYYY-MM-DD）。
        end: 結束日期（YYYY-MM-DD）。

    Returns:
        包含 code、name、records 的字典。
    """
    market = get_market(code)
    name = get_stock_name(code, market) if market else ""

    query = """
        SELECT Date, SecurityCode,
               MarginPurchase, MarginSales,
               MarginPurchaseBalanceOfTheDay,
               ShortSale, ShortCovering,
               ShortSaleBalanceOfTheDay
        FROM DailyPrice
        WHERE SecurityCode = :code
    """
    params: dict = {"code": code}
    if start:
        query += " AND Date >= :start"
        params["start"] = start
    if end:
        query += " AND Date <= :end"
        params["end"] = end
    query += " ORDER BY Date"

    rows = execute_query("MGTS", query, params)

    records = []
    for row in rows:
        records.append({
            "date": str(row["Date"]),
            "margin_purchase": _to_int(row.get("MarginPurchase")),
            "margin_sales": _to_int(row.get("MarginSales")),
            "margin_balance": _to_int(row.get("MarginPurchaseBalanceOfTheDay")),
            "short_sale": _to_int(row.get("ShortSale")),
            "short_covering": _to_int(row.get("ShortCovering")),
            "short_balance": _to_int(row.get("ShortSaleBalanceOfTheDay")),
        })

    return {"code": code, "name": name, "records": records}


def _to_float(value) -> float | None:
    """安全轉換為 float。"""
    if value is None:
        return None
    try:
        val = str(value).replace(",", "").strip()
        if val in ("", "--", "---", "N/A"):
            return None
        return float(val)
    except (ValueError, TypeError):
        return None


def _to_int(value) -> int | None:
    """安全轉換為 int。"""
    f = _to_float(value)
    if f is None:
        return None
    return int(f)
