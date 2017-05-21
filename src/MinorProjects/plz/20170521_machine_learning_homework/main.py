#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio

data_path = "ionosphereData.mat"
data = sio.loadmat(data_path)

inputs, targets = data['X'], list(map(lambda x: x[0][0], data['Y'])) 
