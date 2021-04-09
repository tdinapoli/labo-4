import imageio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy import signal
from scipy import ndimage
from skimage.transform import rescale

def boolean_float(x):
    if x == True:
        return 1
    elif x == False:
        return 0

im = imageio.imread('vil_metal.png') # imagen que queremos analizar

r = im[:,:,0]
g = im[:,:,1]
b = im[:,:,1]

mat_x = np.array([[1,0,-1],[2,0,-2],[1,0,-1]])
mat_y = np.transpose(mat_x)

# Analizamos los verdes?

#plt.imshow(g)


#Nos quedamos con los bordes
H = signal.convolve2d(g, mat_x)
V = signal.convolve2d(g, mat_y)
R = (H**2 + V**2)**0.5

#plt.imshow(R)


# R[1050, :] = ndimage.maximum(R[:])
# plt.figure(1)
# plt.imshow(R)


#con la imagen sin filtrar
inte =  R[1030, 1000:1150]
plt.figure(2)
plt.plot(inte)


# con el filtro de la imagen (booleano)
filtro = (R>40)
fil_fl = np.vectorize(boolean_float)(filtro).astype(float)
plt.figure(3)
plt.imshow(filtro)

inte_2 = fil_fl[1030, 1000:1150]
plt.figure(4)
plt.plot(inte_2)
#data = plt.ginpu(8)


x_data = []
for i in range(8):
    x_data.append(data[i][0])

escala = np.mean(np.diff(x_data))
err_escala = 2*np.std(np.diff(x_data))

lenx, leny = len(R), len(R[0])
resx = [i/escala for i in range(0,lenx)]  #reescaleo del eje x
resy = [i/escala for i in range(0,leny)]  #reescaleo del eje y


plt.figure()
ejex = np.arange(filtro.shape[1])/escala
ejey = np.arange(filtro.shape[0])/escala
plt.imshow(filtro, extent=[ ejex.min(), ejex.max(), ejey.min(), ejey.max()])
plt.xlabel('X [mm]')
plt.ylabel('Y [mm]')

#%%
#Medicion Moneda de 2pesos


plt.figure()
ejex = np.arange(im.shape[1])/escala
ejey = np.arange(im.shape[0])/escala
plt.imshow(im, extent=[ ejex.min(), ejex.max(), ejey.min(), ejey.max()])
plt.xlabel('X [mm]')
plt.ylabel('Y [mm]')



# selec = plt.ginput(4)
# lista = [selec[0][0], selec[1][0]]
# lista2 = [selec[2][1], selec[3][1]]
plt.plot(np.mean(lista), np.mean(lista2), "ro")
plt.xlim(5, 32)
plt.ylim(34, 60)
plt.hlines(np.mean(lista2),0,97)
plt.vlines(np.mean(lista), 0, 62)
#data_medida = plt.ginput(4)
#plt.savefig("imagen_completa.pdf", dpi = 1000)

medida1 = data_medida[1][0]-data_medida[0][0]
medida2 = data_medida[3][1]-data_medida[2][1]

#%%
#Medicion moneda de 1 centavo

plt.figure()
ejex = np.arange(im.shape[1])/escala
ejey = np.arange(im.shape[0])/escala
plt.imshow(im, extent=[ ejex.min(), ejex.max(), ejey.min(), ejey.max()])
plt.xlabel('X [mm]')
plt.ylabel('Y [mm]')
plt.xlim(57, 85)
plt.ylim(17, 40)
# selec = plt.ginput(4)
lista = [selec[0][0], selec[1][0]]
lista2 = [selec[2][1], selec[3][1]]
plt.plot(np.mean(lista), np.mean(lista2), "ro")
plt.hlines(np.mean(lista2),0,97)
plt.vlines(np.mean(lista), 0, 62)
#data_medida = plt.ginput(4)
medida1 = data_medida[1][0]-data_medida[0][0]
medida2 = data_medida[3][1]-data_medida[2][1]
#plt.savefig("moneda_1ce.pdf")
