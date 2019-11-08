import sys

import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
from get_position import get_position,get_angle
from Q_request_handler import POST # なぜかgym_kenageに置かないとerror吐く
import time


class KenageEnv(gym.Env):
    metadata = {'render.modes':['human']}
    #フィールドの大きさ
    size_x = 180
    size_y = 180

    def __init__(self):
        super().__init__()
        # action_space, observation_space, reward_range を設定する
        self.action_space = gym.spaces.Discrete(12) #行動は12通り
        self.observation_space = spaces.Dict({ # 状態空間は(x,y,angle)
            "pos_x": spaces.Box(low = 0, high = self.size_x, shape=(1,)),
            "pos_y": spaces.Box(low = 0, high = self.size_y, shape=(1,)),
            "robo_angle": spaces.Box(low=0, high=360, shape=(1, ))
            })
        self.reward_range = [-10,100.] #報酬の範囲
        self._reset()

    def _reset(self): #状態を初期化、初期の観測値を返す
        #初期位置を取得
        self._find_pos()
        #初期向きを取得
        self._find_angle()
        self.done = False
        self.step = 0
        POST(name="_reset")
        return self._observe()

    def _step(self, action): #actionを実行、結果を返す
        while(1):
            response = int(POST(name="get_espStep"))
            if response != self.step + 1:
                print("waiting esp....")
                print("get espStep is {}".format(response))
                time.sleep(0.3)
            else:
                print("esp step done")
                break
        observation = self._observe()
        reward = self._reward()
        self.done = self._is_done()
        self.step += 1
        return observation, reward, self.done, {}

    def _observe(self):
        #ここで位置と角度を測定
        self._find_pos()
        self._find_angle()
        observation = {"pos_x":self.pos_x,
                        "pos_y":self.pos_y,
                        "robo_angle":self.robo_angle}
        return observation

    def _close(self): #環境を閉じて後処理
        pass
    def _seed(self, seed=None): #ランダムシードを固定
        pass
    def _reward(self):
        # ゴールに到達
        if self._is_goal():
            return 100
        #
        elif not self._is_movable():
            return -5
        else:
            return -1
    def _is_goal(self):

        pass

    def _is_movable(self):
        pass

    def _is_done(self):
        pass

    def _render(self, mode='human'):
        outfile = sys.stdout
        outfile.write(str(self._observe())+"\n")

    def _find_pos(self):
        #Webカメラで位置を測る
        self.pos_x,self.pos_y = get_position()
    def _find_angle(self):
        self.robo_angle = get_angle()
