#include <Servo.h>
int Grado1,i=0;
String grados[];
void setup() {
  Serial.begin(9600); //Inicia puerto serial a 9600 Bits por segundo
}

void loop() {
  if (Serial.available()){
    while(Serial.read()!='.'){
        grados[i]=Serial.read();
        Serial.println(grados[i]);
        i=i+1;
      }
    Grado1 = grados.substring(0,2).toInt()  //Convierte la sub cadena en un entero
    Serial.println(Grado1);
    Serial.println(Grado1*2);
    
    delay(0.1);
    }

