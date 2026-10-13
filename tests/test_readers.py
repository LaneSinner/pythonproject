from unittest.mock import Mock, patch

from src.readers import read_csv_file, read_excel_file


@patch("src.readers.pd.read_csv")
def test_read_csv_file(mock_read_csv: Mock) -> None:
    """Проверяет чтение CSV-файла."""
    mock_dataframe = Mock()
    mock_dataframe.to_dict.return_value = [
        {"id": 1, "amount": 500},
        {"id": 2, "amount": 1200},
    ]
    mock_read_csv.return_value = mock_dataframe

    result = read_csv_file("transactions.csv")

    mock_read_csv.assert_called_once_with("transactions.csv")
    mock_dataframe.to_dict.assert_called_once_with(orient="records")
    assert result == [
        {"id": 1, "amount": 500},
        {"id": 2, "amount": 1200},
    ]


@patch("src.readers.pd.read_excel")
def test_read_excel_file(mock_read_excel: Mock) -> None:
    """Проверяет чтение Excel-файла."""
    mock_dataframe = Mock()
    mock_dataframe.to_dict.return_value = [
        {"id": 1, "amount": 500},
        {"id": 2, "amount": 1200},
    ]
    mock_read_excel.return_value = mock_dataframe

    result = read_excel_file("transactions_excel.xlsx")

    mock_read_excel.assert_called_once_with("transactions_excel.xlsx")
    mock_dataframe.to_dict.assert_called_once_with(orient="records")
    assert result == [
        {"id": 1, "amount": 500},
        {"id": 2, "amount": 1200},
    ]
