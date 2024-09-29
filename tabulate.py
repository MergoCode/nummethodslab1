import math

def f(x):
        return math.sin(x)


def tabulate():
    N = 20
    x0 = 0.0
    xn = 1.0

    x = [0.0] * (N + 1)
    y = [0.0] * (N + 1)
    h = [0.0] * (N + 1)

    hh = (xn - x0) / N

    for i in range(N + 1):
        x[i] = x0 + i * hh
        h[i] = hh
        y[i] = f(x[i])
    with open('input.txt', "w") as finput:
        for i in range(N + 1):
            finput.write(f"{i}\t{x[i]:e}\t{y[i]:e}\t{h[i]:e}\n")
    
    print("DONE")

tabulate()