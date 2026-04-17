import json
from unittest.mock import Mock, mock_open, patch

import pytest

from src.utils import cards_data, currency_rates, data_from_excel, greetings, sort_by_payment, stock_information


def test_greetings_evening():
    """Тест штатного срабатывания на вечер"""

    datetime = "2021-05-05 23:15:15"
    output = greetings(datetime)

    assert output == "Добрый вечер!"


def test_greetings_day():
    """Тест штатного срабатывания на день"""

    datetime = "2021-05-05 13:15:15"
    output = greetings(datetime)

    assert output == "Добрый день!"


def test_greetings_no_input():
    """Тест возбуждения ошибки при некорректной дате"""

    datetime = "2021"
    with pytest.raises(Exception):
        greetings(datetime)


@patch("pandas.read_excel")
def test_data_from_excel_normal_run(mock_read_excel, test_excel_data, test_excel_file):
    """Тест работы с нормальным входным файлом"""

    mock_read_excel.return_value = test_excel_data
    result = data_from_excel("fake_path.xlsx")

    assert result == test_excel_file

    mock_read_excel.assert_called_once_with("fake_path.xlsx")


def test_data_from_excel_no_file():
    """Тест случая, если файл не найден"""

    result = data_from_excel("")
    assert result == []


@pytest.mark.parametrize(
    "test_case, date, expected",
    [
        (
            [
                {
                    "Дата операции": "20.07.2019 15:28:23",
                    "Дата платежа": "22.07.2019",
                    "Номер карты": "*4556",
                    "Статус": "OK",
                    "Сумма операции": -5000.0,
                    "Валюта операции": "RUB",
                    "Сумма платежа": -5000.0,
                    "Валюта платежа": "RUB",
                    "Кэшбэк": "",
                    "Категория": "Наличные",
                    "MCC": 6011.0,
                    "Описание": "Снятие в банкомате Сбербанк",
                    "Бонусы (включая кэшбэк)": 0,
                    "Округление на инвесткопилку": 0,
                    "Сумма операции с округлением": 5000.0,
                },
                {
                    "Дата операции": "20.07.2019 15:27:44",
                    "Дата платежа": "22.07.2019",
                    "Номер карты": "*4556",
                    "Статус": "OK",
                    "Сумма операции": -5000.0,
                    "Валюта операции": "RUB",
                    "Сумма платежа": -5000.0,
                    "Валюта платежа": "RUB",
                    "Кэшбэк": "2",
                    "Категория": "Супермаркеты",
                    "MCC": 6011.0,
                    "Описание": "Снятие в банкомате Сбербанк",
                    "Бонусы (включая кэшбэк)": 2,
                    "Округление на инвесткопилку": 0,
                    "Сумма операции с округлением": 5000.0,
                },
            ],
            "2019-07-25 12:11:23",
            [
                {"last_digits": "4556", "total_spent": -5000.0, "cashback": 0},
                {"last_digits": "4556", "total_spent": -5000.0, "cashback": 50},
            ],
        )
    ],
)
def test_cards_data_normal_run(test_case, date, expected):
    """ "Тест нормального функционирования"""

    assert cards_data(test_case, date) == expected


def test_sort_by_payment(test_excel_file_2):
    """Тест работы при получении нормального файла"""

    datetime = "2019-07-25 12:11:23"
    result = sort_by_payment(test_excel_file_2, datetime)

    assert result == [
        {
            "date": "22.07.2019",
            "amount": -5000.0,
            "category": "Наличные",
            "description": "Снятие в банкомате Сбербанк",
        },
        {
            "date": "22.07.2019",
            "amount": -5000.0,
            "category": "Супермаркеты",
            "description": "Снятие в банкомате Сбербанк",
        },
        {"date": "22.07.2019", "amount": -3000.0, "category": "Супермаркеты", "description": "Лента"},
        {
            "date": "22.07.2019",
            "amount": -2000.0,
            "category": "Наличные",
            "description": "Снятие в банкомате Сбербанк",
        },
        {
            "date": "22.07.2019",
            "amount": -1000.0,
            "category": "Наличные",
            "description": "Снятие в банкомате Сбербанк",
        },
    ]


class TestCurrencyRates:
    @patch("requests.get")
    @patch("os.getenv", return_value="test_key")
    @patch("builtins.open", mock_open(read_data='{"user_currencies": ["USD"]}'))
    @patch("dotenv.load_dotenv")
    def test_successful_execution_currency(self, mock_load_dotenv, mock_getenv, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"result": 95.5}
        mock_get.return_value = mock_response

        rate = currency_rates("dummy_path", "2023-10-01")

        assert len(rate) == 1
        assert rate[0]["currency"] == "USD"
        assert rate[0]["rate"] == 95.5


class TestStockInformation:
    @patch("requests.get")
    @patch("os.getenv", return_value="test_key")
    @patch("dotenv.load_dotenv")
    def test_successful_execution_stocks(self, mock_load_dotenv, mock_getenv, mock_get):

        mock_file_data = json.dumps({"user_stocks": ["AAPL"]})
        with patch("builtins.open", mock_open(read_data=mock_file_data)):

            mock_response = Mock()
            mock_response.json.return_value = [{"symbol": "AAPL", "price": 100}]
            mock_get.return_value = mock_response

            stock_price = stock_information("dummy_path")

        assert len(stock_price) == 1
        assert stock_price[0]["stock"] == "AAPL"
        assert stock_price[0]["price"] == 100
