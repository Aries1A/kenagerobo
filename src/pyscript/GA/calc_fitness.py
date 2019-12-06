import random
from get_progress import get_progress

def calc_fitness(ind):
    fitness = sum(ind)
    position = get_progress()
    return fitness

if __name__ == "__main__":
    calc_fitness()
