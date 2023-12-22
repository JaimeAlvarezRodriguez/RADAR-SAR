#include <Arduino.h>
#include "line_functions.h"
#define PIN_MOTOR 3
#define DELAY_TIME 22

void draw_line(LINE_FUNC callback);
void draw_form(LINE_FUNC *callback_list, int length);
void print_line(LINE_FUNC callback);
void print_form(LINE_FUNC *callback_list, int length);

LINE_FUNC form[] = {FIG::TRIGONOMETRIC::sin_1, FIG::DIAGONAL::upward, 
                    FIG::TRIGONOMETRIC::sin_2, FIG::DIAGONAL::downward,
                    FIG::LINE::high_horizontal, FIG::LINE::medium_horizontal, 
                    FIG::LINE::zero};

int length = sizeof(form) / sizeof(form[0]);

void setup() {
  Serial.begin(9600);
  Serial.println(length);
  print_form(form, length);
}

void loop() {
  //draw_form(form, length);
}

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

void draw_form(LINE_FUNC *callback_list, int length){
  for(int i = 0; i < length; i++){
    draw_line(callback_list[i]);
  }
}

void print_line(LINE_FUNC callback){
  for(int i = 0; i <= 255; i++){
    Serial.print(">value:");
    Serial.println(callback(i));
  }
}

void print_form(LINE_FUNC *callback_list, int length){
  for(int i = 0; i < length; i++){
    print_line(callback_list[i]);
  }
}
