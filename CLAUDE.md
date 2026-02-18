# Tw_stock_webpage 專案指引

## 專案概述

台灣股票資訊網頁應用程式，採用 FastAPI (Python 後端) + React (前端) 架構。

## 技術棧

- **後端框架**: FastAPI
- **前端框架**: React + Vite
- **程式語言**: Python 3.12 / JavaScript
- **資料處理**: pandas, numpy
- **圖表**: Recharts
- **樣式**: Tailwind CSS
- **資料庫**: MySQL (SQLAlchemy + PyMySQL)
- **容器化**: Docker (多階段建置)

## 開發規範

- 所有 Python 程式碼在 Docker container 中執行
- 單元測試使用 `unittest`，測試檔案放在 `tests/` 資料夾
- 日誌檔案存放於 `logs/` 資料夾
- 使用 `logging` 模組記錄日誌

## 重要路徑

- FastAPI 進入點: `src/main.py`
- 資料庫連線: `src/database.py`
- API 路由: `src/routers/stock.py`
- 服務邏輯: `src/services/stock_service.py`
- 技術指標: `src/services/indicator.py`
- 前端原始碼: `frontend/src/`
- 單元測試: `tests/`
- Docker 設定: `docker/`
- 依賴套件: `requirements.txt`
