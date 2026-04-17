from unittest.mock import mock_open, patch
import pytest
from src.views import main_page


class TestMainPage:
    @patch("src.views.stock_information")
    @patch("src.views.currency_rates")
    @patch("src.views.sort_by_payment")
    @patch("src.views.cards_data")
    @patch("src.views.greetings")
    @patch("src.views.data_from_excel")
    @patch("builtins.open", new_callable=mock_open)
    def test_main_page_success(
        self,
        mock_file,
        mock_data_from_excel,
        mock_greetings,
        mock_cards_data,
        mock_sort_by_payment,
        mock_currency_rates,
        mock_stock_information,
    ):

        mock_data_from_excel.return_value = []
        mock_greetings.return_value = "Добрый день"
        mock_cards_data.return_value = [{"card": "1234", "total": 1000}]
        mock_sort_by_payment.return_value = [{"amount": 500}]
        mock_currency_rates.return_value = [{"currency": "USD", "rate": 90}]
        mock_stock_information.return_value = [{"stock": "AAPL", "price": 150}]

        date_str = "2023-10-01 12:00:00"

        result = main_page(date_str)

        assert result["greeting"] == "Добрый день"
        assert result["cards"] == [{"card": "1234", "total": 1000}]
        assert result["top_transactions"] == [{"amount": 500}]
        assert result["currency_rates"] == [{"currency": "USD", "rate": 90}]
        assert result["stock_prices"] == [{"stock": "AAPL", "price": 150}]

        mock_file.assert_called_once_with("../data/json_outputs/main_output.json", "w", encoding="utf-8")


def test_main_page_failure():
    """Тест функции с некорректной датой"""

    date = ""
    with pytest.raises(Exception):
        main_page(date)
