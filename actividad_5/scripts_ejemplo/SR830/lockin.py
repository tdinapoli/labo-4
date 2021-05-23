# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 11:54:57 2020

@author: Publico
"""

import visa
import numpy as np
import time
import matplotlib.pyplot as plt

"""
Manual: https://www.thinksrs.com/downloads/pdfs/manuals/SR830m.pdf

El input de la clase (config) debe ser un diccionario con las
siguientes claves:

    config = {
          'lockin_addr': str,
          'medicion_modo' : int,
          'display_modo' : str,
          'sens' : int,
          'slope' : int,
          't_int' : int,
          'ref_intern' : bool,
          'ref_freq' : int,
          'ref_v' : int,
          }

Los componentes se acceden como los de una lista pero
cuyos índices son strings; ejemplo:

    config['sens']

Ese diccionario será la configuración inicial. Luego, podrán
modificar los parámetros a medida que vayan necesitando usando
los métodos (funciones) de la clase.

"""

class SR830:
    '''Clase para el manejo amplificador Lockin SR830 usando PyVISA de interfaz'''

    def __init__(self, config):

        self._lockin = visa.ResourceManager().open_resource(config['lockin_addr'])
        print(self._lockin.query('*IDN?'))

        #Configuración inicial del Lock In

        #Modo de medición
        self.setModo(config['medicion_modo'])

        #Display del panel frontal
        self.setDisplay(config['display_modo'])

        #Sensibilidad
        self.setSensibility(config['sens'])

        #Slope del filtro
        self.setFilterSlope(config['slope'])

        #Tiempo de integración del filtro
        self.setIntegrationTime(config['t_int'])

        #Referencia
        self.setModoReferencia(config['ref_intern'])
        self.setFreqReferencia(config['ref_freq'])
        self.setVoltReferencia(config['ref_v'])



    def __del__(self):
        self._lockin.close()

    def setModo(self, modo):
        '''Selecciona el modo de medición, 0=A, 1=A-B, 2=I, 3=I(10M)'''
        self._lockin.write(f"ISRC {modo}")

    def setSensibility(self, sens):
        '''Setea la sensibilidad'''
        self._lockin.write(f"SENS {sens}")

    def setIntegrationTime(self, tbase):
        '''Setea el tiempo de integración del filtro'''
        #Página 90 (5-4) del manual
        self._lockin.write(f"OFLT {tbase}")

    def setFilterSlope(self, slope):
        '''Setea la pendiente del filtro pasabajos. 3=24dB/oct '''
        self._lockin.write(f"OFSL {slope}")

    def setModoReferencia(self, isIntern):
        '''Setea si la referencia a usar es interna (True) o externa (False)'''
        self._lockin.write(f"FMOD {int(isIntern)}")

    def setFreqReferencia(self, freq):
        '''Setea la frecuencia de la referencia interna, en Hz'''
        self._lockin.write(f"FREQ {freq}")

    def setVoltReferencia(self, vRef):
        '''Setea el voltaje RMS de la referencia interna, en V'''
        self._lockin.write(f"SLVL {vRef}")

    def setDisplay(self, displaymode):
        '''
        Setea el display del panel frontal del Lock-In:
            -'XY': modo X-Y
            -'RT': modo R-Theta
            -Para otros modos, ver el manual.
         '''
        if displaymode=='XY':
            self._lockin.write('DDEF 1, 0') #Canal 1, x
            self._lockin.write('DDEF 2, 0') #Canal 2, y
        elif displaymode=='RT':
            self._lockin.write('DDEF 1,1') #Canal 1, R
            self._lockin.write('DDEF 2,1') #Canal 2, Theta
        else:
            print('No entendí lo que querés ver en el display')

    def getDisplay(self):
        '''Obtiene la medición que acusa el display.'''

        return self._lockin.query_ascii_values('SNAP? 10, 11', separator=",")

    def getMedicion(self, measurement_mode):
        '''
        Obtiene los valores medidos según measurement_mode:
            -'XY': Valores XY
            -'RT': Valores RT
            -Para otros valores, ver el manual. Es posible obtener
            hasta 6 valores simultáneamente.
        '''
        if measurement_mode=='XY':
            return self._lockin.query_ascii_values('SNAP? 1, 2', separator=',')
        elif measurement_mode=='RT':
            return self._lockin.query_ascii_values('SNAP? 3, 4', separator=',')
        else:
            print('No entendí lo que querés medir')

    def getIntegrationTime(self):

        i = int(self._lockin.query('OFLT?'))

        #Lo siguiente convierte a tiempo el parámetro i de la sección 5-6
        if i % 2 == 0:
            t_int = 1 * 10**(i/2-5)
        else:
            t_int = 3 * 10**((i-1)/2 - 5)

        return t_int


if __name__ == '__main__':

    config = {
          'lockin_addr': 'GPIB0::11::INSTR',
          'medicion_modo' : 0,
          'display_modo' : 'RT',
          'sens' : 21,
          'slope' : 3,
          't_int' : 6,
          'ref_intern' : True,
          'ref_freq' : 500,
          'ref_v' : 0.005,
          }

    lock =  SR830(config)
    print(lock.getMedicion('RT'))














