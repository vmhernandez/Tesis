#####################LIBRERIAS#####################

import psycopg2

##########################FUNCIONES#####################

#FUNCION PARA DARLE FORMATO A LOS DATOS ANTES DE ENVIARLOS AL ARDUINO
def angle_formatting(angle):
    if(int(angle[0])<10):
        angle[0] = "00"+str(angle[0])
    else:
        if(int(angle[0])<100):
            angle[0]="0"+str(angle[0])
                
    if(int(angle[1])<10):
        angle[1] = "00"+str(angle[1])
    else:
        if(int(angle[1])<100):
            angle[1]="0"+str(angle[1])
                
    if(int(angle[2])<10):
        angle[2] = "00"+str(angle[2])
    else:
        if(int(angle[2])<100):
            angle[2]="0"+str(angle[2])

    if(int(angle[3])<10):
        angle[3] = "00"+str(angle[3])
    else:
        if(int(angle[3])<100):
            angle[3]="0"+str(angle[3])
                
    e = "\n"
    Format = str(angle[0])+","+str(angle[1])+","+str(angle[2])+","+str(angle[3])+e
    return Format

#FUNCION PARA CONECTAR A LA BASE DE DATOS
def conectDb():
    db = psycopg2.connect("host='localhost' user='postgres' dbname='arduino' password='Victor15'")
    return db

#FUNCION PARA EXTRAER LOS MINIMOS Y MAXIMOS DE LA BASE DE DATOS
def min_max_extract():
    db=conectDb()
    cur = db.cursor()
    cur.execute("SELECT MIN(sensor1),MAX(sensor1),MIN(sensor2),MAX(sensor2),MIN(sensor3),MAX(sensor3),MIN(sensor4),MAX(sensor4) FROM lectura")
    for row in cur.fetchall():
        print("")
    cur.close()
    return row

#FUNCION PARA EXTRAER LOS PROMEDIOS DE LA BASE DE DATOS
def avg_extract():
    db=conectDb()
    cur = db.cursor()
    cur.execute("SELECT AVG(sensor1),AVG(sensor2),AVG(sensor3),AVG(sensor4) FROM lectura")
    for row in cur.fetchall():
        print("")
    cur.close()
    return row

#FUNCION PARA EXTRAER LA CANTIDAD DE MUESTRAS ALMACENADAS EN LA BASE DE DATOS
def samples_counter():
    db=conectDb()
    cur = db.cursor()
    cur.execute("SELECT COUNT(*) FROM lectura")
    row=cur.fetchone()[0]
    return row

#FUNCION PARA EXTRAER LOS DATOS DE LA BASE DE DATOS
def angle_extract():
    db=conectDb()
    cur = db.cursor()
    cur.execute("SELECT servo1min,servo1max,servo2min,servo2max,servo3min,servo3max,servo4min,servo4max FROM servo ORDER BY fecha DESC LIMIT 1")
    for row in cur.fetchall():
        print("")
    cur.close()
    return row

#FUNCION PARA REALIZAR LOS CALCULOS DE LOS ANGULOS
def angle_calculation(data):

    angle=[0,0,0,0]
    
    value=min_max_extract()
    dbangle=angle_extract()
    
    angle[0]=dbangle[0]+(((data[0]-value[0])*(dbangle[1]-dbangle[0]))/(value[1]-value[0]))
    angle[1]=dbangle[2]+(((data[1]-value[2])*(dbangle[3]-dbangle[2]))/(value[3]-value[2]))
    angle[2]=dbangle[4]+(((data[2]-value[4])*(dbangle[5]-dbangle[4]))/(value[5]-value[4]))
    angle[3]=dbangle[6]+(((data[3]-value[6])*(dbangle[7]-dbangle[6]))/(value[7]-value[6]))
    
    return angle

#FUNCION PARA INSERTAR LOS VALORES OBTENIDOS POR LOS SENSORES A LA BASE DE DATOS
def data_insert(value):
    db=conectDb()
    cur=db.cursor()
    cur.execute("INSERT INTO lectura(sensor1,sensor2,sensor3,sensor4) VALUES (%s,%s,%s,%s)",(value[0],value[1],value[2],value[3]))
    db.commit()
    cur.close()
    return 0
