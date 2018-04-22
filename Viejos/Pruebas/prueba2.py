import serial, time
arduino = serial.Serial('COM4', 9600)
time.sleep(2)


arduino.write(b'180123123123')

rS1 = arduino.readline()
rS2 = arduino.readline()
rS3 = arduino.readline()
rS4 = arduino.readline()

if(arduino.readline()=="Y"):
    rS5 = arduino.readline()
    rS6 = arduino.readline()
    rS7 = arduino.readline()
    rS8 = arduino.readline()

print("valores Sensor")
print(rS1)
print(int(rS1))
print(rS2)
print(rS3)
print(rS4)
print("Valores Servo")
print(rS5)
print(rS6)
print(rS7)
print(rS8)

arduino.close()
