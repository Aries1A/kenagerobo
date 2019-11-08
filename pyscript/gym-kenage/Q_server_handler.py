# -*- coding: utf-8 -*-
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import threading

action = -1
QStep = -1
espStep = 0

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
        global action, QStep, espStep
        # 受け取ったデータ
        content_len = int(self.headers.get('content-length'))
        requestBody = self.rfile.read(content_len).decode('ascii')
        print("received: " + requestBody)
        requestJson = json.loads(requestBody)

        # Nameに従った処理
        #esp32
        # 次に行うactionを取得
        if requestJson["Name"] == "get_action_step":
            try:
                body_raw = str(action) + "," + str(QStep)
                body =  body_raw.encode('utf-8')
            except:
                body = b"-1,-1"
        # 動作終了報告
        elif requestJson["Name"] == "set_espStep":
            espStep = int(requestJson["Data"])
            body = b"espStep set"

        # Q.py
        # 現在のactionをサーバーに記録

        elif requestJson["Name"] == "set_action":
            action = int(requestJson["Data"])
            body = b"action set"
        # 現在のQのstepをサーバーに記録
        elif requestJson["Name"] == "set_QStep":
            QStep = int(requestJson["Data"])
            body = "QStep set : {}".format(QStep)
            body = body.encode("utf-8")
        # esp側のstepを取得
        elif requestJson["Name"] == "get_espStep":
            body = str(espStep).encode('utf-8')
        # 初期化
        elif requestJson["Name"] == "_reset":
            QStep = 0
            espStep = 0
            action = -1
            body = b"reset observation"
        elif requestJson["Name"] == "send_calib":
            with open("../../MPUcalib/calib_data/11_5.csv","a") as f:
                f.write(requestJson["Data"])
                f.write("\n")
            body = b"get calib_data"
        else:
            body = b"not match any request"
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
