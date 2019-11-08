import pandas as pd
import datetime

path = '../gene_data/'

#書き込み
def write_indivisuals(pop,filename,mode="a"):
    dt_now = datetime.datetime.now().strftime('%Y年%m月%d日%H:%M:%S')
    with open(path + filename, mode=mode) as f:
        f.write("{}${}".format(dt_now,str(pop)))
        f.write("\n")
#読み込み
def load_indivisuals(filename):
    df = pd.read_csv(path + filename, names=("TIME","POP"), sep="$")
    latest_indivisuals = df.iloc[-1]["POP"][1:-1]
    latest_indivisuals = [[int(i) for i in [l.split(", ") for l in latest_indivisuals[1:-1].split("], [")][j]] for j in range(len([l.split(", ") for l in latest_indivisuals[1:-1].split("], [")]))]
    return latest_indivisuals
#esp32用にindivisualsをエンコード
def get_esp_indivisuals(indivisuals):
    genes = [''.join(ind.split(', ')) for ind in indivisuals[1:-1].split('], [')]
    genes_s = ','.join(genes)
    return genes_s.encode("UTF-8")


if __name__ == "__main__":
    indivisuals = "[1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]"
    # write_indivisuals(pop=indivisuals,mode="w")
    load_indivisuals("ga_test2.csv")
    df = pd.read_csv("../gene_data/ga_test2.csv", names=("TIME","POP"), sep="$")
    df
    latest_indivisuals = df.iloc[-1]["POP"][1:-1]
    latest_indivisuals
    latest_indivisuals = [[int(i) for i in [l.split(", ") for l in latest_indivisuals[1:-1].split("], [")][j]] for j in range(len([l.split(", ") for l in latest_indivisuals[1:-1].split("], [")]))]


    genes = [''.join(ind.split(', ')) for ind in indivisuals[1:-1].split('], [')]
    genes_s = ','.join(genes)
    genes_s
