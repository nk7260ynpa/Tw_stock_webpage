"""app 模組的單元測試。"""

import unittest
from unittest.mock import patch


class TestApp(unittest.TestCase):
    """測試主應用程式模組。"""

    @patch("streamlit.set_page_config")
    @patch("streamlit.title")
    @patch("streamlit.write")
    def test_main_runs_without_error(self, mock_write, mock_title, mock_config):
        """測試 main 函式能正常執行。"""
        from src.app import main

        main()

        mock_config.assert_called_once()
        mock_title.assert_called_once_with("台灣股票資訊")
        mock_write.assert_called_once()


if __name__ == "__main__":
    unittest.main()
