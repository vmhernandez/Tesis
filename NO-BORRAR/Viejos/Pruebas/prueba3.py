import serial, time

arduino = serial.Serial('COM4', 9600)

time.sleep(2)

while(True):
    comando="R"

    arduino.write(comando.encode())

    rS1 = arduino.readline()
    
    print("valores Sensor")
    print(rS1)
    
    arduino.write()
    
arduino.close()
