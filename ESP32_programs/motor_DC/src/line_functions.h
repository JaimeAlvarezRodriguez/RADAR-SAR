#pragma once
#define __LINE_FUNCTIONS__

#include <Arduino.h>
#include <math.h>
#define MAX_PWM 255
#define MEDIUM_PWM (MAX_PWM / 2)
#define LOW_PWM 10
#define MIN_PWM 0

typedef uint8_t (*LINE_FUNC)(uint8_t);

namespace FIG{

    namespace DIAGONAL{
        uint8_t upward(uint8_t i){
            return i;
        }

        uint8_t downward(uint8_t i){
            return MAX_PWM - i;
        }
    };

    namespace LINE{
        uint8_t high_horizontal(uint8_t){
            return MAX_PWM;
        }

        uint8_t medium_horizontal(uint8_t){
            return MEDIUM_PWM;
        }

        uint8_t low_horizontal(uint8_t){
            return LOW_PWM;
        }

        uint8_t zero(uint8_t){
            return MIN_PWM;
        }

    };


    namespace TRIGONOMETRIC{
        uint8_t sin_1(uint8_t i){
            return MAX_PWM * sin((double)i/MAX_PWM * M_PI);
        }

        uint8_t sin_2(uint8_t i){
            return MAX_PWM * (sin((double)i/MAX_PWM * M_PI + M_PI) + 1);
        } 
    }; 

};