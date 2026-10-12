import json

from src.utils import read_json_file


def test_read_json_file_returns_list(tmp_path):
    file_path = tmp_path / "operations.json"

    data = [{"id": 1}, {"id": 2}]

    file_path.write_text(
        json.dumps(data),
        encoding="utf-8",
    )

    assert read_json_file(file_path) == data


def test_read_json_file_missing_file():
    assert read_json_file("missing.json") == []


def test_read_json_file_empty_file(tmp_path):
    file_path = tmp_path / "empty.json"

    file_path.write_text(
        "",
        encoding="utf-8",
    )
    assert read_json_file(file_path) == []


def test_read_json_file_invalid_json(tmp_path):
    file_path = tmp_path / "broken.json"

    file_path.write_text(
        "not json",
        encoding="utf-8",
    )

    assert read_json_file(file_path) == []


def test_read_json_file_root_is_not_list(tmp_path):
    file_path = tmp_path / "object.json"

    file_path.write_text(
        '{"id": 1}',
        encoding="utf-8",
    )

    assert read_json_file(file_path) == []
