#####################LIBRERIAS#####################

import time
import serial
from Libreria_tesis import *

#####################CONSTANTES#####################edc

#####################PROGRAMA#####################

# Iniciando conexion serial

##arduinoPort = serial.Serial('COM4', 9600, timeout=1)
arduinoPort = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

# Retardo para establecer la conexion serial

time.sleep(1.8)

while(True):
    
  controller(arduinoPort)
  ##controller2(arduinoPort)
        
# Cerrando puerto serial
arduinoPort.close()
