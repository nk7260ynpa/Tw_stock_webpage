"""資料庫連線管理模組。

提供 MySQL 資料庫連線池管理，支援多資料庫（TWSE/TPEX/TAIFEX/MGTS/FAOI）。
"""

import logging
from contextlib import contextmanager

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

# 資料庫連線設定
DB_HOST = "tw_stock_database"
DB_USER = "root"
DB_PASSWORD = "stock"
DB_PORT = 3306

# 支援的資料庫名稱
DATABASE_NAMES = ["TWSE", "TPEX", "TAIFEX", "MGTS", "FAOI"]

# 連線池：每個資料庫一個 engine
_engines = {}
_session_factories = {}


def _get_engine(db_name: str):
    """取得指定資料庫的 SQLAlchemy engine。

    Args:
        db_name: 資料庫名稱。

    Returns:
        SQLAlchemy Engine 實例。
    """
    if db_name not in _engines:
        url = (
            f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
            f"@{DB_HOST}:{DB_PORT}/{db_name}"
        )
        _engines[db_name] = create_engine(
            url,
            pool_size=5,
            max_overflow=10,
            pool_recycle=3600,
            echo=False,
        )
        logger.info("已建立資料庫連線池: %s", db_name)
    return _engines[db_name]


def _get_session_factory(db_name: str):
    """取得指定資料庫的 session factory。

    Args:
        db_name: 資料庫名稱。

    Returns:
        SQLAlchemy sessionmaker 實例。
    """
    if db_name not in _session_factories:
        engine = _get_engine(db_name)
        _session_factories[db_name] = sessionmaker(bind=engine)
    return _session_factories[db_name]


@contextmanager
def get_session(db_name: str):
    """取得資料庫 session 的 context manager。

    Args:
        db_name: 資料庫名稱。

    Yields:
        SQLAlchemy Session 實例。
    """
    factory = _get_session_factory(db_name)
    session = factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def execute_query(db_name: str, query: str, params: dict | None = None):
    """執行 SQL 查詢並回傳結果。

    Args:
        db_name: 資料庫名稱。
        query: SQL 查詢語句。
        params: 查詢參數。

    Returns:
        查詢結果列表，每筆為字典。
    """
    with get_session(db_name) as session:
        result = session.execute(text(query), params or {})
        columns = result.keys()
        return [dict(zip(columns, row)) for row in result.fetchall()]
