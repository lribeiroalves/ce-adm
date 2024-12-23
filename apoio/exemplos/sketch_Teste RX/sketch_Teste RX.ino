void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial2.begin(9600, SERIAL_8N1, 2, 4);

  Serial.println("Iniciando TX");

}

int counter = 0;

void loop() {
  // put your main code here, to run repeatedly:
  Serial.print("Teste ");
  Serial.println(counter);
  Serial2.print("Teste ");
  Serial2.println(counter);

  counter++;

  delay(2000);
}
