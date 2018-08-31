from pylab import *
import os
from PIL import Image
from skimage import morphology
from functools import reduce


def change_bg(orig, background=None,
              threshold_yellow=[(80, 145), (65, 145), (0, 50)],
              threshold_black=[(0, 30), (0, 30), (0, 30)],
              threshold_face=[(42, 90), (20, 70), (0, 42)],
              show_pic=False,
              ):
    thresholds = [threshold_yellow, threshold_black, threshold_face]
    if background is None:
        background = orig * 0
    background = array(Image.fromarray(background).resize(orig.shape[:2][::-1]))
    masks = [orig.copy() for i in range(len(thresholds))]
    for mask_i, threshold in enumerate(thresholds):
        for i, (th_lo, th_hi) in enumerate(threshold):
            masks[mask_i][:, :, i] = (th_lo <= masks[mask_i][:, :, i]).astype(int) * (masks[mask_i][:, :, i] <= th_hi).astype(int)
        mask = masks[mask_i][:, :, 0] * masks[mask_i][:, :, 1] * masks[mask_i][:, :, 2]
        masks[mask_i][:, :, 0], masks[mask_i][:, :, 1], masks[mask_i][:, :, 2] = [mask for i in range(3)]
    mask = 1-reduce(lambda x, y: x * y, [1-w for w in masks])
    mask_orig = mask.copy()
    mask = morphology.dilation(mask, ones([10, 3, 1]))
    mask = morphology.opening(mask, ones([18, 12, 1]))
    mask = morphology.dilation(mask, ones([3, 6, 1]))

    result = (orig * mask + background * (1 - mask))
    if show_pic:
        subplot(221)
        imshow(orig)
        title('orig')
        subplot(222)
        imshow(mask*255)
        title('mask')
        subplot(223)
        imshow(mask_orig*255)
        title('mask_orig')
        subplot(224)
        imshow(result)
        title('result')
        show()
    return result, mask, mask_orig


if __name__ == '__main__':
    pics = tuple(filter(lambda x: x.endswith('.jpg'), os.listdir('original')))
    background = tuple(filter(lambda x: x.split('.')[-1].lower() in {'jpg', 'jpeg', 'png', 'bmp'}, os.listdir('background')))

    for i in ['result', 'mask', 'denoised_mask']:
        if not os.path.isdir(i):
            os.mkdir(i)
    bg_names = 0
    for bg in background:
        bg_names += 1
        pic_names = 0
        for pic in pics:
            pic_names += 1
            print('processing:', bg, pic)
            p = imread(os.path.join('original', pic))
            bgp = imread(os.path.join('background', bg))
            result, denoised_mask, mask = change_bg(p, bgp)
            name = 'bg_{}_pic_{}.jpg'.format(bg_names, pic_names)

            imsave(os.path.join('result', name), result, format='jpeg')
            imsave(os.path.join('mask', name), mask * 255, format='jpeg')
            imsave(os.path.join('denoised_mask', name), denoised_mask * 255, format='jpeg')
