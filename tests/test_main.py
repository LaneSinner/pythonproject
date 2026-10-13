from src import main as main_module


def test_main_success(monkeypatch, capsys):
    """Проверяет успешный запуск программы."""
    operations = [
        {
            "state": "EXECUTED",
            "date": "2019-12-08T12:00:00",
            "description": "Открытие вклада",
            "operationAmount": {
                "amount": "1000",
                "currency": {"name": "руб.", "code": "RUB"},
            },
        }
    ]
    monkeypatch.setattr("builtins.input", lambda _: next(iter(inputs), "нет"))
    inputs = iter(["1", "test.json", "EXECUTED", "нет", "нет", "нет", "нет"])
    monkeypatch.setattr(main_module, "read_json_file", lambda _: operations)
    monkeypatch.setattr(main_module, "get_date", lambda _: "08.12.2019")

    main_module.main()

    output = capsys.readouterr().out
    assert "Добро пожаловать" in output
    assert "Всего банковских операций в выборке: 1" in output
    assert "Открытие вклада" in output


def test_main_invalid_menu(monkeypatch, capsys):
    """Проверяет повторный ввод при неправильном пункте меню."""
    inputs = iter(["9", "1", "test.json", "EXECUTED", "нет", "нет", "нет", "нет"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr(main_module, "read_json_file", lambda _: [])

    main_module.main()

    output = capsys.readouterr().out
    assert "Неверный пункт меню" in output
    assert "Не найдено ни одной транзакции" in output
