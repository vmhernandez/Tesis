#include <Servo.h>

int Grado1,Grado2,Grado3,Grado4,Sensor1,Sensor2,Sensor3,Sensor4;
Servo Servo1,Servo2,Servo3,Servo4; //Define los Servos

void setup() {
  Servo1.attach(2); //Conecta Servo 1 al puerto 2
  Servo2.attach(3); //Conecta Servo 2 al puerto 3
  Servo3.attach(4); //Conecta Servo 3 al puerto 4
  Servo4.attach(5); //Conecta Servo 4 al puerto 5

  Serial.begin(9600);
  while (!Serial) {
    ;
  }
}

void loop() {
  // put your main code here, to run repeatedly:

  while (Serial.available()>0){
     if(Serial.read()=='R'){
      
        Sensor1=analogRead(A0);
        Sensor2=analogRead(A1);
        Sensor3=analogRead(A2);
        Sensor4=analogRead(A3);

        Serial.println(Sensor1);
        Serial.println(Sensor2);
        Serial.println(Sensor3);
        Serial.println(Sensor4);

      }else{
        
        Grado1 = Serial.parseInt();
        Grado2 = Serial.parseInt();
        Grado3 = Serial.parseInt();
        Grado4 = Serial.parseInt();
              
       if (Serial.read()=='\n'){
          
          Servo1.write(Grado1);
          Servo2.write(Grado2);
          Servo3.write(Grado3);
          Servo4.write(Grado4);
          
          Serial.println(Grado1);
          Serial.println(Grado2);          
          Serial.println(Grado3);          
          Serial.println(Grado4);
          
       }
      }
  }
}
