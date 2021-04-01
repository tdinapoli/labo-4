import numpy as np
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
from datetime import datetime, timedelta

datos_path = ['actividad_0/ligo-data/'+f for f in listdir('actividad_0/ligo-data/') if isfile(join('actividad_0/ligo-data/', f))]

datos_path.pop(datos_path.index('actividad_0/ligo-data/readme.txt'))

tiempos_iniciales = []
for p in datos_path:
	with open(p, 'r') as f:
		line = f.read(200)
		tiempo_inicial = line[line.index("GPS")+4:line.index("GPS")+14]
		tiempos_iniciales.append(tiempo_inicial)


datos = [np.loadtxt(d) for d in datos_path]

print(tiempos_iniciales)

for i, data in enumerate(datos):
	utc = datetime(1980, 1, 6) + timedelta(seconds=int(tiempos_iniciales[i]) - (35 - 19))
	x = np.linspace(0, 32, len(data))
	print(len(data))
	plt.title(utc)
	plt.plot(x, data)
	plt.show()

"""
x = np.linspace(0,32,len(datos))
x2 = np.linspace(0, 32, len(datos2))


plt.plot(x, datos)
plt.plot(x2, datos2)
plt.show()

plt.plot(x2, datos2)
plt.show()
"""
