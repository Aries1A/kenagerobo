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
    return response_body

if __name__ == "__main__":
    individuals = ""
    while(1):
        while(1):
            indivisuals = POST(name="get_indivisuals")
            if indivisuals != "":
                print("start")
                break
            else:
                time.sleep(2)
        inds = [l.split(", ") for l in indivisuals[1:-1].split("], [")]
        for ind in inds:
            #ここでサーボ動かす
            time.sleep(4)
            print(POST(name="calc_fit_val"))
        while(1):
            ind_index = POST(name="get_evalReady")
            if ind_index == "0":
                print("pop changed")
                break
            else:
                time.sleep(2)
        if POST(name="get_isStop") == "0":
            print("GA finish")
            break
