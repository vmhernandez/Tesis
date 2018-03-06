#include <Servo.h>

Servo Servo1,Servo2,Servo3,Servo4; //Define los Servos
int i=0,Grado1,Grado2,Grado3,Grado4; //Define como entero los grados para utilizarlos en el movimiento de los servos
char grados[3];
//char grados[13] ; //Define la cadena grados

void setup() {
  Servo1.attach(2); //Conecta Servo 1 al puerto 2
/*
  Servo2.attach(3); //Conecta Servo 2 al puerto 3
  Servo3.attach(4); //Conecta Servo 3 al puerto 4
  Servo4.attach(5); //Conecta Servo 4 al puerto 5
*/
  //delay(1000); //Espera 1 segundo para iniciar (3minutos*60Segundos*1000)
  Serial.begin(9600); //Inicia puerto serial a 9600 Bits por segundo
}

void loop() {
  if (Serial.available()){
    while(Serial.read()!='.'){
        grados[i]=Serial.read();
        Serial.println(grados[i]);
        i=i+1;
      }
    
    Grado1 = int(grados[0]+grados[1]+grados[2]);
    /*
    Grado2 = int(grados[3]+grados[4]+grados[5]);
    Grado3 = int(grados[6]+grados[7]+grados[8]);
    Grado4 = int(grados[9]+grados[10]+grados[11]);
    */
    //Grado1 = int(grados.substring(0,2)); //Convierte la sub cadena en un entero
    //Grado2 = toInt(grados.substring(3,5)); //Convierte la sub cadena en un entero
    //Grado3 = toInt(grados.substring(6,8)); //Convierte la sub cadena en un entero
    //Grado4 = toInt(grados.substring(8,11)); //Convierte la sub cadena en un entero
    //Serial.println('.');
    Serial.println(Grado1); //Escribe por el puerto serial la sub cadena desde el caracter 0 al caracter 2
   /*
    Serial.println(Grado2); //Escribe por el puerto serial la sub cadena desde el caracter 3 al caracter 5
    Serial.println(Grado3); //Escribe por el puerto serial la sub cadena desde el caracter 6 al caracter 8
    Serial.println(Grado4); //Escribe por el puerto serial la sub cadena desde el caracter 9 al caracter 11
  */
    Serial.println('.');
    Servo1.write(Grado1);
   /*
    Servo2.write(Grado2);
    Servo3.write(Grado3);
    Servo4.write(Grado4);
   */
   
    Serial.println(Servo1.read());
   /*
    Serial.println(Servo2.read());
    Serial.println(Servo3.read());
    Serial.println(Servo4.read());
    Serial.println('.');
    */
    delay(1500);
    }
}
