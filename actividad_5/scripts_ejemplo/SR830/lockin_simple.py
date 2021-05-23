    # -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 18:57:36 2020

@author: Publico
"""

import visa
import numpy as np
import time
import matplotlib.pyplot as plt

#%%
"""Abro la comunicación con el lockin"""


resourcemanager = visa.ResourceManager()
print(resourcemanager.list_resources())

lockin_name = 'GPIB0::11::INSTR'

lockin = resourcemanager.open_resource(lockin_name)

#%%
#Le pregunto el nombre: le escribo una instrucción con write y luego leo su respuesta con read.
lockin.write('*IDN?')
lockin.read()

#Puedo hacer ambas cosas con el comando query
lockin.query('*IDN?')

#%%
"""Algunos comandos que se le puede escribir (se listan en el manual)"""

"""Seteo modo de medición: 0: A, 1:A-B, 2:I, etc (ver manual)"""

#3 formas distintas de escribir lo mismo:
lockin.write('ISRC 1')
lockin.query('ISRC?')

#Con format
modo=1
lockin.write("ISRC {0}".format(modo))

#Con f strings (agregados a partir de Python 3.5)
modo=1
lockin.write(f"ISRC {modo}")


""" Setear sensibilidad: sección 5.6 del manual """
sensit=21
lockin.write(f"SENS {sensit}")


#%%
"""Lectura de datos"""

#Se puede leer desde 2 hasta 6 datos simultáneos. Posibilidades: sección 5-15

orden="SNAP? 1, 2" #1: X, 2: Y, 3: R, 4: theta, ...
dato1, dato2 = lockin.query_ascii_values(orden, separator=",")
print(dato1)
print(dato2)


"""
Nota: hay más formas y comandos para leer data.

Algunos menos eficientes:

    OUTP?: lee un solo canal: X, Y, R, Theta
    OUTR?: lee el display, el cual se puede setear con DDEF.

Otros más eficientes:

    TRCA?: lee un buffer almacenado en el dispositivo. Para ello hay que
           setear los parámetros del buffer previamente.


"""














