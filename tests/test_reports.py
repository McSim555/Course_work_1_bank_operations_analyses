from unittest.mock import Mock, mock_open, patch
import pandas as pd

from src.reports import my_decorator, my_decorator_with_param, spending_by_category


def test_normal_behavior(test_excel_data):
    result = spending_by_category(test_excel_data, "Супермаркеты", "2019-07-30")
    assert result["Категория"].iloc[0] == "Супермаркеты"
    assert result["Сумма трат"].iloc[0] == 5000.0


def test_my_decorator_with_mock():
    def spending_by_category_test():
        return pd.DataFrame({"A": [1]})

    decorated = my_decorator(spending_by_category_test)

    with patch("pandas.DataFrame.to_csv") as mock_to_csv:
        result = decorated()
        mock_to_csv.assert_called_once_with("../data/reports/report.csv", index=False, encoding="utf-8")
        assert result.equals(spending_by_category_test())


def test_my_decorator_with_param_mock():
    def spending_by_category_test():
        return pd.DataFrame({"A": [1]})

    file_name = "mock_report.csv"
    decorated = my_decorator_with_param(file_name)(spending_by_category_test)

    with patch("pandas.DataFrame.to_csv") as mock_to_csv:
        result = decorated()
        expected_path = f"../data/reports/{file_name}"
        mock_to_csv.assert_called_once_with(expected_path, index=False)
        assert result.equals(spending_by_category_test())
