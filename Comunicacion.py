#####################LIBRERIAS#####################

import time
import serial
from Libreria_tesis import controller

#####################VARIABLES#####################

port='/dev/ttyACM0'
##port='COM4'
baudrate=9600
timeOut=1
#####################PROGRAMA#####################

# Iniciando conexion serial

arduinoPort = serial.Serial(port,baudrate, timeout=timeOut)

# Retardo para establecer la conexion serial

time.sleep(1.8)

controller(arduinoPort)
        
# Cerrando puerto serial
arduinoPort.close()
