#include "pico/stdlib.h"
#include "pico/multicore.h"
#include "hardware/irq.h"
#include "stdio.h"

typedef struct {

    bool flag1;
    bool flag2;

} data_flags;

volatile data_flags flags_register = {false, false};

void core1_interrupt_handler() {

}

void core1_entry() {

    while(1) {
        
        flags_register.flag1 = !flags_register.flag1;

        sleep_ms(1000);

    }

}

int main() {

    stdio_init_all();

    multicore_launch_core1(core1_entry);

    bool prev_val = flags_register.flag1;

    while(1) {

        if (flags_register.flag1 != prev_val) {
            printf("The flag has changed value!\n");
            prev_val = flags_register.flag1;
        }

        sleep_us(100);

    }

    return 0;
}