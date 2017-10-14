from pylab import *
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA


def plot_embedding(X, y, plot_title=None, unbalanced=True, target_names=None):
    x_min, x_max = X[:, 0].min(), X[:, 0].max()
    y_min, y_max = X[:, 1].min(), X[:, 1].max()
    figure()
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
    name_dict = set()
    for i in range(X.shape[0]):
        name = None
        if target_names is not None:
            if y[i] not in name_dict:
                name_dict.add(y[i])
                name = target_names[y[i]]
        plot(
            X[i, 0],
            X[i, 1],
            '.',
            c=cm.Set1(1 - y[i] / 7),
            markersize=2 if y[i] == 0 and unbalanced else 4,
            label=name)
    if title is not None:
        title(plot_title)
    legend()


def tsne(data_test, data_label, title=None, unbalanced=False, method='tsne', label_names=None, one_hot=False):
    if not one_hot:
        label_n = data_label
    else:
        label_n = argmax(data_label, axis=1)

    models = {
        'tsne': TSNE(n_iter=5000),
        'pca': PCA()}

    model = models[method.lower()]
    tsne_transformed = model.fit_transform(data_test, label_n)

    plot_embedding(tsne_transformed, label_n, title if title else 't-sne projection', unbalanced, label_names)
    return tsne_transformed, label_n
