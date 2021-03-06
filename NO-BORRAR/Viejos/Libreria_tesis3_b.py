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
        if(int(angle[x])<10):
        
            angle[x] = "00"+str(angle[x])
        
        else:
        
            if(int(angle[x])<100):
            
                angle[x]="0"+str(angle[x])

    for x in range(0,4):
        if(int(angle[x])<0):
            numero[x]=1
            angle[x]=angle[x]*(-1)

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

#FUNCION PARA EXTRAER LA MEDIANA DE LOS DATOS OBTENIDOS POR LOS SENSORES

def median():
    
    median=[0,0,0,0]
    
    db=conectDb()
    
    cur = db.cursor()
    
    cur.execute("SELECT median(sensor1),median(sensor2),median(sensor3),median(sensor4) FROM lectura")
    
    row = cur.fetchone()
        
    cur.close()
    
    for x in range(0,4):
        
        median[x]=str(int(row[x]))
    
    return median

#FUNCION PARA CALCULAR Q1

def q1(value):
    
    data=[0,0,0,0]
    
    db=conectDb()
    
    cur = db.cursor()
    
    cur.execute("SELECT median(sensor1) FROM lectura WHERE sensor1 <= (%s);", (value[0],))

    row=cur.fetchone()[0]
    
    data[0]=row
    
    cur.execute("SELECT median(sensor2) FROM lectura WHERE sensor2 <= (%s);", (value[1],))

    row=cur.fetchone()[0]
    
    data[1]=row
    
    cur.execute("SELECT median(sensor3) FROM lectura WHERE sensor3 <= (%s);", (value[2],))

    row=cur.fetchone()[0]
    
    data[2]=row
    
    cur.execute("SELECT median(sensor4) FROM lectura WHERE sensor4 <= (%s);", (value[3],))

    row=cur.fetchone()[0]
    
    data[3]=row
    
    return data

#FUNCION PARA CALCULAR Q3

def q3(value):
    
    data=[0,0,0,0]
    
    db=conectDb()
    
    cur = db.cursor()
    
    cur.execute("SELECT median(sensor1) FROM lectura WHERE sensor1 >= (%s);", (value[0],))

    row=cur.fetchone()[0]
    
    data[0]=row
    
    cur.execute("SELECT median(sensor2) FROM lectura WHERE sensor2 >= (%s);", (value[1],))

    row=cur.fetchone()[0]
    
    data[1]=row
    
    cur.execute("SELECT median(sensor3) FROM lectura WHERE sensor3 >= (%s);", (value[2],))

    row=cur.fetchone()[0]
    
    data[2]=row
    
    cur.execute("SELECT median(sensor4) FROM lectura WHERE sensor4 >= (%s);", (value[3],))

    row=cur.fetchone()[0]
    
    data[3]=row
    
    return data

#FUNCION PARA CALCULAR LOS LIMITES INTERNOS SUPERIORES DE LOS DATOS ALMACENADOS EN LA BASE DE DATOS

def isl():
        
    row=[0,0,0,0]
    
    Median=median()
    
    Q1=q1(Median)
    
    Q3=q3(Median)
    
    for x in range(0,4):
        
        row[x]=Q3[x]+((Q3[x]-Q1[x])*1.5)

    return row

###############Controlador
def controller(arduinoPort):
    min=[0,0,0,0]
    max=[0,0,0,0]
    iSl=[0,0,0,0]
    flagCharacter = 'R'
    
    while(True):
    
        samples=samples_counter()
        
        print("Cantidad de muestras almacenadas")   
        print(samples)
       
        if(samples>=2):
            
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
            iSl=isl()
            
            if(data[0]<=iSl[0] and data[1]<=iSl[1] and data[2]<=iSl[2] and data[2]<=iSl[2] ):
                #Calculo grados
                
                val = angle_calculation(data)
            
                print ('\nGrado 1: %s',int(val[0]))
                print ('\nGrado 2: %s',int(val[1]))
                print ('\nGrado 3: %s',int(val[2]))
                print ('\nGrado 4: %s',int(val[3]))
                
                #Insertar datos en la Base de datos
                
                data_insert(data,val)
                
                #Formateo de datos para enviar al Arduino

                angle = angle_formatting(val)
                
                #Enviar datos al Arduino

                arduinoPort.write(angle.encode())
             
                getSerialValue5 = arduinoPort.readline()
                getSerialValue6 = arduinoPort.readline()
                getSerialValue7 = arduinoPort.readline()
                getSerialValue8 = arduinoPort.readline()
                
                print ('\nGrado 1: %s',getSerialValue5)
                print ('\nGrado 2: %s',getSerialValue6)
                print ('\nGrado 3: %s',getSerialValue7)
                print ('\nGrado 4: %s',getSerialValue8)
            ##AQUI IRIA LO QUE DEBE PASAR EN EL MOMENTO EN QUE LAS LECTURAS DE LOS SENSORES SEAN MAYORES A LOS LIMITES INTERNOS SUPERIORES
                
        if(samples<2):
            print("ENTRENANDO")
            time.sleep(2)
            angle=angle_extract()
            
            anglemin=[angle[0],angle[2],angle[4],angle[6]]
            anglemax=[angle[1],angle[3],angle[5],angle[7]]
            
            ##############REALIZA UNA LECTURA PREVIA PARA REALIZAR LAS COMPARACIONES POSTERIORES###
            arduinoPort.write(flagCharacter.encode())
            getSerialValue1 = arduinoPort.readline()
            getSerialValue2 = arduinoPort.readline()
            getSerialValue3 = arduinoPort.readline()
            getSerialValue4 = arduinoPort.readline()
        
            min=[getSerialValue1,getSerialValue2,getSerialValue3,getSerialValue4]
            max=[getSerialValue1,getSerialValue2,getSerialValue3,getSerialValue4]    
            
            for i in range(0,4):
                print(min[i])
                print(max[i])
                print(angle[(2*i)])
                print(angle[(2*i)+1])
                
            print("RELAJAR MUSCULO")
            time.sleep(2)
            for x in range(0,15):##COMO JUSTIFICO ESTE ENTRENAMIENTO????
                
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
                for i in range(0,4):
                    if(data[i]<min[i]):
                        min[i]=data[i]
                time.sleep(1)
                
            print("CONTRAER MUSCULO")
            time.sleep(2)
            for x in range(0,15):##COMO JUSTIFICO ESTE ENTRENAMIENTO????
                
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
                for i in range(0,4):
                    if(data[i]>max[i]):
                        max[i]=data[i]
                time.sleep(0.5)        
            
            ###############GUARDAR EN LA BASE DE DATOS#########
            data_insert(min,anglemin)
            data_insert(max,anglemax)
            
            for i in range(0,4):
                print(min[i])
                print(max[i])
            print("FIN DEL ENTRENAMIENTO")

    return 0
