#include "pico/stdlib.h"
#include "pico/stdio_usb.h"
#include "tusb.h"               // for tud_cdc_available()

#include "serial_commands.h"

uint8_t usb_rx_buf[256];
uint8_t usb_tx_buf[256];

command_attributes valid_commands[] = {{MOVE_MOTOR_CMD, 3},
                                       {STOP_MOTOR_CMD, 1},
                                       {MOVE_CONT_CMD, 2},
                                       {READ_SENSOR_CMD, 1},
                                       {PUMP_ON_CMD, 1},
                                       {PUMP_OFF_CMD, 1},
                                       {LIGHT_ON_CMD, 1},
                                       {LIGHT_OFF_CMD, 1},
                                       {LED_ON_CMD, 0},
                                       {LED_OFF_CMD, 0}};

int main() {

    stdio_usb_init();

    for(uint8_t x=0; x<10; x++) {

        // Wait for up to 10 seconds for USB serial connection
        // allows us time to connect our terminal program
        // and see the program output. (otherwise we might miss it)
        sleep_ms(100);

        if (stdio_usb_connected()) {
            break;
        }
    }

    uint8_t byte;
    uint8_t counter = 0;
    while(1) {

        while(tud_cdc_available()) {

            byte = getchar_timeout_us(1);

            if (byte == '\n') {

                usb_rx_buf[counter] = '\0';

                printf("MESSAGE OF SIZE (%i) BYTES RECEIVED\n", counter);
                printf("MESSAGE: %s\n\n", usb_rx_buf);

                uint8_t rtn = parse_commands(usb_rx_buf, valid_commands, 10);

                counter = 0;

            } else {

                usb_rx_buf[counter] = byte;
                counter++;
            }    
        }
    }

    return 0;
}