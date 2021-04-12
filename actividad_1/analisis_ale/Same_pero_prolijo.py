import imageio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy import signal
from scipy import ndimage
from skimage.transform import rescale
from scipy import optimize

def boolean_float(x):
    if x == True:
        return 1
    elif x == False:
        return 0
    
def tomar_borde(imagen, inicio=[0,0],fin=[-1, -1] , direccion=True):
    puntos = []
    in_y = inicio[1]
    in_x = inicio[0]
    fin_x = fin[0]
    fin_y = fin[1]

    if direccion:
        while in_x <= fin_x:
            punto_y = in_y
            pix = imagen[in_y, in_x]
            while not pix:
                punto_y = punto_y - 1
                pix = imagen[punto_y, in_x]
            puntos.append([in_x, punto_y])
            in_x += 1
    else:
        while in_x <= fin_x:
            punto_y = in_y
            pix = imagen[in_y, in_x]
            while not pix:
                punto_y = punto_y + 1
                pix = imagen[punto_y, in_x]
            puntos.append([in_x, punto_y])
            in_x += 1
    return puntos

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
#data = plt.ginput(8)


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

escala = 18.976900921658984
#%% Medida de 2 pesos a mano
plt.figure()
ejex = np.arange(im.shape[1])/escala
ejey = np.arange(im.shape[0])/escala
plt.imshow(im, extent=[ ejex.min(), ejex.max(), ejey.min(), ejey.max()])
plt.xlabel('X [mm]')
plt.ylabel('Y [mm]')
plt.xlim(5, 32)
plt.ylim(34, 60)


#selec = plt.ginput(4)
lista = [selec[0][0], selec[1][0]]
lista2 = [selec[2][1], selec[3][1]]
plt.plot(np.mean(lista), np.mean(lista2), "ro")
plt.xlim(5, 32)
plt.ylim(34, 60)
plt.hlines(np.mean(lista2),0,97)
plt.vlines(np.mean(lista), 0, 62)
data_medida = plt.ginput(4)
#plt.savefig("imagen_completa.pdf", dpi = 1000)

medida1 = data_medida[1][0]-data_medida[0][0]
medida2 = data_medida[3][1]-data_medida[2][1]

err_H = np.sqrt((20/escala)**2 + (data_medida[0][0]*err_escala/(escala**2))**2 + (20/escala)**2 +(data_medida[1][0]*err_escala/(escala**2))**2)
err_V = np.sqrt((20/escala)**2 + (data_medida[2][1]*err_escala/(escala**2))**2 + (20/escala)**2 +(data_medida[3][1]*err_escala/(escala**2))**2)

err_medio = np.sqrt((err_H/2)**2 + (err_V/2)**2)
#%% Medida de 2 pesos Mejor
filtro = (R>100)

#borde = tomar_borde(filtro[36:640, 23:600], inicio=[120,30],fin=[350,400], direccion=False)
#borde = tomar_borde(filtro[36:640, 23:600], inicio=[130,30],fin=[500,400], direccion=False)
borde1 = tomar_borde(filtro[36:640, 23:600], inicio=[121,30],fin=[555,400], direccion=False)
borde2 = tomar_borde(filtro[36:640, 23:600], inicio=[120,500],fin=[250,400])#, direccion=False)
borde2.reverse()

borde = np.concatenate((np.array(borde2),np.array(borde1)))
borde = np.array(borde)
borde_x_2 = borde[:,0]
borde_y_2 = borde[:,1]
plt.plot(borde_x_2, borde_y_2, color = 'salmon',linewidth=2)
plt.imshow(filtro[36:640, 23:600])
plt.show()


x_m = np.mean(borde_x_2)
y_m = np.mean(borde_y_2)

# calculation of the reduced coordinates
u = borde_x_2 - x_m
v = borde_y_2 - y_m

# linear system defining the center (uc, vc) in reduced coordinates:
#    Suu * uc +  Suv * vc = (Suuu + Suvv)/2
#    Suv * uc +  Svv * vc = (Suuv + Svvv)/2
Suv  = sum(u*v)
Suu  = sum(u**2)
Svv  = sum(v**2)
Suuv = sum(u**2 * v)
Suvv = sum(u * v**2)
Suuu = sum(u**3)
Svvv = sum(v**3)

# Solving the linear system
A = np.array([ [ Suu, Suv ], [Suv, Svv]])
B = np.array([ Suuu + Suvv, Svvv + Suuv ])/2.0
uc, vc = np.linalg.solve(A, B)

xc_1 = x_m + uc
yc_1 = y_m + vc

# Calcul des distances au centre (xc_1, yc_1)
Ri_1     = np.sqrt((borde_x_2-xc_1)**2 + (borde_y_2-yc_1)**2)
R_1      = np.mean(Ri_1)
residu_1 = sum((Ri_1-R_1)**2)
res = np.array((Ri_1-R_1)**2)
er_circ_medio = np.mean(res)
er = 2*np.std(Ri_1-R_1)



ejex = np.arange(im.shape[1])/escala
ejey = np.arange(im.shape[0])/escala

