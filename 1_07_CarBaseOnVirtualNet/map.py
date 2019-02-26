# Self Driving Car

# Importing the libraries
import numpy as np
from random import random, randint
import matplotlib.pyplot as plt
import time

# Importing the Kivy packages
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line
from kivy.config import Config
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

# Importing the Dqn object from our AI in ai.py
from ai import Dqn

# Adding this line if we don't want the right click to put a red point
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

# Introducing last_x and last_y, used to keep the last point in memory when we draw the sand on the map
last_x = 0
last_y = 0
n_points = 0
length = 0

# Getting our AI, which we call "brain", and that contains our neural network that represents our Q-function
brain = Dqn(5, 3, 0.9)  #
action2rotation = [0, 20, -20]  # 三个方向，前进0，左拐20，右拐-20
last_reward = 0
last_action = 0
scores = []
lines = []
ITE = []
# Initializing the map
first_update = True


def init():
    global scores
    global sand
    global lastCar_x
    global lastCar_y
    global first_update
    global sensitivity
    global TIMES
    global lines
    global ITE
    global SCO
    global ax
    global line_record
    global point_record
    fig = plt.figure(1, figsize=(5, 4), dpi=60)
    ax = fig.add_subplot(1, 1, 1)
    ITE = []
    SCO = []
    plt.ion()  # 使图标实时显示
    plt.show()
    plt.xlabel('iteration')
    plt.ylabel('scores')
    plt.title('ScoreResult')
    try :
        ax.lines.remove(lines[0])
    except Exception:
        pass
    lines = ax.plot(ITE, SCO, 'r-', lw = 3)
    plt.savefig('VirtualScores.png')
    sensitivity = 1.5
    sensitivity = int(10 * sensitivity)
    sand = np.zeros((longueur, largeur))
    lastCar_x = 0
    lastCar_y = 0
    first_update = False
    TIMES = 0
    file = open('data_record.txt', 'w')
    file.write('L_Sen' + '\t' + 'M_Sen' + '\t' + 'R_Sen' \
            + '\t' + 'Dis_x' + '\t\t' + 'Dis_y' + '\t\t'+ 'Act' + '\n')
    file.close()
    line_record = np.loadtxt('line_record.txt')
    point_record = np.loadtxt('point_record.txt')
# Initializing the last distance
last_distance = 0


# Creating the car class

class Car(Widget):
    angle = NumericProperty(0)
    rotation = NumericProperty(0)
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    sensor1_x = NumericProperty(0)
    sensor1_y = NumericProperty(0)
    sensor1 = ReferenceListProperty(sensor1_x, sensor1_y)
    sensor2_x = NumericProperty(0)
    sensor2_y = NumericProperty(0)
    sensor2 = ReferenceListProperty(sensor2_x, sensor2_y)
    sensor3_x = NumericProperty(0)
    sensor3_y = NumericProperty(0)
    sensor3 = ReferenceListProperty(sensor3_x, sensor3_y)  # 传感器位置的坐标列表
    signal1 = NumericProperty(0)
    signal2 = NumericProperty(0)
    signal3 = NumericProperty(0)

    def move(self, rotation):
        self.pos = Vector(*self.velocity) + self.pos
        self.rotation = rotation
        self.angle = self.angle + self.rotation
        self.sensor1 = Vector(30, 0).rotate(self.angle) + self.pos
        self.sensor2 = Vector(30, 0).rotate((self.angle + 30) % 360) + self.pos
        self.sensor3 = Vector(30, 0).rotate((self.angle - 30) % 360) + self.pos
        self.signal1 = int(np.sum(sand[int(self.sensor1_x) - sensitivity:int(self.sensor1_x) + sensitivity,
                                  int(self.sensor1_y) - sensitivity:int(self.sensor1_y) + sensitivity])) / pow(
            2. * sensitivity, 2)  # 以传感器为圆心的20*20像素格内沙子的比例
        self.signal2 = int(np.sum(sand[int(self.sensor2_x) - sensitivity:int(self.sensor2_x) + sensitivity,
                                  int(self.sensor2_y) - sensitivity:int(self.sensor2_y) + sensitivity])) / pow(
            2. * sensitivity, 2)
        self.signal3 = int(np.sum(sand[int(self.sensor3_x) - sensitivity:int(self.sensor3_x) + sensitivity,
                                  int(self.sensor3_y) - sensitivity:int(self.sensor3_y) + sensitivity])) / pow(
            2. * sensitivity, 2)
        if self.sensor1_x > longueur - 10 or self.sensor1_x < 10 or self.sensor1_y > largeur - 10 or self.sensor1_y < 10:  # 传感器探测到地图边沿
            self.signal1 = 1.
        else :
            self.signal1 = 0
        if self.sensor2_x > longueur - 10 or self.sensor2_x < 10 or self.sensor2_y > largeur - 10 or self.sensor2_y < 10:
            self.signal2 = 1.
        else :
            self.signal2 = 0
        if self.sensor3_x > longueur - 10 or self.sensor3_x < 10 or self.sensor3_y > largeur - 10 or self.sensor3_y < 10:
            self.signal3 = 1.
        else :
            self.signal3 = 0


