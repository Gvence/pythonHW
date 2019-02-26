import tkinter as tk
import numpy as np

from tkinter import *
class game ():
    def __init__ (self, WindowW = 1000, WindowH = 800):
        self.Window = Tk()
        self.WindowW = WindowW
        self.WindowH = WindowH
        self.initWindow()

    def initWindow(self):
        self.CarW = 30
        self.CarH = 50
        self.SensorW = self.CarW / 3
        self.SensorH = self.CarH / 5
        self.sensorPosition = []
        self.TargetW = 10
        self.targetPosition = []
        self.ObstacleW = 6
        self.obstaclePosition = []
        self.Window.title('DQN_Car')
        self.canvas = Canvas(self.Window, bg = 'white', width = self.WindowW, height = self.WindowH)
        print('WindowW:', self.WindowW, 'WindowH:', self.WindowH)
        self.initCar()
        self.initButton()
        self.canvas.pack()
        self.Window.mainloop()

    def initCar(self):
        self.carPosition = [self.CarW/2, self.CarH/2]
        self.carWidgetEvent = self.canvas.create_rectangle(self.carPosition[0] - self.CarW/2, self.carPosition[1] - self.CarH/2, \
                                                      self.carPosition[0] + self.CarW/2, self.carPosition[1] + self.CarH/2, fill = 'blue')
        print('CarPosX:', self.carPosition[0], 'CarPosY:', self.carPosition[1])
        self.initSensors(self.carPosition)

    def initButton(self):
        self.placeObstacleButton = Button(self.Window, text = 'Place obstacle', command = self.placeObstacle)
        self.placeObstacleButton.pack(side = BOTTOM)#放置障碍物按钮
        self.placeTargetButton = Button(self.Window, text = 'Place target', command = self.placeTarget)
        self.placeTargetButton.pack(side = BOTTOM)#放置目标点的按钮
        self.resetButton = Button(self.Window, text = 'RESET', command = self.reset)
        self.resetButton.pack(side = BOTTOM)#重置
        self.runButton = Button(self.Window, text = 'RUN', command = self.run)
        self.runButton.pack(side = BOTTOM)#运行按钮


    def placeObstacle(self):
        self.mouseMotionEvent = self.Window.bind(sequence = '<B1-Motion>', func = self.processMouseEvent)

    def processMouseEvent(self, MOUSE):
        self.obstacleWidgetEvent = self.canvas.create_rectangle(MOUSE.x - self.ObstacleW/2, \
                                                                MOUSE.y - self.ObstacleW/2, \
                                                                MOUSE.x + self.ObstacleW/2, \
                                                                MOUSE.y + self.ObstacleW/2, \
                                                                fill = '#9D9D9D')
        self.obstaclePosition.append([MOUSE.x, MOUSE.y])
        print('Obstacle placed at :', self.obstaclePosition[len(self.obstaclePosition) - 1])

    def placeTarget(self):
        try:
            self.Window.unbind('<B1-Motion>', self.mouseMotionEvent)
        except :
            pass
        try:
            self.canvas.delete(self.targetWidgetEvent)
        except AttributeError:
            pass
        self.mousePressEvent = self.Window.bind(sequence = '<Button-1>', func = self.processPlaceTargetEvent)
    def processPlaceTargetEvent(self, MOUSE):
        self.targetWidgetEvent = self.canvas.create_rectangle(MOUSE.x - self.TargetW / 2, \
                                                              MOUSE.y - self.TargetW / 2, \
                                                              MOUSE.x + self.TargetW / 2, \
                                                              MOUSE.y + self.TargetW / 2, \
                                                              fill='#FFDC35')
        self.targetPosition = ([MOUSE.x, MOUSE.y])
        print('Target placed at :', self.targetPosition)
        self.Window.unbind('<Button-1>', self.mousePressEvent)

    def initSensors(self, carPosition):
        sensor1Position = [carPosition[0], carPosition[1] + self.CarH*2/5]    #the front
        sensor2Position = [carPosition[0] - self.CarW*2/5, carPosition[1]]    #left
        sensor3Position = [carPosition[0], carPosition[1] - self.CarH*2/5]    #after end
        sensor4Position = [carPosition[0] + self.CarW*2/5, carPosition[1]]    #right
        self.sensor1WidgetEvent = self.canvas.create_rectangle(sensor1Position[0] - self.SensorW/2, \
                                                               sensor1Position[1] - self.SensorH/2, \
                                                               sensor1Position[0] + self.SensorW/2, \
                                                               sensor1Position[1] + self.SensorH/2, \
                                                               fill = 'white')#the front
        self.sensor2WidgetEvent = self.canvas.create_rectangle(sensor2Position[0] - self.SensorW/2, \
                                                               sensor2Position[1] - self.SensorH/2, \
                                                               sensor2Position[0] + self.SensorW/2, \
                                                               sensor2Position[1] + self.SensorH/2, \
                                                               fill = 'green')#left
        self.sensor3WidgetEvent = self.canvas.create_rectangle(sensor3Position[0] - self.SensorW/2, \
                                                               sensor3Position[1] - self.SensorH/2, \
                                                               sensor3Position[0] + self.SensorW/2, \
                                                               sensor3Position[1] + self.SensorH/2, \
                                                               fill = 'red')#after end
        self.sensor4WidgetEvent = self.canvas.create_rectangle(sensor4Position[0] - self.SensorW/2, \
                                                               sensor4Position[1] - self.SensorH/2, \
                                                               sensor4Position[0] + self.SensorW/2, \
                                                               sensor4Position[1] + self.SensorH/2, \
                                                               fill = '#FF8EFF')#right
        self.sensorPosition = ([sensor1Position, sensor2Position, sensor3Position, sensor4Position])
        print('Sensor position :\n', self.sensorPosition)

    # def moveCar(self, action, velocity, rotation):
        # self.canvas.
        # if action == 'forward':
        #     self.canvas.move()
        #
        #
        # elif action == 'backward':
        #     self.canvas.move()
        #
        # elif action == 'left':
        #     self.canvas.move()
        #
        # elif action == 'right':
        #     self.canvas.move()


    def reset(self):
        self.canvas.delete('all')
        self.initCar()
        self.carPosition = []
        self.obstaclePosition = []
        self.targetPosition = []
        print('CarPositionList :', self.carPosition, '\n'
              'ObstaclePositionList :', self.obstaclePosition, '\n'
              'TargetPositionList :', self.targetPosition, '\n')
        print('GAME RESTART')

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


