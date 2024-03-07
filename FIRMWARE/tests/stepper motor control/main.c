#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include <math.h>

#include "pinout.h"
#include "stepper_motor.h"

// interrupt handler
const uint limit_switch = GPIO1;
int bounce_count = 0;

void motor_boundary(uint gpio, uint32_t events) {

    gpio_put(X_MOTOR_EN, 1);
    bounce_count++;

}

int main() {

    // Initialize chosen serial port
    stdio_init_all();

    stepper_config x_motor = {X_MOTOR_STEP, X_MOTOR_DIR, X_MOTOR_M0, 
                                   X_MOTOR_M1, X_MOTOR_M2, X_MOTOR_EN,
                                   3200*2, 3200*2, 200, 150};
                                   
    // initialize interrupts on limit switches
    gpio_init(GPIO1);
    gpio_set_dir(GPIO1, GPIO_IN);
    gpio_set_pulls(GPIO1, false, false);
    gpio_set_input_hysteresis_enabled(GPIO1, true);
    // gpio_set_slew_rate(GPIO1, GPIO_SLEW_RATE_SLOW);

    // Initialize LED pin
    gpio_init(MCU_LED);
    gpio_set_dir(MCU_LED, GPIO_OUT);

    init_motor(&x_motor, 1, USTEP_1_32);

    // blinking LED to indicate reset/start up
    for (int i=0; i<10; i++) {
        gpio_put(MCU_LED, true);
        sleep_ms(10);
        gpio_put(MCU_LED, false);
        sleep_ms(90);
    }

    sleep_ms(3000);

    gpio_set_irq_enabled_with_callback(GPIO1, GPIO_IRQ_EDGE_RISE, true, &motor_boundary);
    enable_motor(&x_motor);
    sleep_ms(100);

    // Loop forever
    while (true) {

        for (int i=0; i<1; i++) {

            execute_steps(2000*16, 0, &x_motor);
            sleep_ms(1000);
            execute_steps(2000*16, 1, &x_motor);
            sleep_ms(1000);

        }

        disable_motor(&x_motor);

        break;

    }

    while(true) {
        gpio_put(MCU_LED, true);
        sleep_ms(500);
        gpio_put(MCU_LED, false);
        sleep_ms(500);
        printf("Bounce count --> %i\n", bounce_count);
    }

}