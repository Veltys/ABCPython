__author__ = "Omur Sahin"

import sys

from deap.benchmarks import random
import progressbar

import numpy as np


class ABC:

    def __init__(self, conf):
        self.conf = conf
        self.foods = np.zeros((self.conf.FOOD_NUMBER, self.conf.DIMENSION))
        self.f = np.ones((self.conf.FOOD_NUMBER))
        self.fitness = np.ones((self.conf.FOOD_NUMBER)) * np.iinfo(int).max
        self.trial = np.zeros((self.conf.FOOD_NUMBER))
        self.prob = [0 for _ in range(self.conf.FOOD_NUMBER)]
        self.solution = np.zeros((self.conf.DIMENSION))
        self.globalParams = [0 for _ in range(self.conf.DIMENSION)]
        self.globalTime = 0
        self.evalCount = 0
        self.cycle = 0
        self.experimentID = 0
        self.globalOpts = list()

        if (self.conf.SHOW_PROGRESS):
            self.progressbar = progressbar.ProgressBar(max_value=self.conf.MAXIMUM_EVALUATION)
        if (not(conf.RANDOM_SEED)):
            random.seed(conf.SEED)

    def calculate_function(self, sol):
        try:
            if (self.conf.SHOW_PROGRESS):
                self.progressbar.update(self.evalCount)

            return self.conf.OBJECTIVE_FUNCTION(sol)

        except ValueError as err:
            print(
                "An exception occured: Upper and Lower Bounds might be wrong. (" + str(err) + " in calculate_function)")
            sys.exit()

    def calculate_fitness(self, fun):
        self.increase_eval()
        if fun >= 0:
            result = 1 / (fun + 1)
        else:
            result = 1 + abs(fun)
        return result

    def increase_eval(self):
        self.evalCount += 1

    def stopping_condition(self):
        status = bool(self.evalCount >= self.conf.MAXIMUM_EVALUATION)
        if(self.conf.SHOW_PROGRESS):
            if(status == True and not( self.progressbar._finished )):
                self.progressbar.finish()
        return status

    def memorize_best_source(self):
        for i in range(self.conf.FOOD_NUMBER):
            if (self.f[i] < self.globalOpt and self.conf.MINIMIZE == True) or (self.f[i] >= self.globalOpt and self.conf.MINIMIZE == False):
                self.globalOpt = np.copy(self.f[i])
                self.globalParams = np.copy(self.foods[i][:])

    def init(self, index):
        if (not (self.stopping_condition())):
            for i in range(self.conf.DIMENSION):
                self.foods[index][i] = random.random() * (self.conf.UPPER_BOUND - self.conf.LOWER_BOUND) + self.conf.LOWER_BOUND
            self.solution = np.copy(self.foods[index][:])
            self.f[index] = self.calculate_function(self.solution)[0]
            self.fitness[index] = self.calculate_fitness(self.f[index])
            self.trial[index] = 0

    def initial(self):
        for i in range(self.conf.FOOD_NUMBER):
            self.init(i)
        self.globalOpt = np.copy(self.f[0])
        self.globalParams = np.copy(self.foods[0][:])

    def send_employed_bees(self):
        i = 0
        while (i < self.conf.FOOD_NUMBER) and (not (self.stopping_condition())):
            r = random.random()
            self.param2change = (int)(r * self.conf.DIMENSION)

            r = random.random()
            self.neighbour = (int)(r * self.conf.FOOD_NUMBER)
            while self.neighbour == i:
                r = random.random()
                self.neighbour = (int)(r * self.conf.FOOD_NUMBER)
            self.solution = np.copy(self.foods[i][:])

            r = random.random()
            self.solution[self.param2change] = self.foods[i][self.param2change] + (
                        self.foods[i][self.param2change] - self.foods[self.neighbour][self.param2change]) * (
                                                             r - 0.5) * 2

            if self.solution[self.param2change] < self.conf.LOWER_BOUND:
                self.solution[self.param2change] = self.conf.LOWER_BOUND
            if self.solution[self.param2change] > self.conf.UPPER_BOUND:
                self.solution[self.param2change] = self.conf.UPPER_BOUND
            self.ObjValSol = self.calculate_function(self.solution)[0]
            self.FitnessSol = self.calculate_fitness(self.ObjValSol)
            if (self.FitnessSol > self.fitness[i] and self.conf.MINIMIZE == True) or (self.FitnessSol <= self.fitness[i] and self.conf.MINIMIZE == False):
                self.trial[i] = 0
                self.foods[i][:] = np.copy(self.solution)
                self.f[i] = self.ObjValSol
                self.fitness[i] = self.FitnessSol
            else:
                self.trial[i] = self.trial[i] + 1
            i += 1

    def calculate_probabilities(self):
        maxfit = np.copy(max(self.fitness))
        for i in range(self.conf.FOOD_NUMBER):
            self.prob[i] = (0.9 * (self.fitness[i] / maxfit)) + 0.1

    def send_onlooker_bees(self):
        i = 0
        t = 0
        while (t < self.conf.FOOD_NUMBER) and (not (self.stopping_condition())):
            r = random.random()
            if ((r < self.prob[i] and self.conf.MINIMIZE == True) or (r > self.prob[i] and self.conf.MINIMIZE == False)):
                t+=1
                r = random.random()
                self.param2change = (int)(r * self.conf.DIMENSION)
                r = random.random()
                self.neighbour = (int)(r * self.conf.FOOD_NUMBER)
                while self.neighbour == i:
                    r = random.random()
                    self.neighbour = (int)(r * self.conf.FOOD_NUMBER)
                self.solution = np.copy(self.foods[i][:])

                r = random.random()
                self.solution[self.param2change] = self.foods[i][self.param2change] + (
                            self.foods[i][self.param2change] - self.foods[self.neighbour][self.param2change]) * (
                                                                 r - 0.5) * 2
                if self.solution[self.param2change] < self.conf.LOWER_BOUND:
                    self.solution[self.param2change] = self.conf.LOWER_BOUND
                if self.solution[self.param2change] > self.conf.UPPER_BOUND:
                    self.solution[self.param2change] = self.conf.UPPER_BOUND

                self.ObjValSol = self.calculate_function(self.solution)[0]
                self.FitnessSol = self.calculate_fitness(self.ObjValSol)
                if (self.FitnessSol > self.fitness[i] and self.conf.MINIMIZE == True) or (self.FitnessSol <= self.fitness[i] and self.conf.MINIMIZE == False):
                    self.trial[i] = 0
                    self.foods[i][:] = np.copy(self.solution)
                    self.f[i] = self.ObjValSol
                    self.fitness[i] = self.FitnessSol
                else:
                    self.trial[i] = self.trial[i] + 1
            i += 1
            i = i % self.conf.FOOD_NUMBER

    def send_scout_bees(self):
        if np.amax(self.trial) >= self.conf.LIMIT:
            self.init(self.trial.argmax(axis = 0))

    def increase_cycle(self):
        self.globalOpts.append(self.globalOpt)
        self.cycle += 1
    def setExperimentID(self,run,t):
        self.experimentID = t + "-" + str(run)
