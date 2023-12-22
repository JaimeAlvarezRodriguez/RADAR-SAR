/*
Proyect:      RADAR SAR controller
Authon:       Jaime Álvarez Rodríguez
Description:  Controller firmware for the RADAR SAR proyect  
Date:         01/12/2023
Version:      v1.1
*/

#include <Arduino.h>
#include <BluetoothSerial.h>
#include <vector>
#include <constants.h>
//#define DEBUG // Uncomment this line to print action througth serial port 

const char MSSG_STOP[] = "$STOP_RECORDING_ESP32#";
const char name[] = "RADAR_SAR";//Device name for bluetooth

BluetoothSerial BT_serial;

namespace RECORD{
  double samplerate = DEFAULT_SAMPLERATE; //Number of samples per second
  void loop(void *); //send data task
  void record(); //digitalize signal from receiver
  TaskHandle_t thRecord; //task handler of send data task
  const char name[] = "Send record"; //send data task name
  bool active = false; //Flag to continue sampling
  bool send = false; //Flag to send data buffer
  std::vector<uint16_t> buffer(DATA_SIZE, 0); //data buffer
};

void send_info(int value); //Function declaration to send information to aplication

void setup() {
  Serial.begin(9600);
  BT_serial.begin(name); //Begin bluetooth Serial comunication
  xTaskCreate(RECORD::loop, RECORD::name, 4096, NULL, 3, &RECORD::thRecord); //Create task for send data

  pinMode(SYNC_PIN, INPUT); //Enable sync pin as input
  pinMode(SGNL_PIN, INPUT); //Enable signal pin as input
}

void loop() {
  while (!BT_serial.available())
    delay(10); //Wait for a request

  uint8_t command[2]; //Create data buffer for the request command
  BT_serial.readBytes(command, 2); //Read 2 bytes 
  int request = command[0]; //first byte stands for the type of request
  int value = command[1]; //second byte stands for the value of the request
  switch (request){
  case RQST_NONE__: //Request none
    break;
  case RQST_INFO__: //Request information
    send_info(value);
    break;
  case RQST_RECORD: //Request recording action
    switch (value){
    case RECD_START_: //Start recording
      RECORD::active = true;

      #ifdef DEBUG
      Serial.println("Start_recording");
      #endif

      RECORD::record();
      break;
    case RECD_STOP__: //Stop recording
      RECORD::active = false;
      BT_serial.println(MSSG_STOP);

      #ifdef DEBUG
      Serial.println(MSSG_STOP);
      #endif

      break;
    default:
      break;
    }

    break;
  default:
    break;
  }
  
}

/*
Send some information to aplication

@param value Type of information to send
*/
void send_info(int value){
  switch (value){
  case INFO_NAME__: //Send device's name
    BT_serial.println(name);
    break;
  case INFO_MACADR: //Send mac address of Bluetooth device
    BT_serial.println(BT_serial.getBtAddressString());
    break;
  case INFO_SMPRTE: //Send sample rate registered
    BT_serial.println(RECORD::samplerate);
    break;
  default:
    break;
  }
}


/*
Sample the signal from receiver's radar
*/
void RECORD::record(){
  unsigned long t1, t2;//Flags to calculate the samplerate
  while(RECORD::active){
    t1 = micros(); //First flag

    for(unsigned i = 0; i < buffer.size(); i++){
      bool sync = digitalRead(SYNC_PIN);
      uint16_t signal = analogRead(SGNL_PIN);
      buffer[i] = (sync << 15) | signal; //Package information in 2 bytes: signal -> 1-12, sync -> 16
      if(BT_serial.available()){ //If a request occurs, it stops recording
        RECORD::active = false;

        #ifdef DEBUG
        Serial.println("Stopped");
        #endif
        
        return;
      }
    }

    t2 = micros(); //Second flag
    if(t2 > t1) //Prevents overflow error
      RECORD::samplerate = (double)buffer.size() / (t2 - t1) / 1e-6;
    RECORD::send = true; //Activate flag to send data
  }
}

/*
Task for send data to aplication
*/
void RECORD::loop(void *){
  for(;;){
    if(RECORD::send && RECORD::active){ //If both flags are active, then send data
      RECORD::send = false; //Desactive send flag, just do it once until record function activates it again
      BT_serial.flush();
      BT_serial.write((uint8_t *)buffer.data(), RAW_DATA_SIZE); //Send all data buffer
    }
    vTaskDelay(1);
  }
}