#include <stdio.h>
#include "pico/stdlib.h"
#include <math.h>

#include "pinout.h"
#include "stepper_motor.h"

int main() {

    stepper_config motor_config = {X_MOTOR_STEP, X_MOTOR_DIR, X_MOTOR_M0, 
                                   X_MOTOR_M1, X_MOTOR_M2, X_MOTOR_EN,
                                   3200, 3200, 800/2, 400/2};

    // Initialize LED pin
    gpio_init(MCU_LED);
    gpio_set_dir(MCU_LED, GPIO_OUT);

    init_motor(&motor_config, 1, USTEP_1_4);

    // Initialize chosen serial port
    stdio_init_all();

    // blinking LED to indicate reset/start up
    for (int i=0; i<10; i++) {
        gpio_put(MCU_LED, true);
        sleep_ms(10);
        gpio_put(MCU_LED, false);
        sleep_ms(90);
    }

    sleep_ms(5000);
    enable_motor(&motor_config);

    // Loop forever
    while (true) {

        for (int i=0; i<1; i++) {

            execute_steps(1300*4, 0, &motor_config);
            sleep_ms(1000);
            execute_steps(1300*4, 1, &motor_config);
            sleep_ms(1000);

        }

        disable_motor(&motor_config);

        break;

    }

    while(true) {
        gpio_put(MCU_LED, true);
        sleep_ms(500);
        gpio_put(MCU_LED, false);
        sleep_ms(500);
    }

}