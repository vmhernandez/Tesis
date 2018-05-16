from Libreria_tesis import update_angle,drop_data,angle_extract,update_angle,drop_last_angle,samples_counter,conectDb,export_data_to_xls

def close():
    exit()
    
def update():
    newAngle =[0,0,0,0,0,0,0,0]
    print("Actualizar angulos")
    angle=angle_extract()
    print("Servo 1\n","Minimo: ",angle[0],"Maximo: ",angle[1])
    print("Servo 2\n","Minimo: ",angle[2],"Maximo: ",angle[3])
    print("Servo 3\n","Minimo: ",angle[4],"Maximo: ",angle[5])
    print("Servo 4\n","Minimo: ",angle[6],"Maximo: ",angle[7])
    print("\nServo 1\n")
    print(angle[0],"->")
    x0=input()
    print(angle[1],"->")
    x1=input()
    print("\nServo 2\n")
    print(angle[2],"->")
    x2=input()
    print(angle[3],"->")
    x3=input()
    print("\nServo 3\n")
    print(angle[4],"->")
    x4=input()
    print(angle[5],"->")
    x5=input()
    print("\nServo 4\n")
    print(angle[6],"->")
    x6=input()
    print(angle[7],"->")
    x7=input()
    newAngle=[x0,x1,x2,x3,x4,x5,x6,x7]
    update_angle(newAngle)
    
def delete():
    print("Eliminar muestras")
    drop_data()

def delete_angle():
    print("Eliminar ultimo angulo")
    drop_last_angle()


#####CORREGIR######
def export():
    export_data_to_xls()
    
options ={0: close,
          1: update,
          2: delete,
          3: delete_angle,
          4: export
    }

def menu():
    op=1
    while(op<4 or op>0):
        print("0->Close\n1->Update Servo Angle\n2->Delete Samples\n3->Delete Last Angle\n4->Export to .XLS")
        op = int(input())
        if(op>=0 and op<=4):
            options[op]()
        
    
menu()
