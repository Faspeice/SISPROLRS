import numpy as np
import matplotlib.pyplot as plt

def f(x):
    """Подынтегральная функция (комплексный логарифм)."""
    return np.log((-x**2 - 1 + 0j) / (x**2 + 2))

def trapezoidal(a, b, n):
    """Метод трапеций для n разбиений."""
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)
    return h / 2 * (y[0] + 2 * np.sum(y[1:-1]) + y[-1])

def adaptive_trapezoidal(a, b, epsilon, max_iter=1000):
    """Адаптивный метод трапеций с точностью epsilon."""
    if a == b:
        return 0j, 1
    n = 10
    I_prev = trapezoidal(a, b, n)
    for _ in range(max_iter):
        n *= 2
        I_curr = trapezoidal(a, b, n)
        if abs(I_curr - I_prev) < epsilon:
            return I_curr, n
        I_prev = I_curr
    return I_curr, n

def plot_results(a, b, n, Z):
    """Графическая интерпретация результата."""
    x = np.linspace(a - 0.5, b + 0.5, 500)
    y = f(x)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    # Действительная часть
    ax1.plot(x, y.real, 'b-', linewidth=2, label='Re[f(x)]')
    ax1.fill_between(x[(x >= a) & (x <= b)],
                     0, y.real[(x >= a) & (x <= b)],
                     alpha=0.3, color='green',
                     label=f'∫ Re = {Z.real:.6f}')
    ax1.axvline(a, color='red', linestyle='--')
    ax1.axvline(b, color='red', linestyle='--')
    ax1.set_title('Действительная часть подынтегральной функции')
    ax1.legend(); ax1.grid(True)

    # Мнимая часть
    ax2.plot(x, y.imag, 'm-', linewidth=2, label='Im[f(x)] = π')
    ax2.fill_between(x[(x >= a) & (x <= b)],
                     0, y.imag[(x >= a) & (x <= b)],
                     alpha=0.3, color='orange',
                     label=f'∫ Im = {Z.imag:.6f}')
    ax2.axvline(a, color='red', linestyle='--')
    ax2.axvline(b, color='red', linestyle='--')
    ax2.set_title('Мнимая часть подынтегральной функции')
    ax2.legend(); ax2.grid(True)

    plt.suptitle(f'Z = {Z.real:.6f} + {Z.imag:.6f}i  (n={n})', fontsize=13)
    plt.tight_layout()
    plt.show()

# Параметры интегрирования
a, b, eps = 0, 1, 1e-6
Z, n = adaptive_trapezoidal(a, b, eps)
print(f"Z = {Z.real:.10f} + {Z.imag:.10f}i")
print(f"Разбиений: n = {n}")
plot_results(a, b, n, Z)