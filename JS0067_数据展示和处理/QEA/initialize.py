def init(population,m):
    Q = []
    for i in range(population):
        Q.append([])
    for i in range(population):
        for j in range(m):
            Q[i].append([1/2**0.5,1/2**0.5])
    return Q

