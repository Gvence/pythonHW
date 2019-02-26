import tensorflow as tf
import numpy as np
np.set_printoptions(threshold=np.inf)
import matplotlib.pyplot as plt
import matplotlib.animation as anim
BATCH_START = 0  # 建立 batch data 时候的 index
TIME_STEPS = 5  # backpropagation through time 的time_steps
BATCH_SIZE = 10
INPUT_SIZE = 4  # 数据输入size
OUTPUT_SIZE = 3  # 数据输出 size
CELL_SIZE = 128  # RNN的 hidden unit size
LR = 0.006  # learning rate

#加载数据
data_train = np.loadtxt('sensor_Data_train.txt')

# 定义一个生成数据的 get_batch function:
def get_batch():
    global BATCH_START, TIME_STEPS,data_train
    xs = data_train[BATCH_START:BATCH_START + TIME_STEPS*BATCH_SIZE, :].reshape((-1,TIME_STEPS ,INPUT_SIZE))
    ys = data_train[BATCH_START + 1:BATCH_START + TIME_STEPS*BATCH_SIZE + 1, :-1].reshape((-1,TIME_STEPS,OUTPUT_SIZE))
    if BATCH_START == 450:
        BATCH_START = 0
    BATCH_START += TIME_STEPS
    return [xs, ys, xs]

# 定义 LSTMRNN 的主体结构
class LSTMRNN(object):
    def __init__(self, n_steps, input_size, output_size, cell_size, batch_size, norm = False):
        self.norm = norm
        self.n_steps = n_steps
        self.input_size = input_size
        self.output_size = output_size
        self.cell_size = cell_size
        self.batch_size = batch_size
        with tf.name_scope('inputs'):
            self.xs = tf.placeholder(tf.float32, [None, n_steps, input_size], name='xs')
            self.ys = tf.placeholder(tf.float32, [None, n_steps, output_size], name='ys')
        with tf.variable_scope('in_hidden'):
            self.add_input_layer()
        with tf.variable_scope('LSTM_cell'):
            self.add_cell()
        with tf.variable_scope('out_hidden'):
            self.add_output_layer()
        with tf.name_scope('cost'):
            self.compute_cost()
        with tf.name_scope('train'):
            self.train_op = tf.train.AdamOptimizer(LR).minimize(self.cost)

    def normalize(self, data_in, dim, dim_size):
        fc_mean, fc_var = tf.nn.moments(
            data_in,
            axes=[dim]
        )
        scale = tf.Variable(tf.ones([dim_size]))
        shift = tf.Variable(tf.zeros([dim_size]))
        epsilon = 0.001
        # apply moving average for mean and var when train on batch
        ema = tf.train.ExponentialMovingAverage(decay=0.5)

        def mean_var_with_update():
            ema_apply_op = ema.apply([fc_mean, fc_var])
            with tf.control_dependencies([ema_apply_op]):
                return tf.identity(fc_mean), tf.identity(fc_var)

        mean, var = mean_var_with_update()

        output = tf.nn.batch_normalization(data_in, mean, var, shift, scale, epsilon)
        return output
    # 设置 add_input_layer 功能, 添加 input_layer:
    def add_input_layer(self, ):
        l_in_x = tf.reshape(self.xs, [-1, self.input_size], name='2_2D')  # (batch*n_step, in_size)
        # Ws (in_size, cell_size)
        Ws_in = self._weight_variable([self.input_size, self.cell_size])
        # bs (cell_size, )
        bs_in = self._bias_variable([self.cell_size, ])
        # l_in_y = (batch * n_steps, cell_size)
        with tf.name_scope('Wx_plus_b'):
            l_in_y = tf.matmul(l_in_x, Ws_in) + bs_in
        # reshape l_in_y ==> (batch, n_steps, cell_size)
        self.l_in_y = tf.reshape(l_in_y, [-1, self.n_steps, self.cell_size], name='2_3D')
        if self.norm    :
            self.l_in_y = self.normalize(self.l_in_y, 0, self.cell_size)

    # 设置 add_cell 功能, 添加 cell, 注意这里的 self.cell_init_state,
    #  因为我们在 training 的时候, 这个地方要特别说明.
    def add_cell(self):
        lstm_cell = tf.contrib.rnn.BasicLSTMCell(self.cell_size, forget_bias=1.0, state_is_tuple=True)
        with tf.name_scope('initial_state'):
            self.cell_init_state = lstm_cell.zero_state(self.batch_size, dtype=tf.float32)
        self.cell_outputs, self.cell_final_state = tf.nn.dynamic_rnn(
            lstm_cell, self.l_in_y, initial_state=self.cell_init_state, time_major=False)
        if self.norm :
            self.cell_outputs = self.normalize(self.cell_outputs, 0, self.cell_size)
    # 设置 add_output_layer 功能, 添加 output_layer:
    def add_output_layer(self):
        # shape = (batch * steps, cell_size)
        l_out_x = tf.reshape(self.cell_outputs, [-1, self.cell_size], name='2_2D')
        Ws_out = self._weight_variable([self.cell_size, self.output_size])
        bs_out = self._bias_variable([self.output_size, ])
        # shape = (batch * steps, output_size)
        with tf.name_scope('Wx_plus_b'):
            self.pred = tf.matmul(l_out_x, Ws_out) + bs_out
        #self.pred = tf.reshape(pred, [-1, self.n_steps, self.output_size], name='2_3D')
    # 添加 RNN 中剩下的部分:
    def compute_cost(self):
        losses = tf.contrib.legacy_seq2seq.sequence_loss_by_example(
            [tf.reshape(self.pred, [-1], name='reshape_pred')],
            [tf.reshape(self.ys, [-1], name='reshape_target')],
            [tf.ones([self.batch_size * self.n_steps * self.output_size], dtype=tf.float32)],
            average_across_timesteps=True,
            softmax_loss_function=self.ms_error,
            name='losses'
        )
        with tf.name_scope('average_cost'):
            self.cost = tf.div(
                tf.reduce_sum(losses, name='losses_sum'),
                self.batch_size,
                name='average_cost')
            tf.summary.scalar('cost', self.cost)

    @staticmethod
    def ms_error(labels, logits):
        return tf.square(tf.subtract(labels, logits))

    def _weight_variable(self, shape, name='weights'):
        initializer = tf.random_normal_initializer(mean=0., stddev=1., )
        return tf.get_variable(shape=shape, initializer=initializer, name=name)

    def _bias_variable(self, shape, name='biases'):
        initializer = tf.constant_initializer(0.1)
        return tf.get_variable(name=name, shape=shape, initializer=initializer)

