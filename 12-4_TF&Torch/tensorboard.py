import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
def addLayer (inputs, inputSize, outputSize, n_layer,  activationFunction = None):
    layer_name = 'layer%s'%n_layer
    with tf.name_scope(layer_name):
        Weights = tf.Variable(tf.random_normal([inputSize, outputSize]), name = 'Weight')
        tf.summary.histogram('weights', Weights)
        bias = tf.Variable(tf.zeros([1, outputSize]) + 0.1, name = 'Bias')
        tf.summary.histogram('biases', bias)
        WxPlusBias = tf.matmul(inputs, Weights) + bias
        tf.summary.histogram('WxPlushBias', WxPlusBias)
        if activationFunction is None:
            output = WxPlusBias
        else:
            output = activationFunction(WxPlusBias)
        tf.summary.histogram('output', output)
        return output

#tf_GPU 使用权限配置
gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction = 0.7)


xData = np.linspace(-1, 1, 300)[:, np.newaxis]
noise = np.random.normal(0, 0.05, xData.shape)
yData = np.square(xData) - 0.5 + noise
with tf.name_scope('inputs'):
    xs = tf.placeholder(tf.float32, [None,1], name = 'x_input')
    ys = tf.placeholder(tf.float32, [None,1], name = 'y_input')
l1 = addLayer(xs, 1, 10, n_layer = 1, activationFunction = tf.nn.relu)
prediction = addLayer(l1, 10, 1, n_layer = 2,  activationFunction = None)
with tf.name_scope('loss'):
    loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys - prediction), reduction_indices = 1), name = 'loss')
    tf.summary.scalar('loss', loss)
with tf.name_scope('train'):
    trainStep = tf.train.GradientDescentOptimizer(0.1).minimize(loss)
init = tf.initialize_all_variables()
sess = tf.Session(config = tf.ConfigProto(gpu_options = gpu_options))
merged = tf.summary.merge_all()#合并所有summary收集的数据
writer = tf.summary.FileWriter('loglog/', sess.graph)#绘制summary 收集的数据
sess.run(init)

fig = plt.figure(1, figsize = (10, 8), dpi = 120)
ax = fig.add_subplot(1, 1, 1)
ax.scatter(xData, yData)
plt.ion()#使图标实时显示
plt.show()
plt.xlabel('x')
plt.ylabel('y')
plt.title('regression')
for i in range (1000):
    sess.run(trainStep, feed_dict={xs: xData, ys: yData})
    if i%50 == 0:
        result = sess.run(merged, feed_dict={xs:xData, ys:yData})
        writer.add_summary(result, i)
        try:
            ax.lines.remove(lines[0])
        except Exception:
            pass
        predictionValue = sess.run(prediction, feed_dict = {xs: xData})
        lines = ax.plot(xData, predictionValue, 'r-', lw = 3)
        print(sess.run(loss, feed_dict={xs: xData, ys: yData}))
        plt.pause(0.1)
plt.savefig("regression.png")
plt.ioff()
