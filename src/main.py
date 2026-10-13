from typing import Any
from src.processing import (
    filter_by_state,
    process_bank_operations,
    process_bank_search,
    sort_by_date,
)
from src.readers import read_csv_file, read_excel_file
from src.utils import read_json_file
from src.widget import get_date, mask_account_card


def main() -> None:
    """Запускает интерфейс для поиска и фильтрации банковских операций."""
    print("Привет! Добро пожаловать в программу работы " "с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    file_types = {
        "1": ("JSON", read_json_file),
        "2": ("CSV", read_csv_file),
        "3": ("XLSX", read_excel_file),
    }

    while True:
        choice = input("Ваш выбор: ").strip()

        if choice in file_types:
            file_type, reader = file_types[choice]
            break

        print("Неверный пункт меню. Введите 1, 2 или 3.")

    print(f"Для обработки выбран {file_type}-файл.")
    file_path = input("Введите путь к файлу: ").strip()

    try:
        operations = reader(file_path)
    except (OSError, ValueError, KeyError) as error:
        print(f"Не удалось прочитать файл: {error}")
        return

    if not operations:
        print("Не найдено ни одной транзакции.")
        return

    available_states = {"EXECUTED", "CANCELED", "PENDING"}

    while True:
        print(
            "Введите статус, по которому необходимо выполнить фильтрацию.\n"
            "Доступные статусы: EXECUTED, CANCELED, PENDING"
        )
        status = input("Статус: ").strip().upper()

        if status in available_states:
            break

        print(f'Статус операции "{status}" недоступен.')

    filtered = filter_by_state(operations, status)
    print(f'Операции отфильтрованы по статусу "{status}".')

    answer = input("Отсортировать операции по дате? Да/Нет: ").strip().lower()

    if answer in ("да", "д", "yes", "y"):
        while True:
            order = input("Сортировать по возрастанию или по убыванию? ").strip().lower()

            if order in ("по возрастанию", "возрастание"):
                filtered = sort_by_date(filtered, descending=False)
                break
            if order in ("по убыванию", "убывание"):
                filtered = sort_by_date(filtered, descending=True)
                break

            print("Введите «по возрастанию» или «по убыванию».")

    answer = input("Выводить только рублевые транзакции? Да/Нет: ").strip().lower()

    if answer in ("да", "д", "yes", "y"):
        filtered = [
            operation
            for operation in filtered
            if operation.get("operationAmount", {}).get("currency", {}).get("code") == "RUB"
        ]

    answer = input("Отфильтровать список транзакций по слову в описании? Да/Нет: ").strip().lower()

    if answer in ("да", "д", "yes", "y"):
        search = input("Введите поисковую строку: ").strip()
        filtered = process_bank_search(filtered, search)

    if not filtered:
        print("Не найдено ни одной транзакции, подходящей " "под ваши условия фильтрации.")
        return

    print("Распечатываю итоговый список транзакций...")
    print(f"Всего банковских операций в выборке: {len(filtered)}")

    for operation in filtered:
        date = get_date(str(operation.get("date", "")))
        description = operation.get("description", "Без описания")
        amount_data: dict[str, Any] = operation.get("operationAmount", {})
        amount = amount_data.get("amount", 0)
        currency = amount_data.get("currency", {}).get("name", "")

        print(f"\n{date} {description}")

        for key in ("from", "to"):
            if operation.get(key):
                print(mask_account_card(str(operation[key])))

        print(f"Сумма: {amount} {currency}")

    answer = input("Посчитать количество операций по категориям? Да/Нет: ").strip().lower()

    if answer in ("да", "д", "yes", "y"):
        categories_input = input("Введите названия категорий через запятую: ")
        categories = [category.strip() for category in categories_input.split(",") if category.strip()]
        counts = process_bank_operations(filtered, categories)

        for category, count in counts.items():
            print(f"{category}: {count}")


if __name__ == "__main__":
    main()
