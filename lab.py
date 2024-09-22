import matplotlib.pyplot as plt
import math
import numpy as np

def f(x):
    return math.sin(x)

def progonka(y, h, N, c):
    i = 1
    alfa = [0.0] * (N+1)
    beta = [0.0] * (N+1)
    hamma = [0.0] * (N+1)
    delta = [0.0] * (N+1)
    A = [0.0] * (N+1)
    B = [0.0] * (N+1)
    alfa[1]=hamma[1]=delta[1]=0.0
    beta[1] = 1.0
    for i in range(2, N):
        alfa[i] = h[i-1]
        beta[i] = 2*(h[i-1]+h[i])
        hamma[i] = h[i]
        delta[i] = 3 * (((y[i]-y[i-1])/h[i]) - ((y[i-1] - y[i-2]/h[i-1])))
    hamma[N] = 0.0
    A[1] = -hamma[1]/beta[1]
    B[1] = delta[1]/beta[1]
    for i in range(2, N-1):
        A[i] = -hamma[i]/(alfa[i] * A[i-1] + beta[i])
        B[i] = (delta[i] - alfa[i] * B[i-1])/(alfa[i] * A[i-1] + beta[i])
    c[N] = (delta[N] - alfa[N] * B[N-1]) / (alfa[N] * A[N-1] + beta[i])
    for i in range(N, 1, -1):
        c[i-1] = A[i-1] * c[i] + B[i-1]
    

def main():
    filename = "input.txt"
    output_filename = "output.txt"
    # Step 1: Read data from file
    with open(filename, "r") as fdata:
        lines = fdata.readlines()

    N = len(lines) - 1  # Number of rows minus the header
    x = np.zeros(N + 1)
    y = np.zeros(N + 1)
    h = np.zeros(N + 1)
    a = np.zeros(N + 1)
    b = np.zeros(N + 1)
    c = np.zeros(N + 1)
    d = np.zeros(N + 1)
    
    # Step 2: Parse file and store values
    for i in range(1, N + 1):
        _, x[i], y[i], h[i] = map(float, lines[i].split())
    
    x0 = x[0]
    hh = h[0]
    
    # Assuming you have the progonka function defined elsewhere
    progonka(y, h, N, c)
    
    for i in range(1, N):
        a[i] = y[i - 1]
        b[i] = (y[i] - y[i - 1]) / h[i] - (h[i] / 3) * (c[i + 1] + 2 * c[i])
        d[i] = (c[i + 1] - c[i]) / (3 * h[i])
    
    a[N] = y[N - 1]
    b[N] = (y[N] - y[N - 1]) / h[N] - (2.0 / 3.0) * h[N] * c[N]
    d[N] = -c[N] / (3 * h[N])

    # Step 3: Generate interpolated values
    xm = np.zeros(20 * N + 1)
    ym = np.zeros(20 * N + 1)
    
    hh /= 20.0
    for i in range(20 * N + 1):
        xm[i] = x0 + i * hh
        ym[i] = f(xm[i])  # Assuming `f` is your function

    # Step 4: Compute spline and errors
    s_values = np.zeros(20 * N + 1)  # Fix dimension to match xm and ym
    eps_values = np.zeros(20 * N + 1)
    j = 1

    with open(output_filename, "w") as foutput:
        for i in range(20 * N + 1):  # Ensure this loop runs for the same length as xm and ym
            s = (a[j] + b[j] * (xm[i] - x[j - 1]) + c[j] * (xm[i] - x[j - 1]) ** 2 +
                 d[j] * (xm[i] - x[j - 1]) ** 3)
            eps = abs(s - ym[i])
            s_values[i] = s
            eps_values[i] = eps
            foutput.write(f"[{i},{j}]\t{xm[i]:e}\t{ym[i]:e}\t{s:e}\t{eps:e}\n")
            if i != 0 and i % 20 == 0:
                j += 1

    # Step 5: Plot the results using matplotlib
    plt.figure(figsize=(10, 6))
    plt.plot(xm, ym, label="Original Function", color="blue")
    plt.plot(xm, s_values, label="Spline Approximation", color="red", linestyle='--')
    plt.legend()
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Original Function vs Spline Approximation")
    plt.grid(True)
    plt.show()

main()
