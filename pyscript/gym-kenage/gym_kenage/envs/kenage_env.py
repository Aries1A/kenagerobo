import sys

import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
from get_position import get_position,get_angle,get_goal,change_base
from Q_request_handler import POST # なぜかgym_kenageに置かないとerror吐く
import time
from go_home import distance, stop_roll

HOME_X = 0
HOME_Y = 45

class KenageEnv(gym.Env):
    metadata = {'render.modes':['human']}
    #フィールドの大きさ
    size_x = 270
    size_y = 90

    def __init__(self):
        # super().__init__()
        # action_space, observation_space, reward_range を設定する
        self.action_space = gym.spaces.Discrete(12) #行動
        self.observation_space = spaces.Dict({ # 状態空間は(x,y,angle)
            "pos_x": spaces.Box(low = 0, high = self.size_x, shape=(1,)),
            "pos_y": spaces.Box(low = 0, high = self.size_y, shape=(1,)),
            "robo_angle": spaces.Box(low=0, high=360, shape=(1, ))
            })
        self.reward_range = [-10,100.] #報酬の範囲
        self.pos_x = HOME_X
        self.pos_y = HOME_Y
        self.post_pos_x = self.pos_x
        self.post_pos_y = self.pos_y
        self.robo_angle = 20
        self.camera_num = 1
        self.nonmovable_count = 0
        print("pos_x={} pos_y={}".format(self.pos_x,self.pos_y))

        self._reset()

    def _reset(self): #状態を初期化、初期の観測値を返す
        print("pos_x={} pos_y={}".format(self.pos_x,self.pos_y))

        #初期位置を取得
        self._find_pos()
        #初期向きを取得
        self._find_angle()
        self.done = False
        self.step = 0
        self.nonmovable_count = 0
        POST(name="_reset")
        print("pos_x={} pos_y={}".format(self.pos_x,self.pos_y))
        # change_base(self.camera_num)
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
        self._find_goal()
        self.goal_distance = distance(self.pos_x,self.pos_y,self.goal_x,self.goal_y)
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
        reward = 0
        if self._is_goal():
            reward += 1000
        else:
            reward += -10
            if self.pos_x<10 and self.pos_x > 80:
                reward += -50
            pos_d =  distance(self.post_pos_x,self.post_pos_y,self.goal_x,self.goal_y)
            cur_d = distance(self.pos_x,self.pos_y,self.goal_x,self.goal_y)
            reward += (pos_d - cur_d) * 10
            print("pos_d:{} cur_d:{} reward:{}".format(pos_d,cur_d,reward))
        print("post_pos_x= {}".format(self.post_pos_x))
        print("reward: {}".format(reward))
        return reward
    def _is_goal(self):
        return distance(self.pos_x,self.pos_y,self.goal_x,self.goal_y) < 30
    def _is_movable(self):
        pos_d =  distance(self.post_pos_x,self.post_pos_y,self.goal_x,self.goal_y)
        cur_d = distance(self.pos_x,self.pos_y,self.goal_x,self.goal_y)
        if abs(cur_d - pos_d) < 10:
            self.nonmovable_count += 1
        else:
            self.nonmovable_count = 0
        print("nonmovable_count = {}".format(self.nonmovable_count))
        return self.nonmovable_count < 10

    def _is_done(self):
        return self._is_goal() or not self._is_movable()

    def _render(self, mode='human'):
        outfile = sys.stdout
        outfile.write(str(self._observe())+"\n")

    def _find_pos(self):
        #Webカメラで位置を測る
        self.post_pos_x = self.pos_x
        self.post_pos_y = self.pos_y
        self.pos_x,self.pos_y = get_position(self.camera_num)
        print("pos_x={} pos_y={}".format(self.pos_x,self.pos_y))
    def _find_angle(self):
        self.robo_angle = get_angle()
    def _find_goal(self):
        self.goal_x,self.goal_y = get_goal()
