#coding=gbk

from FeatureSelectionGA.fitness_function import FitnessFunction
import random
from deap import base, creator, tools
import numpy as np


class FeatureSelectionGA:
    global acc
    acc = 0

    def __init__(self, x, y, verbose=1, ff_obj=None):
        self.n_features = x.shape[1]
        self.toolbox = None
        self.creator = self._create()
        self.x = x
        self.y = y
        self.verbose = verbose
        if self.verbose == 1:
            print("Shape of train_x:{} and target:{}".format(x.shape, y.shape))
        self.final_fitness = []
        self.fitness_in_generation = {}
        self.best_ind = None
        if ff_obj == None:
            self.fitness_function = FitnessFunction()  # 初始化一个对象的意思
        else:
            self.fitness_function = ff_obj

    def evaluate(self, individual):
        fitness = 0.0
        fit_obj = self.fitness_function
        np_ind = np.asarray(individual)
        if np.sum(np_ind != 0):
            feature_idx = np.where(np_ind == 1)[0]  # 找到n维数组中特定数值的索引 [0]表示行索引
            fitness = fit_obj.calculate_fitness(self.x[:, feature_idx], self.y)
            if self.verbose == 1:
                print("Individual:{} Fitness_score:{}".format(individual, fitness))
        return (fitness,)

    def _create(self):
        creator.create("FeatureSelect", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FeatureSelect)
        return creator

    def create_toolbox(self):
        self._init_toolbox()
        return self.toolbox

    def register_toolbox(self, toolbox):
        toolbox.register("evaluate", self.evaluate)
        self.toolbox = toolbox

    def _init_toolbox(self):
        toolbox = base.Toolbox()
        toolbox.register("attr_bool", random.randint, 0, 1)
        # Structure initializers
        toolbox.register(
            "individual",
            tools.initRepeat,
            creator.Individual,
            toolbox.attr_bool,
            self.n_features,
        )
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        return toolbox

    def _default_toolbox(self):
        toolbox = self._init_toolbox()
        toolbox.register("mate", tools.cxTwoPoint)  # 执行两个点的交叉  两点交叉
        toolbox.register("mutate", tools.mutFlipBit, indpb=0.1)  # 突变
        toolbox.register("select", tools.selTournament, tournsize=3)  # 选择 选择适应度值最大的个体
        toolbox.register("evaluate", self.evaluate)
        return toolbox

    def get_final_scores(self, pop, fits):
        self.final_fitness = list(zip(pop, fits))

    def generate(self, n_pop, cxpb, mutxpb, ngen, set_toolbox=False):
        """
        Generate evolved population
        Parameters
        -----------
            n_pop : {int}
                    population size
            cxpb  : {float}
                    crossover probablity
            mutxpb: {float}
                    mutation probablity
            n_gen : {int}
                    number of generations
            set_toolbox : {boolean}
                          If True then you have to create custom toolbox before calling
                          method. If False use default toolbox.
        Returns
        --------
            Fittest population
        """
        if self.verbose == 1:
            print("Population: {}, crossover_probablity: {}, mutation_probablity: {}, total generations: {}"
                  .format(n_pop, cxpb, mutxpb, ngen))
        if not set_toolbox:
            self.toolbox = self._default_toolbox()
        else:
            raise Exception(
                "Please create a toolbox.Use create_toolbox to create and register_toolbox to register. Else set set_toolbox = False to use defualt toolbox")
        pop = self.toolbox.population(n_pop)
        CXPB, MUTPB, NGEN = cxpb, mutxpb, ngen

        # Evaluate the entire population
        print("EVOLVING.......")
        fitnesses = list(map(self.toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit

        for g in range(NGEN):
            print("--GENERATION{}--".format(g + 1))
            offspring = self.toolbox.select(pop, len(pop))
            self.fitness_in_generation[str(g + 1)] = max([ind.fitness.values[0] for ind in pop])
            # Clone the selected individuals
            offspring = list(map(self.toolbox.clone, offspring))

            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < CXPB:
                    self.toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values

            for mut in offspring:
                if random.random() < MUTPB:
                    self.toolbox.mutate(mut)
                    del mut.fitness.values

            # 评估没有适应度值的个体
            weak_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = list(map(self.toolbox.evaluate, weak_ind))
            for ind, fit in zip(weak_ind, fitnesses):
                ind.fitness.values = fit

            pop[:] = offspring

        fits = [ind.fitness.values[0] for ind in pop]

        print("--Only the fittest survives --")
        self.best_ind = tools.selBest(pop,1)[0]
        print("best individual is %s" % self.best_ind)
        self.get_final_scores(pop, fits)

        return self.best_ind
