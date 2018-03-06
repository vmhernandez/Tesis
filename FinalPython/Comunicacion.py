#####################LIBRERIAS#####################

import time
import serial
import psycopg2

##########################FUNCIONES#####################

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
                
    e = "\n"
    formato = str(grado[0])+","+str(grado[1])+","+str(grado[2])+","+str(grado[3])+e
    return formato

#FUNCION PARA CONECTAR A LA BASE DE DATOS
def conectarBd():
    db = psycopg2.connect("host='localhost' user='postgres' dbname='arduino' password='Victor15'")
    return db

#FUNCION PARA EXTRAER LOS MINIMOS Y MAXIMOS DE LA BASE DE DATOS
def extraer_min_max():
    db=conectarBd()
    cur = db.cursor()
    cur.execute("SELECT MIN(sensor1),MAX(sensor1),MIN(sensor2),MAX(sensor2),MIN(sensor3),MAX(sensor3),MIN(sensor4),MAX(sensor4) FROM lectura")
    for row in cur.fetchall():
        print("")
    cur.close()
    return row

#FUNCION PARA EXTRAER LA CANTIDAD DE MUESTRAS ALMACENADAS EN LA BASE DE DATOS
def contador_muestras():
    db=conectarBd()
    cur = db.cursor()
    cur.execute("SELECT COUNT(*) FROM lectura")
    row=cur.fetchone()[0]
    return row

#FUNCION PARA EXTRAER LOS DATOS DE LA BASE DE DATOS
def extraer_angulos():
    db=conectarBd()
    cur = db.cursor()
    cur.execute("SELECT servo1min,servo1max,servo2min,servo2max,servo3min,servo3max,servo4min,servo4max FROM servo ORDER BY fecha DESC LIMIT 1")
    for row in cur.fetchall():
        print("")
    cur.close()
    return row

#FUNCION PARA REALIZAR LOS CALCULOS DE LOS ANGULOS
def calc_degree(data):
    value=extraer_min_max()
    dbdegree=extraer_angulos()
    ############FIX HERE###################
    contador=contador_muestras()
    degree=[0,0,0,0]
    degree[0]=dbdegree[0]+(((data[0]-value[0])*(dbdegree[1]-dbdegree[0]))/(value[1]-value[0]))

    degree[1]=dbdegree[2]+(((data[1]-value[2])*(dbdegree[3]-dbdegree[2]))/(value[3]-value[2]))

    degree[2]=dbdegree[4]+(((data[2]-value[4])*(dbdegree[5]-dbdegree[4]))/(value[5]-value[4]))

    degree[3]=dbdegree[6]+(((data[3]-value[6])*(dbdegree[7]-dbdegree[6]))/(value[7]-value[6]))
    
    return degree

#FUNCION PARA INSERTAR LOS VALORES OBTENIDOS POR LOS SENSORES A LA BASE DE DATOS
def insertar_datos(value):
    db=conectarBd()
    cur=db.cursor()
    cur.execute("INSERT INTO lectura(sensor1,sensor2,sensor3,sensor4) VALUES (%s,%s,%s,%s)",(value[0],value[1],value[2],value[3]))
    db.commit()
    cur.close()
    return 0

#FUNCION PARA REALIZAR LOS CALCULOS DE LOS ANGULOS
def calc_degree(data):
    value=extraer_min_max()
    dbdegree=extraer_angulos()
    contador=contador_muestras()
    degree=[0,0,0,0]
    degree[0]=dbdegree[0]+(((data[0]-value[0])*(dbdegree[1]-dbdegree[0]))/(value[1]-value[0]))

    degree[1]=dbdegree[2]+(((data[1]-value[2])*(dbdegree[3]-dbdegree[2]))/(value[3]-value[2]))

    degree[2]=dbdegree[4]+(((data[2]-value[4])*(dbdegree[5]-dbdegree[4]))/(value[5]-value[4]))

    degree[3]=dbdegree[6]+(((data[3]-value[6])*(dbdegree[7]-dbdegree[6]))/(value[7]-value[6]))
    
    return degree


#####################PROGRAMA#####################

# Iniciando conexion serial
arduinoPort = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
flagCharacter = 'R'

#Conectar a la Base de datos
conectarBd()

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
    
    datos= [int(getSerialValue1),int(getSerialValue2),int(getSerialValue3),int(getSerialValue4)]
    
    
    print("Cantidad de muestras almacenadas")
    muestras=contador_muestras()
    print(muestras)
    
    #Calculo grados
    val = calc_degree(datos)
    
    print ('\nGrado 1: %s',val[0])
    print ('\nGrado 2: %s',val[1])
    print ('\nGrado 3: %s',val[2])
    print ('\nGrado 4: %s',val[3])
    
    #Insertar datos en la Base de datos
    insertar_datos(datos)
    
    #Formateo de datos para enviar al Arduino
    grados = formatear_grados(val)
    
    #Enviar datos al Arduino
    arduinoPort.write(grados.encode())
 
    getSerialValue5 = arduinoPort.readline()
    getSerialValue6 = arduinoPort.readline()
    getSerialValue7 = arduinoPort.readline()
    getSerialValue8 = arduinoPort.readline()
    print ('\nValor retornado del grado 1: %s',int(getSerialValue5))
    print ('\nValor retornado del grado 2: %s',int(getSerialValue6))
    print ('\nValor retornado del grado 3: %s',int(getSerialValue7))
    print ('\nValor retornado del grado 4: %s',int(getSerialValue8))
    
    print("Cantidad de muestras almacenadas")
    muestras=contador_muestras()
    print(muestras)
    
# Cerrando puerto serial
arduinoPort.close()
