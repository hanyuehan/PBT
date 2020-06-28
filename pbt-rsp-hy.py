#!/usr/bin/env python
import numpy as np
import random

update_n = 10
N = 50
steps = 10000
K = 32
group_n = 4
battle_n = 10000

class Worker():
    def __init__(self, idx, p):
        self.idx = idx
        self.p = p
        self.r = 0
        self.s = 0

    def maxS(self):
        r = self.p[0]
        s = self.p[1] - self.p[0]
        p = 1 - self.p[1]
        x = [r, s, p].index(max([r, s, p]))
        if x == 2:
            return 1
        elif x == 1:
            return 0
        else:
            return 2


def exploit(worker_i, worker_j):
    """copy params from the member in the population with the highest performance"""
    worker_i.p = worker_j.p
    # worker_i.r = worker_j.r


def explore(worker):
    """perturb parameters with noise from a normal distribution"""
    while (True):
        eps = [np.random.normal(0, 0.002), np.random.normal(0, 0.002)]
        list = np.array(eps) + np.array(worker.p)
        if ~(list[0] < 0 or list[1] > 1 or list[0] > list[1]):
            worker.p = list
            break


def battle(worker_i, worker_j):
    s_i = 0
    s_j = 0

    for i in range(battle_n):
        action = ["R", "S", "P"]
        if random.random() < 0.7:
            worker_i_strategy = random_pick(action, [worker_i.p[0], worker_i.p[1] - worker_i.p[0], 1 - worker_i.p[1]])
            worker_j_strategy = random_pick(action, [worker_j.p[0], worker_j.p[1] - worker_j.p[0], 1 - worker_j.p[1]])
        else:
            worker_i_strategy = action[worker_j.maxS()]
            worker_j_strategy = action[worker_i.maxS()]

        if worker_i_strategy == 'R' and worker_j_strategy == "S":
            s_i += 1
        if worker_i_strategy == 'R' and worker_j_strategy == "P":
            s_j += 1
        if worker_i_strategy == 'S' and worker_j_strategy == "P":
            s_i += 1
        if worker_i_strategy == 'S' and worker_j_strategy == "R":
            s_j += 1
        if worker_i_strategy == 'P' and worker_j_strategy == "R":
            s_i += 1
        if worker_i_strategy == 'P' and worker_j_strategy == "S":
            s_j += 1
        if worker_i_strategy == 'R' and worker_j_strategy == "R":
            s_i += 0
            s_j += 0

    worker_i.r += s_i
    worker_j.r += s_j

    # s_elo_i = 1 / (1 + 10 ** ((worker_j.r - worker_i.r) / 400))
    # s_elo_j = 1 / (1 + 10 ** ((worker_i.r - worker_j.r) / 400))
    # #print(s_elo_i, s_elo_j)
    # if s_i > s_j:
    #     worker_i.r += K * (1 - s_elo_i)
    #     worker_j.r -= K * (1 - s_elo_i)
    # else:
    #     worker_i.r -= K * (1 - s_elo_j)
    #     worker_j.r += K * (1 - s_elo_j)


def random_pick(some_list, probabilities):
    x = random.uniform(0, 1)
    cumulative_probability = 0.0
    for item, item_probability in zip(some_list, probabilities):
        cumulative_probability += item_probability
        if x < cumulative_probability:
            break
    return item


def random_P():
    x1 = random.random()
    x2 = random.uniform(x1, 1)
    return x1, x2

def normalize(list):
    return (list - np.min(list)) / (np.max(list) - np.min(list))

def run(population):
    for step in range(steps):
        for i in range(0, len(population)):
            population[i].r = 0
        # for i in range(0, len(population), group_n):
        #     for j in range(i, i + group_n):
        #         for x in range(j, i + group_n):
        #             battle(population[j], population[x])

        for i in range(0, len(population)):
            for j in range(i, len(population)):
                battle(population[i], population[j])

        population.sort(key=lambda x: x.r)
        print(step, population[-1].r, population[-1].p)

        for i in range(update_n):
            exploit(population[i], population[-i])
            explore(population[i])

def main():
    population = []
    #population.append(Worker(999, [1 / 3, 2 / 3]))

    # initialize N worker
    for i in range(N):
        p_i = random_P()
        print(i, p_i)
        population.append(Worker(i, p_i))

    run(population)
    population.sort(key=lambda x: x.r)

    for worker in population:
        print(worker.p, worker.r)

if __name__ == '__main__':
    main()






