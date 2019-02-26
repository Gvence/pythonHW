import tensorflow as tf

state = tf.Variable(0, name = 'zero')
one = tf.constant(1)

new_value = tf.add(state, one)#将参数相加
update = tf.assign(state, new_value)#将tf值new_value 复制给tf值state

init = tf.initialize_all_variables()
sess = tf.Session()
sess.run(init)
sess.run(update)
print(sess.run(state))
sess.close()