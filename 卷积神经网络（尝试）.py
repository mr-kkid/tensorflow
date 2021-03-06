import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

sess=tf.InteractiveSession()
mnist=input_data.read_data_sets("MNIST_data/",one_hot=True)


x=tf.placeholder(tf.float32,shape=[None,784])
y_=tf.placeholder(tf.float32,shape=[None,10])

def weight_variable(shape):
    init=tf.truncated_normal(shape=shape,stddev=0.1)
    return tf.Variable(init)

def bias_constant(shape):
    init=tf.constant(0.1,shape=shape)
    return tf.Variable(init)

def conv2d(x,w):
    return tf.nn.conv2d(x,w,strides=[1,1,1,1],padding='SAME')

def max_pool_2x2(x):
    return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')

####################################################

w_conv1=weight_variable([5,5,1,32])
b_conv1=bias_constant([32])
x_images=tf.reshape(x,[-1,28,28,1])
h_conv1=tf.nn.relu(conv2d(x_images,w_conv1)+b_conv1)
h_pool1=max_pool_2x2(h_conv1)

###############################

w_conv2=weight_variable([5,5,32,64])
b_conv2=bias_constant([64])
h_conv2=tf.nn.relu(conv2d(h_pool1,w_conv2)+b_conv2)
h_pool2=max_pool_2x2(h_conv2)

#############################################################

w_fc1=weight_variable([7*7*64,1024])
b_fc1=bias_constant([1024])

h_pool2_flag=tf.reshape(h_pool2,[-1,7*7*64])
h_fc1=tf.nn.relu(tf.matmul(h_pool2_flag,w_fc1)+b_fc1)
###
keep_prob = tf.placeholder("float")
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)
#####
w_fc2=weight_variable([1024,10])
b_fc2=bias_constant([10])
y_conv=tf.nn.softmax(tf.matmul(h_fc1_drop,w_fc2)+b_fc2)

cross_entropy = -tf.reduce_sum(y_*tf.log(y_conv))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
sess.run(tf.global_variables_initializer())

for i in range(1000):
    batch=mnist.train.next_batch(50)
    if i % 100 == 0:
        train_accuracy = accuracy.eval(feed_dict={
            x: batch[0], y_: batch[1], keep_prob: 1.0})
        print ("step %d, training accuracy %g" % (i, train_accuracy))
    train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})

print( "test accuracy %g" % accuracy.eval(feed_dict={
        x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))