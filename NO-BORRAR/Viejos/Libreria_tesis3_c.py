#####################LIBRERIAS#####################

import psycopg2
import xlwt
import datetime
import time

##########################FUNCIONES#####################

#FUNCION PARA DARLE FORMATO A LOS DATOS ANTES DE ENVIARLOS AL ARDUINO
def angle_formatting(angle):
    
    numero=[0,0,0,0]
    for x in range(0,4):
        if(int(angle[x])<0):
            numero[x]=1
            angle[x]=angle[x]*(-1)
    for x in range(0,4):
        if(int(angle[x])<10):
        
            angle[x] = "00"+str(angle[x])
        
        else:
        
            if(int(angle[x])<100):
            
                angle[x]="0"+str(angle[x])

    e = "\n"
    
    Format = str(angle[0])+","+str(angle[1])+","+str(angle[2])+","+str(angle[3])+","+str(numero[0])+","+str(numero[1])+","+str(numero[2])+","+str(numero[3])+e
    
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

#FUNCION PARA EXTRAER LOS PROMEDIOS DE LAS LECTURAS DE LOS SENSORES DE LA BASE DE DATOS
def avg_x():
    
    db=conectDb()
    
    cur = db.cursor()
    
    cur.execute("SELECT AVG(sensor1),AVG(sensor2),AVG(sensor3),AVG(sensor4) FROM lectura")
    
    for row in cur.fetchall():
        
        print()
        
    cur.close()
    
    return row

#FUNCION PARA EXTRAER LOS PROMEDIOS DE LOS ANGULOS DE LA BASE DE DATOS
def avg_y():
    
    db=conectDb()
    
    cur = db.cursor()
    
    cur.execute("SELECT AVG(angle1),AVG(angle2),AVG(angle3),AVG(angle4) FROM lectura")
    
    for row in cur.fetchall():
        
        print()
        
    cur.close()
    
    return row

#FUNCION PARA CALCULAR LA VARIANZA
def var(square,n,avg):
    
    var=[0,0,0,0]
    
    for x in range(0,4):
        
        for y in range(0,n):
            
            var[x]=var[x]+(((int(square[y][x])-int(avg[x]))**2)/n)
    
    return var

#FUNCION PARA CALCULAR LA VARIANZA DE LAS MUESTRAS OBTENIDAS POR LOS SENSORES ALMACENADAS EN LA BASE DE DATOS
def var_x(avgX):
    
    varX=[0,0,0,0]
    
    n=samples_counter()
    
    db=conectDb()
    
    cur = db.cursor()
    
    cur.execute("SELECT sensor1,sensor2,sensor3,sensor4 FROM lectura")
    
    rows = cur.fetchall()

    cur.close()
        
    varX = var(rows,n,avgX)
    
    return varX

#FUNCION PARA CALCULAR LA COVARIANZA
def covar(mult,n,avgX,avgY):
    
    covar=[0,0,0,0]
    
    for x in range(0,n):
        for y in range(0,4):
            covar[y]=covar[y]+(((mult[x][y]-avgX[y])*(mult[x][y+4]-avgY[y]))/(n))
        
    return covar

#FUNCION PARA CALCULAR LA COVARIANZA
def covarXY(avgX,avgY):
    
    covarXY=[0,0,0,0]
    
    db=conectDb()
    
    cur = db.cursor()
    
    cur.execute("SELECT sensor1,sensor2,sensor3,sensor4,angle1,angle2,angle3,angle4 FROM lectura")
    
    rows = cur.fetchall()
        
    cur.close()
    
    n=samples_counter()
    
    covarXY =covar(rows,n,avgX,avgY)
    
    return covarXY

#FUNCION PARA REALIZAR LOS CALCULOS DE LOS ANGULOS REGRESION LINEAL
def angle_calculation(data):

    angle=[0,0,0,0]
    
    dbangle=[0,0,0,0,0,0,0,0]
    
    avgX = avg_x()
    
    avgY = avg_y()
    
    varX = var_x(avgX)
    
    coVar = covarXY(avgX,avgY)
    
    dbangle=angle_extract()
    
    ##Calculo de angulo
        
    for x in range(0,4):
        angle[x]=int((float(coVar[x])/varX[x])*(data[x]-float(avgX[x]))+float(avgY[x]))
    
    
    for x in range(0,4):
        if(dbangle[x*2]>dbangle[(x*2)+1]):
            auxangle=dbangle[x*2]
            dbangle[x*2]=dbangle[(x*2)+1]
            dbangle[(x*2)+1]=auxangle
    
    for x in range(0,4):
        if(angle[x]>dbangle[(x*2)+1]):
            angle[x]=dbangle[(x*2)+1]
        else:
            if(angle[x]<dbangle[x*2]):
                angle[x]=dbangle[x*2]    
        
    return angle

