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
import numpy as np
from time import sleep
import matplotlib.pyplot as plt

frecs = np.logspace(np.log10(40), np.log10(50000), 100, dtype=int) #Vector 
#equiespaciado logarítimcamente entre 40 y 50k
Rs = []
Ts = []

#Seteamos los parámetros relevantes: sensibilidad, frecuencia de corte
#y orden del filtro y la primera frecuencia
sens = 12
f_corte = 8
orden = 3
lock.setSensibility(sens) 
lock.setIntegrationTime(f_corte)
lock.setFilterSlope(orden)
lock.setFreqReferencia(frecs[0])
sleep(5)

#Medimos para cada frecuencia
for fr in frecs:
    lock.setFreqReferencia(fr)
    sleep(1)
    R, T = lock.getMedicion("RT")
    Rs.append(R)
    Ts.append(T)

#Guardamos los datos
Rs = np.array(Rs)
Ts = np.array(Ts)
np.savetxt(f"R_p2_fc{f_corte}_s{sens}_o{orden}.txt", Rs, delimiter=",")
np.savetxt(f"T_p2_fc{f_corte}_s{sens}_o{orden}.txt", Ts, delimiter=",")
#%%
import numpy as np
from time import sleep
import matplotlib.pyplot as plt

frecs = np.arange(82, 131, 1, dtype=int) #Vector 
#equiespaciado linealmente entre 82 y 130
Rs = []
Ts = []

#Seteamos los parámetros relevantes: sensibilidad, frecuencia de corte
#y orden del filtro y la primera frecuencia
sens = 12
f_corte = 8
orden = 3
lock.setSensibility(sens) 
lock.setIntegrationTime(f_corte)
lock.setFilterSlope(orden)
lock.setFreqReferencia(frecs[0])
sleep(5)

#Medimos para cada frecuencia
for fr in frecs:
    lock.setFreqReferencia(fr)
    sleep(0.5)
    R, T = lock.getMedicion("RT")
    Rs.append(R)
    Ts.append(T)

#Guardamos los datos
Rs = np.array(Rs)
Ts = np.array(Ts)
np.savetxt(f"R_p2__fino_fc{f_corte}_s{sens}_o{orden}.txt", Rs, delimiter=",")
np.savetxt(f"T_p2_fino_fc{f_corte}_s{sens}_o{orden}.txt", Ts, delimiter=",")

#%%
import matplotlib.pyplot as plt

fig, ax = plt.subplots(2, figsize=(16,20))
ax[0].plot(frecs, Ts, '.r')
ax[1].plot(frecs, Rs, '.b')
plt.show()