from unittest.mock import mock_open, patch
from src.services import cashback_categories


@patch("pandas.read_excel")
@patch("builtins.open", new_callable=mock_open)
def test_cashback_categories_normal_run(mock_file_open, mock_read_excel, test_excel_data):
    mock_read_excel.return_value = test_excel_data
    result = cashback_categories("fake_path.xlsx", "2019", "07")
    assert result == {"Наличные": 0, "Супермаркеты": 2}