class Ball1(Widget):  # 三个代表传感器的球
    pass


class Ball2(Widget):
    pass


class Ball3(Widget):
    pass


# Creating the game class

class Game(Widget):
    car = ObjectProperty(None)
    ball1 = ObjectProperty(None)
    ball2 = ObjectProperty(None)
    ball3 = ObjectProperty(None)

    def serve_car(self):
        self.car.center = self.center
        self.car.velocity = Vector(6, 0)

    def update(self, bt ):

        global brain
        global last_reward
        global scores
        global last_distance
        global lastCar_x
        global lastCar_y
        global longueur
        global largeur
        global TIMES
        global lines
        global ITE
        global SCO
        global ax
        global last_action
        longueur = self.width
        largeur = self.height
        if first_update:
            init()

        #xx = goal_x - self.car.x
        #yy = goal_y - self.car.y
        #orientation = Vector(*self.car.velocity).angle((xx, yy)) / 180.  # 小车速度 乘上小车向目标方向的修正等一现在小车朝着目标方向开
        last_signal = [self.car.signal1, self.car.signal2, self.car.signal3, last_distance,
                       last_action]  # 将小车的正负运动方向和小车的传感器的回馈作为输入
        action = brain.update(last_reward, last_signal)  # 通过学习小车状态和环境回报选择方向
        file = open('data_record.txt', 'a')
        file.write('%.2f'%self.car.signal1 + '\t' + '%.2f'%self.car.signal2 + '\t' + '%.2f'%self.car.signal3 \
                   + '\t' + '%.2f'%self.car.x + '\t\t' + '%.2f'%self.car.y + '\t\t' + str(action.numpy())+ '\n')
        file.close()
        last_action = action
        scores.append(brain.score())  # 记录每一次学习后的得分
        rotation = action2rotation[action]  # 通过网络跑出的动作转换成小车的运动方向，左转还是右转还是前进

        self.car.move(rotation)

        if self.car.x >= self.width/2 :
            dis_x = self.width - self.car.x
        else:
            dis_x = self.car.x
        if self.car.y >= self.height/2 :
            dis_y = self.height - self.car.y
        else:
            dis_y = self.car.y
        #distance = np.array([dis_x, dis_y]).min()
        distance = Vector(dis_x, dis_y).rotate(self.car.angle).length()
        #distance = np.array([np.sqrt((self.car.x - self.width) ** 2), np.sqrt((self.car.y - self.height) ** 2)]).min()
        #distance = np.sqrt((self.car.x - goal_x)**2 + (self.car.y - goal_y)**2)
        self.ball1.pos = self.car.sensor1
        self.ball2.pos = self.car.sensor2
        self.ball3.pos = self.car.sensor3
        self.car.velocity = Vector(6, 0).rotate(self.car.angle)
        if sand[int(self.car.x), int(self.car.y)] > 0:
            last_reward = -1
        else:
            last_reward = 0.5
        if abs(lastCar_x - self.car.x) < 10:
            last_reward -= 0.5
        if abs(lastCar_y - self.car.y) < 10:
            last_reward -= 0.5
        lastCar_x = self.car.x
        lastCar_y = self.car.y
        if self.car.x < 10:
            self.car.x = 10
            last_reward -= 1
        if self.car.x > self.width - 10:
            self.car.x = self.width - 10
            last_reward -= 1
        if self.car.y < 10:
            self.car.y = 10
            last_reward -= 1
        if self.car.y > self.height - 10:
            self.car.y = self.height - 10
            last_reward -= 1
        if distance - last_distance < 0:
            last_reward += 0.1
        else:
            last_reward -= 0.5
        if distance <= 50:  # 小车会向右下角开当与右下角的距离《100时向左上角开周而复始，遇到障碍躲避
            last_reward -= 0.5
        if distance >100 and distance < 150:
            last_reward += 1
            #goal_x = self.width - goal_x
            #goal_y = self.height - goal_y
        last_distance = distance
        TIMES += 1
        if TIMES % 1000 == 0 :
            ITE.append(TIMES)
            SCO.append(scores[len(scores) - 1])
            Time = time.strftime('%H:%M:%S', time.localtime(time.time()))
            print("%s saving brain..." % Time)
            brain.save()
            lines = ax.plot(ITE, SCO, 'r-', lw=3)
            plt.pause(0.05)
            plt.savefig('VirtualScores.png')


    def reset(self):
        self.car.x = self.width/2
        self.car.y = self.height/2



