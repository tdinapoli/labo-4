import numpy as np
import matplotlib.pyplot as plt
import datetime
from gwpy.time import tconvert


date = tconvert(1126259447)#tiempo en el q fueron tomadas las mediciones
data = np.loadtxt('H-H1_GWOSC_4KHZ_R1-1126259447-32.txt')
tiempo = np.linspace(0, 32, 4096*32)

plt.style.use('dark_background')

plt.figure(1)
plt.title('Fecha de inicio ' + str(date))
plt.plot(tiempo, data, linewidth = 0.1)
plt.xlabel("tiempo [s]")
plt.ylabel("Tensión de onda gravitacional")
plt.grid(False)
plt.savefig('Ligo_data_compl.jpg', dpi=900)

plt.figure(2)
plt.plot(tiempo, data)
plt.xlabel("tiempo")
plt.ylabel("grav_waves")
plt.xlim(0, 2)
plt.grid(False)

for i in range(10):
    plt.figure(i +3)
    plt.title('Ampliación entre ' + str(3*i+3) +'s y ' + str(i*3+5) +'s')
    plt.plot(tiempo, data, linewidth = 1)
    plt.xlabel("tiempo [s]")
    plt.ylabel("Tensión de onda gravitacional")
    plt.xlim(i*3+3, i*3+5)
    plt.grid(False)
    plt.savefig('Ampliación' + str(3*i+3)+ str(3*i+5) +'.jpg', dpi = 900)
datetime.datetime()