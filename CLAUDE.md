# Tw_stock_webpage 專案指引

## 專案概述

台灣股票資訊網頁應用程式，使用 Streamlit 為前端框架。

## 技術棧

- **前端框架**: Streamlit
- **程式語言**: Python 3.12
- **資料處理**: pandas
- **圖表**: Plotly
- **容器化**: Docker

## 開發規範

- 所有 Python 程式碼在 Docker container 中執行
- 單元測試使用 `unittest`，測試檔案放在 `tests/` 資料夾
- 日誌檔案存放於 `logs/` 資料夾
- 使用 `logging` 模組記錄日誌

## 重要路徑

- 主程式進入點: `src/app.py`
- 單元測試: `tests/`
- Docker 設定: `docker/`
- 依賴套件: `requirements.txt`
