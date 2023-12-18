#include <Arduino.h>
#include <BluetoothSerial.h>
#include <constants.h>

const char MSSG_STOP[] = "$STOP_RECORDING_ESP32#";
const char name[] = "RADAR_SAR";

BluetoothSerial BT_serial;

namespace RECORD{
  double samplerate = 10800;
};

void get_info(int value);

void setup() {
  BT_serial.begin(name);
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