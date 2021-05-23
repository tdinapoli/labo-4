
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
          'sens' : 12, #Sensibilidad 20mV
          'slope' : 0, #Orden del filtro 6dB/oct
          't_int' : 8, #Frecuencia de corte 10Hz 
          'ref_intern' : True, #Él mismo genera la referencia
          'ref_freq' : 80, #Con frecuencia 80Hz
          'ref_v' : 0.1, #Con amplitud 0.1V
          }

lock = SR830(config)

#%%
def medir(lock):
    R, tita = lock.getMedicion("RT")

    print(f"R (amplitud) tiene un valor de {R}Volts\n tita tiene un valor de {tita}")
    return [R, tita]

#%%
import numpy as np
from time import sleep
from time import time
import matplotlib.pyplot as plt

frecs = np.logspace(np.log10(40), np.log10(50000), dtype=int)
Rs = []
titas = []

for frec in frecs:
    lock.setFreqReferencia(frec)
    sleep(0.5)
    R, tita = lock.getMedicion("RT")
    Rs.append(R)
    titas.append(tita)

np.savetxt("barrido_R_s12_f8.txt", Rs,delimiter=",")
np.savetxt("barrido_titas_s12_f8.txt", titas,delimiter=",")

plt.plot(frecs, Rs, '.r')
plt.xscale("log")
plt.show()