# 训练 LSTMRNN
if __name__ == '__main__':
    # 搭建 LSTMRNN 模型
    model = LSTMRNN(TIME_STEPS, INPUT_SIZE, OUTPUT_SIZE, CELL_SIZE, BATCH_SIZE, norm = True)
    sess = tf.Session()
    merged = tf.summary.merge_all()
    writer = tf.summary.FileWriter("logs", sess.graph)
    sess.run(tf.global_variables_initializer())

    # relocate to the local dir and run this line to view it on Chrome (http://0.0.0.0:6006/):
    # $ tensorboard --logdir='logs'

    # matplotlib可视化
    plt.ion()  # 设置连续 plot
    plt.show()
    fig = plt.figure()
    iteration = 0
    cost_list = []
    # 训练 200 次
    while(True):
        iteration += 1
        seq, res, xs = get_batch()  # 提取 batch data
        #xs = np.arange(0,50)
        if iteration == 1:
            # 初始化 data
            feed_dict = {
                model.xs: seq,
                model.ys: res,
            }
        else:
            feed_dict = {
                model.xs: seq,
                model.ys: res,
                model.cell_init_state: state  # 保持 state 的连续性
            }

        # 训练
        _, cost, state, pred = sess.run(
            [model.train_op, model.cost, model.cell_final_state, model.pred],
            feed_dict=feed_dict)
        # # 打印 cost 结果
        if iteration % 1000 ==0:
            cost_list = []
        #cost保留四位小数输出
        print('cost: ', round(cost, 4), 'iteration: ', iteration)
        cost_list.append(cost)
        #每50回合记录一次log
        if iteration%50 == 0 :
            result = sess.run(merged, feed_dict)
            writer.add_summary(result, iteration)
        # # # 绘制数据动态图
        plt.clf()
        chart_1 = fig.add_subplot(6, 1, 1, xlim=(0, 50))
        chart_1.set_title('S_L')
        chart_2 = fig.add_subplot(6, 1, 2, xlim=(0, 50))
        chart_2.set_title('S_M')
        chart_3 = fig.add_subplot(6, 1, 3, xlim=(0, 50))
        chart_3.set_title('S_R')
        # chart_4 = fig.add_subplot(6, 1, 4, xlim=(0, 50))
        # chart_4.set_title('Dis_1')
        # chart_5 = fig.add_subplot(6, 1, 5, xlim=(0, 50))
        # chart_5.set_title('Dis_2')
        chart_6 = fig.add_subplot(6, 1, 6, xlim=(0, 1000))
        chart_6.set_title('Loss')
        label = res.reshape(-1, OUTPUT_SIZE)
        output = pred.reshape(-1, OUTPUT_SIZE)
        #S_L
        chart_1.scatter(np.arange(0, 50), label[:, 0], c='blue', s=10, marker='o')
        chart_1.scatter(np.arange(0, 50), output[:, 0], c='red', s=10, marker='x')
        #S_M
        chart_2.scatter(np.arange(0, 50), label[:, 1], c='blue', s=10, marker='o')
        chart_2.scatter(np.arange(0, 50), output[:, 1], c='red', s=10, marker='x')
        #S_R
        chart_3.scatter(np.arange(0, 50), label[:, 2], c='blue', s=10, marker='o')
        chart_3.scatter(np.arange(0, 50), output[:, 2], c='red', s=10, marker='x')
        # #Dis_1
        # chart_4.plot(np.arange(0, 50), label[:, 3], 'b-', lw=4)
        # chart_4.plot(np.arange(0, 50), output[:, 3], 'r--', lw=2)
        # #Dis_2
        # chart_5.plot(np.arange(0, 50), label[:, 4], 'b-', lw=4)
        # chart_5.plot(np.arange(0, 50), output[:, 4], 'r--', lw=2)
        #Cost
        chart_6.plot(np.arange(0, len(cost_list)), cost_list, 'r-', lw = 2)
        plt.pause(0.1)