#FUNCION PARA INSERTAR LOS VALORES OBTENIDOS POR LOS SENSORES A LA BASE DE DATOS
def data_insert(data,value):
    db=conectDb()
    cur=db.cursor()
    cur.execute("INSERT INTO lectura(sensor1,sensor2,sensor3,sensor4,angle1,angle2,angle3,angle4) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(data[0],data[1],data[2],data[3],value[0],value[1],value[2],value[3]))
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
    
    cur.execute("UPDATE lectura SET angle1=%s WHERE sensor1=%s",(dbangle[0],value[0]))
    db.commit()
    
    cur.execute("UPDATE lectura SET angle1= %s WHERE sensor1=%s",(dbangle[1],value[1]))
    db.commit()
    
    cur.execute("UPDATE lectura SET angle2= %s WHERE sensor2=%s",(dbangle[2],value[2]))
    db.commit()
    
    cur.execute("UPDATE lectura SET angle2= %s WHERE sensor2=%s",(dbangle[3],value[3]))
    db.commit()
    
    cur.execute("UPDATE lectura SET angle3= %s WHERE sensor3=%s",(dbangle[4],value[4]))
    db.commit()
    
    cur.execute("UPDATE lectura SET angle3= %s WHERE sensor3=%s",(dbangle[5],value[5]))
    db.commit()
    
    cur.execute("UPDATE lectura SET angle4= %s WHERE sensor4=%s",(dbangle[6],value[6]))
    db.commit()
    
    cur.execute("UPDATE lectura SET angle4= %s WHERE sensor4=%s",(dbangle[7],value[7]))
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

#FUNCION PARA CALCULAR LOS LIMITES INTERNOS DE LOS DATOS MEDIANTE MAD (MEDIAN ABSOLUTE DEVIATION)
def outlier():
    
    db=conectDb()
    
    cur = db.cursor()
    
    cur.execute("select median(sensor1)-2.5*median(abs(sensor1 - (select median(sensor1) from lectura))),median(sensor1)+2.5*median(abs(sensor1 - (select median(sensor1) from lectura))),median(sensor2)-2.5*median(abs(sensor2 - (select median(sensor2) from lectura))),median(sensor2)+2.5*median(abs(sensor2 - (select median(sensor2) from lectura))),median(sensor3)-2.5*median(abs(sensor3 - (select median(sensor3) from lectura))),median(sensor3)+2.5*median(abs(sensor3 - (select median(sensor3) from lectura))),median(sensor4)-2.5*median(abs(sensor4 - (select median(sensor4) from lectura))),median(sensor4)+2.5*median(abs(sensor4 - (select median(sensor4) from lectura))) from lectura")

    for row in cur.fetchall():
    
        print()
        
    cur.close()
    
    return row

def training(arduinoPort,flagCharacter):
    
    print("ENTRENANDO")
            
    angle=angle_extract()
            
    anglemin=[angle[0],angle[2],angle[4],angle[6]]
    anglemax=[angle[1],angle[3],angle[5],angle[7]]
            
    suma1=[0,0,0,0]
    suma2=[0,0,0,0]
    
    min=[0,0,0,0]
    max=[0,0,0,0]
    
    arduinoPort.write(flagCharacter.encode())

    getSerialValue1 = arduinoPort.readline()
    getSerialValue2 = arduinoPort.readline()
    getSerialValue3 = arduinoPort.readline()
    getSerialValue4 = arduinoPort.readline()
    
    min=[int(getSerialValue1),int(getSerialValue2),int(getSerialValue3),int(getSerialValue4)]
    max=[int(getSerialValue1),int(getSerialValue2),int(getSerialValue3),int(getSerialValue4)]
    
    print("RELAJAR MUSCULO")
            
    time.sleep(3)
            
    for x in range(0,101):
                
        arduinoPort.write(flagCharacter.encode())

        getSerialValue1 = arduinoPort.readline()
        getSerialValue2 = arduinoPort.readline()
        getSerialValue3 = arduinoPort.readline()
        getSerialValue4 = arduinoPort.readline()
        print ('\nValor retornado de Arduino 1: %s',int(getSerialValue1))
##                print ('\nValor retornado de Arduino 2: %s',int(getSerialValue2))
##                print ('\nValor retornado de Arduino 3: %s',int(getSerialValue3))
##                print ('\nValor retornado de Arduino 4: %s',int(getSerialValue4))
                
##        suma1[0]=suma1[0]+int(getSerialValue1)
##        suma1[1]=suma1[1]+int(getSerialValue2)
##        suma1[2]=suma1[2]+int(getSerialValue3)
##        suma1[3]=suma1[3]+int(getSerialValue4)
        
        if(int(getSerialValue1)<int(min[0])):
            min[0]=int(getSerialValue1)
            
        if(int(getSerialValue2)<int(min[1])):
            min[1]=int(getSerialValue2)
            
        if(int(getSerialValue3)<int(min[2])):
            min[2]=int(getSerialValue3)
            
        if(int(getSerialValue4)<int(min[3])):
            min[3]=int(getSerialValue4)
            
        time.sleep(0.1)
                
    print("CONTRAER MUSCULO")
            
    time.sleep(3)
            
    for x in range(0,101):
                
        arduinoPort.write(flagCharacter.encode())

        getSerialValue1 = arduinoPort.readline()
        getSerialValue2 = arduinoPort.readline()
        getSerialValue3 = arduinoPort.readline()
        getSerialValue4 = arduinoPort.readline()
        print ('\nValor retornado de Arduino 1: %s',int(getSerialValue1))
##                print ('\nValor retornado de Arduino 2: %s',int(getSerialValue2))
##                print ('\nValor retornado de Arduino 3: %s',int(getSerialValue3))
##                print ('\nValor retornado de Arduino 4: %s',int(getSerialValue4))
            
##        suma2[0]=suma2[0]+int(getSerialValue1)
##        suma2[1]=suma2[1]+int(getSerialValue2)
##        suma2[2]=suma2[2]+int(getSerialValue3)
##        suma2[3]=suma2[3]+int(getSerialValue4)

        if(int(getSerialValue1)>int(max[0])):
            max[0]=int(getSerialValue1)
            
        if(int(getSerialValue2)>int(max[1])):
            max[1]=int(getSerialValue2)
            
        if(int(getSerialValue3)>int(max[2])):
            max[2]=int(getSerialValue3)
            
        if(int(getSerialValue4)>int(max[3])):
            max[3]=int(getSerialValue4)
            
        time.sleep(0.1)
                
            ###############GUARDAR EN LA BASE DE DATOS#########
##    for x in range(0,4):
##        min[x]=suma1[x]/101
##        max[x]=suma2[x]/101
                
    for i in range(0,4):
        print(min[i])
        print(max[i])
    print("FIN DEL ENTRENAMIENTO")

    data_insert(min,anglemin)
    data_insert(max,anglemax)
    
def execution(arduinoPort,flagCharacter):
    
    arduinoPort.write(flagCharacter.encode())

    getSerialValue1 = arduinoPort.readline()
    getSerialValue2 = arduinoPort.readline()
    getSerialValue3 = arduinoPort.readline()
    getSerialValue4 = arduinoPort.readline()
            
    print ('\nSensor 1: %s',int(getSerialValue1))
    print ('\nSensor 2: %s',int(getSerialValue2))
    print ('\nSensor 3: %s',int(getSerialValue3))
    print ('\nSensor 4: %s',int(getSerialValue4))
            
    data= [int(getSerialValue1),int(getSerialValue2),int(getSerialValue3),int(getSerialValue4)]

##    val = angle_calculation(data)
##    data_insert(data,val)
##    angle = angle_formatting(val)
##    arduinoPort.write(angle.encode())
##             
##    getSerialValue5 = arduinoPort.readline()
##    getSerialValue6 = arduinoPort.readline()
##    getSerialValue7 = arduinoPort.readline()
##    getSerialValue8 = arduinoPort.readline()

    limits=outlier()

    for x in range(0,8):
        print(limits[x])
        
    ##if(data[0]>=limits[0] and data[0]<=limits[1] and data[1]>=limits[2] and data[1]<=limits[3] and data[2]>=limits[4] and data[2]<=limits[5] and data[3]>=limits[6] and data[3]<=limits[7]):
    if(data[0]>=limits[0] and data[0]<=limits[1]):
                
        val = angle_calculation(data)         
        print ('\nGrado 1: %s',int(val[0]))
        print ('\nGrado 2: %s',int(val[1]))
        print ('\nGrado 3: %s',int(val[2]))
        print ('\nGrado 4: %s',int(val[3]))     
        data_insert(data,val)
        angle = angle_formatting(val)
        arduinoPort.write(angle.encode())
             
        getSerialValue5 = arduinoPort.readline()
        getSerialValue6 = arduinoPort.readline()
        getSerialValue7 = arduinoPort.readline()
        getSerialValue8 = arduinoPort.readline()
                
        print ('\nGrado 1: %s',getSerialValue5)
        print ('\nGrado 2: %s',getSerialValue6)
        print ('\nGrado 3: %s',getSerialValue7)
        print ('\nGrado 4: %s',getSerialValue8)
     
###############Controlador
def controller(arduinoPort):

    limits=[0,0,0,0,0,0,0,0]

    flagCharacter = 'R'
    
    while(True):
    
        samples=samples_counter()
        
        print("Cantidad de muestras almacenadas")   
        print(samples)
       
        if(samples>=2):
            execution(arduinoPort,flagCharacter)    
                
        if(samples<2):
                training(arduinoPort,flagCharacter)
    return 0