# -*- coding: utf-8 -*-
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import threading

action = 0
QStep = 0
espStep = 0
episodeStart = 0
goHome = 0
moving = 0
angle = 0

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
        print(self)
        global action, QStep, espStep,episodeStart,goHome,moving,angle
        # 受け取ったデータ
        content_len = int(self.headers.get('content-length'))
        requestBody = self.rfile.read(content_len).decode('ascii')
        print("received: " + requestBody)
        requestJson = json.loads(requestBody)

        # Nameに従った処理
        #esp32
        # 次に行うactionを取得
        if requestJson["Name"] == "get_action_step":
            body_raw = str(action) + "," + str(QStep)
            body =  body_raw.encode('utf-8')
        # episodeの準備状態を取得
        elif requestJson["Name"] == "get_episodeStart":
            body = str(episodeStart).encode("utf-8")
        # 動作終了報告
        elif requestJson["Name"] == "set_espStep":
            espStep = int(requestJson["Data"])
            body = b"espStep set"
        # angle送信
        elif requestJson["Name"] == "set_angle":
            angle = int(requestJson["Data"])
            body = b"angle set"

        # Q.py
        # episodeの準備状態を送信
        elif requestJson["Name"] == "set_episodeStart":
            episodeStart = requestJson["Data"]
            if episodeStart == "0":
                body = b"episode not ready."
            else:
                body = b"episode ready."
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
            action = 0
            episodeStart = 0
            body = b"reset observation"
        elif requestJson["Name"] == "send_calib":
            with open("../../MPUcalib/calib_data/11_5.csv","a") as f:
                f.write(requestJson["Data"])
                f.write("\n")
            body = b"get calib_data"
        # goHome状態を送信
        elif requestJson["Name"] == "set_goHome":
            goHome = requestJson["Data"]
            if goHome == "0":
                body = b"not goHome."
            else:
                body = b"goHome."
        #巻き取り機が動いているか取得
        elif requestJson["Name"] == "get_moving":
            body = str(moving).encode("utf-8")
        #angle取得
        elif requestJson["Name"] == "get_angle":
            body = str(angle).encode("utf-8")


        # 巻き取り機
        elif requestJson["Name"] == "get_goHome":
            body = str(goHome).encode("utf-8")
        elif requestJson["Name"] == "set_moving":
            moving = requestJson["Data"]
            if moving == "0":
                body = b"not moving."
            else:
                body = b"moving."

        else:
            body = b"not match any request"
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Content-length', len(body))
        self.end_headers()
        self.wfile.write(body)
        print("response: {}".format(body))


def set_server():
    server = HTTPServer(('', 90), Client)
    thread = threading.Thread(target = server.serve_forever)
    thread.daemon = True
    thread.start()

if __name__ == "__main__":
    with HTTPServer(('', 80), Client) as server:
        server.serve_forever()
