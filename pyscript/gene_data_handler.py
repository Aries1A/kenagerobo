import pandas as pd
import datetime

path = '../gene_data/'

def write_individuals(pop,filename,mode="a"):
    dt_now = datetime.datetime.now().strftime('%Y年%m月%d日%H:%M:%S')
    with open(path + filename, mode=mode) as f:
        f.write("{}${}".format(dt_now,str(pop)))
        f.write("\n")

def load_individuals(filename):
    df = pd.read_csv(path + filename, names=("TIME","POP"), sep="$")
    latest_individuals = df.iloc[-1]["POP"]
    latest_individuals = [[int(i) for i in [l.split(", ") for l in latest_individuals[1:-1].split("], [")][j]] for j in range(len([l.split(", ") for l in latest_individuals[1:-1].split("], [")]))]
    return latest_individuals

if __name__ == "__main__":
    indivisuals = "[1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],[1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],[1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]"
    write_individuals(pop=indivisuals,mode="w")
    load_individuals()
