import time
import serial
 
# Iniciando conexión serial
arduinoPort = serial.Serial('COM4', 9600, timeout=1)
flagCharacter = 'R'
grados ='001,004,005,090\n'
# Retardo para establecer la conexión serial
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
    
    arduinoPort.write(grados.encode())
 
    getSerialValue5 = arduinoPort.readline()
    getSerialValue6 = arduinoPort.readline()
    getSerialValue7 = arduinoPort.readline()
    getSerialValue8 = arduinoPort.readline()
    print ('\nValor retornado del grado 1: %s',int(getSerialValue5))
    print ('\nValor retornado del grado 2: %s',int(getSerialValue6))
    print ('\nValor retornado del grado 3: %s',int(getSerialValue7))
    print ('\nValor retornado del grado 4: %s',int(getSerialValue8))

    
# Cerrando puerto serial
arduinoPort.close()
