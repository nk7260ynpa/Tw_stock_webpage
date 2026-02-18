"""台灣股票資訊網頁應用程式的主要進入點。"""

import logging
from pathlib import Path

import streamlit as st

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


def main():
    """主程式進入點。"""
    st.set_page_config(
        page_title="台灣股票資訊",
        page_icon="📈",
        layout="wide",
    )

    st.title("台灣股票資訊")
    st.write("歡迎使用台灣股票資訊網頁應用程式。")
    logger.info("應用程式已啟動")


if __name__ == "__main__":
    main()
