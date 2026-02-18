"""Pydantic 回應模型定義。

定義 API 回應的資料結構。
"""

from pydantic import BaseModel


class StockItem(BaseModel):
    """股票清單項目。"""

    code: str
    name: str
    market: str  # "TWSE" 或 "TPEX"


class StockListResponse(BaseModel):
    """股票清單回應。"""

    stocks: list[StockItem]


class PriceRecord(BaseModel):
    """單日股價紀錄。"""

    date: str
    open: float | None = None
    high: float | None = None
    low: float | None = None
    close: float | None = None
    change: float | None = None
    volume: int | None = None
    trade_value: float | None = None
    transaction: int | None = None


class IndicatorData(BaseModel):
    """技術指標資料。"""

    date: str
    ma5: float | None = None
    ma10: float | None = None
    ma20: float | None = None
    ma60: float | None = None
    rsi: float | None = None
    macd: float | None = None
    macd_signal: float | None = None
    macd_hist: float | None = None
    k: float | None = None
    d: float | None = None
    bb_upper: float | None = None
    bb_middle: float | None = None
    bb_lower: float | None = None


class PriceHistoryResponse(BaseModel):
    """股價歷史回應（含技術指標）。"""

    code: str
    name: str
    market: str
    prices: list[PriceRecord]
    indicators: list[IndicatorData]


class StockInfoResponse(BaseModel):
    """股票最新資訊回應。"""

    code: str
    name: str
    market: str
    date: str
    close: float | None = None
    change: float | None = None
    open: float | None = None
    high: float | None = None
    low: float | None = None
    volume: int | None = None
    trade_value: float | None = None
    transaction: int | None = None
    pe_ratio: float | None = None


class InstitutionalRecord(BaseModel):
    """三大法人單日紀錄。"""

    date: str
    foreign_buy_sell: float | None = None
    investment_trust_buy_sell: float | None = None
    dealer_buy_sell: float | None = None
    total_buy_sell: float | None = None


class InstitutionalResponse(BaseModel):
    """三大法人回應。"""

    code: str
    name: str
    records: list[InstitutionalRecord]


class MarginRecord(BaseModel):
    """融資融券單日紀錄。"""

    date: str
    margin_purchase: int | None = None
    margin_sales: int | None = None
    margin_balance: int | None = None
    short_sale: int | None = None
    short_covering: int | None = None
    short_balance: int | None = None


class MarginResponse(BaseModel):
    """融資融券回應。"""

    code: str
    name: str
    records: list[MarginRecord]
