import visa

rm = visa.ResourceManager()

print(rm.list_resources()) #Preguntamos los puertos

#Vemos que devuelve el puerto "GPIB0::11::INSTR" que es el que queremos, pero aún así lo chequeamos

inst = rm.open_resource("GPIB0::11::INSTR") #Inicializamos comunicación con ese puerto
print(inst.query("*IDN?")) #Le preguntamos que instrumento esta conectado al puerto

#Debería devolver que es el lock-in SR830

#%%

from lockin import SR830

config = {
          'lockin_addr': 'GPIB0::11::INSTR', 
          'medicion_modo' : 0, #Canal A single-ended
          'display_modo' : 'RT', #Nos muestra R y Tita
          'sens' : 25, #Sensibilidad 12 = 20muV
          'slope' : 3, #Orden del filtro 2 = 18dB/oct
          't_int' : 8, #Frecuencia de corte 10Hz 
          'ref_intern' : False, #Él mismo genera la referencia
          'ref_freq' : 5000, #Con frecuencia 80Hz
          'ref_v' : 0.1, #Con amplitud 0.1V
          }

lock = SR830(config)

#%%

from GeneradorFunciones import AFG3021B
from barrido_refexterna import barrido

genfunc = AFG3021B()

genfunc.getFrequency()
genfunc.setFrequency(3e4)
genfunc.getFrequency()

#%%

freqini = 1
freqfini = 100000
n_med = 500

freqs, rs, ts = barrido(lock, genfunc, freqini, freqfini, n_med)

sens = inst.query("SENS?")
slope = inst.query("OFSL?")
t_int = inst.query("OFLT?")
ref_v = inst.query("SLVL?")

#%%
#Guardamos los datos
import numpy as np

med_num = 10
header = f"sens: {sens}slope: {slope}t_int: {t_int}ref_v: {ref_v}freqini: {freqini}freqfini: {freqfini}n_med: {n_med}Los datos estan ordenados de forma freqs, rs, ts."
data = np.zeros((len(freqs), 3))
data[:,0] = freqs
data[:,1] = rs
data[:,2] = ts

np.savetxt(f"0606/med{med_num}.txt", data, header=header, delimiter=",")
#np.savetxt(f"0506/med{med_num}_freqs.txt", freqs)
#np.savetxt(f"0506/med{med_num}_rs.txt", rs)
#np.savetxt(f"0506/med{med_num}_ts.txt", ts)



#%%
import matplotlib.pyplot as plt

datos = np.loadtxt(f"0606/med{med_num}.txt", delimiter=",")
freqs_txt = datos[:,0]
rs_txt = datos[:,1]
ts_txt = datos[:,2]

fig, ax = plt.subplots(1, figsize=(10,8))

ax.plot(freqs_txt, rs_txt, 'ok')
#ax.set_yscale('log')
plt.show()

#%%

fig, ax = plt.subplots(1, figsize=(9, 7))
for med in [1,2,3,4,5,6,7,8]:
    datos = np.loadtxt(f"0606/med{med}.txt", delimiter=",")
    freqs_txt = datos[:,0]
    rs_txt = datos[:,1]
    ts_txt = datos[:,2]
    ax.plot(freqs_txt, rs_txt, 'o')
    ax.set_yscale('log')
plt.show()



