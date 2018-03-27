# coding=utf-8
# author:Star
import tensorflow as tf
import numpy as np

x_data = np.random.rand(100).astype(np.float32)

y_data = x_data * 0.1 + 0.3

Weights = tf.Variable(tf.random_uniform([1], -1.0, 1.0))

bias = tf.Variable(tf.zeros([1]))

y = Weights * x_data + bias

loss = tf.reduce_mean(tf.square(y - y_data))

optimizer = tf.train.GradientDescentOptimizer(0.5)

train = optimizer.minimize(loss=loss)

init = tf.global_variables_initializer()

session = tf.Session()

session.run(init)

for step in range(201):
    session.run(train)
    if step % 20 == 0:
        print("Step {}, Weights are:{}. Biases are:{}".format(step, session.run(Weights), session.run(bias)))

