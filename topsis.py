from numpy import *
import matplotlib.pyplot as plt
import timeit
def norm(x, y):
    if y == 'v':
        k = array(cumsum(x**2, 0))
        z = array([[round(x[i, j] / sqrt(k[x.shape[0] - 1, j]), 3) for j in range(x.shape[1])]for i in range(x.shape[0])])
        return z
    else:
        yy = []
        for i in range(x.shape[1]):
            yy.append(amax(x[:, i:i + 1]))
            k = array(yy)
        z = array([[round(x[i, j] / k[j], 3)for j in range(x.shape[1])]for i in range(x.shape[0])])
        return z
def mul_w(r, t):
    z = array([[round(t[i, j] * r[j], 3)for j in range(t.shape[1])]for i in range(t.shape[0])])
    return z
def zenith_nadir(x, y):
    if y == 'm':
        bb = []
        cc = []
        for i in range(x.shape[1]):
            bb.append(amax(x[:, i:i + 1]))
            b = array(bb)
            cc.append(amin(x[:, i:i + 1]))
            c = array(cc)
        return (b, c)
    else:
        b = ones(x.shape[1])
        c = zeros(x.shape[1])
        return (b, c)
def distance(x, y, z):
    a = array([[(x[i, j] - y[j])**2 for j in range(x.shape[1])]for i in range(x.shape[0])])
    b = array([[(x[i, j] - z[j])**2 for j in range(x.shape[1])]for i in range(x.shape[0])])
    return (sqrt(sum(a, 1)), sqrt(sum(b, 1)))
def topsis(matrix, weight, norm_m, id_sol, pl):
    z = mul_w(weight, norm(matrix, norm_m))
    s, f = zenith_nadir(z, id_sol)
    p, n = distance(z, s, f)
    final_s = array([n[i] / (p[i] + n[i])for i in range(p.shape[0])])
    if pl == 'y':
        q = [i + 1 for i in range(matrix.shape[0])]
        plt.plot(q, p, 'p--', color = 'red',markeredgewidth = 2, markersize = 8)
        
        plt.plot(q, n, '*--', color = 'blue',markeredgewidth = 2, markersize = 8)
        plt.plot(q, final_s, 'o--', color = 'green',markeredgewidth = 2, markersize = 8)
        plt.title('TOPSIS results')
        plt.legend(['Distance from the ideal','Distance from the anti-ideal','Closeness coefficient'])
        plt.xticks(range(matrix.shape[0] + 2))
        plt.axis([0, matrix.shape[0] + 1, 0, 3])
        plt.xlabel('Alternatives')
        plt.legend()
        plt.grid(True)
        plt.show()
    return final_s
x = array([[8, 7, 2, 1], [5, 3, 7, 5], [7, 5, 6, 4],[9, 9, 7, 3], [11, 10, 3, 7], [6, 9, 5, 4]])
w = array([0.4, 0.3, 0.1, 0.2])
start = timeit.default_timer()
topsis(x, w, 'v', 'm', 'n')
stop = timeit.default_timer()
print("time = ", stop - start)
print("Closeness coefficient = ",topsis(x, w, 'v', 'm', 'y'))

