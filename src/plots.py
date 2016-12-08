import tensorflow as tf
import numpy as np
from sklearn import preprocessing
# import seaborn as sns
import pandas as pd
from pylab import *
import seaborn as sns
from matplotlib.pylab import *

data = pd.read_excel('1202/Auto+softmax/train_data.xlsx')
label = pd.read_excel('1202/Auto+softmax/train_label.xlsx')
# data = pd.concat([label, data], axis=1)


def get_index(label, n):
    return list(label.iloc[n]).index(1)


tmp = list()
for i in range(len(label)):
    tmp.append(get_index(label, i))
labels = set(tmp)
tmp = pd.DataFrame(tmp)

plots = list()
for i in labels:
    plots.append(data.loc[tmp[tmp[0] == i].index])


def get_shape(a, b, c, data=plots):
    cr = list('rgyckmb')
    scatter(plots[c].values[:, a], plots[c].values[:, b], c=cr[c % len(cr)], label='feature %d and %d, malfunction %d' % (a, b, c))
    xlabel('feature %d and %d, malfunction %d' % (a, b, c))


def get_all_shapes(a, b, data=plots, show=1):
    mina = []
    maxa = []
    minb = []
    maxb = []
    for i in data:
        mina.append(min(i.values[:, a]))
        maxa.append(max(i.values[:, a]))
        minb.append(min(i.values[:, b]))
        maxb.append(max(i.values[:, b]))
    mina = min(mina)
    maxa = max(maxa)
    minb = min(minb)
    maxb = max(maxb)
    la = (maxa - mina) * .05
    lb = (maxb - minb) * .05
    ax = [mina - la, maxa + la, minb - lb, maxb + lb]
    if not show:
        return ax
    for i in range(8):
        subplot(2, 4, i + 1)
        get_shape(a, b, i, data)
        axis(ax)
        xlabel('feature %d and %d, malfunction %d' % (a, b, i))
    # figure()
    # for i in range(8):
        # get_shape(a, b, i, data)
        # axis(ax)
    # xlabel('all data with feature %d and %d' % (a, b))
    return ax


# for i in range(8):
#     subplot(2, 4, i + 1)
#     get_shape(0, 1, 2)


xr = data
yr = label
X_train = np.array(xr)
Y_train = np.array(yr)
print(X_train.shape)
print(Y_train.shape)

scaler1 = preprocessing.StandardScaler()
scaler1.fit(X_train)
X = scaler1.transform(X_train)

scaler2 = preprocessing.MinMaxScaler()
scaler2.fit(X)
X = scaler2.transform(X)

ttt = .75
X = X * ttt + (1 - ttt) / 2

Y = Y_train.astype(np.float32)


def ae(struct_of_net=[150, 8]):
    # Create the model
    x = tf.placeholder(tf.float32, [None, 24])
    W1 = tf.Variable(tf.zeros([24, struct_of_net[0]]))
    b1 = tf.Variable(tf.zeros([struct_of_net[0]]))
    y1 = tf.nn.sigmoid(tf.matmul(x, W1) + b1)

    W3 = tf.Variable(tf.random_normal([struct_of_net[0], struct_of_net[-1]]))
    b3 = tf.Variable(tf.random_normal([struct_of_net[-1]]))
    y3 = tf.nn.sigmoid(tf.matmul(y1, W3) + b3)

    W4 = tf.Variable(tf.random_normal([struct_of_net[-1], struct_of_net[0]]))
    b4 = tf.Variable(tf.random_normal([struct_of_net[0]]))
    y4 = tf.nn.sigmoid(tf.matmul(y3, W4) + b4)

    W2 = tf.Variable(tf.zeros([struct_of_net[0], 24]))
    b2 = tf.Variable(tf.zeros([24]))
    y2 = tf.nn.sigmoid(tf.matmul(y4, W2) + b2)
    y_true = x
    # Define cost and optimizer, minimize the squared error
    cost = tf.reduce_mean(tf.pow(y_true - y2, 2))
    optimizer = tf.train.RMSPropOptimizer(1e-3).minimize(cost)

    # Initializing the variables
    init = tf.initialize_all_variables()

    # Launch the graph
    with tf.Session() as sess:
        sess.run(init)
        for epoch in range(1000):
            # Loop over all batches
            for i in range(10):
                fd = {x: X[:(i + 1) * 100, :]}
                _, c = sess.run([optimizer, cost], feed_dict=fd)
            # Display logs per epoch step
            if epoch % 1 == 0:
                print("Epoch:", '%04d' % (epoch + 1),
                      "cost=", "{:.9f}".format(c), end='\r')
        print("AutoEncoder Optimization Finished!")
        datas, feature = sess.run([y2, y3], feed_dict={x: X})
        #for i in range(12):
        #    figure()
        #    scatter(datas[:, 2 * i], datas[:, 2 * i + 1], c='r', label='Raw data')
        #    scatter(X[:, 2 * i], X[:, 2 * i + 1], c='g', label='Restored data')
        #    xlabel('feature %d, %d' % (2 * i, 2 * i + 1))
        #    title('autoencoder restoration')
        ind = [2,3,6,7,10,11,20,21]
        figure()
        ss=1
        for i in range(4):
            subplot(2,2,i+1)
            scatter(X[:,ind[ 2 * i]], X[:,ind[ 2 * i + 1]],c='r', label='Raw data', edgecolors='r', s=ss)
            scatter( datas[:, ind[2 * i]], datas[:, ind[2 * i + 1]], c='black', label='Restored data', marker='+', edgecolors='black', s=20)
            xlabel('feature %d, %d' % (2 * i, 2 * i + 1))
            # title('autoencoder restoration')
        legend()
    return datas, X, feature


def main():
    ##################################################
    # 设置风格，可选项有white, dark, whitegrid, darkgrid, ticks
    sns.set_style('whitegrid')
    ###################################################
    # autoencoder
    # 画出自编码还原效果
    datas, x, feature = ae()

    fs = list()
    for i in labels:
        fs.append(data.loc[tmp[tmp[0] == i].index])

    ###################################################
    # 画出自编码压缩后的特征
    ax = get_all_shapes(6, 7, show=0, data=fs)
    figure()
    subplot(221)
    get_shape(6, 7, 0, data=fs)
    axis(ax)

    subplot(222)
    get_shape(6, 7, 1, data=fs)
    axis(ax)

    subplot(223)
    get_shape(6, 7, 5, data=fs)
    axis(ax)

    subplot(224)
    get_shape(6, 7, 7, data=fs)
    axis(ax)


    ####################################################
    # 画出自编码压缩之前的特征
    ax = get_all_shapes(14, 15, show=0)
    figure()
    subplot(221)
    get_shape(14, 15, 0)
    axis(ax)

    subplot(222)
    get_shape(14, 15, 1)
    axis(ax)

    subplot(223)
    get_shape(14, 15, 5)
    axis(ax)

    subplot(224)
    get_shape(14, 15, 7)
    axis(ax)

    show()
    ####################################################


if __name__ == '__main__':
    main()
    # get all features

    # for i in range(12):
    #     figure()
    #     get_all_shapes(2 * i, 2 * i + 1)
    #     title('%d, %d' % (2 * i, 2 * i + 1))

    # features = [1, 6, 7, 8, 10, 11, 14, 15, 20, 23]
    # for i in range(int(len(features) / 2)):
    #     figure()
    #     get_all_shapes(features[2 * i], features[2 * i + 1])
    #     title('%d, %d' % (features[2 * i], features[2 * i + 1]))

