"""
The template of the main script of the machine learning process
"""

import pickle
import random
import os
import json

# 定義一個 MLPlay 類別
class MLPlay:
    def __init__(self, ai_name, *args, **kwargs):
        """
        初始化函數，這裡可以初始化一些遊戲的變量
        """
        self.training_data = []
        self.frame = 0
        self.round = 0
        self.passed = False
        
        # Access the LEVEL from the game_params
        self.level = kwargs['game_params']['level']
        print(f"Current Level: {self.level}")

        # rm ./datafile.pickle
        if os.path.exists('datafile.pickle'):
            os.remove('datafile.pickle')


    def update(self, scene_info, *args, **kwargs):
        """
        生成指令來控制遊戲，根據接收到的 `scene_info`
        """
        command = "NONE"
        direction = -1
        self.frame = scene_info["frame"]

        # 檢查遊戲狀態，如果遊戲結束，則重置
        if scene_info["status"] == "GAME_OVER":
            self.passed = False
            return "RESET"
        elif scene_info["status"] == "GAME_PASS":
            self.passed = True
            return "RESET"

        # Initialize last_frame with default values
        last_frame = (98, 395)

         # Check if the pickle file exists before attempting to load it
        if os.path.exists('datafile.pickle'):
            with open('datafile.pickle', 'rb') as file:
                last_frame = pickle.load(file)

        delta_X = scene_info["ball"][0] - last_frame[0]
        delta_Y = scene_info["ball"][1] - last_frame[1]
    
        if delta_X != 0:
            slope = delta_Y / delta_X
            if delta_X > 0 and delta_Y > 0:
                direction = 0 # 右下
            elif delta_X > 0 and delta_Y < 0:
                direction = 1 # 右上
            elif delta_X < 0 and delta_Y > 0:
                direction = 2 # 左下
            elif delta_X < 0 and delta_Y < 0:
                direction = 3 # 左上

        # 如果球尚未發出，則向左發球
        if not scene_info["ball_served"]:
            # 隨機決定發球方向
            if random.random() > 0.5:
                command = "SERVE_TO_RIGHT"
            else:
                command = "SERVE_TO_LEFT"
            self.ball_served = True
        elif delta_Y > 0 and delta_X != 0: # 球正在向下
            # 根據斜直線方程式計算球與板子的交點
            # y = mx + c
            # c = y - mx
            # x = (y - c) / m
            # m = slope
            c = scene_info["ball"][1] - slope * scene_info["ball"][0]
            intersection = (400 - c) / slope
            # 要依照反彈的次數(intersection / 200)來計算出實際落地的座標
            # 如果反彈偶數次，則預測座標為 abs(intersection - 200*撞牆次數)
            # 若反彈為奇數次，要取鏡像座標，即(200 - abs(intersection - 200*撞牆次數))
            # 得到座標後，就可以操縱平台前往座標，成功接球
            num_of_bounce = int(intersection / 200)
            if num_of_bounce % 2 == 0:
                intersection = abs(intersection - 200 * num_of_bounce)
            else:
                intersection = 200 - abs(intersection - 200 * num_of_bounce)
            
            random_bias = random.randint(0, 15)
            if intersection > (scene_info["platform"][0] + 20 + random_bias):
                command = "MOVE_RIGHT"
            elif intersection < (scene_info["platform"][0] + 20 - random_bias):
                command = "MOVE_LEFT"
            else:
                command = "NONE"


        taining_data_at_this_frame = {
            "level": self.level,
            "ball_coordinate": scene_info["ball"],
            "platform_X": scene_info["platform"][0],
            "direction": direction,
            "delta_X": delta_X,
            "delta_Y": delta_Y,
            "command": command
        }
        self.training_data.append(taining_data_at_this_frame)

        # 將這一偵的資料寫入 pickle file        
        with open('datafile.pickle', 'wb') as file:
            pickle.dump(scene_info["ball"], file)

        return command

    def reset(self):
        """
        重置遊戲狀態，可以在這裡重置一些在遊戲中使用的變量
        """
        self.ball_served = False
        # 如果過關，將訓練資料寫入檔案
        if self.passed:
            print('win')
            self.round += 1
            directory = f"./data/collected_data2/level_{self.level}"
            os.makedirs(directory, exist_ok=True)  # Create directory if it does not exist
            file_path = f"{directory}/{self.frame}frames_round{self.round}.json"
            with open(file_path, 'w') as file:
                json.dump(self.training_data, file, indent=4)
        else:
            print('lose')

        self.passed = False
        self.training_data = []



# scene_info 是一個字典，包含了遊戲當前的資訊
# {
#     "frame": 130,               # 第幾幀
#     "status": "GAME_ALIVE",     # 遊戲狀態
#     "ball": (148, 406),         # 球的位置(x, y)
#     "ball_served": True,      # 是否已發球
#     "platform": (0, 400),       # 平台的位置(x, y)
#     "bricks": [(0, 100), (175, 100), ...],  # 磚塊的位置(x, y)
#     "hard_bricks": [(150, 330), (175, 330), ...]  # 硬磚塊的位置(x, y)
# }