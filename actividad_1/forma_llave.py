import imageio
import numpy as np
from scipy import signal, ndimage
import matplotlib.pyplot as plt

im = imageio.imread('llave.png')
im = im[230:660,480:900,:]



kernel = [[1,2,1],[0,0,0],[-1,-2,-1]]



fig, axs = plt.subplots(2,2)

axs[0][0].imshow(im)

H = signal.convolve2d(im[:,:,0], kernel)
V = signal.convolve2d(im[:,:,0], np.transpose(kernel))

axs[1][0].imshow(V)
axs[0][1].imshow(H)

bordes = H + V
axs[1][1].imshow(bordes)

plt.show()

	
