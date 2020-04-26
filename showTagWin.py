from mttkinter import mtTkinter as tk
import Analyser
from showImgWin import ShowImgWin


class ShowTagWin:

    def __init__(self):
        self.showTagWin = tk.Tk()
        self.showTagWin.title('查找tag')
        self.showTagWin.geometry('300x200')
        self.showTagWin.protocol("WM_DELETE_WINDOW", self.showTagWin.quit())
        self.tag_input_lb = tk.Label(master=self.showTagWin, text='请输入tag:')
        self.tag_input_lb.pack(side=tk.LEFT, padx=5, pady=20)
        self.tag_input_txt = tk.Entry(master=self.showTagWin)
        self.tag_input_txt.pack(side=tk.LEFT, padx=5, pady=20)
        self.show_bt = tk.Button(master=self.showTagWin, text='显示', command=self.find)
        self.show_bt.pack(side=tk.LEFT, padx=10, pady=50)
        self.showTagWin.mainloop()

    def find(self):
        tag = self.tag_input_txt.get()
        data = Analyser.draw(mode=1, val=tag)
        # self.showTagWin.destroy()
        siw = ShowImgWin(**data)

    def close(self):
        self.showTagWin.destroy()

