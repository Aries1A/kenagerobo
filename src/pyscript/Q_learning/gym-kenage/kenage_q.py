import gym
import gym_kenage
import numpy as np
import time
from Q_request_handler import POST
from go_home import go_home,leave_home,distance,stop_roll
import datetime

# フィールドの大きさ
size_x = 270
size_y = 90

# 離散化


def bins(clip_min, clip_max, num):
    return np.linspace(clip_min, clip_max, num + 1)[1:-1]

# 状態を離散化

def digitize_state(observation):
    pos_x, pos_y, robo_angle = observation.values()
    digitized = [
        np.digitize(pos_x, bins=bins(0, size_x, num_dizitized)),
        np.digitize(pos_y, bins=bins(0, size_y, num_dizitized)),
        np.digitize(robo_angle, bins=bins(0, 360, num_dizitized)),
    ]
    return sum([x * (num_dizitized**i) for i, x in enumerate(digitized)])

# 行動a(t)を求める関数


def get_action(next_state, episode):
    epsilon = 0.5 * (1 / (episode + 1))
    if epsilon <= np.random.uniform(0, 1):
        next_action = np.argmax(q_table[next_state])
    else:
        next_action = np.random.choice([0, 1])
    return next_action

# Qテーブルを更新する関数
def update_Qtable(q_table, state, action, reward, next_state):
    gamma = 0.99
    alpha = 0.5
    next_Max_Q = max(q_table[next_state][0], q_table[next_state][1])
    q_table[state, action] = (1 - alpha) * q_table[state, action] +\
            alpha * (reward + gamma * next_Max_Q)

    return q_table


# Q学習のmain関数
if __name__ == '__main__':
    env = gym.make('kenage-v0')
    max_number_of_steps = 40  # 1試行のstep数
    num_consecutive_iterations = 2  # 学習完了評価に使用する平均試行回数(謎)
    num_episodes = 1000  # 総試行回数
    num_dizitized = 6  # 分割数
    try:
        q_table = np.load(file="./params/q_params.npy")
        print("q_table loaded")
    except:
        q_table = np.random.uniform(
        low=-1, high=1, size=(num_dizitized**3, env.action_space.n))  # q_rableをランダムに初期化 (ここで学習途中のものloadしたら続きからできるかも)
        print("q_table init")
    print(q_table)
    total_reward_vec = np.zeros(num_consecutive_iterations)  # 各試行の報酬を格納
    final_x = np.zeros((num_episodes, 1))  # 学習後、各試行のt=200でのｘの位置を格納
    islearned = 0  # 学習終了フラグ
    print("esp reboot")
    POST(name = "set_action_step", data = "-1,0") #esp32をreboot
    time.sleep(5)
    for episode in range(num_episodes):  # 試行回数分繰り返す
        # POST(name="set_QStep",data="0")
        # homeポジションに移動
        go_home(env.camera_num)
        # 環境の初期化
        observation = env._reset()
        # 状態の離散化
        state = digitize_state(observation)
        # 最初の行動選択
        action = np.argmax(q_table[state])
        POST(name = "set_action_step", data = str(action)+","+str("0"))

        # episodeの報酬を初期化
        episode_reward=0
        # episodeReadyを1に
        POST(name = "set_episodeStart", data = "1")

        for t in range(max_number_of_steps):  # 1試行のループ
            env._render()
            print("action: {},step: {}".format(action, env.step))
            if islearned == 1:  # 学習完了時の操作
                pass
            # 弛ませながら移動
            # leave_home(env.pos_x,env.pos_y,env.post_pos_x,env.post_pos_y)
            # 行動a_{t}の実行によって、s_{t+1},r_{t}などを計算する
            observation, reward, done, info=env._step(action)  # ここでESP32の実行待ち
            print(observation)
            print(reward)
            episode_reward += reward  # 報酬を追加
            # 離散状態s_{t+1}を求め、Q関数を更新する
            next_state=digitize_state(observation)  # t+1での観測状態を離散値に変換
            q_table=update_Qtable(q_table, state, action, reward, next_state)
            np.save("./params/q_params",q_table)
            #ログを記録
            with open('./data/q_data_.csv','a') as f:
                dt_now = datetime.datetime.now().strftime('%Y年%m月%d日%H:%M:%S')
                f.write("\n")
                f.write("{},{},{},{},{},{},{},{}".format(dt_now,env.step-1,env.pos_x,env.pos_y,env.robo_angle,action,reward,episode_reward))

            # 次の行動a_{t+1}を求める
            action=get_action(next_state, episode)
            state=next_state

            # 終了時の処理
            if done:
                print('%d Episode finished after %f time steps / mean %f' %
                      (episode, t + 1, total_reward_vec.mean()))
                total_reward_vec=np.hstack((total_reward_vec[1:],
                                              episode_reward))  # 報酬を記録
                # if islearned == 1:  #学習終わってたら最終のx座標を格納
                #     final_x[episode, 0] = observation[0]
                POST(name = "set_action_step", data = str(-1)+","+str(env.step))
                time.sleep(7)
                break

            # サーバにa_{t+1}を送信
            POST(name = "set_action_step", data = str(action)+","+str(env.step))
            # POST(name="set_QStep", data=str(env.step))
            #episodeStartを0に
            POST(name="set_episodeStart", data="0")
