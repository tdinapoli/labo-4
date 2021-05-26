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
          'sens' : 21, #Sensibilidad 20mV
          'slope' : 3, #Orden del filtro 6dB/oct
          't_int' : 8, #Frecuencia de corte 10Hz 
          'ref_intern' : True, #Él mismo genera la referencia
          'ref_freq' : 80, #Con frecuencia 80Hz
          'ref_v' : 0.1, #Con amplitud 0.1V
          }

lock = SR830(config)

#%%

import numpy as np
from time import sleep
from time import time

freqs_corte = np.arange(2, 15, 1, dtype=int) #Estas son las frecuencias de corte entre 10kHz y 0.01Hz
sens = np.arange(8, 24, 1, dtype=int) #Estas son las sensibilidades que van de 1microV a 100mV
Rs = [] #Al final van a quedar en cada columna una frecuencia distinta y en cada fila una sensibilidad distinta
titas = [] #Lo mismo con este array

lock.setFilterSlope(3) #Seteamos el orden del filtro al máximo (se puede cambiar, hay que probar)
sleep(5)

for ii, sen in enumerate(sens):
    Rs_fil = []
    titas_fil = []
    for jj, freq in enumerate(freqs_corte):
        lock.setSensibility(sen)
        lock.setIntegrationTime(freq)
        R, tita = lock.getMedicion("RT")
        Rs_fil.append(R)
        titas_fil.append(tita)
        sleep(0.2)
    Rs.append(Rs_fil)
    titas.append(titas_fil)

#Guardamos los datos 
Rs = np.array(Rs)
titas = np.array(titas)
np.savetxt("R_frecs_y_sens.txt", Rs, delimiter=",")
np.savetxt("titas_frecs_y_sens.txt", titas, delimiter=",")

#%%
import matplotlib.pyplot as plt
import numpy as np

f_corte = 8 #Frecuencia deseada
sens = 12 #Sensibilidad deseada
orden = 3 #Orden del filtro
lock.setSensibility(sens) 
lock.setIntegrationTime(f_corte)
lock.setFilterSlope(orden)
Rs = []
Ts = []
sleep(5) #Esperamos a que se estabilice la configuración

#Medimos para 100 datos
for ii, med in enumerate(range(100)):
    R, T = lock.getMedicion("RT")
    Rs.append(R)
    Ts.append(T)
    sleep(0.5)

plt.plot(Rs,'.r')

#Guardamos los datos. Esta vez es un vector
np.savetxt(f"R_p1_fc{f_corte}_s{sens}_o{orden}.txt", Rs, delimiter=",")
np.savetxt(f"T_p1_fc{f_corte}_s{sens}_o{orden}.txt", Ts, delimiter=",")


