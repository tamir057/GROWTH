#include "stdio.h"
#include "pico/stdlib.h"
#include "pinout.h"

int main() {

    gpio_init(MCU_LED);
    gpio_set_dir(MCU_LED, GPIO_OUT);

    stdio_init_all();

    for (int i=0; i<10; i++) {
        gpio_put(MCU_LED, true);
        sleep_ms(10);
        gpio_put(MCU_LED, false);
        sleep_ms(90);
    }

    while(1) {}

    return 0;
}