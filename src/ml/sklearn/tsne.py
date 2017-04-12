import os
import pandas as pd
from pylab import *
from sklearn.manifold import TSNE


def plot_embedding(X, y, plot_title=None, unbalanced=True):
    x_min, x_max = X[:, 0].min(), X[:, 0].max()
    y_min, y_max = X[:, 1].min(), X[:, 1].max()
    figure()
    ax1 = subplot(111)
    for i in range(X.shape[0]):
        text(
            X[i, 0],
            X[i, 1],
            str(y[i]),
            color=cm.Set1(1 - y[i] / 7),
            fontdict={
                'weight': 'bold',
                'size': 4 if y[i] == 0 and unbalanced else 9})
    if title is not None:
        title(plot_title)

    factor = 0.1
    margin_x, margin_y = factor * (x_max - x_min), factor * (y_max - y_min)
    axis([
        x_min - margin_x,
        x_max + margin_x,
        y_min - margin_y,
        y_max + margin_y])

    figure()
    ax2 = subplot(111)
    for i in range(X.shape[0]):
        plot(
            X[i, 0],
            X[i, 1],
            '.',
            c=cm.Set1(1 - y[i] / 7),
            markersize=2 if y[i] == 0 and unbalanced else 4)
    if title is not None:
        title(plot_title)

def tsne(data_test, data_label):
    label_n = argmax(data_label, axis=1)

    model = TSNE(n_iter=10000)
    tsne_transformed = model.fit_transform(data_test, label_n)

    plot_embedding(tsne_transformed, label_n, 't-sne projection')

    show()


def main():
    data_path = '/home/charlesxu/Workspace/xcc/projects/ccdc/essay_ccdc/code/asort/1202/Auto+softmax'

    data_test = pd.read_excel(
        os.path.join(data_path, 'train_data.xlsx')).values

    data_label = pd.read_excel(
        os.path.join(data_path, 'train_label.xlsx')).values

    tsne(data_test, data_label)


if __name__ == '__main__':
    main()
