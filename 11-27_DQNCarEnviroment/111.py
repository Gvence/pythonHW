'''
tkinter 模块创建一个window窗体，添加一个按钮
tkinter的事务处理，点击退出按钮执行退出关闭窗体程序
'''
from tkinter import *
class Window(Frame):

    def __init__(self,master = None):
        Frame.__init__(self,master)
        self.master = master
        self.init_window(WindowW = 1000, WindowH = 800, title = 'DQN_Car')
    def init_window(self, WindowW, WindowH, title): #设置窗体的标题，若不设置，默认显示tk

        self.master.title(title) #调用pack方法，让它根据文本自适应窗口大小
        self.pack(fill = BOTH,expand = 1) #创建一个按钮，调用tkinter下的Button类
        #1添加一个command进行事务处理，点击这里执行退出程序
        quitButton = Button(self,text = "Don't click",
                            command = self.client_exit) #按钮位置
        quitButton.place(x =60,y = 0) #2创建另一个exit按钮，点击后关闭窗体
        Button(root,text = 'exit',command = root.quit).pack() #1
    def client_exit(self): exit() #初始化一个Tk对象，Tk()这个类描述的是一个主窗体
root = Tk() #创建一个打印hello,world的窗体
w = Label(root,text = "Hello,world!")
w.pack() #设置窗体大小
root.geometry("200x150") #把root这个顶层窗体作为一个对象传入参数到我们定义的Window类
app = Window() #mainloop()是执行Tcl主要的loop
root.mainloop()