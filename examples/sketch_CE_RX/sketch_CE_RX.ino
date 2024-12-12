//#include <SoftwareSerial.h>
#define RXD2 4
#define TXD2 2

void setup() {
  // Note the format for setting a serial port is as follows: Serial2.begin(baud-rate, protocol, RX pin, TX pin);
  Serial.begin(9600);
  //Serial1.begin(9600, SERIAL_8N1, RXD2, TXD2);
  Serial2.begin(1200, SERIAL_8N1, RXD2, TXD2);
  Serial.println("Iniciando RX");
}

//const int size_msg = 13;
//byte input[size_msg];

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial2.available()){
    delay(150);

    const int size_msg = Serial2.available();
    byte input[size_msg];

    //Serial.print("Size: ");
    //Serial.println(size_msg);
    //Serial.print(" / ");

    for (int i = 0; i < size_msg; i++) {
      input[i] = Serial2.read();
    }

    //Serial.println(input[0]);

    for (int i = 0; i < size_msg; i++) {
      Serial.print(input[i]);
      Serial.print(" ");
    }

    //Serial.println();

    //Serial.print("rssi: ");
    //Serial.print(-(256-(input[size_msg - 1])));
    //Serial.println(" dBm");
  }
}
