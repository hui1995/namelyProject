import math
def update_Q(Q,B,P,Pf,Bf,population,m):
    new_Q = []
    angle = 0
    for i in range(population):
        for j in range(m):
            a = 0
            b = 0
            if P[i][j] == 0 and B[i][j] == 1 and Pf[i] < Bf[i]:
                angle = 0.01 * math.pi
            elif P[i][j] == 1 and B[i][j] == 0 and Pf[i] < Bf[i]:
                angle = -0.01 * math.pi
            else:
                angle = 0
            #位于第一三象限
            if (Q[i][j][0] > 0 and Q[i][j][1] > 0) or (Q[i][j][0] < 0 and Q[i][j][1] < 0):
                a = Q[i][j][0] * math.cos(angle) - Q[i][j][1] * math.sin(angle)
                b = Q[i][j][0] * math.sin(angle) + Q[i][j][1] * math.cos(angle)
            #位于第二四象限
            else:
                a = Q[i][j][0] * math.cos(-angle) - Q[i][j][1] * math.sin(-angle)
                b = Q[i][j][0] * math.sin(-angle) + Q[i][j][1] * math.cos(-angle)
            Q[i][j][0] = a
            Q[i][j][1] = b
    new_Q = Q
    return new_Q