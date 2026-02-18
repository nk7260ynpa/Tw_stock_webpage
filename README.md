# 台灣股票資訊網頁 (Tw_stock_webpage)

台灣股票資訊網頁應用程式，使用 Streamlit 建立互動式股票資訊查詢介面。

## 專案架構

```text
Tw_stock_webpage/
├── docker/                # Docker 相關檔案
│   ├── build.sh           # 建立 Docker image 的執行腳本
│   ├── Dockerfile         # Docker image 定義
│   └── docker-compose.yaml
├── logs/                  # 日誌檔案存放資料夾
├── src/                   # 原始碼
│   ├── __init__.py
│   └── app.py             # Streamlit 應用程式主進入點
├── tests/                 # 單元測試
│   ├── __init__.py
│   └── test_app.py
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt       # Python 依賴套件
└── run.sh                 # 啟動主程式腳本
```

## 環境需求

- Docker

## 快速開始

### 使用 run.sh 啟動

```bash
bash run.sh
```

此腳本會自動建立 Docker image、啟動 container 並掛載 logs 資料夾。
啟動後請開啟瀏覽器前往 <http://localhost:8501>。

### 使用 Docker Compose 啟動

```bash
cd docker
docker compose up -d
```

## 開發

### 建立 Docker image

```bash
bash docker/build.sh
```

### 執行單元測試

```bash
docker run --rm tw-stock-webpage:latest python -m pytest tests/ -v
```

## 授權

本專案採用 MIT 授權條款，詳見 [LICENSE](LICENSE) 檔案。
