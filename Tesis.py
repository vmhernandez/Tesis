import psycopg2
import serial
import time

#FUNCION PARA DARLE FORMATO A LOS DATOS ANTES DE ENVIARLOS AL ARDUINO
def formatear_grados(grado1,grado2,grado3,grado4):
    if(int(grado1)<10):
        grado1 = "00"+str(grado1)
    else:
        if(int(grado1)<100):
            grado1="0"+str(grado1)
                
    if(int(grado2)<10):
        grado2 = "00"+str(grado2)
    else:
        if(int(grado2)<100):
            grado2="0"+str(grado2)
                
    if(int(grado3)<10):
        grado3 = "00"+str(grado3)
    else:
        if(int(grado3)<100):
            grado3="0"+str(grado3)

    if(int(grado4)<10):
        grado4 = "00"+str(grado4)
    else:
        if(int(grado4)<100):
            grado4="0"+str(grado4)
                
    e = ","
    formato = str(grado1)+str(grado1)+str(grado3)+str(grado4)+e
    return formato

#FUNCION PARA CONECTAR A LA BASE DE DATOS
def conectarBd():
    db = psycopg2.connect("host='localhost' user='postgres' dbname='arduino' password='Victor15'")
    return db

#FUNCION PARA EXTRAER LOS DATOS DE LA BASE DE DATOS
def extraer_min_max():
    db=conectarBd()
    cur = db.cursor()
    cur.execute("SELECT * FROM servo ORDER BY fecha DESC LIMIT 1")
    for row in cur.fetchall():
        print("")
    cur.close()
    return row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]

#FUNCION PARA INSERTAR LOS VALORES OBTENIDOS POR LOS SENSORES A LA BASE DE DATOS
def insertar_datos(value1,value2,value3,value4):
    db=conectarBd()
    cur=db.cursor()
    cur.execute("INSERT INTO lectura(sensor1,sensor2,sensor3,sensor4) VALUES (%s,%s,%s,%s)",(value1,value2,value3,value4))
    db.commit()
    cur.close()
    return 0

#FUNCION PARA CONECTAR AL ARDUINO
def conectarArd():
    arduino=serial.Serial('/dev/ttyACM1',baudrate=9600, timeout = 3.0)

    return arduino

#FUNCION PARA ENVIAR DATOS AL ARDUINO
def enviarDatos(cadena):
    txt = ''
    arduino=conectarArd()
    arduino.write(cadena) #Enviar grados al arduino
    time.sleep(0.1)
    arduino.close() #Finalizamos comunicacion
    
    return 0



#COMIENZO DEL PROGRAMA
values=extraer_min_max()

print("Datos extraidos de la base de datos")
print(values[0])
print(values[1])
print(values[2])
print(values[3])
print(values[4])
print(values[5])
print(values[6])
print(values[7])

cadena=formatear_grados(values[4],values[2],values[3],values[0])

print("Cadena a enviar al arduino")
print(cadena)

print("Enviando datos al arduino")
#enviarDatos(cadena)

print("Datos a guardar en la base de datos")
valor1=input()
valor2=input()
valor3=input()
valor4=input()

insertar_datos(valor1,valor2,valor3,valor4)    

print("ok")
