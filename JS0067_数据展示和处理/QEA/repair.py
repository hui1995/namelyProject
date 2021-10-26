import random
def repair_P(P,weight,population,m,C):
    new_P = [] #修复后的P
    sum = 0
    w = []  #各个个体的重量
    knapsack_overfilled = False
    for i in range(population):
        for j in range(m):
            sum = sum + P[i][j]*weight[j]
        w.append(sum)
        sum = 0
    #print(w)
    for i in range(population):
        if w[i] > C:
            knapsack_overfilled = True

        while knapsack_overfilled:
            P[i][random.randint(0,m-1)] = 0
            for j in range(m):
                sum = sum + P[i][j]*weight[j]
            if sum <=C:
                knapsack_overfilled = False
            sum = 0

        while not knapsack_overfilled:
            n = random.randint(0, m - 1)
            P[i][n] = 1
            for j in range(m):
                sum = sum + P[i][j] * weight[j]
            if sum > C:
                knapsack_overfilled = True
                P[i][n] = 0
            sum = 0
    new_P = P
    return  new_P