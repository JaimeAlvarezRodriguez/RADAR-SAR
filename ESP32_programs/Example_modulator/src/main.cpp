#include <Arduino.h>

#define SYNC_PIN    25
#define SIGNAL_PIN  26
#define START 64
#define STOP 144
#define TIME 230 

void setup() {
  Serial.begin(9600);

  pinMode(SYNC_PIN, OUTPUT);

  for(;;){
    unsigned long t1 = micros();
    digitalWrite(SYNC_PIN, HIGH);
    for(int i = START; i <= STOP; i++){
      dacWrite(SIGNAL_PIN, i);
      delayMicroseconds(TIME);
    }
    digitalWrite(SYNC_PIN, LOW);
    for(int i = STOP; i >= START; i--){
      dacWrite(SIGNAL_PIN, i);
      delayMicroseconds(TIME);
    }
    Serial.printf(">t:%u\n", micros() - t1);
  }
  
  
}

void loop() {
  // put your main code here, to run repeatedly:
}
