from numpy import *
import matplotlib.pyplot as plt
import timeit


def agg_fuzzy_value(a, b, k):
    f = zeros((len(b), 4))
    for j in range(len(b)):
        k0 = a[b[j][0]][0]
        k1 = 0
        k2 = 0
        k3 = a[b[j][0]][3]
        for i in range (len(b[1])):
            if k0 > a[b[j][i]][0]:
                k0 = a[b[j][i]][0]
        k1 = k1 + a[b[j][i]][1]
        k2 = k2 + a[b[j][i]][2]
        if k3 < a[b[j][i]][3]:
            k3 = a[b[j][i]][3]
        f[j][0] = round(k0, 3)
        f[j][1] = round(k1 / k, 3)
        f[j][2] = round(k2 / k, 3)
        f[j][3] = round(k3, 3)
    return f


def defuzz(a):
    return (-a[0] * a[1] + a[2] * a[3] + 1 / 3 * (a[3] - a[2])**2 - 1 / 3 * (a[1] - a[0])**2) / (-a[0] - a[1] + a[2] + a[3])

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
            u = c[j] * (b[j, 0] - a[i, j])/ (b[j, 0] - b[j, 1])
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



def f_vikor(a, b, c, d, e, n, m, k, pl):
    w = agg_fuzzy_value(a, b, k)
    f_rdm_all = agg_fuzzy_value(c, d, k)
    crisp_weights = zeros(n)
    for i in range(n):
        crisp_weights[i] = round(defuzz(w[i]), 3)
    crisp_alternative_ratings = zeros((m, n))
    k = 0
    for i in range(n):
        for j in range(m):
            crisp_alternative_ratings[j][i] = round(defuzz(f_rdm_all[k]), 3)
            k = k + 1
    s, r = SR(crisp_alternative_ratings,best_worst_fij(crisp_alternative_ratings, e),crisp_weights)
    q = Q(s, r, len(w))
    if pl == 'y':
        h = [i + 1 for i in range(m)]
        plt.plot(h, s, 'p--', color = 'red',markeredgewidth = 2, markersize=8)
        plt.plot(h, r, '*--', color = 'blue',markeredgewidth = 2, markersize = 8)
        plt.plot(h, q, 'o--', color = 'green',markeredgewidth = 2, markersize = 8)
        plt.legend(['S', 'R', 'Q'])
        plt.xticks(range(m + 2))
        plt.axis([0, m + 1, 0,max(maximum(maximum(s, r), q)) + 1])
        plt.title("Fuzzy VIKOR results")
        plt.xlabel("Alternatives")
        plt.legend()
        plt.grid(True)
        plt.show()
    return s, r, q

m=6
n=4
k=3

cw = {'VL':[0, 0, 0.1, 0.2], 'L':[0.1, 0.2, 0.2, 0.3],'ML':[0.2, 0.3, 0.4, 0.5], 'M':[0.4, 0.5, 0.5, 0.6],'MH':[0.5, 0.6, 0.7, 0.8], 'H':[0.7, 0.8, 0.8, 0.9],'VH':[0.8, 0.9, 1, 1]}

r = {'VP':[0.0, 0.0, 0.1, 0.2], 'P':[0.1, 0.2, 0.2, 0.3],'MP':[ 0.2, 0.3, 0.4, 0.5], 'F':[0.4, 0.5, 0.5, 0.6],'MG':[0.5, 0.6, 0.7, 0.8], 'G':[0.7, 0.8, 0.8, 0.9],'VG':[0.8, 0.9, 1.0, 1.0]}

cdw = [['H', 'VH', 'VH'], ['M', 'H', 'VH'],['M', 'MH', 'ML'], ['H', 'VH', 'MH']]

c1 = [['VG', 'G', 'MG'], ['F', 'MG', 'MG'],['P', 'P', 'MP'], ['G', 'VG', 'G']]
c2 = [['MP', 'F', 'F'], ['F', 'VG', 'G'],['MG', 'VG', 'G'], ['MG', 'F', 'MP']]
c3 = [['MG', 'MP', 'F'], ['MG', 'MG', 'VG'],['MP', 'F', 'F'], ['MP', 'P', 'P']]
c4 = [['MG', 'VG', 'VG'], ['G', 'G', 'VG'],['MG', 'VG', 'G'], ['VP', 'F', 'P']]
c5 = [['VP', 'P', 'G'], ['P', 'VP', 'MP'],['G', 'G', 'VG'], ['G', 'MG', 'MG']]
c6 = [['F', 'G', 'G'], ['F', 'MP', 'MG'],['VG', 'MG', 'F'], ['P', 'MP', 'F']]

all_ratings = vstack((c1, c2, c3, c4, c5, c6))

crit_max_min = array(['max', 'max', 'max', 'max'])

start = timeit.default_timer()

f_vikor(cw, cdw, r, all_ratings, crit_max_min, n, m,k, 'n')
stop = timeit.default_timer()
print(stop - start)
s, r, q = f_vikor(cw, cdw, r, all_ratings,crit_max_min, n, m, k, 'y')
print("S = ", s)
print("R = ", r)
print("Q = ", q)
































