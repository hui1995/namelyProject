import initialize
import observe
import evaluate
import update

t = 0  # 世代数
MAX_GEN = 100  # 循环次数


def main(instance):
    # print(instance)

    number = len(instance)  # 实例数

    # 数据处理
    for i in range(number):
        instance[i] = instance[i].replace('\n', '')
        instance[i] = instance[i].split(',')
        for j in range(len(instance[i])):
            instance[i][j] = eval(instance[i][j])
        tab.append(instance[i][len(instance[i]) - 1])
        del instance[i][len(instance[i]) - 1]

    # print(instance)
    # print(tab)

    m = len(instance[0])  # 特征数

    population = 20  # 种群大小 1,10

    Q = []  # 种群
    P = []  # 包含多个由01序列组成的解
    B = []  # 相对最优解
    Pf = []  # 适应度
    Bf = []  # 适应度
    b = []  # 最优特征
    bf = 0  # 最优特征的得分

    # 1.初始化Q(0)
    Q = initialize.init(population, m)
    # print(Q)

    # 2.从Q(0)中观测出P(0)
    P = observe.oberserve_Q(Q, population, m)
    # print(P)

    # 3.评估P(0)
    Pf = evaluate.evaluate_P(P, instance, tab, number, population, m)
    # print(Pf)

    # 4.将P(0)存储到B(0)
    B = P
    Bf = Pf
    # print(B)
    # print(Bf)

    while t < MAX_GEN:
        t = t + 1

        # 1.从Q(t-1)观测出P(t)
        P = observe.oberserve_Q(Q, population, m)
        # print(P)

        # 2.评估P(t)
        Pf = evaluate.evaluate_P(P, instance, tab, number, population, m)
        # print(Pf)

        # 3.更新Q(t)
        Q = update.update_Q(Q, B, P, Pf, Bf, population, m)
        # print(Q)

        # 4.将B(t-1)和P(t)中的最优解存入B(t)
        for i in range(population):
            if Pf[i] >= Bf[i]:
                B[i] = P[i]
                Bf[i] = Pf[i]
        # print(B)
        # print(Bf)

        # 5.从B(t)中记录最优解b
        bf = max(Bf)
        for i in range(population):
            if Bf[i] == bf:
                b = B[i]
                break
        # print(bf)
        # print(b)

        # 6.是否满足迁移条件 局部迁移、全局迁移
        # 全局迁移，迁移周期为1
        for i in range(population):
            B[i] = b
            Bf[i] = bf

    n = 0  # 选择的特征数
    for i in range(len(b)):
        if (b[i] == 1):
            n = n + 1
    result=[]
    result.append(f'特征数:{m}')
    result.append(f'世代数:{t}')
    result.append(f'特征选择最优解:{b}')
    result.append(f'已选择特征数:{n}')
    s = pow(bf, 1 / (1 + n ** 0.5))  # 分类精度
    result.append(f'适应度:{bf}')
    result.append(f'分类精度:{s}')

    return result

    # print(b)
