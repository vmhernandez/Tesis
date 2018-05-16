import psycopg2

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

print("Cantidad de muestras almacenadas")
muestras=contador_muestras()
print(muestras)

print("Calculo de angulo")
numero=[300,250,364,400]
degree=calc_degree(numero)

print(degree[0])
print(degree[1])
print(degree[2])
print(degree[3])
