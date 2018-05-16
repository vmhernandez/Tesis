#include <Servo.h>

String inString = "";    // string to hold input
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
  while (Serial.available() > 0) {

    Sensor1=analogRead(A0);
    Sensor2=analogRead(A1);
    Sensor3=analogRead(A2);
    Sensor4=analogRead(A3);
    Serial.println(Sensor1);
    Serial.println(Sensor2);
    Serial.println(Sensor3);
    Serial.println(Sensor4);
    
    int inChar = Serial.read();
    if (isDigit(inChar)) {
      // convert the incoming byte to a char and add it to the string:
      inString += (char)inChar;
    }
    // if you get a newline, print the string, then the string's value:
    if (inChar == '\n') {
      Grado1=inString.substring(0,3).toInt();
      Grado2=inString.substring(3,6).toInt();
      Grado3=inString.substring(6,9).toInt();
      Grado4=inString.substring(9,12).toInt();

      Serial.print("Value:");
      Serial.println(Grado1);
      
      Serial.print("Value:");
      Serial.println(Grado2);
      
      Serial.print("Value:");
      Serial.println(Grado3);
      
      Serial.print("Value:");
      Serial.println(Grado4);
      
      inString = "";
    }
  }
   Servo1.write(Grado1);
   Servo2.write(Grado2);
   Servo3.write(Grado3);
   Servo4.write(Grado4);
}
