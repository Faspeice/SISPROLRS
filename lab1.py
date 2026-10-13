import math


def calculate_pascal_element(row: int, position: int) -> int:
    """
    Вычисляет элемент треугольника Паскаля.
    :param row: номер строки (начинается с 1)
    :param position: номер позиции в строке (начинается с 1)
    :return: значение элемента треугольника
    """
    if row <= 0 or position <= 0 or position > row:
        raise ValueError("Некорректные координаты.")

    # Переводим в 0-индексацию для формулы сочетаний
    n = row - 1
    k = position - 1
    return math.comb(n, k)


def get_user_input() -> tuple:
    """Запрашивает и валидирует ввод пользователя."""
    while True:
        try:
            row = int(input("Введите номер строки (целое число > 0): "))
            if row <= 0:
                print("Ошибка: номер строки должен быть строго больше 0.\n")
                continue

            position = int(input(f"Введите номер позиции в строке {row} (от 1 до {row}): "))
            if position < 1 or position > row:
                print(f"Ошибка: позиция должна быть в диапазоне от 1 до {row}.\n")
                continue

            return row, position
        except ValueError:
            print("Ошибка: необходимо ввести целое число. Попробуйте снова.\n")


def main():
    print("=== Поиск элемента треугольника Паскаля ===")
    print("Пример: Строка 4, Позиция 2 -> Элемент 3 (1 3 3 1)\n")

    row, position = get_user_input()
    result = calculate_pascal_element(row, position)

    print(f"\nРезультат: Элемент на позиции {position} в строке {row} равен {result}.")


if __name__ == "__main__":
    main()