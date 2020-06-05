/* -*- mode: c++; tab-width: 2; c-basic-offset: 2 -*-

   Manoel Vilela © Copyright 2018

   IR CONTROLLER MANOEL VILELA 22/01/2018
   STOLEN CODE FROM MYSELF

   Use version 1.0.0 of IRremote.h, otherwise it will not work


**/

#include <IRremote.h>

const int irReceiverPin = 6;
IRrecv irrecv(irReceiverPin);
decode_results decodedSignal;

long time = millis();
const int DELAY = 75; // ms
const int PIN_LED_SIGNAL = 2;
const long LED_BUTTON = 0x61F4906F;
const long header = 0x61F40000;
const long headerMask = 0xFFFF0000;

inline void inverse(int pin) {
  digitalWrite(pin, !digitalRead(pin));
}

inline bool checkHeader(long signal) {
  return (signal & headerMask) == header;
}

inline void controlIR(void) {
  if (irrecv.decode(&decodedSignal)) {
    if (millis() - time > DELAY) {
      if (checkHeader(decodedSignal.value)) {
        Serial.println(decodedSignal.value, HEX);
        if (LED_BUTTON == decodedSignal.value) {
          inverse(PIN_LED_SIGNAL);
          delay(DELAY); // wait for resume the irrecv a little
        } else {
          inverse(PIN_LED_SIGNAL);
          delay(DELAY);
          inverse(PIN_LED_SIGNAL);
        }
      }
      time = millis();
      irrecv.resume();
    }
  }
}

void setup() {
  //Serial transmission Begin!
  Serial.begin(9600);

  //IrStart
  pinMode(PIN_LED_SIGNAL, OUTPUT);
  irrecv.enableIRIn();
}


void loop() {
  //Ir Control
  controlIR();
}
