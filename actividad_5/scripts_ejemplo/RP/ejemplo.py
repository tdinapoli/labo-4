#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Importamos lirerías útiles
import numpy as np
from matplotlib import pyplot as plt

# Para medir tiempos o generar tiempos de espera
from time import sleep,time


# Esta librería sólo se puede improtar si estás en la misma carpeta 
# que el archivo control_finn.py
from control_finn import RedPitayaApp, reg_labels




# Con esto nos vinculamos a la Red Pitaya
# PERO LA APP TENEMOS QUE ABRIRLA DESDE EL NAVEGADOR PARA QUE ESTÉ CARGADA!

rp  = RedPitayaApp('http://rp-f00a3b.local/lock_in+pid_harmonic/?type=run', name='rp')




#%% Ejemplo configuración de modulación 

frecuencia  = rp.set_freq( 10 )
# es equivalente a hacer:
#   rp.lock.gen_mod_hp = 10


Vmod_out1   = rp.set_modulation_amplitud(2046, ch='out1')
# es equivalente a hacer:
#   rp.lock.mod_out1 = 2046

Vmod_out2   = rp.set_modulation_amplitud(1024, ch='out2')
# es equivalente a hacer:
#   rp.lock.mod_out2 = 1024

print(f"Configuramos la frecuencia de modulación en {frecuencia} Hz")
print(f"A la salida out1 se le suma la modulación con {Vmod_out1} V de amplitud")
print(f"A la salida out2 se le suma la modulación con {Vmod_out2} V de amplitud")



# Si cambio alguno de los parámetros desde la interfase web y quiero recuperarlo por código:
frecuencia  = rp.get_freq()

Vmod_out1   = rp.get_modulation_amplitud( 1 )
Vmod_out2   = rp.get_modulation_amplitud( 'out2' )

# NOTA:  La señal que sale por out1 es proporcional a cos_ref

#%% Ejemplo de configuración y adquisición lock-in

# line='ref' aplica a los armónicos de referencia cos_ref y sin_ref
# Los valores VAL de pasabajos deben ir de 14 a 29
# Eso representa un tau = 2**VAL * 8 ns
rp.set_lpf(16 , order=1 , line='ref' ) 

tau , orden = rp.get_lpf('ref')

print(f"El pasabajos para la democulación de X e Y es de orden {orden} y tiempo característico {tau} seg ")
print(f"La frecuencia de corte es fc={1/(tau*2*np.pi)} Hz ")

# Adquisición de UN dato del canal X
X_en_ints  = rp.lock.X_28  # Leemos el dato crudo en int
# esta forma de adquisición es mas directa y permite 
# leer realizar alrededor de 25 lecturas por segundo


# El dato en Volts es aproximadamente:  rp.lock.X_28 /2**24  Volts

# La función rp.get_XY() permite leer X e Y en simultáneo y convierte a Volts 
# usando la calibración interna de la RP

X, Y = rp.get_XY()

print(f"El valor obtenido del lock-in es: X={X} V  e  Y={Y} V")


# IMPORTANTE ******************************************************************
# La mayoría de los lock-in, por herencia de la implementación                *
# analógica, miden la mitad de la amplitud (es lo que surje de multiplicar    *
# y filtrar con pasabajos). Esto es R= Amedida/2                              *
# En ESTA versión del lock-in ese factor está compenzado. Esto es:            *
# Acá R = sqrt(X² + Y²) = Amedida   !!!                                       *
#******************************************************************************


# Esta última forma de lectura es más lenta pq realiza algunos comandos extra
# (congela los valores antes de leerlos, para que X e Y sean del mismo instante)
# y permite hacer algo así como 5 mediciones por segundo




#%% Ejemplo de configuración de Fase y utilziación de otras demodulaciones.



# line='1f' aplica a los armónicos de referencia cos_ref y sin_ref
# Los valores VAL de pasabajos deben ir de 14 a 29
# Eso representa un tau = 2**VAL * 8 ns

orden = 1
tau   = rp.set_lpf(18 , order=orden , line='1f' ) 

# Configuramos una relacion de fase entre cos_ref y cos_1f
# Los valores admitidos van de 0 a 2519 (2520 serían 360 grados)
fase  = rp.set_phase(315)

print(f"El pasabajos para la democulación de 1F es de orden {orden} y tiempo característico {tau} seg ")

print(f"La señal para la demodulación de F1 está a {fase}° de cos_ref")

X,Y,F1,F2,F3 = rp.get_XY(F=True)

print(f"El valor de F1 es {F1} Volts")





#%% Otros ejemplos accesorios

# Podemos asignar valores constantes o un offset para la modulación de salida
# asignando a un puerto de salida el valor auxiliar A y luego modificando ese valor


# Asignar a out1 la señal de salida
# podemos ver los pisbles valores en : reg_labels['out1_sw'])
rp.lock.out1_sw = 'aux_A'

# La modulación configurada antes se SUMA a esa señal


# Asignar valor a aux_A
rp.lock.aux_A = 2048


# La escala es la misma que los DAC: 8192 es 1 Volt

