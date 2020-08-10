from numpy import *
import matplotlib.pyplot as plt
import timeit
def best_worst_fij(a, b):
    f = zeros((b.shape[0], 2))
    for i in range(b.shape[0]):
        if b[i] == 'max':
            f[i, 0] = a.max(0)[i]
            f[i, 1] = a.min(0)[i]
        elif b[i] == 'min':
            f[i, 0] = a.min(0)[i]
            f[i, 1] = a.max(0)[i]
    return f
def SR(a, b, c):
    s = zeros(a.shape[0])
    r = zeros(a.shape[0])
    for i in range(a.shape[0]):
        k = 0
        o = 0
        for j in range(a.shape[1]):
            k = k + c[j] * (b[j, 0] - a[i, j]) / (b[j, 0] - b[j, 1])
            u = c[j] * (b[j, 0] - a[i, j]) / (b[j, 0] - b[j, 1])
            if u > o:
                o = u
                r[i] = round(o, 3)
            else:
                r[i] = round(o, 3)
        s[i] = round(k, 3)
    return s, r
def Q(s, r, n):
    q = zeros(s.shape[0])
    for i in range(s.shape[0]):
        q[i] = round((((n + 1) / (2 * n)) *(s[i] - min(s)) / (max(s) - min(s)) +(1 - (n + 1) / (2 * n)) *(r[i] - min(r)) / (max(r) - min(r))), 3)
    return q
def vikor(a, b, c, pl):
    s, r = SR(a, best_worst_fij(a, b), c)
    q = Q(s, r, len(c))
    if pl == 'y':
        e = [i + 1 for i in range(a.shape[0])]
        plt.plot(e, s, 'p--', color = 'red',markeredgewidth = 2, markersize = 8)
        
        plt.plot(e, r, '*--', color = 'blue',markeredgewidth = 2, markersize = 8)
        plt.plot(e, q, 'o--', color = 'green',markeredgewidth = 2, markersize = 8)
        plt.legend(['S', 'R', 'Q'])
        plt.xticks(range(a.shape[0] + 2))
        plt.axis([0, a.shape[0] + 1, 0,
        max(maximum(maximum(s, r), q)) + 0.3])
        plt.title("VIKOR results")
        plt.xlabel("Alternatives")
        plt.legend()
        plt.grid(True)
        plt.show()
    return s, r, q
x = array([[8, 7, 2, 1], [5, 3, 7, 5], [7, 5, 6, 4],[9, 9, 7, 3], [11, 10, 3, 7], [6, 9, 5, 4]])
w = array([0.4, 0.3, 0.1, 0.2])
crit_max_min = array(['max', 'max', 'max', 'max'])
start = timeit.default_timer()
vikor(x, crit_max_min, w, 'n')
stop = timeit.default_timer()
print(stop - start)
s, r, q = vikor(x, crit_max_min, w, 'y')
print("S = ", s)
print("R = ", r)
print("Q = ", q)