circulo2pe = plt.Circle((xc_1,yc_1), R_1, color = 'orangered', fill = False)

plt.figure()
#plt.imshow(im[94:607],[645,1138])
plt.imshow(im[36:640, 23:600])#, extent=[ ejex.min(), ejex.max(), ejey.min(), ejey.max()])
plt.plot(borde_x_2, borde_y_2, color = 'blue',linewidth=2)
plt.plot(xc_1, yc_1, "go")
plt.gca().add_patch(circulo2pe)
# plt.xlabel('X [mm]')
# plt.ylabel('Y [mm]')
#plt.savefig("2_pesos_inc.png")
error_malo = np.sqrt((2*residu_1/escala)**2 + (2*R_1*err_escala/(escala**2))**2)
error = np.sqrt((2*er/escala)**2 + (2*R_1*err_escala/(escala**2))**2)

#%%Moneda 1 centavo a mano

plt.figure()
ejex = np.arange(im.shape[1])/escala
ejey = np.arange(im.shape[0])/escala
plt.imshow(im, extent=[ ejex.min(), ejex.max(), ejey.min(), ejey.max()])
plt.xlabel('X [mm]')
plt.ylabel('Y [mm]')
plt.xlim(57, 85)
plt.ylim(17, 40)
#selec = plt.ginput(4)
lista = [selec[0][0], selec[1][0]]
lista2 = [selec[2][1], selec[3][1]]
plt.plot(np.mean(lista), np.mean(lista2), "ro")
plt.hlines(np.mean(lista2),0,97)
plt.vlines(np.mean(lista), 0, 62)
data_medida = plt.ginput(4)
medida1 = data_medida[1][0]-data_medida[0][0]
medida2 = data_medida[3][1]-data_medida[2][1]


err_H = np.sqrt((20/escala)**2 + (data_medida[0][0]*err_escala/(escala**2))**2 + (20/escala)**2 +(data_medida[1][0]*err_escala/(escala**2))**2)
err_V = np.sqrt((20/escala)**2 + (data_medida[2][1]*err_escala/(escala**2))**2 + (20/escala)**2 +(data_medida[3][1]*err_escala/(escala**2))**2)

err_medio = np.sqrt((err_H/2)**2 + (err_V/2)**2)

#%%Moneda 1 centavo mas preciso

filtro = (R>200)
fil_fl = np.vectorize(boolean_float)(filtro).astype(float)
#borde = tomar_borde(filtro[450:850,1100:1600], inicio=[96,159],fin=[180,0])#, direccion = False)
borde = tomar_borde(filtro[450:850,1100:1600], inicio=[300,58],fin=[400,160], direccion = False)

borde = np.array(borde)
borde_x = borde[:,0]
borde_y = borde[:,1]
plt.plot(borde_x, borde_y, color = 'salmon',linewidth=2)
plt.imshow(filtro[450:900,1100:1600])
plt.show()


x_m = np.mean(borde_x)
y_m = np.mean(borde_y)

# calculation of the reduced coordinates
u = borde_x - x_m
v = borde_y - y_m

# linear system defining the center (uc, vc) in reduced coordinates:
#    Suu * uc +  Suv * vc = (Suuu + Suvv)/2
#    Suv * uc +  Svv * vc = (Suuv + Svvv)/2
Suv  = sum(u*v)
Suu  = sum(u**2)
Svv  = sum(v**2)
Suuv = sum(u**2 * v)
Suvv = sum(u * v**2)
Suuu = sum(u**3)
Svvv = sum(v**3)

# Solving the linear system
A = np.array([ [ Suu, Suv ], [Suv, Svv]])
B = np.array([ Suuu + Suvv, Svvv + Suuv ])/2.0
uc, vc = np.linalg.solve(A, B)

xc_1 = x_m + uc
yc_1 = y_m + vc

# Calcul des distances au centre (xc_1, yc_1)
Ri_1     = np.sqrt((borde_x-xc_1)**2 + (borde_y-yc_1)**2)
R_1      = np.mean(Ri_1)
residu_1 = sum((Ri_1-R_1)**2)
res = np.array((Ri_1-R_1)**2)
er_circ_medio = np.mean(res)
er = 2*np.std(Ri_1-R_1)

centro = xc_1, yc_1

ejex = np.arange(im.shape[1])/escala
ejey = np.arange(im.shape[0])/escala

circulo1ce = plt.Circle((xc_1,yc_1), R_1, color = 'orangered', fill = False)


plt.figure()
plt.imshow(im[450:900,1100:1600])
plt.plot(borde_x, borde_y, color = 'blue',linewidth=2)
plt.plot(xc_1,yc_1, "ro")
plt.gca().add_patch(circulo1ce)
plt.savefig('1centavo.png')
#plt.plot(centro, 'bo')
plt.xlabel('X [mm]')
plt.ylabel('Y [mm]')


error_malo = np.sqrt((2*residu_1/escala)**2 + (2*R_1*err_escala/(escala**2))**2)
error = np.sqrt((2*er/escala)**2 + (2*R_1*err_escala/(escala**2))**2)
