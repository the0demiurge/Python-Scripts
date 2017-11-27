#!/usr/bin/env python3
from sklearn.datasets import load_breast_cancer
from tsne import *
import pandas as pd
from pylab import *
import seaborn as sns
from functools import reduce
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
data = load_breast_cancer()

x, y, label_names = data['data'], data['target'], data['target_names']
scaler = MinMaxScaler()
scaler.fit(x)
x = scaler.transform(x)

tsne(x, y, label_names=label_names)

trainx, testx, trainy, testy = train_test_split(x, reshape(y, [-1, 1]), test_size=0.1)


def variance(x, u):
    x = reshape(x, [-1, 1])
    return (x - u).dot(x - u).T


def lda2(x, y):
    x0, x1 = mat(x[y.T[0] == 0]), mat(x[y.T[0] == 1])
    u0, u1 = x0.mean(axis=0), x1.mean(axis=0)

    sigma0, sigma1 = reduce(lambda x, y: x + y, [variance(i, u0) for i in x0]), reduce(lambda x, y: x + y, [variance(i, u1) for i in x1])

    w = (u0 - u1).dot(pinv(sigma0 / x0.shape[0] + sigma1 / x1.shape[0]))
    return w


def transform(w, x):
    return w.dot(x.T).T


def predict(reduced, threshold, classes=None):
    if isinstance(threshold, (int, float)):
        threshold = [threshold]
    if classes is None:
        classes = range(len(threshold))
    threshold.sort()
    predicted = zeros(reduced.shape)
    for i, j, c in zip(threshold[:-1], threshold[1:], classes[1:-1]):
        predicted[reduced >= i and reduced < j] = c
    predicted[reduced < threshold[0]] = classes[0]
    predicted[reduced >= threshold[0]] = classes[-1]
    return predicted


def plot_prediction(reduced, predicted, target, threshold, label_names=None):
    colors = 'rgbcmyk'
    marks = '+xo.*'
    classes = set(list(target))
    if label_names is None:
        label_names = [None] * len(classes)
    for i in classes:
        subscription = target == i
        plot(reduced[subscription], predicted[subscription], '{}{}'.format(colors[i], marks[i]), label=label_names[i])
    plot([threshold, threshold], [-.5, 1.5], 'grey', label='Classify boundary')
    xlabel('Result after dimention reduced')
    ylabel('Predicted')
    legend()


def plot_prediction2(transformed, predicted, y, label_names, threshold):
    plot([threshold, threshold], [-50, 50], 'grey', label='Classify boundary')
    t = pd.DataFrame(transformed, columns=['Dimention Reduction Result After LDA Transform'])
    p = pd.DataFrame([label_names[int(i[0])] for i in predicted], columns=['prediction'])
    lab = pd.DataFrame([label_names[int(i[0])] for i in y], columns=['label'])
    data_t = pd.concat([t, p, lab], axis=1)
    sns.swarmplot(y='label', x='Dimention Reduction Result After LDA Transform', hue='prediction', data=data_t)


w = lda2(trainx, trainy)
threshold = -0.061

traint = transform(w, trainx)
trainp = predict(traint, threshold, [0, 1])
trainerr = mean(abs(reshape(trainp, [1, -1]) - reshape(trainy, [1, -1])))

testt = transform(w, testx)
testp = predict(testt, threshold, [0, 1])
testerr = mean(abs(reshape(testp, [1, -1]) - reshape(testy, [1, -1])))


figure()
plot_prediction2(
    np.vstack([traint, testt]),
    np.vstack([mat(trainp) + 4, mat(testp) + 6]),
    np.vstack([trainy, testy + 2]),
    list(map(lambda x: 'training set ' + x, label_names)) +
    list(map(lambda x: 'testing set ' + x, label_names)) +
    list(map(lambda x: 'train prediction ' + x, label_names)) +
    list(map(lambda x: 'test prediction ' + x, label_names)),
    threshold)
print('train err:', trainerr,
      '\ntest err:', testerr)
show()
# figure()
# plot_prediction(transformed, predicted, y, label_names)


# \documentclass{article}
# \usepackage{amsmath}
# \usepackage{amssymb}
# \usepackage{ctex}
# \begin{document}
# LDA：
# $\omega = S^{-1}_\omega(\mu_0 - \mu_1)$\\
# $S^{-1}_\omega = V\Sigma^{-1}U^T$\\
# 使用奇异值分解，实际$S^{-1}$直接用pinv就行(psedu invert)\\
# $S_\omega = \Sigma_0 + \Sigma_1 $

# \end{document}
