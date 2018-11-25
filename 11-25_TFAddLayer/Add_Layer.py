import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
def addLayer (inputs, inputSize, outputSize, activationFunction = None):
    Weights = tf.Variable(tf.random_normal([inputSize, outputSize]))
    bias = tf.Variable(tf.zeros([1, outputSize]) + 0.1)
    WxPlusBias = tf.matmul(inputs, Weights) + bias
    if activationFunction is None :
        return WxPlusBias
    else:
        return activationFunction(WxPlusBias)

#tf_GPU 使用权限配置
gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction = 0.7)


xData = np.linspace(-1, 1, 300)[:, np.newaxis]
noise = np.random.normal(0, 0.05, xData.shape)
yData = np.square(xData) - 0.5 + noise

xs = tf.placeholder(tf.float32, [None,1])
ys = tf.placeholder(tf.float32, [None,1])
l1 = addLayer(xs, 1, 10, activationFunction = tf.nn.relu)
prediction = addLayer(l1, 10, 1, activationFunction = None)

loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys - prediction), reduction_indices = 1))
trainStep = tf.train.GradientDescentOptimizer(0.1).minimize(loss)
init = tf.initialize_all_variables()
sess = tf.Session(config = tf.ConfigProto(gpu_options = gpu_options))
sess.run(init)

fig = plt.figure(1, figsize = (10, 8), dpi = 120)
ax = fig.add_subplot(1, 1, 1)
ax.scatter(xData, yData)
plt.ion()#使图标实时显示

for i in range (1000):
    sess.run(trainStep, feed_dict={xs: xData, ys: yData})
    if i%50 == 0:
        plt.pause(0.5)
        #print(sess.run(loss, feed_dict={xs:xData, ys:yData}))
        # try:
        #     #ax.lines.remove(lines[0])
        # except Exception:
        #     pass
        predictionValue = sess.run(prediction, feed_dict = {xs: xData})
        lines = ax.plot(xData, predictionValue, 'r-', lw = 3)
        print(sess.run(loss, feed_dict={xs: xData, ys: yData}))
        plt.show()
plt.ioff()
