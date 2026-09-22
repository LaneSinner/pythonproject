# Виджет банковских операций
Проект предназначен для обработки данных о банковских операциях.

## Функции

### filter_by_state

Фильтрует список банковских операций по значеню ключа 'state'.

По умолчанию используется статус 'EXECUTED'.

Пример:

```python
filter_by_state(operations)
filter_by_state(operations, "CANCELED")

