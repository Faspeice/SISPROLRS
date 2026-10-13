import numpy as np
import matplotlib.pyplot as plt


# ==============================================================================
# 1. МАТЕМАТИЧЕСКИЕ ФУНКЦИИ
# ==============================================================================

def f(x):
    """
    Подынтегральная функция.
    Добавление 0j гарантирует, что вычисления будут вестись в комплексной области,
    так как аргумент логарифма (-x^2 - 1)/(x^2 + 2) всегда отрицателен.
    """
    return np.log((-x ** 2 - 1 + 0j) / (x ** 2 + 2))


def trapezoidal(a, b, n):
    """
    Базовый метод трапеций для фиксированного числа разбиений n.
    """
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)
    # Формула трапеций: h/2 * (y_0 + 2*y_1 + ... + 2*y_{n-1} + y_n)
    return (h / 2) * (y[0] + 2 * np.sum(y[1:-1]) + y[-1])


def adaptive_trapezoidal(a, b, epsilon, max_iter=1000):
    """
    Адаптивный метод трапеций с автоматическим подбором n для достижения точности epsilon.
    """
    if epsilon <= 0:
        raise ValueError("Точность epsilon должна быть строго больше 0")

    if a == b:
        return 0j, 1

    n = 10  # Начальное количество разбиений
    I_prev = trapezoidal(a, b, n)

    for _ in range(max_iter):
        n *= 2  # Удваиваем число разбиений (правило Рунге)
        I_curr = trapezoidal(a, b, n)

        # Проверка сходимости (модуль разности комплексных чисел)
        if abs(I_curr - I_prev) < epsilon:
            return I_curr, n

        I_prev = I_curr

    # Если максимальное число итераций достигнуто, возвращаем лучший результат
    return I_curr, n


# ==============================================================================
# 2. ГРАФИЧЕСКАЯ ИНТЕРПРЕТАЦИЯ
# ==============================================================================

