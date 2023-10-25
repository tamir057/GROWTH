#include "stdio.h"
#include "pico/stdlib.h"

#include "adc122s021.h"

int main() {

    const uint cs_pin = 5;
    const uint sck_pin = 2;
    const uint mosi_pin = 3;
    const uint miso_pin = 4;

    spi_inst_t* spi_port = spi0;

    stdio_init_all();

    gpio_init(cs_pin);
    gpio_set_dir(cs_pin, GPIO_OUT);
    gpio_put(cs_pin, true);

    spi_init(spi_port, 1000 * 1000);
    spi_set_format(spi_port, 8, 1, 1, SPI_MSB_FIRST);

    gpio_set_function(sck_pin, GPIO_FUNC_SPI);
    gpio_set_function(mosi_pin, GPIO_FUNC_SPI);
    gpio_set_function(miso_pin, GPIO_FUNC_SPI);

    while(true) {
        printf("%x\n", ADC122021_ReadADC(spi_port, cs_pin, 1));
        sleep_ms(1000);
    }

    return 0;
}