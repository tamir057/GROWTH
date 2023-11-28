#include "adc122s021.h"

// read 12-bit ADC value from the ADC122S021
/* ARGS
    spi     -> SPI port
    cs      -> chip select pin
    channel -> ADC channel to read from (0 or 1)
*/
uint16_t ADC122S021_ReadADC(spi_inst_t* spi, const uint cs, bool channel) {

    uint8_t ctrl_reg_val[2] = {(uint8_t) (channel << 3), 0};
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

    ADC122S021_ReadADC(spi, cs, channel);
    double volts = 3.300 * ((double) ADC122S021_ReadADC(spi, cs, channel)) / (double) 4095;

    return volts;
}

double pH_reading(double sensor_voltage, double offset) {
    double pH = 4.0322 * sensor_voltage + offset;
    return pH;
}

double conductivity_reading(double sensor_voltage, double temp){
    float TempCoefficient = 1.0+0.0185*(temp-25.0);
    float CoefficientVoltage = (float)sensor_voltage/TempCoefficient;
    float conductivity;
    if (CoefficientVoltage < 150){
        // return no solution error
    }
    else if (CoefficientVoltage > 3300){
        // return out of range error
    }
    else{
        if (CoefficientVoltage <= 448){
            conductivity = 6.84*CoefficientVoltage-64.32;
        } else if (CoefficientVoltage < 1457){
            conductivity = 6.98*CoefficientVoltage-127;
        } else{
            conductivity = 5.3*CoefficientVoltage+2278;
        }
        conductivity = conductivity/1000; //convert from us/cm to ms/cm
    }
    return (double) conductivity;
}