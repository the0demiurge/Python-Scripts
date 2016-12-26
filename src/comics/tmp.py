import os
import shutil

path = '.'


def rename_nums(path):
    for index, name in enumerate(os.listdir(path)):
        if not os.path.isdir('%s/%s' % (path, name)):
            shutil.move('%s/%s' % (path, name), '%s/%d.%s' % (path, index, name.split('.')[-1]))


comics = {
    'zip': 'cbz',
    'rar': 'cbr'
}


def rename_cbz_cbr(path):
    for index, name in enumerate(os.listdir(path)):
        if name.split('.')[-1] in comics.keys():
            shutil.move('%s/%s' % (path, name), '%s/%s.%s' % (path, name.split('.')[0], comics[name.split('.')[-1]]))