# Adding the painting tools

class MyPaintWidget(Widget):
    def on_touch_down(self, touch):
        global length, n_points, last_x, last_y
        with self.canvas:
            Color(0.8, 0.7, 0)
            d = 10.
            if touch.button == 'left':
                i = line_record[0]
                touch.ud['line'] = Line(points=(i[0], i[1]), width=10)
                # 测试时记录point的位置
                # file = open('point_record.txt', 'a')
                # file.write(str(touch.x) + '\t' + str(touch.y) + '\n')
                # file.close()
                last_x = int(i[0])
                last_y = int(i[1])
                n_points = 0
                length = 0
                sand[int(i[0]), int(i[1])] = 1
            if touch.button == 'right':
                i = point_record[0]
                touch.ud['line'] = Line(points=(i[0], i[1]), width=10)
                last_x = int(i[0])
                last_y = int(i[1])
                n_points = 0
                length = 0
                sand[int(i[0]), int(i[1])] = 1
    def on_touch_move(self, touch):
        global length, n_points, last_x, last_y
        if touch.button == 'left':
            for i in line_record:
                touch.ud['line'].points += [i[0],i[1]]
                x = int(i[0])
                y = int(i[1])
                # 测试时记录line的位置
                # file = open('line_record.txt', 'a')
                # file.write(str(touch.x) + '\t' + str(touch.y) + '\n')
                # file.close()
                length += np.sqrt(max((x - last_x) ** 2 + (y - last_y) ** 2, 2))
                n_points += 1.
                density = n_points / (length)
                touch.ud['line'].width = int(20 * density + 1)
                sand[int(i[0]) - 10: int(i[0]) + 10, int(i[1]) - 10: int(i[1]) + 10] = 1
                last_x = x
                last_y = y
        if touch.button == 'right':
            for i in point_record:
                touch.ud['line'].points += [i[0],i[1]]
                x = int(i[0])
                y = int(i[1])
                # file = open('line_record.txt', 'a')
                # file.write(str(touch.x) + '\t' + str(touch.y) + '\n')
                # file.close()
                length += np.sqrt(max((x - last_x) ** 2 + (y - last_y) ** 2, 2))
                n_points += 1.
                density = n_points / (length)
                touch.ud['line'].width = int(20 * density + 1)
                sand[int(i[0]) - 10: int(i[0]) + 10, int(i[1]) - 10: int(i[1]) + 10] = 1
                last_x = x
                last_y = y



# Adding the API Buttons (clear, save and load)

class CarApp(App):

    def build(self):
        self.parent = Game()
        self.parent.serve_car()
        Clock.schedule_interval(self.parent.update, 1.0 / 60.0)
        self.painter = MyPaintWidget()
        clearbtn = Button(text='clear')
        savebtn = Button(text='save', pos=(self.parent.width, 0))
        loadbtn = Button(text='load', pos=(2 * self.parent.width, 0))
        resetbtn = Button(text='reset', pos=(3 * self.parent.width, 0))
        clearbtn.bind(on_release=self.clear_canvas)
        savebtn.bind(on_release=self.save)
        loadbtn.bind(on_release=self.load)
        resetbtn.bind(on_release = self.reset)
        self.parent.add_widget(self.painter)
        self.parent.add_widget(clearbtn)
        self.parent.add_widget(savebtn)
        self.parent.add_widget(loadbtn)
        self.parent.add_widget(resetbtn)
        return self.parent

    def clear_canvas(self, obj):
        global sand
        self.painter.canvas.clear()
        sand = np.zeros((longueur, largeur))

    def save(self, obj):
        print("saving brain...")
        brain.save()
        plt.plot(scores)
        plt.show()

    def load(self, obj):
        print("loading last saved brain...")
        brain.load()

    def reset(self, obj):
        print('reset....')
        self.parent.reset()


# Running the whole thing
if __name__ == '__main__':
    CarApp().run()
