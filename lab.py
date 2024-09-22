import matplotlib.pyplot as plt
import math

def f(x):
    return math.sin(x)

def progonka(y, h, N, c):
    alfa = [0.0] * (N + 1)
    beta = [0.0] * (N + 1)
    hamma = [0.0] * (N + 1)
    delta = [0.0] * (N + 1)
    A = [0.0] * (N + 1)
    B = [0.0] * (N + 1)
    
    for i in range(1, N):
        alfa[i] = h[i]
        beta[i] = 2 * (h[i] + h[i-1])
        hamma[i] = h[i-1]
        delta[i] = 3 * ((y[i+1] - y[i]) / h[i] - (y[i] - y[i-1]) / h[i-1])
    
    for i in range(2, N):
        m = hamma[i] / beta[i-1]
        beta[i] -= m * alfa[i-1]
        delta[i] -= m * delta[i-1]
    
    c[N] = 0
    for i in range(N-1, 0, -1):
        c[i] = (delta[i] - alfa[i] * c[i+1]) / beta[i]

def main():
    x = [0.0, 1.0, 2.0, 3.0, 4.0]
    y = [f(xi) for xi in x]
    N = len(x) - 1
    h = [x[i+1] - x[i] for i in range(N)]
    
    c = [0.0] * (N + 1)
    progonka(y, h, N, c)

    a = y[:-1]
    b = [(y[i+1] - y[i]) / h[i] - (h[i] * (2*c[i] + c[i+1])) / 3 for i in range(N)]
    d = [(c[i+1] - c[i]) / (3 * h[i]) for i in range(N)]
    
    x_plot = []
    y_plot = []
    y_nabl = []

    for i in range(N):
        xs = [x[i] + j * (h[i] / 20) for j in range(21)]
        ys = [a[i] + b[i] * (xi - x[i]) + c[i] * (xi - x[i])**2 + d[i] * (xi - x[i])**3 for xi in xs]
        x_plot.extend(xs)
        y_plot.extend(ys)
        y_nabl.extend([f(xi) for xi in xs])

    plt.figure(figsize=(10, 8))

    plt.subplot(2, 1, 1)
    x_fine = [i * 0.1 for i in range(41)]
    y_fine = [f(xi) for xi in x_fine]
    plt.plot(x_fine, y_fine, label="Original Function f(x)", color='blue', linestyle='-', linewidth=2)
    plt.plot(x_plot, y_plot, label="Cubic Spline", color='red', linestyle='--', linewidth=2)
    plt.title("Comparison of Function f(x) and Cubic Spline")
    plt.xlabel("x")
    plt.ylabel("f(x) / Spline(x)")
    plt.legend(loc="best")
    plt.grid(True)

    epsilon = [abs(y_nabl[i] - y_plot[i]) for i in range(len(y_plot))]

    plt.subplot(2, 1, 2)
    plt.plot(x_plot, epsilon, label="Error |f(x) - Spline(x)|", color='green', linestyle='-', linewidth=2)
    plt.title("Error between Original Function and Cubic Spline")
    plt.xlabel("x")
    plt.ylabel("Error")
    plt.legend(loc="best")
    plt.grid(True)

    plt.tight_layout()
    plt.show()

main()
