import tensorflow as tf
import numpy as np
class process ():
    def __init__(self):
        self.x_data = np.random.rand(100).astype(np.float32)
        #np.random.rand按照标准正太方程，随机生成100个数,并构成一维的ndparray
        #astype(),将数据转化为固定类型
        #np.float32专属于np的32位浮点数据
        self.y_data = self.x_data*0.1 + 0.3   #create data

        self.Weights = tf.Variable(tf.random_uniform([1], -1.0, 1.0))#权重参数
        #随机生成一个-1--1之间的tf一维矩阵
        self.biases = tf.Variable(tf.zeros([1])) #create tf structure，偏执参数
        #tf.Variable():tf变量
        #tf.zeros([1])，生成一个tf的一维全零矩阵

        self.out = self.Weights*self.x_data + self.biases
        self.loss = tf.reduce_mean(tf.square(self.out - self.y_data))#计算误差，tf.square(x)对x内的所有参数平方，在此是计算平方差
        self.optimizer = tf.train.GradientDescentOptimizer(0.5)#以0.5的alpha 新建一个GradientDescentOptimizer优化器
        self.train = self.optimizer.minimize(self.loss)#使用优化器最小化loss，并将该操作实例化为train

        self.init = tf.initialize_all_variables()#tf的初始化所有参数，并将该操作实例化
        self.sess = tf.Session()  # 实例化神经网络的session，用于控制网络运行

if __name__ == '__main__':
    regression = process()
    regression.sess.run(regression.init)#让启动者sess,控制init启动
    for step in range(201):
        regression.sess.run(regression.train)
        if step%20 == 0 :
            print("step:", step, "bias:", regression.sess.run(regression.biases), "weight:", \
                  regression.sess.run(regression.Weights), "loss:", regression.sess.run(regression.loss))
    regression.sess.close()