def plot_results(a, b, n, Z):
    """
    Построение графиков действительной и мнимой частей функции и закрашивание площади интеграла.
    """
    # Для гладкой линии графика используем фиксированное высокое разрешение
    x_plot = np.linspace(a - 0.5, b + 0.5, 1000)
    y_plot = f(x_plot)

    # Для закрашивания трапеций ограничиваем число точек, чтобы график не тормозил при огромных n
    n_plot = min(n, 1000)
    x_fill = np.linspace(a, b, n_plot + 1)
    y_fill = f(x_fill)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    # --- Действительная часть ---
    ax1.plot(x_plot, y_plot.real, 'b-', linewidth=2, label='Re[f(x)] = ln((x²+1)/(x²+2))')
    ax1.fill_between(x_fill, 0, y_fill.real, alpha=0.3, color='green',
                     label=f'∫ Re = {Z.real:.6f}')
    ax1.axvline(a, color='red', linestyle='--', linewidth=1)
    ax1.axvline(b, color='red', linestyle='--', linewidth=1)
    ax1.set_title('Действительная часть подынтегральной функции')
    ax1.set_ylabel('Re[f(x)]')
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.5)

    # --- Мнимая часть ---
    ax2.plot(x_plot, y_plot.imag, 'm-', linewidth=2, label='Im[f(x)] = π')
    ax2.fill_between(x_fill, 0, y_fill.imag, alpha=0.3, color='orange',
                     label=f'∫ Im = {Z.imag:.6f}')
    ax2.axvline(a, color='red', linestyle='--', linewidth=1)
    ax2.axvline(b, color='red', linestyle='--', linewidth=1)
    ax2.set_title('Мнимая часть подынтегральной функции')
    ax2.set_xlabel('x')
    ax2.set_ylabel('Im[f(x)]')
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.5)

    plt.suptitle(f'Результат интегрирования: Z = {Z.real:.6f} + {Z.imag:.6f}i  (n={n} разбиений)',
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()


# ==============================================================================
# 3. ТЕСТИРОВАНИЕ (Нормальные, Экстремальные, Исключительные)
# ==============================================================================

def run_tests():
    print("\n" + "=" * 80)
    print("ТЕСТИРОВАНИЕ ПРОГРАММЫ")
    print("=" * 80)

    # 1. Нормальные ситуации
    print("\n[1] НОРМАЛЬНЫЕ СИТУАЦИИ:")
    print("-" * 80)
    normal_cases = [
        (0, 1, 1e-6, "Стандартный интервал [0, 1], ε=1e-6"),
        (-1, 1, 1e-6, "Симметричный интервал [-1, 1], ε=1e-6"),
        (0, 2, 1e-6, "Интервал [0, 2], ε=1e-6"),
        (0, 1, 1e-8, "Повышенная точность ε=1e-8"),
    ]
    for a, b, eps, desc in normal_cases:
        try:
            Z, n = adaptive_trapezoidal(a, b, eps)
            print(f"✓ {desc}")
            print(f"  Результат: {Z.real:.8f} + {Z.imag:.8f}i | Разбиений (n): {n}")
        except Exception as e:
            print(f"✗ {desc} -> Ошибка: {e}")

    # 2. Экстремальные ситуации
    print("\n[2] ЭКСТРЕМАЛЬНЫЕ СИТУАЦИИ:")
    print("-" * 80)
    extreme_cases = [
        (0, 100, 1e-6, "Очень широкий интервал [0, 100]"),
        (0, 1, 1e-12, "Сверхвысокая точность ε=1e-12"),
        (0.999, 1.001, 1e-6, "Сверхузкий интервал [0.999, 1.001]"),
        (-50, 50, 1e-4, "Широкий симметричный интервал с низкой точностью"),
    ]
    for a, b, eps, desc in extreme_cases:
        try:
            Z, n = adaptive_trapezoidal(a, b, eps)
            print(f"✓ {desc}")
            print(f"  Результат: {Z.real:.8f} + {Z.imag:.8f}i | Разбиений (n): {n}")
        except Exception as e:
            print(f"✗ {desc} -> Ошибка: {e}")

    # 3. Исключительные (ошибочные) ситуации
    print("\n[3] ИСКЛЮЧИТЕЛЬНЫЕ СИТУАЦИИ (Обработка ошибок):")
    print("-" * 80)
    exceptional_cases = [
        (1, 1, 1e-6, "Нулевой интервал (a = b)"),
        (0, 1, 0, "Нулевая точность (ε = 0)"),
        (0, 1, -1e-6, "Отрицательная точность (ε < 0)"),
        (1, 0, 1e-6, "Перевёрнутые пределы (a > b)"),
    ]
    for a, b, eps, desc in exceptional_cases:
        try:
            Z, n = adaptive_trapezoidal(a, b, eps)
            print(f"✓ {desc} -> Обработано корректно. Результат: {Z.real:.6f} + {Z.imag:.6f}i")
        except ValueError as ve:
            print(f"✓ {desc} -> Корректно перехвачено исключение: {ve}")
        except Exception as e:
            print(f"✗ {desc} -> Неожиданная ошибка: {e}")


# ==============================================================================
# 4. ОСНОВНАЯ ПРОГРАММА
# ==============================================================================

if __name__ == "__main__":
    # Параметры по умолчанию для основного запуска
    a_main = 0
    b_main = 1
    epsilon_main = 1e-6

    print("ЗАПУСК ОСНОВНОЙ ПРОГРАММЫ")
    print("-" * 80)
    print(f"Вычисление интеграла от ln((-x²-1)/(x²+2)) на интервале [{a_main}, {b_main}]")
    print(f"Требуемая точность: ε = {epsilon_main}\n")

    try:
        Z_result, n_result = adaptive_trapezoidal(a_main, b_main, epsilon_main)
        print("Успешно вычислено:")
        print(f"Значение интеграла Z = {Z_result.real:.10f} + {Z_result.imag:.10f}i")
        print(f"Потребовалось разбиений: n = {n_result}")
        print("\nОткрытие окна с графиками...")

        # Вызов графической интерпретации
        plot_results(a_main, b_main, n_result, Z_result)

    except Exception as e:
        print(f"Критическая ошибка при выполнении: {e}")

    # Запуск набора тестов
    run_tests()