void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  char command[] = "b122";
  command[3] = 0;
  int pos = atoi(&command[1]); 
  Serial.write(pos);
  delay(1000);
}
