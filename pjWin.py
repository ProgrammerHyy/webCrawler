# 主窗口
from mttkinter import mtTkinter as tk
import Analyser
from showImgWin import ShowImgWin
from showTagWin import ShowTagWin


class PjWin:

    def __init__(self):     # 窗口初始化
        self.windows = tk.Tk()      # 生成窗口
        self.windows.title('project')
        self.windows.geometry('300x300')    # 设置窗口尺寸
        # 创建并设置按钮
        self.show_tag_bt = tk.Button(master=self.windows, text='显示tag比例', command=self.show_img)
        self.show_tag_bt.pack(pady=20)
        self.find_tag_bt = tk.Button(master=self.windows, text='查找关联tag比例',command=self.show_tag)
        self.find_tag_bt.pack(pady=20)
        self.windows.mainloop()

    #  转到其他界面的函数
    def show_tag(self):
        # self.windows.destroy()
        sw = ShowTagWin()

    def show_img(self):
        # self.windows.destroy()
        data = Analyser.draw(mode=0)
        siw = ShowImgWin(**data)

    def close(self):
        self.windows.destroy()
