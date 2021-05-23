# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 13:12:20 2020

@author: Publico
"""
import numpy as np
import matplotlib.pyplot as plt
import time
from lockin import SR830


def barrido(lock, frecini, frecfin, pasos):

    freqvec = np.linspace(frecini, frecfin, pasos)

    rvector = []
    thetavector = []

    t_int = lock.getIntegrationTime()

    for f in freqvec:
        lock.setFreqReferencia(f)
        time.sleep(10*t_int)
        r, theta = lock.getMedicion('RT')
        rvector.append(r)
        thetavector.append(theta)
        print(f)

    return freqvec, rvector, thetavector

if __name__ == '__main__':

    config = {
          'lockin_addr': 'GPIB0::08::INSTR',
          'medicion_modo' : 'XY', 
          'display_modo' : 'XY', 
          'sens' : 22,
          'slope' : 3, 
          't_int' : 7,
          'ref_intern' : True,
          'ref_freq' : 5000,
          'ref_v' : 0.1,
          }
    
    lock_in = SR830(config)
    time.sleep(5)
    
    frecini = 1e3
    frecfin = 80e3
    
#    frecini = 20e3
#    frecfin = 40e3
    
    pasos = 500

    F, R, Theta = barrido(lock_in, frecini, frecfin, pasos)

    plt.figure(1),plt.clf()
    fig, ax= plt.subplots(2,1,num=1,sharex=True)
    ax[0].plot(F, R)
    #ax[0].set_xlabel('Frecuencia (kHz)')
    ax[0].set_ylabel('R')

    ax[1].plot(F, Theta)
    ax[1].set_xlabel('Frecuencia (kHz)')
    ax[1].set_ylabel('Theta')
    fig.tight_layout()
    
    np.savetxt('barridoLargo.dat',np.transpose([F,R,Theta]),header='frec[Hz] R theta')
    plt.savefig('barridoLargo.svg')
    




