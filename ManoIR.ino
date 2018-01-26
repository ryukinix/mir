/*
 *
 *  Manoel Vilela © Copyright 2018
 *
 *  IR CONTROLLER MANOEL VILELA 22/01/2018
 *  STOLEN CODE FROM MYSELF
 *
 *
 **/

#include "IRremote.h"

const int irReceiverPin = 4;
IRrecv irrecv(irReceiverPin);
decode_results decodedSignal;

long time = millis();
const int DELAY = 75; // ms
const int PIN_LED_SIGNAL = 2;
const long SKY_BUTTON = 0x61F458A7;

inline void inverse(int pin) {
  digitalWrite(pin, !digitalRead(pin));
}

inline void controlIR(void){
  if (irrecv.decode(&decodedSignal)) {
    if(millis() - time > DELAY){
      Serial.println(decodedSignal.value, HEX);
      if (SKY_BUTTON == decodedSignal.value) {
        inverse(PIN_LED_SIGNAL);
        delay(DELAY); // wait for resume the irrecv a little
      } else {
        inverse(PIN_LED_SIGNAL);
        delay(DELAY);
        inverse(PIN_LED_SIGNAL);
      }

      time = millis();
      irrecv.resume();
    }
  }
}

void setup(){
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
