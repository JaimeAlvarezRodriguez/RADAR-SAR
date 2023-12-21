/*
Proyect:      RADAR SAR controller
Authon:       Jaime Álvarez Rodríguez
Description:  Controller firmware for the RADAR SAR proyect  
Date:         01/12/2023
Version:      v1.0
*/


#include <Arduino.h>
#include <BluetoothSerial.h>
#include <vector>
#include <constants.h>

const char MSSG_STOP[] = "$STOP_RECORDING_ESP32#";
const char name[] = "RADAR_SAR";

BluetoothSerial BT_serial;

namespace RECORD{
  double samplerate = 11670;
  void loop(void *);
  void record();
  TaskHandle_t thRecord;
  const char name[] = "Send record";
  bool active = false;
  bool send = false;
  std::vector<uint16_t> buffer(DATA_SIZE, 0);
};

void get_info(int value);

void setup() {
  Serial.begin(9600);
  BT_serial.begin(name);
  xTaskCreate(RECORD::loop, RECORD::name, 4096, NULL, 3, &RECORD::thRecord);

  pinMode(SYNC_PIN, INPUT);
  pinMode(SGNL_PIN, INPUT);
}

void loop() {
  while (!BT_serial.available());
  uint8_t command[2];
  BT_serial.readBytes(command, 2);
  int request = command[0];
  int value = command[1];
  switch (request){
  case RQST_NONE__:
    break;
  case RQST_INFO__:
    get_info(value);
    break;
  case RQST_RECORD:
    switch (value){
    case RECD_START_:
      RECORD::active = true;
      RECORD::record();
      break;
    case RECD_STOP__:
      RECORD::active = false;
      break;
    default:
      break;
    }
    if(value == RECD_START_){
      
    }
    break;
  default:
    break;
  }
  
}


void get_info(int value){
  switch (value){
  case INFO_NAME__:
    BT_serial.println(name);
    break;
  case INFO_MACADR:
    BT_serial.println(BT_serial.getBtAddressString());
    break;
  case INFO_SMPRTE:
    BT_serial.println(RECORD::samplerate);
    break;
  default:
    break;
  }
}



void RECORD::record(){
  unsigned long t1, t2;
  while(RECORD::active){
    t1 = micros();
    for(unsigned i = 0; i < buffer.size(); i++){
      bool sync = digitalRead(SYNC_PIN);
      uint16_t signal = analogRead(SGNL_PIN);
      buffer[i] = (sync << 15) | signal;
    }
    t2 = micros();
    if(t2 > t1)
      RECORD::samplerate = (double)buffer.size() / (t2 - t1) / 1e-6;
    RECORD::send = true;
  }
}

void RECORD::loop(void *){
  for(;;){
    if(BT_serial.available())
      RECORD::active = false;
    if(RECORD::send && RECORD::active){
      RECORD::send = false;
      BT_serial.flush();
      BT_serial.write((uint8_t *)buffer.data(), RAW_DATA_SIZE);
      BT_serial.flush();
    }
    
    vTaskDelay(1);
  }
}