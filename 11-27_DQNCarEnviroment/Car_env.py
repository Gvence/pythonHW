import tkinter as tk
import numpy as np

from tkinter import *
class game ():
    def __init__ (self, WindowW = 1000, WindowH = 800):
        self.Window = Tk()
        self.WindowW = WindowW
        self.WindowH = WindowH
        self.CarW = 30
        self.CarH = 50
        self.ObtacleW = 6
        self.obstaclePosition = []
        self.initWindow()


    def initWindow(self):
        self.Window.title('DQN_Car')
        self.canvas = Canvas(self.Window, bg = 'black', width = self.WindowW, height = self.WindowH)
        print('WindowW:', self.WindowW, 'WindowH:', self.WindowH)
        self.initCar()
        self.initButton()
        self.canvas.pack()
        self.Window.mainloop()

    def initCar(self):
        self.carPosition = [self.CarW/2, self.CarH/2]
        self.carWidget = self.canvas.create_rectangle(self.carPosition[0] - self.CarW/2, self.carPosition[1] - self.CarH/2, \
                                                      self.carPosition[0] + self.CarW/2, self.carPosition[1] + self.CarH/2, fill = 'blue')
        print('PosX:', self.carPosition[0], 'PosY:', self.carPosition[1])

    def initButton(self):
        self.placeObstacleButton = Button(self.Window, text = "Place obstacle", command = self.placeObstacle)
        self.placeObstacleButton.pack(side = BOTTOM)
        self.runButton = Button(self.Window, text = 'RUN', command = self.run)
        self.runButton.pack(side = BOTTOM)


    def placeObstacle(self):
        self.Window.bind_all(sequence='<B1-Motion>', func=self.processMouseEvent)

    def processMouseEvent(self, MOUSE):
        self.obstacleWidget = self.canvas.create_rectangle(MOUSE.x - self.ObtacleW/2, MOUSE.y - self.ObtacleW/2, \
                                                           MOUSE.x + self.ObtacleW/2, MOUSE.y + self.ObtacleW/2, fill = 'yellow')
        self.obstaclePosition.append([MOUSE.x, MOUSE.y])
        # print('Obstacle place at :',self.obstaclePosition[(np.size(self.obstaclePosition) - 1), :])
        print(self.obstaclePosition[len(self.obstaclePosition) - 1])
    def run(self):
        print('GAME BEGINS')





# def main():
#     tk = Tk()
#     canvas = Canvas(tk, width = 1000, height = 800) #设置画布
#     canvas.pack() #显示画布
#     def moveCar(event):  # 绑定方向键
#         if event.keysym == "Up":
#             canvas.move(1,0,-5) # 移动的是 ID为1的事物【move（2,0,-5）则移动ID为2的事物】，使得横坐标加0，纵坐标减5
#         elif event.keysym == "Down":
#             canvas.move(1,0,5)
#         elif event.keysym == "Left":
#             canvas.move(1,-5,0)
#         elif event.keysym == "Right":
#             canvas.move(1,5,0)
#     '事件ID可能跟程序的先后顺序有关，例如，下面先创建了200*200的矩形，后创建了20*20的矩形'
#     r = canvas.create_rectangle(180,180,220,220,fill="red") # 事件ID为1
#     print(r) #打印ID验证一下
#     m = canvas.create_rectangle(10,10,20,20,fill="blue") #事件ID为2
#     print(m) #打印ID验证一下
#     canvas.bind_all("<KeyPress-Up>",moverectangle) #绑定方向键与函数
#     canvas.bind_all("<KeyPress-Down>",moverectangle)
#     canvas.bind_all("<KeyPress-Left>",moverectangle)
#     canvas.bind_all("<KeyPress-Right>",moverectangle)
#     tk.mainloop()
if __name__ == '__main__':
    game = game()


