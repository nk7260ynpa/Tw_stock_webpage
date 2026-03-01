# 台灣股票資訊網頁 (Tw_stock_webpage)

台灣股票資訊網頁應用程式，採用 FastAPI (Python 後端) + React (前端) 架構，
提供上市櫃股票查詢、K 線圖、技術指標、三大法人買賣超及融資融券等資訊。

## 專案架構

```text
Tw_stock_webpage/
├── docker/                        # Docker 相關檔案
│   ├── build.sh                   # 建立 Docker image 的執行腳本
│   ├── Dockerfile                 # 多階段建置（前端 + 後端）
│   └── docker-compose.yaml
├── frontend/                      # React 前端
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── api/
│       │   └── stock.js           # API 呼叫封裝
│       ├── components/
│       │   ├── StockSelector.jsx   # 股票搜尋選擇器
│       │   ├── StockInfoCards.jsx   # 基本資訊卡片
│       │   ├── CandlestickChart.jsx # K 線圖 + 成交量
│       │   ├── IndicatorChart.jsx   # 技術指標圖表
│       │   ├── InstitutionalInfo.jsx # 三大法人資訊
│       │   └── MarginInfo.jsx       # 融資融券資訊
│       └── styles/
│           └── index.css
├── logs/                          # 日誌檔案存放資料夾
├── src/                           # Python 後端
│   ├── __init__.py
│   ├── main.py                    # FastAPI 應用程式進入點
│   ├── database.py                # 資料庫連線管理
│   ├── models.py                  # Pydantic 回應模型
│   ├── routers/
│   │   └── stock.py               # 股票 API 路由
│   └── services/
│       ├── stock_service.py       # 股票資料查詢邏輯
│       └── indicator.py           # 技術指標計算
├── tests/                         # 單元測試
│   ├── __init__.py
│   ├── test_stock_service.py
│   └── test_indicator.py
├── .gitignore
├── LICENSE
├── README.md
├── pyproject.toml                 # Python 套件設定（PEP 621）
├── requirements.txt               # Python 釘版依賴（Docker 環境用）
└── run.sh                         # 啟動主程式腳本
```

## 功能特色

- 股票搜尋：支援代號或名稱搜尋，自動判斷上市/上櫃
- K 線圖：蠟燭圖 + 成交量，可疊加均線與布林通道
- 技術指標：RSI、MACD、KD 指標切換顯示
- 三大法人：外資、投信、自營商買賣超長條圖
- 融資融券：融資融券餘額與買賣變化圖

## API 端點

| 方法 | 路徑 | 說明 |
|------|------|------|
| GET | `/api/stocks` | 取得所有股票清單 |
| GET | `/api/stocks/{code}/price?start=&end=` | 股價歷史 + 技術指標 |
| GET | `/api/stocks/{code}/info` | 最新一日基本資訊 |
| GET | `/api/stocks/{code}/institutional?start=&end=` | 三大法人買賣超 |
| GET | `/api/stocks/{code}/margin?start=&end=` | 融資融券資訊 |
| GET | `/api/health` | 健康檢查 |

## 環境需求

- Docker

## 快速開始

### 使用 run.sh 啟動

```bash
bash run.sh
```

此腳本會自動建立 Docker image、啟動 container 並掛載 logs 資料夾。
啟動後請開啟瀏覽器前往 <http://localhost:7938>。

### 使用 Docker Compose 啟動

```bash
cd docker
docker compose up -d
```

### API 文件

啟動後可前往 <http://localhost:7938/docs> 查看 FastAPI 自動生成的互動式 API 文件。

## 開發

### 建立 Docker image

```bash
bash docker/build.sh
```

### 執行單元測試

```bash
docker run --rm nk7260ynpa/tw-stock-webpage python -m pytest tests/ -v
```

## 授權

本專案採用 MIT 授權條款，詳見 [LICENSE](LICENSE) 檔案。
