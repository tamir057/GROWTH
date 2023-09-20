#include <stdio.h>
#include "pico/stdlib.h"
#include <math.h>

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


typedef struct {

// define pins
const uint step_pin;    // sends step pulse to advance the stepper motor
const uint dir_pin;     // controls the direction of rotation
const uint M0_pin;      // LSB of microstepping inputs
const uint M1_pin;      // intermediate bit of microstepping input
const uint M2_pin;      // MSB of microstepping inputs
const uint en_pin;      // logic low -> enabled ... logic high -> disabled

// important parameters
uint32_t S_accel;       // number of steps to achieve max velo.
uint32_t S_decel;       // number of steps to achieve min velo.
uint32_t Delay_max;     // longest delay between steps (i.e min velo.)
uint32_t Delay_min;     // shortest delay between steps (i.e max velo.)

} stepper_config;

void execute_steps(uint32_t steps, uint8_t dir, stepper_config* cfg) {

    double delay_mag = (cfg->Delay_max - cfg->Delay_min) / 2.0;
    double delay_offset = (cfg->Delay_max + cfg->Delay_min) / 2.0;
    uint32_t delay;

    if (dir > 0) {
        gpio_put(cfg->dir_pin, true);
    } else {
        gpio_put(cfg->dir_pin, false);
    }

    if (steps <= (cfg->S_accel + cfg->S_decel)) {

        double correction_factor = 0.3;
        double new_ampl_min = (1-correction_factor) * (delay_mag * cos(M_PI * (double) (steps) / (2 * (double) cfg->S_accel)) + delay_offset) + correction_factor;
        double new_mag = (cfg->Delay_max - new_ampl_min) / 2.0;
        double new_offset = (cfg->Delay_max + new_ampl_min) / 2.0;

        for (uint32_t S=0; S<steps; S++) {
            delay = (uint32_t) (new_mag * cos(2 * M_PI * (double) S / (double) steps) + new_offset) / 2;

            gpio_put(cfg->step_pin, true);
            sleep_us(delay);
            gpio_put(cfg->step_pin, false);
            sleep_us(delay);
        }

    } else {

        // acceleration stage
        for (uint32_t A=0; A<cfg->S_accel; A++) {
            delay = (uint32_t) ((delay_mag * cos(M_PI * ((double) A) / ((double) cfg->S_accel)) + delay_offset) / 2);

            gpio_put(cfg->step_pin, true);
            sleep_us(delay);
            gpio_put(cfg->step_pin, false);
            sleep_us(delay);
        }

        // constant velo. stage
        delay = cfg->Delay_min / 2;
        for (uint32_t K=0; K<(steps - (cfg->S_accel + cfg->S_decel)); K++) {
            gpio_put(cfg->step_pin, true);
            sleep_us(delay);
            gpio_put(cfg->step_pin, false);
            sleep_us(delay);
        }

        // deceleration stage
        for (uint32_t D=0; D<cfg->S_decel; D++) {
            delay = (uint32_t) ((delay_mag * cos(M_PI * ((double) (D + cfg->S_decel)) / ((double) cfg->S_decel)) + delay_offset) / 2);

            gpio_put(cfg->step_pin, true);
            sleep_us(delay);
            gpio_put(cfg->step_pin, false);
            sleep_us(delay);
        }

    }

}

int main() {

    const uint led_pin = 15;

    const uint step_pin = 0;
    const uint dir_pin = 1;
    const uint M0_pin = 2;
    const uint M1_pin = 3;
    const uint M2_pin = 4;
    const uint en_pin = 5;

    stepper_config motor_config = {step_pin, dir_pin, M0_pin, M1_pin, M2_pin, en_pin, 6400, 6400, 2500/8, 250/8};

    // Initialize LED pin
    gpio_init(led_pin);
    gpio_set_dir(led_pin, GPIO_OUT);

    for (uint p=0; p<6; p++) {
        gpio_init(p);
        gpio_set_dir(p, GPIO_OUT);
    }

    gpio_put(en_pin, true);
    gpio_put(step_pin, false);
    gpio_put(dir_pin, false);

    gpio_put(M0_pin, true);
    gpio_put(M1_pin, true);
    gpio_put(M2_pin, true);

    // Initialize chosen serial port
    stdio_init_all();

    // Loop forever
    gpio_put(en_pin, false);
    while (true) {

        for (int i=0; i<1; i++) {

            execute_steps(11200*4, 0, &motor_config);
            sleep_ms(1000);
            execute_steps(11200*4, 1, &motor_config);
            sleep_ms(1000);

        }

        gpio_put(en_pin, true);

        break;

    }

    while(true) {}
}