#include <Arduino.h>

class PiscaLed {
  // atributos
  int ledPin;     // pino do Led
  long timeOn;     // tempo ligado
  long timeOff;    // tempo desligado

  int ledState;   // estado atual do LED
  unsigned long prevTime;   // último momento de alterção do estado do LED

  // construtor
  public:
  PiscaLed(int pin, long on, long off) {
    ledPin = pin;
    pinMode(ledPin, OUTPUT);

    timeOn = on;
    timeOff = off;

    ledState = LOW;
    prevTime = 0;
  }

  // método
  void Update() {
    // verifica o momento atual
    unsigned long currTime = millis();

    // verifica se já é o momento de alternar o LED
    if ((ledState == HIGH) && (currTime >= prevTime + timeOn)) {
      digitalWrite(ledPin, LOW);
      ledState = LOW;
      prevTime = currTime;
    }
    else if ((ledState == LOW) && (currTime >= prevTime + timeOff)) {
      digitalWrite(ledPin, HIGH);
      ledState = HIGH;
      prevTime = currTime;
    }
  }
};
