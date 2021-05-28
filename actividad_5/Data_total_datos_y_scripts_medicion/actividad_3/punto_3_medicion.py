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
          'sens' : 12, #Sensibilidad 12 = 20muV
          'slope' : 2, #Orden del filtro 2 = 18dB/oct
          't_int' : 8, #Frecuencia de corte 10Hz 
          'ref_intern' : True, #Él mismo genera la referencia
          'ref_freq' : 80, #Con frecuencia 80Hz
          'ref_v' : 0.1, #Con amplitud 0.1V
          }

lock = SR830(config)

#%%

import numpy as np
from time import sleep

Rs = []
Ts = []
Rmean = []
Rstd = []
Tmean = []
Tstd = []

sens = 12 #sensibilidad 12 = 20muV
orden = 2 #Orden 2 del filtro = 18dB/oct
f_corte = 8 #Frecuencia de corte 8 = 10Hz
frecs = np.logspace(np.log10(40), np.log10(50000), 50, dtype=int)
lock.setSensibility(sens)
lock.setFilterSlope(orden)
lock.setIntegrationTime(f_corte)
lock.setFreqReferencia(frecs[0])
sleep(5)

for orden_iter in [0, 1, 2, 3]:
    
    #seteamos orden del filtro
    lock.setFilterSlope(orden_iter)
    sleep(5)
    
    #Medimos para todas las frecuencias 50 veces
    for fr in frecs:
        R_fila = []
        T_fila = []
        for med in range(50):
            R, T = lock.getMedicion("RT")
            R_fila.append(R)
            T_fila.append(T)
        Rs.append(R_fila)
        Ts.append(T_fila)
        lock.setFreqReferencia(fr)
        sleep(0.5)
        
        Rmean.append(np.mean(R_fila))
        Rstd.append(np.std(R_fila))
        Tmean.append(np.mean(T_fila))
        Tmean.append(np.std(T_fila))

    #Guardamos los archivos 
    np.savetxt(f"R_p3_fc{f_corte}_s{sens}_o{orden_iter}.txt",
               Rs, delimiter=",")
    np.savetxt(f"T_p3_fc{f_corte}_s{sens}_o{orden_iter}.txt",
               Ts, delimiter=",")
    np.savetxt(f"Rmean_p3_fc{f_corte}_s{sens}_o{orden_iter}.txt",
               Rmean, delimiter=",")
    np.savetxt(f"Tmean_p3_fc{f_corte}_s{sens}_o{orden_iter}.txt",
               Tmean, delimiter=",")
    np.savetxt(f"Rstd_p3_fc{f_corte}_s{sens}_o{orden_iter}.txt",
               Rstd, delimiter=",")
    np.savetxt(f"Tstd_p3_fc{f_corte}_s{sens}_o{orden_iter}.txt",
               Tstd, delimiter=",")