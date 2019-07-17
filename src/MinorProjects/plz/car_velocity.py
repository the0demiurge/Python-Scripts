import numpy as np
import seaborn as sns
from pylab import *
import random


sns.set_style('whitegrid')
v1 = 1
v2 = 2
v3 = 1.5

nums_v1 = 50
nums_v2 = 30
nums_v3 = 55

transit = 10

nums = list()

v, num = (v1, nums_v1)
for j in range(num):
    nums.append(v + random.gauss(0, .01 * v))
    pass

for j in range(int(transit * (v2 - v1))):
    nums.append(v1 + (v2 - v1) / abs(int(transit * (v2 - v1))) * j + random.gauss(0, .02 * v))

v, num = (v2, nums_v2)
for j in range(num):
    nums.append(v + random.gauss(0, .01 * v))
    pass

for j in range(abs(int(transit * (v3 - v2)))):
    nums.append(v2 + (v3 - v2) / abs(int(transit * (v3 - v2))) * j + random.gauss(0, .02 * v))

v, num = (v3, nums_v3)
for j in range(num):
    nums.append(v + random.gauss(0, .01 * v))
    pass




plot(nums)
