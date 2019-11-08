import urllib.request, json
import time

def POST(name, data=""):
    url = "http://localhost:80"
    method = "POST"
    headers = {"Content-Type": "application/json"}
    requestJ = "{{\"Name\":\"{}\",\"Data\":\"{}\"}}".format(name,data)
    json_data = requestJ.encode("utf-8")

    request = urllib.request.Request(url, data=json_data, method=method, headers=headers)
    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode("utf-8")
    print(response_body)
    return response_body

if __name__ == "__main__":
    indivisuals = ""
    while(1):
        # 状態0 待機
        while(1):
            indivisuals = POST(name="get_indivisuals")
            if indivisuals != "0":
                print("start")
                break
            else:
                time.sleep(2)
        inds = [l.split(", ") for l in indivisuals[1:-1].split(",")]
        print(inds)
        #状態1 サーボ動作実行
        for ind in inds:
            #ここでサーボ動かす
            time.sleep(1.5)
            print(POST(name="calc_fit_val"))
        #状態2 次の世代がくるまで待機
        while(1):
            ind_index = POST(name="get_evalReady")
            print(ind_index)
            if ind_index == "0":
                print("pop changed")
                break
            else:
                time.sleep(2)
        if POST(name="get_isStop") == "1":
            print("GA finish")
            break
