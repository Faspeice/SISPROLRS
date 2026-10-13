import numpy as np
import math


def generate_normal_sequence(size: int, mean: float, variance: float) -> np.ndarray:
    """
    Генерирует последовательность случайных чисел с нормальным распределением.
    :param size: количество элементов в последовательности
    :param mean: математическое ожидание (mx)
    :param variance: дисперсия (dx)
    :return: массив сгенерированных чисел
    """
    if size <= 0:
        raise ValueError("Размер последовательности должен быть больше 0.")

    std_dev = math.sqrt(variance)
    return np.random.normal(loc=mean, scale=std_dev, size=size)


def calculate_cumulative_sum(sequence: np.ndarray) -> np.ndarray:
    """
    Формирует новую последовательность yi = yi-1 + xi (кумулятивная сумма).
    :param sequence: исходная последовательность xi
    :return: последовательность yi
    """
    return np.cumsum(sequence)


def calculate_statistics(sequence: np.ndarray) -> tuple:
    """
    Вычисляет среднее значение и дисперсию последовательности.
    :param sequence: анализируемая последовательность
    :return: кортеж (среднее значение, выборочная дисперсия)
    """
    mean_val = np.mean(sequence)
    # ddof=1 используется для вычисления несмещенной (выборочной) дисперсии
    variance_val = np.var(sequence, ddof=1)
    return mean_val, variance_val


def print_histogram(sequence: np.ndarray, bins: int = 10, max_bar_width: int = 50) -> None:
    """
    Выводит гистограмму распределения последовательности в консоль.
    :param sequence: данные для гистограммы
    :param bins: количество интервалов
    :param max_bar_width: максимальная ширина столбца в символах
    """
    min_val = float(np.min(sequence))
    max_val = float(np.max(sequence))
    bin_width = (max_val - min_val) / bins

    # Подсчёт попаданий в каждый интервал
    counts = np.zeros(bins, dtype=int)
    for value in sequence:
        idx = int((value - min_val) / bin_width)
        if idx == bins:  # граничный случай для максимального значения
            idx -= 1
        counts[idx] += 1

    max_count = int(np.max(counts))
    if max_count == 0:
        print("Нет данных для построения гистограммы.")
        return

    print("\n" + "=" * 60)
    print(f"{'Гистограмма последовательности Y':^60}")
    print(f"{'(диапазон разбит на ' + str(bins) + ' интервалов)':^60}")
    print("=" * 60)

    for i in range(bins):
        left = min_val + i * bin_width
        right = left + bin_width
        # Нормируем длину столбца
        bar_length = int((counts[i] / max_count) * max_bar_width)
        bar = "█" * bar_length
        print(f"[{left:8.2f}, {right:8.2f}) | {bar} ({counts[i]})")

    print("=" * 60)


def main():
    print("=== Статистический анализ последовательности ===")

    # 1. Генерация исходной последовательности X
    n = 100
    mx = 5.0
    dx = 2.0
    x_sequence = generate_normal_sequence(size=n, mean=mx, variance=dx)

    # 2. Формирование последовательности Y
    y_sequence = calculate_cumulative_sum(x_sequence)

    # 3. Вычисление статистик
    mean_y, var_y = calculate_statistics(y_sequence)

    print(f"Количество элементов: {n}")
    print(f"Среднее значение последовательности Y: {mean_y:.4f}")
    print(f"Дисперсия последовательности Y: {var_y:.4f}")

    # 4. Визуализация в консоли
    print_histogram(y_sequence, bins=10)


if __name__ == "__main__":
    main()