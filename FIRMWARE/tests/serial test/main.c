#include "pico/stdlib.h"
#include "pico/stdio_usb.h"
#include "tusb.h"               // for tud_cdc_available()

uint8_t usb_rx_buf[256];
uint8_t usb_tx_buf[256];

void usb_send_bytes(uint8_t* buf, uint8_t len) {
    fwrite(buf, 1, len, stdout);
}

int main() {

    stdio_usb_init();

    for(uint8_t x=0; x<10; x++) {
    // Wait for up to 10 seconds for USB serial connection
    // allows us time to connect our terminal program
    // and see the program output. (otherwise we might miss it)
    sleep_ms(100);

    if (stdio_usb_connected())
        break;
    }

    // usb_tx_buf[0] = 'T';
    // usb_tx_buf[1] = 'E';
    // usb_tx_buf[2] = 'S';
    // usb_tx_buf[3] = 'T';
    // usb_tx_buf[4] = '\n';
    // usb_tx_buf[5] = '8';

    uint8_t arr[4] = {41, 42, 43, 44};

    while(1) {

        // fwrite(usb_tx_buf, 1, 5, stdout);
        usb_send_bytes((uint8_t*) arr, 4);
        sleep_ms(5000);

    }

    return 0;
}