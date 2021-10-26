import random
def oberserve_Q(Q,population,m):
    P = []
    for i in range(population):
        P.append([])
        for j in range(m):
            if random.uniform(0,1) < Q[i][j][1]*Q[i][j][1]:
                P[i].append(1)
            else:
                P[i].append(0)
    return P