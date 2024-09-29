import math
import matplotlib.pyplot as plt

def f(x):
    return math.sin(x)

def progonka(y, h, N):
    #create set of arrays that i will use later, i also create c-array instead of using it as parametr, i will return that array in the end
    alfa = [0.0] * (N + 1)
    beta = [0.0] * (N + 1)
    hamma = [0.0] * (N + 1)
    delta = [0.0] * (N + 1)
    A = [0.0] * (N + 1)
    B = [0.0] * (N + 1)
    c = [0.0] * (N + 1)

    alfa[1] = hamma[1] = delta[1] = 0.0
    beta[1] = 1.0 # it is 1, otherwise A[1] and B[1] won`t be able to be calculated 0/0

    #i set values for threediagonal matrix
    for i in range(2, N + 1):
        alfa[i] = h[i - 1]
        beta[i] = 2 * (h[i - 1] + h[i])
        hamma[i] = h[i]
        delta[i] = 3 * (((y[i] - y[i - 1]) / h[i]) - ((y[i - 1] - y[i - 2]) / h[i - 1]))

    #check if there is only one solution
    for i in range(1,N):
        if abs(beta[i]) <  abs(alfa[i]) + abs(hamma[i]):
            print("error")

    #c[n] = 0, that is why gamma[n] should be equal 0, вільний кубічний сплайн
    hamma[N] = 0.0

    #calculate A and B starting
    A[1] = -hamma[1] / beta[1]
    B[1] = delta[1] / beta[1]

    #progonka
    for i in range(2, N):
        A[i] = -hamma[i] / (alfa[i] * A[i - 1] + beta[i])
        B[i] = (delta[i] - alfa[i] * B[i - 1]) / (alfa[i] * A[i - 1] + beta[i])

    #claculate last c, after that we can start reverse progonka 
    c[N] = (delta[N] - alfa[N] * B[N - 1]) / (alfa[N] * A[N - 1] + beta[N])

    #reverse progonka
    for i in range(N, 1, -1):
        c[i - 1] = A[i - 1] * c[i] + B[i - 1]

    #return c array
    return c

def main():
    # read input file
    with open("input.txt", "r") as fdata:
        lines = fdata.readlines()

    # calculate number symbols
    N = len(lines) - 1

    # create arrays
    x = [0.0] * (N + 1)
    y = [0.0] * (N + 1)
    h = [0.0] * (N + 1)
    a = [0.0] * (N + 1)
    b = [0.0] * (N + 1)
    c = [0.0] * (N + 1)
    d = [0.0] * (N + 1)

    # set values for arrays from input file
    for i in range(N + 1):
        j, xi, yi, hi = lines[i].strip().split("\t")
        x[i] = float(xi)
        y[i] = float(yi)
        h[i] = float(hi)

    # progonka
    c = progonka(y, h, N)
    xm = []
    ym = []
    x0 = x[0]
    hh = h[0]

    # calculate a, b, d using formula from metodichka
    for i in range(1, N):
        a[i] = y[i - 1]
        b[i] = (y[i] - y[i - 1]) / h[i] - (h[i] / 3) * (c[i + 1] + 2 * c[i])
        d[i] = (c[i + 1] - c[i]) / (3 * h[i])

    a[N] = y[N - 1]
    b[N] = (y[N] - y[N - 1]) / h[N] - (2.0 / 3.0) * h[N] * c[N]
    d[N] = -c[N] / (3 * h[N])

    temp = 0
    ys=[]
    eps_arr = []

    # output file
    with open("output.txt", "w") as foutput:
        hh /=20
        # Generate xm and ym arrays
        for i in range(20 * N + 1):
            xm_i = x0 + i * hh
            xm.append(xm_i)
            ym.append(f(xm_i))

        # Calculate spline values and errors
        s = 0.0
        eps = 0.0
        j = 1
        for i in range(20 * (N) + 1):
            s=a[j]+b[j]*(xm[i]-x[j-1])+c[j]*(xm[i]-x[j-1])*(xm[i]-x[j-1])* 2 + 3 * d[j]*(xm[i]-x[j-1])*(xm[i]-x[j-1])*(xm[i]-x[j-1]);            ys.append(s)
            eps = abs(s - ym[i])
            eps_arr.append(eps)
            foutput.write(f"[{i},{j}]    \t{xm[i]:.6f}\t{ym[i]:.6f}\t{s:.6f}\t{eps:.10f}\n")
            if (i != 0) and (i % 20 == 0):
                j += 1

    plt.plot(x, y, '.', label='Табульовані точки')  # Початкові точки
    
    plt.plot(xm, ym, color="red",  label='Оригінальна функція sin(x)')
    plt.plot(xm, ys, color="black", label='Наближене значення через сплайн')
    plt.plot(xm, eps_arr, color="green",label='Похибка')
    plt.legend()
    plt.show()

    print("DONE")

main()