"""
The template of the main script of the machine learning process
"""

# 導入 pygame module 以獲取鍵盤輸入
import pygame

# 定義一個 MLPlay 類別
class MLPlay:
   
    # __init__() 是 Constuctor
    # First argument of __init__() is always self
    # self is a reference to the instance of the class
    # It is used to access variables that belongs to the class
    def __init__(self, ai_name, *args, **kwargs):
        """
        初始化函數，設置球是否發出的標誌
        """
        # 宣告一個變數 ball_served 來記錄球是否已經發出
        self.ball_served = False
        

    # keyboard 若沒有被指定，則預設為 None
    def update(self, scene_info, keyboard=None, *args, **kwargs):
        """
        根據接收到的 `scene_info` 和鍵盤輸入生成指令
        """
        # 確保 keyboard 變量不為 None
        if keyboard is None:
            keyboard = []

        # 如果遊戲狀態為 GAME_OVER 或 GAME_PASS，則重置遊戲
        if scene_info["status"] in ["GAME_OVER", "GAME_PASS"]:
            return "RESET"

        # 根據鍵盤輸入決定發球方向或是移動方向
        if pygame.K_q in keyboard:
            command = "SERVE_TO_LEFT"  # 向左發球
            self.ball_served = True
        elif pygame.K_e in keyboard:
            command = "SERVE_TO_RIGHT"  # 向右發球
            self.ball_served = True
        elif pygame.K_LEFT in keyboard or pygame.K_a in keyboard:
            command = "MOVE_LEFT"  # 向左移動
        elif pygame.K_RIGHT in keyboard or pygame.K_d in keyboard:
            command = "MOVE_RIGHT"  # 向右移動
        else:
            command = "NONE"  # 不進行操作

        return command

    def reset(self):
        """
        重置遊戲狀態
        """
        self.ball_served = False

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