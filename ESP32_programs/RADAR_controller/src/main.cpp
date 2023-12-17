#include <Arduino.h>
#include <BluetoothSerial.h>

#define RQST_NONE__  0
#define RQST_INFO__  1
#define RQST_RECORD  3

#define INFO_MACADR  1
#define INFO_SMPRTE  2

#define RECD_START_  1
#define RECD_STOP__  2

#define RAW_DATA_SIZE 10000
#define DATA_SIZE     5000

const char MSSG_STOP[] = "$STOP_RECORDING_ESP32#";

BluetoothSerial BT_serial;

namespace RECORD{
  double samplerate = 10800;
};

void get_info(int value);

void setup() {
  BT_serial.begin("RADAR_SAR");
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
    break;
  default:
    break;
  }
  
}


void get_info(int value){
  switch (value){
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