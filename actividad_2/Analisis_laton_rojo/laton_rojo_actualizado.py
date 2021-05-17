import imageio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy import optimize
from scipy import signal
from scipy import ndimage
from scipy.signal import find_peaks
from scipy.stats import linregress
import pint
from scipy.optimize import curve_fit


un = pint.UnitRegistry()


def boolean_float(x):
    if x == True:
        return 1
    elif x == False:
        return 0

def dist(x1,x2):
    dist = np.sqrt(((x1[0]-x2[0])**2)+ ((x1[1]-x2[1])**2))
    return dist

def minimos(lista):
    datos = []
    for i in range(1,len(lista)-1):
        if lista[i-1] > lista[i] and lista[i+1]>lista[i]:
            datos.append(i)
        
    return np.array(datos)

def lineal(x, m, b):
    y = m*x + b
    return y

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
err_esc = 2*5.936078079715683*10
#%%

im_r = []
for i in range(len(imagenes)):
    im_r.append((imagenes[i][:,:,0]))
    
angulos = [0.7,1.4,1.6,2.8,3,3,3.8,4,4.5,5]
for i in range(len(imagenes)):
    im_r[i] = ndimage.rotate(im_r[i], angulos[i])
    plt.imshow(im_r[i])
    
datos = []
for i in range(len(im_r)):
    data = []
    for j in range(len(im_r[i])):
        data.append(sum(im_r[i][j]))
    datos.append(data)
    
#%%
plt.figure()
plt.imshow(im_r[0]/esc)
plt.axvline(270, color = 'red')
plt.axis('off')
#plt.savefig('patron.pdf')
#%%

conv = []
for i in range(len(datos)):
    if i<3:
        con_2 = np.convolve(datos[i][7:878], np.ones(3)/3)
        conv.append(con_2)   
    elif i>2 and i<6:
        con_2 = np.convolve(datos[i][40:830], np.ones(3)/3)
        conv.append(con_2)
    else:
        con_2 = np.convolve(datos[i][100:830], np.ones(3)/3)
        conv.append(con_2)

#%%

x = np.linspace(0, 600, 600)
plt.figure()
plt.title('Convolución unidimensional del patrón de difracción', fontsize = 15)
plt.plot(x/esc, conv[2][100:700], label = 'Patrón de difracción')
plt.ylabel('Suma de intensidades horizontales')
plt.xlabel('Posición de la Fila [cm]')
plt.grid(True, alpha = 0.7)
#data = plt.ginput(7)
plt.plot(data_x, data_y, 'r.', label = 'Mínimos seleccionados')
plt.legend()
plt.savefig('difreaccion_2.pdf')

data = np.array(data)
data_x= data[:,0]
data_y = data[:,1]
# dist_media = np.mean(np.diff(data_x/(esc)))
# err_dist = np.std(np.diff(data_x/esc))

#%%
dist_med = [0.6034848128196065, 0.3268876069439535, 0.2845979515001553, 0.18744604034548384, 0.20230456793384535, 0.16115787615069035, 0.13144082097396734, 0.13029785731332413, 0.10543012457206946, 0.09029412919081233] #cm
err_dist = [0.02018876345940681, 0.01710631369463916, 0.01102234237574917, 0.007581563222729211, 0.006565826351281345, 0.006565826351281209, 0.012149870371294048, 0.005680696998058207, 0.008133520313288893, 0.009214867629044355] #cm

masas = [0, 2.517, 5.022, 7.486, 10.870 ,12.502, 15.013, 17.491, 20.280, 22.513]  #+18

#%%
D = 1250 #mm
er_D = 5 #mm
lon_laser = 0.0006328 #mm
#a = dlamda /delatz
a = []
for i in range(len(dist_med)):
    a.append(D*lon_laser/(dist_med[i]*10))

#%%

# E= F/(2I)(lx^2-x^3/3)
L = 310 #mm
er_L = 5# mm
d = 4.6 #mm de diametro
er_d = 0.2 #mm
masas = np.array(masas)
masas = masas +18
g = 9800 #mm/s^2
F = masas*g
I = np.pi* d**4/64
x = 220 #mm posicion de la rendija
er_x = 5 #mm

E =[]
for i in range(len(masas)):
    mod = F[i]/(2*I*a[i]) *(L*x**2 - ((x**3)/3))
    E.append(mod)
    
#%%
aprox = np.polyfit(F, a, 1)
p=np.poly1d(aprox)
#print("aprox", aprox)

#c=pearsonr(F, a)
#print("pearson r", a)
b=linregress(F, a)
x_varios = np.linspace(177000,410000, 10000)
y = x_varios*b[0] + b[1]

plt.plot(F,a,'.', label ='datos adquiridos')
plt.plot(x_varios,y , label = 'recta aproximada')
plt.legend()
plt.savefig('ajuste_lineal.pdf')

er_F = np.zeros(len(F)) + g*0.01
k = (L*x**2 - ((x**3)/3))/(2*I)

E =( k/b[0])*un.gram/(un.millimeter*un.second**2)


#%%
er_a = []

for i in range(len(a)):
    er_a.append(np.sqrt(((er_D*lon_laser/(dist_med[i]*10)))**2 + (D*lon_laser*2*err_dist[i]*10/((dist_med[i]*10)**2))**2))
    #er_a.append(er_a)
cor_a_n = 1000000   
x_varios = np.linspace(min(F/cor_a_n)-0.01,max(F/cor_a_n)+0.01, 10000)


popt, pcov = curve_fit(lineal,F, a, sigma = er_a, absolute_sigma=True)
perr = np.sqrt(np.diag(pcov))

y_af = x_varios*popt[0]+ popt[1]
plt.title('Apertura de la rendija en función de la fuerza', fontsize = 15)
plt.errorbar(F, a,yerr = er_a, xerr = er_F, fmt = '.',label = 'datos adquirios')
plt.plot(x_varios,y_af ,label = 'recta aproximada')
plt.ylabel('Apertura de la rendija [mm]')
plt.xlabel('Fuerza gravitatoria[N]')
plt.legend(loc = 'upper left')
plt.grid(True, alpha = 0.7)
plt.savefig('ajuste_lineal.pdf')

er_k_L = er_L* x**2/ (2*I)
er_k_x = (L*2*x*er_x - x**2 *er_x)/(2*I)
er_k_d = (L*x**2 - ((x**3)/3))*64*4*er_d/(np.pi*d**5)

E = k/popt[0] *un.gram/(un.millimeter*un.second**2)
err_E = np.sqrt((er_k_L/popt[0])**2 + (er_k_x/popt[0])**2 + (er_k_d/popt[0])**2 + (k*perr[0]/popt[0])**2)*un.gram/(un.millimeter*un.second**2)
