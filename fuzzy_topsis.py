from numpy import *
import matplotlib.pyplot as plt
import timeit


def cal(a, b, k):
    f = []
    for i in range(len(b)):
        c = []
        for z in range(3):
            x = 0
            for j in range (k):
                x = x + a[b[i][j]][z]
            c.append(round(x / k, 3))
        f.append(c)
    return asarray(f)

def fndm(a, n, m):
    x = amax(a[:, 2:3])
    f = zeros((n * m, 3))
    for i in range(n * m):
        for j in range(3):
            f[i][j] = round(a[i][j] / x, 3)
    return f

def weighted_fndm(a, b, n, m):
    f = zeros((n * m, 3))
    z = 0
    for i in range(n * m):
        if i % len(b) == 0:
            z = 0
        else:
            z = z + 1
        for j in range(3):
            f[i][j] = round(a[i][j] * b[z][j], 3)
    return f


def distance(a, b):
    return sqrt(1/3 * ((a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2))


def func_dist_fpis(a, n, m):
    fpis = ones((3, 1))
    dist_pis = zeros(m)
    p = 0
    for i in range(m):
        for j in range(n):
            dist_pis[i] = dist_pis[i] + distance(a[p + j],fpis)
        p = p + n
    return dist_pis

def func_dist_fnis(a, n, m):
    fnis = zeros((3, 1))
    dist_nis = zeros(m)
    p = 0
    for i in range(m):
        for j in range(n):
            dist_nis[i] = dist_nis[i] + distance(a[p + j],fnis)
        p = p + n
    return dist_nis


def f_topsis(a, b, c, d, n, m, k, pl):
    # Steps 3 and 4
    fuzzy_weights = cal(a, b, k)
    fuzzy_decision_matrix = cal(c, d, k)
    fuzzy_norm_decision_matrix = fndm(fuzzy_decision_matrix,n, m)

    # Step 5
    weighted_fuzzy_norm_decision_matrix = weighted_fndm(fuzzy_norm_decision_matrix,fuzzy_weights, n, m)

    # Steps 6 and 7
    a_plus = func_dist_fpis(weighted_fuzzy_norm_decision_matrix, n, m)
    a_minus = func_dist_fnis(weighted_fuzzy_norm_decision_matrix, n, m)
    # Step 8
    CC = [] # closeness coefficient
    for i in range(m):
        CC.append(round(a_minus[i] / (a_plus[i] + a_minus[i]), 3))
    if pl == 'y':
        q = [i + 1 for i in range(m)]
        plt.plot(q, a_plus, 'p--', color = 'red',markeredgewidth = 2, markersize = 8)
        plt.plot(q, a_minus, '*--', color = 'blue',markeredgewidth = 2, markersize = 8)
        plt.plot(q, CC, 'o--', color = 'green',markeredgewidth = 2, markersize = 8)
        plt.title('Fuzzy TOPSIS results')
        plt.legend(['Distance from the ideal','Distance from the anti-ideal','Closeness coeficient'])
        plt.xticks(range(m + 2))
        plt.axis([0, m + 1, 0, 3])
        plt.xlabel('Alternatives')
        plt.legend()
        plt.grid(True)
        plt.show()
    return CC

m=6
n=4
k=3


cw = {'VL':[0, 0, 0.1], 'L':[0, 0.1, 0.3],'ML':[0.1, 0.3, 0.5], 'M':[0.3, 0.5, 0.7],'MH':[0.5, 0.7, 0.9], 'H':[0.7, 0.9, 1],'VH':[0.9, 1, 1]}
r = {'VP':[0, 0, 1], 'P':[0, 1, 3], 'MP':[1, 3, 5],'F':[3, 5, 7], 'MG':[5, 7, 9], 'G':[7, 9, 10],'VG':[9, 10, 10]}


cdw = [['H', 'VH', 'VH'], ['M', 'H', 'VH'],['M', 'MH', 'ML'], ['H', 'VH', 'MH']]
c1 = [['VG', 'G', 'MG'], ['F', 'MG', 'MG'],['P', 'P', 'MP'], ['G', 'VG', 'G']]
c2 = [['MP', 'F', 'F'], ['F', 'VG', 'G'],['MG', 'VG', 'G'], ['MG', 'F', 'MP']]
c3 = [['MG', 'MP', 'F'], ['MG', 'MG', 'VG'],['MP', 'F', 'F'], ['MP', 'P', 'P']]
c4 = [['MG', 'VG', 'VG'], ['G', 'G', 'VG'],['MG', 'VG', 'G'], ['VP', 'F', 'P']]
c5 = [['VP', 'P', 'G'], ['P', 'VP', 'MP'],['G', 'G', 'VG'], ['G', 'MG', 'MG']]
c6 = [['F', 'G', 'G'], ['F', 'MP', 'MG'],['VG', 'MG', 'F'], ['P', 'MP', 'F']]

all_ratings = vstack((c1, c2, c3, c4, c5, c6))

# final results
start = timeit.default_timer()
f_topsis(cw, cdw, r, all_ratings, n, m, k, 'n')
stop = timeit.default_timer()
print(stop - start)
print("Closeness coefficient = ",f_topsis(cw, cdw, r, all_ratings, n, m, k, 'y'))


























