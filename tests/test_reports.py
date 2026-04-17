from unittest.mock import mock_open, patch
import pandas as pd
from src.reports import my_decorator, my_decorator_with_param, spending_by_category


def test_normal_behavior(test_excel_data):
    result = spending_by_category(test_excel_data, "Супермаркеты", "2019-07-30")
    assert result["Категория"].iloc[0] == "Супермаркеты"
    assert result["Сумма трат"].iloc[0] == 5000.0


def test_my_decorator_with_mock():
    def dummy():
        return pd.DataFrame({"A": [1]})

    decorated = my_decorator(dummy)

    with (
        patch("pandas.DataFrame.to_json") as mock_to_json,
        patch("builtins.open", mock_open()) as mock_file,
        patch("json.dump") as mock_json_dump,
    ):
        mock_to_json.return_value = '{"A":[1]}'
        result = decorated()

        mock_to_json.assert_called_once_with()
        mock_file.assert_called_once_with("../data/json_outputs/spending_by_category.json", "w", encoding="utf-8")
        mock_json_dump.assert_called_once()
        assert result.equals(pd.DataFrame({"A": [1]}))


def test_my_decorator_with_mock_with_param():
    def dummy():
        return pd.DataFrame({"A": [1]})

    file_name = "mock_report.json"

    decorated = my_decorator_with_param(file_name)(dummy)

    with (
        patch("pandas.DataFrame.to_json") as mock_to_json,
        patch("builtins.open", mock_open()) as mock_file,
        patch("json.dump") as mock_json_dump,
    ):
        mock_to_json.return_value = '{"A":[1]}'
        result = decorated()

        mock_to_json.assert_called_once_with()
        mock_file.assert_called_once_with(f"../data/json_outputs/{file_name}", "w", encoding="utf-8")
        mock_json_dump.assert_called_once()
        assert result.equals(pd.DataFrame({"A": [1]}))
