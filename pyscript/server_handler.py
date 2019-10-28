import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import threading
from calc_fitness import calc_fitness

class Client(BaseHTTPRequestHandler):
    """
    受け取るデータはjson型(例：{"Name":"get_indivisuals"})
    Nameの値が、
    - get_indivisuals: esp32にindivisualsを送る
    - set_indivisuals: global変数indivisualsをrequestBodyに更新
    - calc_fit_val: esp32から動作完了の信号を受け取ってカメラから進んだ距離を計算してfit_valに格納する。格納が完了したらesp32にresponseを返す
    - get_fit_val: kenage_ga.pyにfit_valを送る

    """
    def do_POST(self):
        global indivisuals, fit_vals, ind_index, isStop
        # 受け取ったデータ
        content_len = int(self.headers.get('content-length'))
        requestBody = self.rfile.read(content_len).decode('ascii')
        print("received: " + requestBody)
        requestJson = json.loads(requestBody)

        # Nameに従った処理
        #esp32
        #今の世代のpopulationを取得
        if requestJson["Name"] == "get_indivisuals":
            try:
                body = indivisuals.encode("UTF-8")
            except:
                body = b""
        #動作実行後に進んだ距離の計算を開始する信号を送る
        elif requestJson["Name"] == "calc_fit_val":
            print(indivisuals,ind_index)
            ind = [int(i) for i in [l.split(", ") for l in indivisuals[1:-1].split("], [")][ind_index]]
            fit_vals = str(calc_fitness(ind))
            ind_index += 1
            body = b"finish calc"
        #世代の中の全ての個体で動作を完了した後に次の世代まで進んでいいか否かを取得
        elif requestJson["Name"] == "get_evalReady":
            try:
                body = str(ind_index).encode("utf-8")
            except:
                body = b"0"
        #学習終了かどうか取得
        elif requestJson["Name"] == "get_isStop":
            body = str(isStop).encode("utf-8")
        # GA.py
        #今の世代のpopulationを更新
        elif requestJson["Name"] == "set_indivisuals":
            indivisuals = requestJson["Data"]
            fit_vals = ""
            ind_index = 0
            isStop = 1
            body = b"changed"
        #適応度を取得
        elif requestJson["Name"] == "get_fit_val":
            body = fit_vals.encode("UTF-8")
            fit_vals = ""
        #終了
        elif requestJson["Name"] == "complete":
            ind_index = 0
            isStop = 0
        else:
            body = b"Name does not match any key"

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Content-length', len(body))
        self.end_headers()
        self.wfile.write(body)


def set_server():
    server = HTTPServer(('', 90), Client)
    thread = threading.Thread(target = server.serve_forever)
    thread.daemon = True
    thread.start()

if __name__ == "__main__":
    with HTTPServer(('', 80), Client) as server:
        server.serve_forever()
