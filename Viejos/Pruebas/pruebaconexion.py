import serial
cont=1
ok=0
while(cont<=4):
    while(ok!="1"):
        try:
            arduino = serial.Serial("COM"+str(cont),9600)
            if(arduino.name!="arduino"):
                cont=cont+1
                print(arduino.name)
                arduino.close()
                ok=1
            else:
                print("Aun no encuentra la placa")
    print("Lo logre")
