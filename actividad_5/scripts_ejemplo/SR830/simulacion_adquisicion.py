#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Importamos lirerías útiles
import numpy as np
from matplotlib import pyplot as plt
from time import sleep,time




#%% Instrumentos virtuales

class ADC:
    
    def __init__(self):
        self.t0 = time()
    
    def leer(self):
        
        sleep(0.001  + np.random.uniform()/1000)
        
        if np.random.uniform()>0.9:
            sleep(0.1)
        
        return np.random.normal()/20 + 3*np.cos( (time()-self.t0)*2*np.pi*1 ) - 1*np.cos( (time()-self.t0)*2*np.pi*0.5 )



adc = ADC()



class Laser:
    def __init__(self):
        self.corriente = 0
        self.umbral    = 4
    
    def leer_potencia(self):
        x = self.corriente
        rta =  np.exp(x-3) if x<self.umbral else np.exp(self.umbral-3)*(x-self.umbral)+np.exp(self.umbral-3)
        sleep(0.1)
        
        if np.random.uniform()>0.95:
            sleep(1)
            raise ValueError('ERROR DE COMUNICACION')
        
        return rta  + np.random.uniform()
    
    def set_corriente(self,valor):
        """
        Configura la corriente del laser.
            valor : valor a asignar en mA
        """
        self.corriente = valor


laser = Laser()



#%% Insrumento ADC 



medicion = []
tiempo   = []

t0 = time()

for jj in range(500):
    medicion.append(  adc.leer()  )
    tiempo += [ time()-t0 ]


plt.plot(tiempo,medicion ,  lw=3 , alpha=0.9  , label='Con tiempos')

plt.plot(np.linspace(0,1,len(medicion))*max(tiempo) ,medicion ,  alpha=0.7, label='Asumiendo Sample Rate cte')

plt.legend(loc=1)




#%% Medicion lineal del laser


corrientes = np.linspace(0,20,10)
potencias  = np.zeros(len(corrientes))

t0 = time()

for ii,corriente in enumerate(corrientes):
    laser.set_corriente( corriente )
    
    try:
        potencias[ii] = laser.leer_potencia()
    except:
        print(f'Hubo un error en la medición {ii} ... pruebo de vuelta en 1 seg')
        sleep(1)
        potencias[ii] = laser.leer_potencia()

plt.plot(corrientes , potencias  , '.')


print(f"La medición de {len(potencias)} valores tardó {time()-t0} seg")

#    plt.semilogx()
#    
#    plt.semilogy()

plt.semilogx()

plt.semilogy()

#%% Medicion en barrido logarítmico

N = 10

corrientes = np.logspace(0,np.log10(20),10)
potencias  = np.zeros( (len(corrientes) , N )  )

t0 = time()

for ii,corriente in enumerate(corrientes):
    laser.set_corriente( corriente )
    
    for jj in range(N):
        try:
            potencias[ii,jj] = laser.leer_potencia()
        except:
            print(f'Hubo un error en la medición {ii} ... pruebo de vuelta en 1 seg')
            sleep(1)
            potencias[ii] = laser.leer_potencia()
        
    print(f"{time()-t0} | {ii}: corriente={corriente} potencia={potencias[ii,:].mean()} ")

plt.plot(corrientes , potencias  , '.' , color='gray')

plt.plot(corrientes , potencias.mean(1)  , '-')



plt.semilogx()

plt.semilogy()



np.savez('grupo0_datos.npz', corrientes=corrientes , potencias=potencias )




#%% Cargar datos y graficar

# referencia: https://marceluda.github.io/python-para-fisicos/tuto/repositorio/IO/


datos = np.load('grupo0_datos.npz')


corrientes  = datos['corrientes']
potencias   = datos['potencias']


# plt.plot( corrientes , potencias , color='C0' , alpha=0.3  )

# plt.errorbar( corrientes , potencias.mean(1) , (potencias.max(1)-potencias.min(1))/2 , fmt='.' , color='black' , ms=1, mew=3)

plt.errorbar( corrientes , potencias.mean(1) , potencias.std(1) , color='black' , ms=1, mew=3)



plt.semilogx()

#plt.semilogy()



