#include <stdio.h>
#include "pico/stdlib.h"
#include <math.h>

#include "stepper_motor.h"

int main() {

    const uint led_pin = 15;

    const uint step_pin = 0;
    const uint dir_pin = 1;
    const uint M0_pin = 2;
    const uint M1_pin = 3;
    const uint M2_pin = 4;
    const uint en_pin = 5;

    stepper_config motor_config = {step_pin, dir_pin, M0_pin, M1_pin, M2_pin, en_pin, 3200, 3200, 1250/2, 250/2};

    // Initialize LED pin
    gpio_init(led_pin);
    gpio_set_dir(led_pin, GPIO_OUT);

    init_motor(&motor_config, 1, USTEP_1_4);

    // Initialize chosen serial port
    stdio_init_all();

    // blinking LED to indicate reset/start up
    for (int i=0; i<10; i++) {
        gpio_put(led_pin, true);
        sleep_ms(10);
        gpio_put(led_pin, false);
        sleep_ms(90);
    }

    gpio_put(en_pin, false);

    // Loop forever
    while (true) {

        for (int i=0; i<1; i++) {

            execute_steps(3600*4, 0, &motor_config);
            sleep_ms(1000);
            execute_steps(3600*4, 1, &motor_config);
            sleep_ms(1000);

        }

        gpio_put(en_pin, true);

        break;

    }

    while(true) {}
}