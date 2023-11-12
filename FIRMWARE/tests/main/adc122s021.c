#include "adc122s021.h"

// read 12-bit ADC value from the ADC122S021
/* ARGS
    spi     -> SPI port
    cs      -> chip select pin
    channel -> ADC channel to read from (0 or 1)
*/
uint16_t ADC122S021_ReadADC(spi_inst_t* spi, const uint cs, bool channel) {

    uint8_t ctrl_reg_val[2] = {(uint8_t) ((channel ^ 0x01) << 3), 0};
    uint8_t adc_val[2] = {0, 0};
    uint16_t adc_reading;

    gpio_put(cs, false);
    spi_write_read_blocking(spi, ctrl_reg_val, adc_val, 2);
    gpio_put(cs, true);

    adc_reading = (adc_val[0] << 8) + adc_val[1];

    return adc_reading;
}

// returns ADC value as a voltage (assuming 3.3V reference)
/* ARGS
    spi     -> SPI port
    cs      -> chip select pin
    channel -> ADC channel to read from (0 or 1)
*/
double ADC122S021_GetVoltage(spi_inst_t* spi, const uint cs, bool channel) {

    double volts = 3.300 * ((double) ADC122S021_ReadADC(spi, cs, channel)) / (double) 4095;

    return volts;
}