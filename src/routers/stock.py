"""股票 API 路由模組。

定義所有股票相關的 API 端點。
"""

import logging

from fastapi import APIRouter, Query

from src.models import (
    InstitutionalResponse,
    MarginResponse,
    PriceHistoryResponse,
    StockInfoResponse,
    StockListResponse,
)
from src.services import stock_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["stocks"])


@router.get("/stocks", response_model=StockListResponse)
def list_stocks():
    """取得所有股票清單（代號+名稱，含市場別）。"""
    stocks = stock_service.get_all_stocks()
    logger.info("查詢股票清單，共 %d 檔", len(stocks))
    return StockListResponse(stocks=stocks)


@router.get("/stocks/{code}/price", response_model=PriceHistoryResponse)
def get_price(
    code: str,
    start: str | None = Query(None, description="開始日期 (YYYY-MM-DD)"),
    end: str | None = Query(None, description="結束日期 (YYYY-MM-DD)"),
):
    """取得股價歷史與技術指標。"""
    logger.info("查詢股價: %s (%s ~ %s)", code, start, end)
    data = stock_service.get_price_history(code, start, end)
    return PriceHistoryResponse(**data)


@router.get("/stocks/{code}/info", response_model=StockInfoResponse)
def get_info(code: str):
    """取得最新一日基本資訊。"""
    logger.info("查詢最新資訊: %s", code)
    data = stock_service.get_latest_info(code)
    return StockInfoResponse(**data)


@router.get("/stocks/{code}/institutional", response_model=InstitutionalResponse)
def get_institutional(
    code: str,
    start: str | None = Query(None, description="開始日期 (YYYY-MM-DD)"),
    end: str | None = Query(None, description="結束日期 (YYYY-MM-DD)"),
):
    """取得三大法人買賣超。"""
    logger.info("查詢三大法人: %s (%s ~ %s)", code, start, end)
    data = stock_service.get_institutional(code, start, end)
    return InstitutionalResponse(**data)


@router.get("/stocks/{code}/margin", response_model=MarginResponse)
def get_margin(
    code: str,
    start: str | None = Query(None, description="開始日期 (YYYY-MM-DD)"),
    end: str | None = Query(None, description="結束日期 (YYYY-MM-DD)"),
):
    """取得融資融券資訊。"""
    logger.info("查詢融資融券: %s (%s ~ %s)", code, start, end)
    data = stock_service.get_margin(code, start, end)
    return MarginResponse(**data)
