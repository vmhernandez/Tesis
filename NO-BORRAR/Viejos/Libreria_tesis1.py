#####################LIBRERIAS#####################

import psycopg2
import xlwt
import datetime

##########################FUNCIONES#####################

#FUNCION PARA DARLE FORMATO A LOS DATOS ANTES DE ENVIARLOS AL ARDUINO
def angle_formatting(angle):
    
    for x in range(0,4):
        if(int(angle[x])<10):
        
            angle[x] = "00"+str(angle[x])
        
        else:
        
            if(int(angle[x])<100):
            
                angle[x]="0"+str(angle[x])
                  
    e = "\n"
    
    Format = str(angle[0])+","+str(angle[1])+","+str(angle[2])+","+str(angle[3])+e
    
    return Format

#FUNCION PARA CONECTAR A LA BASE DE DATOS
def conectDb():
    
    db = psycopg2.connect("host='localhost' user='postgres' dbname='arduino' password='Victor15'")
    
    return db
#FUNCION PARA EXPORTAR DATOS EN UN ARCHIVO XLS
def export_data_to_xls():
    
    samples=samples_counter()

    book=xlwt.Workbook(encoding="utf-8")

    sheet1=book.add_sheet("Sensor")

    sheet1.write(0,0,"Sensor1")
    sheet1.write(0,1,"Sensor2")
    sheet1.write(0,2,"Sensor3")
    sheet1.write(0,3,"Sensor4")
    sheet1.write(0,4,"TimeStamp")
    sheet1.write(0,5,"Angulo1")
    sheet1.write(0,6,"Angulo2")
    sheet1.write(0,7,"Angulo3")
    sheet1.write(0,8,"Angulo4")

    db=conectDb()
    
    cur = db.cursor()
    
    cur.execute("SELECT * FROM lectura ORDER BY fecha")
    
    rows = cur.fetchall()

    cur.close()
    
    fila=0
    
    for n in range(0,samples):
        for i in range(0,9):
            fila=n+1
            sheet1.write(fila,i,rows[n][i])
    
    book.save(str(datetime.datetime.now())+".xls")

    return 0

#FUNCION PARA EXTRAER LOS MINIMOS Y MAXIMOS DE LA BASE DE DATOS
def min_max_extract():
    
    db=conectDb()
    
    cur = db.cursor()
    
    cur.execute("SELECT MIN(sensor1),MAX(sensor1),MIN(sensor2),MAX(sensor2),MIN(sensor3),MAX(sensor3),MIN(sensor4),MAX(sensor4) FROM lectura")
    
    for row in cur.fetchall():
        
        print()
        
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
   
    row=[0,0,0,0,0,0,0,0]
    
    db=conectDb()
    
    cur = db.cursor()
    
    cur.execute("SELECT servo1min,servo1max,servo2min,servo2max,servo3min,servo3max,servo4min,servo4max FROM servo WHERE id=(SELECT MAX(id) FROM servo)")
   
    for row in cur.fetchall():
        
        print()
        
    cur.close()
    
    return row

#FUNCION PARA REALIZAR LOS CALCULOS DE LOS ANGULOS ECUACION DE LA RECTA
def angle_calculation(data):

    angle=[1,0,0,0]
    
    value=min_max_extract()
    
    dbangle=angle_extract()
    
    angle[0]=int(dbangle[0]+(((data[0]-value[0])*(dbangle[1]-dbangle[0]))/(value[1]-value[0])))
    angle[1]=int(dbangle[2]+(((data[1]-value[2])*(dbangle[3]-dbangle[2]))/(value[3]-value[2])))
    angle[2]=int(dbangle[4]+(((data[2]-value[4])*(dbangle[5]-dbangle[4]))/(value[5]-value[4])))
    angle[3]=int(dbangle[6]+(((data[3]-value[6])*(dbangle[7]-dbangle[6]))/(value[7]-value[6])))
    
    for x in range(0,4):
        if(angle[x]>dbangle[(x*2)+1]):
            angle[x]=dbangle[(x*2)+1]
        else:
            if(angle[x]<dbangle[x*2]):
                angle[x]=dbangle[x*2]
        
    return angle

