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

    print(f"R (amplitud) tiene un valor de {R}Volts\ntita tiene un valor de {tita}")
    return [R, tita]
#%%
import numpy as np
from time import sleep
from time import time

freqs_corte = np.arange(0, 20, 1, dtype=int)
sens = np.arange(8, 26, 1, dtype=int)
Rs = []
titas = []

for ii, sen in enumerate(sens):
    Rs_fil = []
    titas_fil = []
    for jj, freq in enumerate(freqs_corte):
        lock.setSensibility(sen)
        lock.setIntegrationTime(freq)
        R, tita = medir(lock)
        Rs_fil.append(R)
        titas_fil.append(tita)
        sleep(0.2)
    Rs.append(Rs_fil)
    titas.append(titas_fil)

#%%
    
Rs = np.array(Rs)
titas = np.array(titas)

np.savetxt("datos_R.txt", Rs, delimiter=",")
np.savetxt("datos_tita.txt", titas, delimiter=",")

#%%
import matplotlib.pyplot as plt

R_plot = Rs[11,:]
plt.plot(R_plot, '.b')
plt.yscale("log")
plt.grid()
plt.show()

#%%

frec = 8
sens = 12
lock.setSensibility(sens)
lock.setIntegrationTime(frec)
Rs = []
titas = []
sleep(1)

for ii, med in enumerate(range(100)):
    R, tita = lock.getMedicion("RT")
    Rs.append(R)
    titas.append(tita)
    sleep(0.1)

plt.plot(Rs,'.r')

np.savetxt("R_f8_s12.txt", Rs, delimiter=",")
np.savetxt("tita_f8_s12.txt", titas, delimiter=",")

#estamos midiendo la salida, no la tranferencia, para 
#esto hay q dividir por 0.1 y probablemente multiplicar 
#por 2 ( por como funciona el lock-in)


