#ifndef STEPPER_MOTOR_H
#define STEPPER_MOTOR_H

#include "pico/stdlib.h"
#include <math.h>

/* THINGS TO ADD

- ability to count steps
- ability to zero step count
- ability to set limits on motion

*/

/* MICROSTEPPING SELECTION GUIDE

M2  |  M1  |  M0  |  Microstepping
===============================
0   |  0   |  0   |  full-step
0   |  0   |  1   |  1/2 step
0   |  1   |  0   |  1/4 step
0   |  1   |  1   |  1/8 step
1   |  0   |  0   |  1/16 step
1   |  0   |  1   |  1/32 step
1   |  1   |  0   |  1/32 step
1   |  1   |  1   |  1/32 step

*/

// use these with init_motor() to set microstepping mode
#define USTEP_FULL  0
#define USTEP_1_2   1
#define USTEP_1_4   2
#define USTEP_1_8   3
#define USTEP_1_16  4
#define USTEP_1_32  5

typedef struct {

    // define hardware pins
    const uint step_pin;    // sends step pulse to advance the stepper motor
    const uint dir_pin;     // controls the direction of rotation
    const uint M0_pin;      // LSB of microstepping inputs
    const uint M1_pin;      // intermediate bit of microstepping input
    const uint M2_pin;      // MSB of microstepping inputs
    const uint en_pin;      // logic low -> enabled ... logic high -> disabled

    // acceleration and velocity parameters
    uint32_t s_accel;       // number of steps to achieve max velo.
    uint32_t s_decel;       // number of steps to achieve min velo.
    uint32_t delay_max;     // longest delay between steps (i.e min velo.)
    uint32_t delay_min;     // shortest delay between steps (i.e max velo.)

    // position tracking
    int32_t current_pos;    // tracks the current position of the robot
    
} stepper_config;

void init_motor(stepper_config* cfg, uint8_t en, uint8_t ustep);        // initialize motor GPIO pins and microstepping
void execute_steps(uint32_t steps, uint8_t dir, stepper_config* cfg);   // advance motor # steps in desired direction
void disable_motor(stepper_config* cfg);                                // disable output to motor
void enable_motor(stepper_config* cfg);                                 // enable output to motor

#endif