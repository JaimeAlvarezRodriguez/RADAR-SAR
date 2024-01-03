/*
Proyect:      DC motor speed controller for RADAR SAR project
Authon:       Jaime Álvarez Rodríguez
Description:  Controls a dc motor's speed for see a figure in doppler analysis from RADAR SAR
Date:         21/12/2023
Version:      v1.0
*/

#include <Arduino.h>
#include "line_functions.h"
#define PIN_MOTOR 3
#define DELAY_TIME 22

void draw_line(LINE_FUNC callback);
void draw_form(LINE_FUNC *callback_list, int length);
void print_line(LINE_FUNC callback);
void print_form(LINE_FUNC *callback_list, int length);

/*
Select functions from FIG namespace to draw a figure
*/
LINE_FUNC form[] = {FIG::TRIGONOMETRIC::sin_1, FIG::DIAGONAL::upward, 
                    FIG::TRIGONOMETRIC::sin_2, FIG::DIAGONAL::downward,
                    FIG::LINE::high_horizontal, FIG::LINE::medium_horizontal, 
                    FIG::LINE::zero};


int length = sizeof(form) / sizeof(form[0]);//Calculates number of funtions pointers from the form array

void setup() {
  Serial.begin(9600);
  //print_form(form, length);//Uncomment to print form by monitor serial (use Teleplot extension from vs code)
}

void loop() {
  draw_form(form, length);//Generates the figure by controlling motor's speed
}

/*
Control motor's speed for generate a curve in RADAR'S SAR doppler analysis
@param callback Function that generate a value from 0 to 255 by giving a value in the same range
*/
void draw_line(LINE_FUNC callback){
  unsigned long t1 = micros();
  for(int i = 0; i <= 255; i++){
    analogWrite(PIN_MOTOR, callback(i));
    delay(DELAY_TIME);
  }
  unsigned long t2 = micros();
  Serial.print(">micros:");
  Serial.println(t2-t1);
}

/*
Control motor's speed for generate a figure from several curves in RADAR'S SAR doppler analysis
@param callback_list Pointer to function array, eash function generate a value from 0 to 255 by giving a value in the same range
@param length Size of the array
*/
void draw_form(LINE_FUNC *callback_list, int length){
  for(int i = 0; i < length; i++){
    draw_line(callback_list[i]);
  }
}

/*
Print values generated from a LINE_FUNC in the monitor serial
@param callback Function that generate a value from 0 to 255 by giving a value in the same range
*/
void print_line(LINE_FUNC callback){
  for(int i = 0; i <= 255; i++){
    Serial.print(">value:");
    Serial.println(callback(i));
  }
}

/*
Print values generated from a LINE_FUNC array in the monitor serial
@param callback_list Pointer to function array, eash function generate a value from 0 to 255 by giving a value in the same range
@param length Size of the array
*/
void print_form(LINE_FUNC *callback_list, int length){
  for(int i = 0; i < length; i++){
    print_line(callback_list[i]);
  }
}