#FUNCION PARA INSERTAR LOS VALORES OBTENIDOS POR LOS SENSORES A LA BASE DE DATOS
def data_insert(value):
    
    db=conectDb()
    
    cur=db.cursor()
    
    cur.execute("INSERT INTO lectura(sensor1,sensor2,sensor3,sensor4) VALUES (%s,%s,%s,%s)",(value[0],value[1],value[2],value[3]))
    db.commit()
    
    cur.close()
    
    return 0

#FUNCION PARA VACIAR LAS LECTURAS DE LA BASE DE DATOS
def drop_data():
    
    db=conectDb()
    
    cur=db.cursor()
    
    cur.execute("DELETE FROM lectura")
    db.commit()
    
    cur.close()
    
    return 0

#FUNCION PARA VACIAR LAS LECTURAS DE LA BASE DE DATOS
def data_update():

    value=min_max_extract()
    
    dbangle=angle_extract()

    db=conectDb()
    
    cur=db.cursor()
    
    cur.execute("UPDATE lectura SET angle1= %s WHERE sensor1=(SELECT MAX(sensor1) FROM lectura)"),(dbangle[1])
    db.commit()
    
    cur.execute("UPDATE lectura SET angle1= %s WHERE sensor1=(SELECT MIN(sensor1) FROM lectura)"),(dbangle[0])
    db.commit()
    
    cur.execute("UPDATE lectura SET angle2= %s WHERE sensor2=(SELECT MAX(sensor2) FROM lectura)"),(dbangle[3])
    db.commit()
    
    cur.execute("UPDATE lectura SET angle2= %s WHERE sensor2=(SELECT MIN(sensor2) FROM lectura)"),(dbangle[2])
    db.commit()
    
    cur.execute("UPDATE lectura SET angle3= %s WHERE sensor3=(SELECT MAX(sensor3) FROM lectura)"),(dbangle[5])
    db.commit()
    
    cur.execute("UPDATE lectura SET angle3= %s WHERE sensor3=(SELECT MIN(sensor3) FROM lectura)"),(dbangle[4])
    db.commit()
    
    cur.execute("UPDATE lectura SET angle4= %s WHERE sensor4=(SELECT MAX(sensor4) FROM lectura)"),(dbangle[7])
    db.commit()
    
    cur.execute("UPDATE lectura SET angle4= %s WHERE sensor4=(SELECT MIN(sensor4) FROM lectura)"),(dbangle[6])
    db.commit()
    
    cur.close()
    
    return 0

#FUNCION PARA ACTUALIZAR LOS ANGULOS EN LA BASE DE DATOS
def update_angle(value):
    
    db=conectDb()
    
    cur=db.cursor()
    
    cur.execute("INSERT INTO servo(servo1min,servo1max,servo2min,servo2max,servo3min,servo3max,servo4min,servo4max) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(value[0],value[1],value[2],value[3],value[4],value[5],value[6],value[7]))
    db.commit()
    
    cur.close()
    
    return 0

#FUNCION PARA ELIMINAR EL ULTIMO ANGULO EN LA BASE DE DATOS
def drop_last_angle():
    
    db=conectDb()
    
    cur=db.cursor()
    
    cur.execute("DELETE FROM servo WHERE fecha=(SELECT MAX(FECHA) FROM servo)")
    db.commit()
    
    cur.close()
    
    return 0

###############Controlador
def controller(arduinoPort):
    
    flagCharacter = 'R'
    
    print("Cantidad de muestras almacenadas")
    
    samples=samples_counter()
    
    print(samples)
    
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

    if(samples<2):
                
        data_insert(data)
        
    else:
        #Calculo grados
        
        val = angle_calculation(data)
    
        print ('\nGrado 1: %s',int(val[0]))
        print ('\nGrado 2: %s',int(val[1]))
        print ('\nGrado 3: %s',int(val[2]))
        print ('\nGrado 4: %s',int(val[3]))
        
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
        
        print ('\nValor retornado del grado 1: %s',getSerialValue5)
        print ('\nValor retornado del grado 2: %s',getSerialValue6)
        print ('\nValor retornado del grado 3: %s',getSerialValue7)
        print ('\nValor retornado del grado 4: %s',getSerialValue8)
        
        print("Cantidad de muestras almacenadas")
        
        samples=samples_counter()
        
        print(samples)
        
        return 0