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
          'slope' : 3, #Orden del filtro 2 = 18dB/oct
          't_int' : 8, #Frecuencia de corte 10Hz 
          'ref_intern' : True, #Él mismo genera la referencia
          'ref_freq' : 80, #Con frecuencia 80Hz
          'ref_v' : 0.1, #Con amplitud 0.1V
          }

lock = SR830(config)
#%%

import numpy as np
from time import sleep

vmax = 0.2
amplitudes = np.arange(0.005, vmax, 0.002)

sens = 17
f_corte = 8
f_mod = 1e3
orden = 3
lock.setSensibility(sens) 
lock.setIntegrationTime(f_corte)
lock.setFreqReferencia(f_mod)
lock.setFilterSlope(orden)
lock.setVoltReferencia(amplitudes[0])
sleep(5)

Rs = []
Ts = []
Rmean = []
Rstd = []
Tmean = []
Tstd = []
for amp in amplitudes:
    Rs_fila = []
    Ts_fila = []
    lock.setVoltReferencia(amp)
    sleep(0.5)
    for i in range(50):
        R, T = lock.getMedicion("RT")
        Rs_fila.append(R)
        Ts_fila.append(T)
        
    Rmean.append(np.mean(Rs_fila))
    Rstd.append(np.std(Rs_fila))
    Tmean.append(np.mean(Ts_fila))
    Tmean.append(np.std(Ts_fila))
    
np.savetxt(f"Rs_fino2_p4_fc{f_corte}_s{sens}_o{orden}_fm{f_mod}_vmax{vmax}.txt",
           Rs, delimiter=",")
np.savetxt(f"Ts_fino2_p4_fc{f_corte}_s{sens}_o{orden}_fm{f_mod}_vmax{vmax}.txt",
           Ts, delimiter=",") 
np.savetxt(f"Rmean_fino2_p4_fc{f_corte}_s{sens}_o{orden}.txt",
               Rmean, delimiter=",")
np.savetxt(f"Tmean_fino2_p4_fc{f_corte}_s{sens}_o{orden}.txt",
           Tmean, delimiter=",")
np.savetxt(f"Rstd_fino2_p4_fc{f_corte}_s{sens}_o{orden}.txt",
           Rstd, delimiter=",")
np.savetxt(f"Tstd_fino2_p4_fc{f_corte}_s{sens}_o{orden}.txt",
           Tstd, delimiter=",")
#%%

import matplotlib.pyplot as plt

rm1 = np.loadtxt("actividad_4/datos/Rmean_p4_fc8_s17_o3.txt", delimiter = ",")
rm2 = np.loadtxt("actividad_4/datos/Rmean_fino_p4_fc8_s17_o3.txt", delimiter = ",")
rm3 = np.loadtxt("actividad_4/datos/Rmean_fino2_p4_fc8_s17_o3.txt", delimiter = ",")
rs1 = np.loadtxt("actividad_4/datos/Rstd_p4_fc8_s17_o3.txt", delimiter = ",")
rs2 = np.loadtxt("actividad_4/datos/Rstd_fino_p4_fc8_s17_o3.txt", delimiter = ",")
rs3 = np.loadtxt("actividad_4/datos/Rstd_fino2_p4_fc8_s17_o3.txt", delimiter = ",")
vm1 = 4.95
vm2 = 1
vm3 = 0.2
a1 = np.arange(0.05, vm1, 0.05)
a2 = np.arange(0.05, vm2, 0.01)
a3 = np.arange(0.005, vm3, 0.002)


plt.plot(a1, rs1/rm1, ".r")
plt.plot(a2, rs2/rm2, '.g')
plt.plot(a3, rs3/rm3, ".b")
plt.show()



