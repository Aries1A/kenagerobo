import random
import time
from deap import base
from deap import creator
from deap import tools
from request_handler import POST
from gene_data_handler import write_individuals, load_individuals
import sys

#交叉率、個体突然変異率、ループを回す世代数,一世代の個体数,遺伝子の長さ
CXPB, MUTPB, NGEN,NIND,LGENE = 0.5, 0.2, 10, 8, 16

creator.create("FitnessMax", base.Fitness, weights=(1.0,)) #目的関数を最大化
creator.create("Individual", list, fitness=creator.FitnessMax) #適応度fitnessのメンバ変数を追加

toolbox = base.Toolbox()

toolbox.register("attr_bool", random.randint, 0, 1) #遺伝子を作成する関数、attr_boolはデフォルトでランダムに0,1を返す関数
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, LGENE) #LGENE回toolbox.attr_boolを実行し、その値をcreator.Individualに格納して返す関数individualを作成
toolbox.register("population", tools.initRepeat, list, toolbox.individual) #個体をtoolbox.individualで作成してlistに格納し、世代を生成するpopulation関数を作成



def evalOneMax(individual): #評価関数
    #進んだ距離(fit_val)計算
    #arduinoからの動作完了待ち
    print("waiting calc.",end="")
    while(1):
        fit_val = POST(name="get_fit_val")
        if fit_val != "":
            break
        print(".")
        time.sleep(1)
    print("\n{}: {}".format(str(individual),fit_val))
    return int(fit_val),

toolbox.register("evaluate", evalOneMax) #評価関数
toolbox.register("mate", tools.cxTwoPoint) #交叉
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05) #突然変異関数、5%
toolbox.register("select", tools.selTournament, tournsize=3) #選択関数


def main(mode,filename):
    random.seed(64)

    #学習を途中から開始するモード
    if mode == "L":
        try:
            pop = load_individuals(filename) #既存の世代をロード
            pop = [creator.Individual(l) for l in pop] #Individual型に変更
        except FileNotFoundError:
            pop = toolbox.population(n=NIND) #初期世代を作成
    #新しく学習を開始するモード
    elif mode == "N":
        pop = toolbox.population(n=NIND) #初期世代を作成
        write_individuals(pop=pop,filename=filename)

    else:
        exit(1)
    print(POST(name = "set_indivisuals",data=str(pop)[1:-1]))

    print("Start of evolution")

    fitnesses = list(map(toolbox.evaluate, pop)) #初期世代をここで評価
    for ind, fit in zip(pop, fitnesses): # 初期世代の各個体の適応度を記録
        ind.fitness.values = fit

    print("  Evaluated %i individuals" % len(pop))

    for g in range(NGEN):
        print("-- Generation %i --" % g)

        offspring = toolbox.select(pop, len(pop)) #適応度を元に次世代の親となる子孫選択
        offspring = list(map(toolbox.clone, offspring))

        for child1, child2 in zip(offspring[::2], offspring[1::2]):

            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:

            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        print(POST(name="set_indivisuals",data=str(invalid_ind)[1:-1]))

        fitnesses = map(toolbox.evaluate, invalid_ind) #再評価
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        print("  Evaluated %i individuals" % len(invalid_ind))

        pop[:] = offspring

        # 最新の世代を保存
        write_individuals(pop=pop,filename=filename)

        fits = [ind.fitness.values[0] for ind in pop]

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5

        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)

    print("-- End of (successful) evolution --")

    best_ind = tools.selBest(pop, 1)[0]
    print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))
    POST(name="complete")

if __name__ == "__main__":
    args = sys.argv
    main(args[1],args[2])
