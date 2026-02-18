"""FastAPI 應用程式進入點。

提供股票資料 API 與前端靜態檔案服務。
"""

import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.routers.stock import router as stock_router

# 設定 logging
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "app.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="台灣股票資訊 API",
    description="提供台灣上市櫃股票資訊查詢服務",
    version="1.0.0",
)

# CORS 設定（開發環境允許所有來源）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 註冊 API 路由
app.include_router(stock_router)


@app.get("/api/health")
def health_check():
    """健康檢查端點。"""
    return {"status": "ok"}


# 提供前端靜態檔案（必須在所有 API 路由之後）
STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
if STATIC_DIR.exists():
    app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")
    logger.info("已掛載靜態檔案目錄: %s", STATIC_DIR)
else:
    logger.warning("靜態檔案目錄不存在: %s", STATIC_DIR)
