#####################LIBRERIAS#####################

import time
import serial
from Libreria_tesis import *

#####################CONSTANTES#####################

flagCharacter = 'R'

#####################PROGRAMA#####################

# Iniciando conexion serial

arduinoPort = serial.Serial('COM4', 9600, timeout=1)
##arduinoPort = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

# Retardo para establecer la conexion serial

time.sleep(1.8)

while(True):

    arduinoPort.write(flagCharacter.encode())

    getSerialValue1 = arduinoPort.readline()
    getSerialValue2 = arduinoPort.readline()
    getSerialValue3 = arduinoPort.readline()
    getSerialValue4 = arduinoPort.readline()
    
    print ('\nValor retornado de Arduino 1: %s',int(getSerialValue1))
    print ('\nValor retornado de Arduino 2: %s',int(getSerialValue2))
    print ('\nValor retornado de Arduino 3: %s',int(getSerialValue3))
    print ('\nValor retornado de Arduino 4: %s',int(getSerialValue4))
    
    data= [int(getSerialValue1),int(getSerialValue2),int(getSerialValue3),int(getSerialValue4)]
    
    
    print("Cantidad de muestras almacenadas")
    samples=samples_counter()
    print(samples)
    
    #Calculo grados

    val = angle_calculation(data)
    
    print ('\nGrado 1: %s',val[0])
    print ('\nGrado 2: %s',val[1])
    print ('\nGrado 3: %s',val[2])
    print ('\nGrado 4: %s',val[3])
    
    #Insertar datos en la Base de datos
    
    data_insert(data)
    
    #Formateo de datos para enviar al Arduino

    angle = angle_formatting(val)
    
    #Enviar datos al Arduino

    arduinoPort.write(angle.encode())
 
    getSerialValue5 = arduinoPort.readline()
    getSerialValue6 = arduinoPort.readline()
    getSerialValue7 = arduinoPort.readline()
    getSerialValue8 = arduinoPort.readline()
    print ('\nValor retornado del grado 1: %s',int(getSerialValue5))
    print ('\nValor retornado del grado 2: %s',int(getSerialValue6))
    print ('\nValor retornado del grado 3: %s',int(getSerialValue7))
    print ('\nValor retornado del grado 4: %s',int(getSerialValue8))
    
    print("Cantidad de muestras almacenadas")
    samples=samples_counter()
    print(samples)
    
# Cerrando puerto serial
arduinoPort.close()
