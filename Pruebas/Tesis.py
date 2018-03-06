import psycopg2
import serial
import time

#FUNCION PARA DARLE FORMATO A LOS DATOS ANTES DE ENVIARLOS AL ARDUINO
def formatear_grados(grado):
    if(int(grado[0])<10):
        grado[0] = "00"+str(grado[0])
    else:
        if(int(grado[0])<100):
            grado[0]="0"+str(grado[0])
                
    if(int(grado[1])<10):
        grado[1] = "00"+str(grado[1])
    else:
        if(int(grado[1])<100):
            grado[1]="0"+str(grado[1])
                
    if(int(grado[2])<10):
        grado[2] = "00"+str(grado[2])
    else:
        if(int(grado[2])<100):
            grado[2]="0"+str(grado[2])

    if(int(grado[3])<10):
        grado[3] = "00"+str(grado[3])
    else:
        if(int(grado[3])<100):
            grado[3]="0"+str(grado[3])
                
    e = ","
    formato = str(grado[0])+str(grado[1])+str(grado[2])+str(grado[3])+e
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
    return row

#FUNCION PARA INSERTAR LOS VALORES OBTENIDOS POR LOS SENSORES A LA BASE DE DATOS
def insertar_datos(value):
    db=conectarBd()
    cur=db.cursor()
    cur.execute("INSERT INTO lectura(sensor1,sensor2,sensor3,sensor4) VALUES (%s,%s,%s,%s)",(value[0],value[1],value[2],value[3]))
    db.commit()
    cur.close()
    return 0

#FUNCION PARA REALIZAR EL CALCULO DE LOS ANGULOS
def calculo(value)
    data=extraer_min_max()
    
    return grado

#FUNCION PARA CONECTAR AL ARDUINO
##MEJORAR###########################
def conectarArd():
    puerto='/dev/ttyACM'
    ok=0
    i=0
    while(ok=0)
        arduino=serial.Serial(puerto+string(i),baudrate=9600, timeout = 3.0)    
        if(arduino.name='Arduino')
            ok=1
        else
            i++
    return arduino

#FUNCION PARA ENVIAR DATOS AL ARDUINO
def enviarDatos(cadena):
    #arduino=conectarArd()
    arduino.write(cadena) #Enviar grados al arduino
    time.sleep(0.1)
    arduino.close() #Finalizamos comunicacion
    
    return 0


#FUNCION PARA RECIBIR DATOS DEL ARDUINO
def recibirDatos():
    arduino=conectarArd()
    var1=arduino.read()
    var2=arduino.read()
    var3=arduino.read()
    var4=arduino.read()
    time.sleep(0.1)
    #arduino.close() #Finalizamos comunicacion
    
    return var1,var2,var3,var4


#COMIENZO DEL PROGRAMA

values=extraer_min_max()

#print("Datos extraidos de la base de datos")
#print(values[0])
#print(values[1])
#print(values[2])
#print(values[3])
#print(values[4])
#print(values[5])
#print(values[6])
#print(values[7])

datos=recibirDatos()

insertar_datos(datos)    

grado=calculo(datos)

cadena=formatear_grados(grado)

#print("Cadena a enviar al arduino")
#print(cadena)

#print("Enviando datos al arduino")
#datos=enviarDatos(cadena)


enviarDatos(cadena)

#print("Datos a guardar en la base de datos")
#valor1=input()
#valor2=input()
#valor3=input()
#valor4=input()

#insertar_datos(datos[0],datos[1],datos[2],datos[3])    

print("ok")
