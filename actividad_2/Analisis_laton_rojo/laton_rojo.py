import imageio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy import optimize
from scipy import signal
from scipy import ndimage


def boolean_float(x):
    if x == True:
        return 1
    elif x == False:
        return 0

def dist(x1,x2):
    dist = np.sqrt(((x1[0]-x2[0])**2)+ ((x1[1]-x2[1])**2))
    return dist

calibracion = imageio.imread('grilla_cali_rojo.jpg')

imagenes = []
for i in range(10):
   imagenes.append(imageio.imread('datosrojo' + str(i+1)+'.jpg'))


#%%Calibracion    
r = calibracion[:,:,0]
g = calibracion[:,:,1]
b = calibracion[:,:,1]
#trabajamos con la matriz de los rojos, es en la que se distingue algo

plt.imshow(r)
#escala = plt.ginput(5)
# dist_med = []
# for i in range(len(escala)-1):
#     dist_med.append(dist(escala[i+1], escala[i]))


# escala_de_verded = np.mean(dist_med)
# err_escala = 2*np.std(np.diff(dist_med))
esc = 145.20236051247952
err_esc = 5.936078079715683
#%%Analisis
plt.imshow(imagenes[0][0:900, 200:400])#[250:350,0:200])
plt.axvline(100)

r = imagenes[0][:,:,0]
g = imagenes[0][:,:,1]
b = imagenes[0][:,:,1]

# plt.imshow(r)
# plt.figure()
# plt.imshow(im_0_rotada[0:900, 200:400])
# plt.axvline(106)

im_0_rotada = ndimage.rotate(r, 1)
im_r_rec = im_0_rotada[:,200:400]

datos_a = []
for i in range(len(im_r_rec)):
    datos_a.append(sum(im_r_rec[i])/esc)


x_escalado = np.linspace(0,len(datos_a)/esc, 871)
plt.figure()
plt.plot(x_escalado,np.array(datos_a[7:878]))

plt.figure()
plt.plot(datos_a)


#%%
im_r = []
for i in range(len(imagenes)):
    im_r.append((imagenes[i][:,:,0]))

im_r[0] = ndimage.rotate(im_r[0],1)
im_r[1] = ndimage.rotate(im_r[1],1)
for i in range(4):
    im_r[i+2] = ndimage.rotate(im_r[i+2], 3)

for i in range(4):
    im_r[i+6] = ndimage.rotate(im_r[i+6],5)
    
for i in range(len(im_r)):
    im_r[i] = im_r[i][:,200:450]

datos = []
for i in range(len(im_r)):
    data = []
    for j in range(len(im_r[i])):
        data.append(sum(im_r[i][j])/esc)
    datos.append(data)


for i in range(len(datos)):
    if i<3:
        plt.figure()
        x_esc = np.linspace(0,len(datos[i])/esc, 871)
        plt.plot(x_esc,datos[i][7:878])
        plt.xlabel('mm')
    elif i>2 and i<6:
        plt.figure()
        x_esc = np.linspace(0, len(datos[i])/esc, 790)
        plt.plot(x_esc, datos[i][40:830])
        plt.xlabel('mm')
    else:
        plt.figure()
        x_esc = np.linspace(0, len(datos[i])/esc, 730)
        plt.plot(x_esc, datos[i][100:830])
        plt.xlabel('mm')