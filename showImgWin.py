# 统计图片展示窗口
from mttkinter import mtTkinter as tk
import matplotlib as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class ShowImgWin:

    def __init__(self, **data):
        self.show_win = tk.Tk()
        self.show_win.title('tag比例')
        self.show_win.protocol("WM_DELETE_WINDOW", self.show_win.quit())
        self.fig = Figure(figsize=(10, 8), dpi=100)     # 设置画布绘制时需要的参数绘制的尺寸与分辨率
        self.sub_plot = self.fig.add_subplot(111)       # 设置绘制的图的位置
        self.ok_bt = tk.Button(master=self.show_win, text='确定', command=self.ok, padx=50).pack(side=tk.BOTTOM)
        self.draw(**data)
        self.show_win.mainloop()

    # 统计图绘制函数（使用matplotlib）
    def draw(self, **data):
        # 创建画布
        self.canvs = FigureCanvasTkAgg(self.fig, master=self.show_win)
        # 设置中文字体，防止乱码
        font = {'family': 'SimHei',
                'weight': '50',
                'size': '30'}
        plt.rc('font', **font)
        # 画图
        self.sub_plot.pie(x=data['count'], labels=data['tag'], colors=data['color'], explode=data['explode'], shadow=True)
        self.canvs.draw()   # 绘制到画布上
        # 画布的设置
        self.canvs.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

    # 退出该界面
    def ok(self):
        self.show_win.destroy()


